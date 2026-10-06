"""Second, bounded correction pass for the chest's missing lid end panel.

Run only through the existing Blender Lab connection.  It preserves the base
builder and inserts real closing geometry before the export target is joined.
"""
from pathlib import Path

SOURCE = Path(__file__).with_name("build.py")
code = SOURCE.read_text(encoding="utf-8-sig")
injection = '''# Close each domed-lid end with an inset arch-shaped board.  The
# profile follows the existing staves and sits flush beneath their outer edges,
# avoiding a circular cap that bulges beyond the chest sides.
profile=[(.62*math.cos(math.pi-i*math.pi/12),1.18+.47*math.sin(math.pi-i*math.pi/12)) for i in range(13)]
xs=(1.125,1.195);verts=[(x,y,z) for x in xs for y,z in profile];count=len(profile)
faces=[tuple(reversed(range(count))),tuple(range(count,2*count))]
faces += [(i,(i+1)%count,(i+1)%count+count,i+count) for i in range(count)]
mesh=bpy.data.meshes.new('Lid end arch mesh');mesh.from_pydata(verts,[],faces);mesh.update()
lid_end=bpy.data.objects.new('Flush lid end arch',mesh);s.collection.objects.link(lid_end);mesh.materials.append(wood)
assets.append(lid_end)
'''
code = code.replace('# Join evaluated parts into a compact target, retaining a detailed source.', injection + '\n# Join evaluated parts into a compact target, retaining a detailed source.', 1)
namespace = {'__file__': str(SOURCE), '__name__': '__main__'}
exec(compile(code, str(SOURCE), 'exec'), namespace)
