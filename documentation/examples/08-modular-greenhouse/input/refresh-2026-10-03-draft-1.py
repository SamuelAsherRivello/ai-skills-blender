"""Focused greenhouse fidelity refresh, run through the existing Blender Lab connection."""
from pathlib import Path

SOURCE = Path(__file__).with_name("build.py")
code = SOURCE.read_text(encoding="utf-8-sig")
injection = '''# Keep the garden layout open: pot beds sit directly beside the
# path. Add masonry joints and use dedicated low-reflection roof glazing so
# the roof remains transparent enough to read its structure and planting.
roofglass=mat('Low-reflection roof glazing',(.68,.82,.74),.055)
rp=roofglass.node_tree.nodes['Principled BSDF'];rp.inputs['Transmission Weight'].default_value=1;rp.inputs['IOR'].default_value=1.45
if rp.inputs.get('Specular IOR Level'):rp.inputs['Specular IOR Level'].default_value=.22
for obj in [o for o in s.objects if o.name.startswith('Roof glass')]:
    obj.data.materials.clear();obj.data.materials.append(roofglass)
for y in [-2.04,-1.02,0,1.02,2.04]:
    box('Foundation mortar joint',(0,y,.375),(3.03,.025,.025),stone,.002)
for x in [-1.45,1.45]:
    for y in [-1.5,-.5,.5,1.5]: box('Foundation vertical joint',(x,y,.375),(.025,.04,.30),stone,.001)
'''
code = code.replace("studio(9,(0,-.3,1.25),(7,-9,6));", injection + "\nstudio(9,(0,-.3,1.25),(7,-9,6));", 1)
namespace = {'__file__': str(SOURCE), '__name__': '__main__'}
exec(compile(code, str(SOURCE), 'exec'), namespace)
