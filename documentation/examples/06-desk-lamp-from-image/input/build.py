from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
exec(compile((ROOT/'documentation/examples/_shared/build_common.py').read_text(encoding='utf-8-sig'),'common','exec'))
begin('06-desk-lamp-from-image')
black=mat('Black powder coat',(.021,.022,.024),.30,.65);gold=mat('Mustard enamel',(.92,.54,.012),.24,.25);white=mat('Shade white interior',(.9,.86,.68),.35);steel=mat('Joint screws',(.23,.25,.27),.2,.85);table=mat('Oak tabletop',(.28,.16,.067),.6)
cone('Weighted circular base',(0,0,.10),.44,.44,.2,black,64);cone('Base inset',(0,0,.206),.38,.38,.018,black,64)
a=(0,0,.27);b=(.36,0,1.32);c=(-.45,0,2.06)
for off in [-.06,.06]:
 pipe('Lower parallel arm',(a[0],off,a[2]),(b[0],off,b[2]),.036,black);pipe('Upper parallel arm',(b[0],off,b[2]),(c[0],off,c[2]),.038,black)
for loc in [a,b,c]:
 pipe('Hinge',tuple(Vector(loc)+Vector((0,-.10,0))),tuple(Vector(loc)+Vector((0,.10,0))),.10,black,32);pipe('Hinge screw',tuple(Vector(loc)+Vector((0,-.13,0))),tuple(Vector(loc)+Vector((0,-.105,0))),.037,steel,24)
curve('Power cable',[(.22,.10,.12),(.45,.15,.04),(.65,.2,.02),(.93,.1,.02)],.012,black)
# Hollow conical shade, mesh rings with distinct inner material.
top=Vector((-.49,0,2.04));axis=Vector((-.40,0,-.92)).normalized();u=Vector((0,1,0));v=axis.cross(u).normalized();verts=[]
for distance,radius in [(0,.12),(.59,.37),(.59,.35),(.025,.10)]:
 center=top+axis*distance
 for i in range(64):a=i*math.tau/64;verts.append(center+radius*(u*math.cos(a)+v*math.sin(a)))
faces=[]
for k in range(4):
 for i in range(64):faces.append((k*64+i,k*64+(i+1)%64,((k+1)%4)*64+(i+1)%64,((k+1)%4)*64+i))
mesh=bpy.data.meshes.new('Hollow shade mesh');mesh.from_pydata(verts,[],faces);o=bpy.data.objects.new('Yellow hollow shade',mesh);s.collection.objects.link(o);finish_obj(o,'Yellow hollow shade',gold);mesh.materials.append(white)
for f in mesh.polygons:f.use_smooth=True;f.material_index=1 if 128<=f.index<192 else 0
bulbmat=mat('Warm bulb',(.95,.75,.36));p=bulbmat.node_tree.nodes['Principled BSDF'];p.inputs['Emission Color'].default_value=(1,.72,.25,1);p.inputs['Emission Strength'].default_value=4
sphere('Bulb',top+axis*.24,(.09,.09,.13),bulbmat)
d=bpy.data.lights.new('Warm working light','SPOT');d.energy=90;d.color=(1,.65,.27);d.spot_size=math.radians(80);d.spot_blend=.7;light=bpy.data.objects.new('Warm working light',d);s.collection.objects.link(light);light.location=top+axis*.40;light.rotation_euler=axis.to_track_quat('-Z','Y').to_euler()
box('Desktop',(0,0,-.075),(200,200,.14),table,0);studio(4.8,(-.2,0,1.05),(2,-7,2.6),floor=False);seconds=render();views={}
for name,loc in [('matching-view.png',(0,-7,2.4)),('rear-view.png',(-3,5,3.2)),('side-view.png',(5,-2,2.7))]:
 s.camera.location=loc;s.camera.rotation_euler=(Vector((-.2,0,1.05))-s.camera.location).to_track_quat('-Z','Y').to_euler();views[name]=render(name,(640,360))
s.camera.location=(2,-7,2.6);s.camera.rotation_euler=(Vector((-.2,0,1.05))-s.camera.location).to_track_quat('-Z','Y').to_euler()
result=save({'render_seconds':seconds,'additional_views':views,'source_panel':'input/source.png top-left Photorealistic panel','assumptions':'Dimensions, joint depth, cable and hidden shade geometry inferred; reference is stylized illustration, not a measured photograph.'})
