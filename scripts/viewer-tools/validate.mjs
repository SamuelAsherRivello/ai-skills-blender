import {NodeIO} from '@gltf-transform/core';
import {ALL_EXTENSIONS,EXTMeshoptCompression} from '@gltf-transform/extensions';
import {MeshoptDecoder} from 'meshoptimizer';
import {validateBytes} from 'gltf-validator';
import {readFile,glob} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=fileURLToPath(new URL('../../',import.meta.url));
await MeshoptDecoder.ready;
const io=new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({'meshopt.decoder':MeshoptDecoder});
let count=0;
for await(const relative of glob('documentation/examples/**/*.export.json',{cwd:root})){
 const report=JSON.parse(await readFile(root+'/'+relative,'utf8'));let bytes=await readFile(root+'/'+report.glbPath);
 if(createHash('sha256').update(bytes).digest('hex')!==report.glbSha256)throw new Error('Stale report '+relative);
 if(report.optimized){const doc=await io.readBinary(bytes);doc.getRoot().listExtensionsUsed().find(e=>e.extensionName===EXTMeshoptCompression.EXTENSION_NAME)?.dispose();bytes=await io.writeBinary(doc);}
 const result=await validateBytes(bytes,{maxIssues:10000});
 const warnings=[...new Set(result.issues.messages.filter(m=>m.severity===1).map(m=>m.code))];
 console.log(JSON.stringify({path:report.glbPath,errors:result.issues.numErrors,warnings}));
 if(result.issues.numErrors)throw new Error('Invalid GLB '+relative);
 count++;
}
console.log('Validated '+count+' exports (compressed files validated after lossless decoding).');
if(!count)throw new Error('No exports found');
