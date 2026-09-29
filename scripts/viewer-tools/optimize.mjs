import {NodeIO} from '@gltf-transform/core';
import {ALL_EXTENSIONS,EXTMeshoptCompression} from '@gltf-transform/extensions';
import {MeshoptEncoder,MeshoptDecoder} from 'meshoptimizer';
import {dedup,prune,weld} from '@gltf-transform/functions';
import {readFile,writeFile,stat,glob} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=fileURLToPath(new URL('../../',import.meta.url));
const hash=b=>createHash('sha256').update(b).digest('hex');
await MeshoptEncoder.ready;await MeshoptDecoder.ready;
const io=new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({'meshopt.encoder':MeshoptEncoder,'meshopt.decoder':MeshoptDecoder});
function triangles(a){let text='';for(let i=0;i<a.length;i+=3){const tri=Array.from(a.slice(i,i+3)),j=tri.indexOf(Math.min(...tri));text+=tri.slice(j).concat(tri.slice(0,j)).join(',')+';';}return hash(text);}
function signature(d){return d.getRoot().listMeshes().map(m=>m.listPrimitives().map(p=>({attributes:p.listSemantics().sort().map(k=>[k,hash(JSON.stringify(Array.from(p.getAttribute(k).getArray())))]),triangles:triangles(p.getIndices().getArray())})));}
for await(const relative of glob('documentation/examples/**/*.export.json',{cwd:root})){
 const reportPath=root+'/'+relative,report=JSON.parse(await readFile(reportPath,'utf8')),path=root+'/'+report.glbPath;
 if((await stat(path)).size<50*1024*1024||report.optimized)continue;
 const doc=await io.read(path);await doc.transform(dedup(),weld(),prune());
 const before=signature(doc);
 // Encoder method alone does not quantize: no quantize transform is applied.
 doc.createExtension(EXTMeshoptCompression).setRequired(true).setEncoderOptions({method:EXTMeshoptCompression.EncoderMethod.QUANTIZE});
 const bytes=await io.writeBinary(doc),decoded=await io.readBinary(bytes);
 if(JSON.stringify(before)!==JSON.stringify(signature(decoded)))throw new Error('Compression changed vertex attributes or triangle topology: '+relative);
 if(bytes.length>=100*1024*1024)throw new Error('Export exceeds GitHub file limit: '+relative);
 await writeFile(path,bytes);
 report.glbSha256=hash(bytes);report.byteSize=bytes.length;report.optimized=true;
 report.warnings.push('Lossless EXT_meshopt_compression; decoded vertex attributes and triangle topology verified unchanged. Requires Meshopt decoder.');
 await writeFile(reportPath,JSON.stringify(report,null,2)+'\n');
 console.log(report.glbPath+': '+bytes.length+' bytes');
}
