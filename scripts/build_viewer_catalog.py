"""Build the public viewer contract after exporting and validating all models."""
import hashlib
import json
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def glb_document(path):
    data = path.read_bytes()
    magic, version, size = struct.unpack_from('<4sII', data)
    assert magic == b'glTF' and version == 2 and size == len(data), str(path)
    length, kind = struct.unpack_from('<II', data, 12)
    assert kind == 0x4E4F534A
    doc = json.loads(data[20:20+length])
    assert doc.get('meshes'), 'No meshes: ' + str(path)
    assert all('uri' not in b for b in doc.get('buffers', [])), 'External buffer'
    assert all('bufferView' in i for i in doc.get('images', [])), 'External image'
    return doc


def metadata(source):
    output = source.parent
    example = ROOT / Path(*source.relative_to(ROOT).parts[:3])
    rows = []
    manifest = output/'manifest.json'
    if manifest.exists():
        data = json.loads(manifest.read_text(encoding='utf-8-sig'))
        for key in ('scene','blender','engine','objects','resolution','render_seconds','samples','clip','duration_seconds','rig','iteration'):
            if key in data:
                value = data[key]
                rows.append({'label':key.replace('_',' ').capitalize(),'value':json.dumps(value,ensure_ascii=False) if not isinstance(value,str) else value,'provenancePath':manifest.relative_to(ROOT).as_posix()})
    review = output/'review.md'
    if review.exists():
        text = review.read_text(encoding='utf-8-sig')
        # Preserve exact authored paragraph; no generative claims or target metadata.
        paragraphs = re.split(r'\n\s*\n',text)
        summary = next((p.strip() for p in paragraphs if p.strip() and not p.lstrip().startswith(('#','[','-','|'))),None)
        if summary:
            rows.append({'label':'Review','value':summary,'provenancePath':review.relative_to(ROOT).as_posix()})
    prompt = example/'input/prompt.txt'
    if 'transfer-checks' in source.parts:
        prompt = example/'input/transfer-checks/prompt.txt'
    if prompt.exists():
        rows.append({'label':'Example prompt','value':prompt.read_text(encoding='utf-8-sig').strip(),'provenancePath':prompt.relative_to(ROOT).as_posix()})
    return rows


def build():
    entries=[]
    for source in sorted((ROOT/'documentation/examples').rglob('*.blend')):
        output=source.with_suffix('.glb')
        report=json.loads(source.with_suffix('.export.json').read_text(encoding='utf-8'))
        assert report['sourceSha256']==sha(source), 'Stale source export: '+str(source)
        assert report['glbSha256']==sha(output), 'Export changed after report'
        doc=glb_document(output)
        path=source.relative_to(ROOT).as_posix()
        parts=path.split('/')
        title=re.sub(r'^\d+-','',parts[2]).replace('-',' ').title()
        variant='/'.join(parts[4:-1])
        if variant:title+=' / '+variant.replace('-',' ').replace('/',' / ').title()
        entry={'id':path,'title':title,'sourcePath':path,'glbPath':output.relative_to(ROOT).as_posix(),'byteSize':output.stat().st_size,'sourceSha256':report['sourceSha256'],'glbSha256':report['glbSha256'],'warnings':report['warnings'],'metadata':metadata(source),'exported':{'meshes':len(doc.get('meshes',[])),'materials':len(doc.get('materials',[])),'animations':[a.get('name','Unnamed') for a in doc.get('animations',[])]}}
        preview=source.with_suffix('.png')
        if report.get('view'):entry['view']=report['view']
        if preview.exists():entry['previewPath']=preview.relative_to(ROOT).as_posix()
        entries.append(entry)
    destination=ROOT/'documentation/models/index.json'
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps({'schemaVersion':1,'models':entries},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f'Catalog: {len(entries)} complete model entries')


if __name__=='__main__':
    build()
