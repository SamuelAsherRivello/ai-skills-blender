from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
exec(compile((ROOT/'documentation/examples/_shared/build_common.py').read_text(encoding='utf-8-sig'),'common','exec'))
begin('05-fox-sprite-sheet')
orange=mat('Fox orange',(.75,.19,.025),.65);cream=mat('Ivory fur',(.9,.8,.59),.8);brown=mat('Dark paws',(.055,.027,.014),.8);black=mat('Eyes and nose',(.008,.011,.015),.22);pink=mat('Ear inner',(.25,.063,.045),.7)
def ico(name,loc,scale,m,sub=1):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=loc);o=bpy.context.object;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return finish_obj(o,name,m)
body=[];head=[];tail=[]
i=len(assets);ico('Fox body',(0,.12,.81),(.39,.68,.49),orange,2);ico('Chest bib',(0,-.43,.87),(.31,.18,.39),cream,2)
for x in [-.25,.25]:
 for y in [-.36,.51]:
  pipe('Leg',(x,y,.70),(x,y,.18),.105,orange,8);ico('Dark paw',(x,y-.04,.13),(.13,.19,.13),brown,1)
body=list(assets[i:]);i=len(assets);ico('Fox head',(0,-.61,1.26),(.43,.40,.38),orange,2);ico('Left cheek',(-.22,-.8,1.14),(.25,.29,.19),cream,1);ico('Right cheek',(.22,-.8,1.14),(.25,.29,.19),cream,1);ico('Muzzle',(0,-.99,1.19),(.18,.25,.14),cream,1);ico('Nose',(0,-1.21,1.21),(.105,.08,.075),black,1)
for side in [-1,1]:
 x=side*.29
 verts=[(x-.17,-.56,1.43),(x+.17,-.56,1.43),(x,-.48,1.98),(x-.13,-.28,1.43),(x+.13,-.28,1.43)]
 mesh=bpy.data.meshes.new('Ear mesh');mesh.from_pydata(verts,[],[(0,1,2),(1,4,2),(4,3,2),(3,0,2),(0,3,4,1)]);o=bpy.data.objects.new('Pointed ear',mesh);s.collection.objects.link(o);finish_obj(o,'Pointed ear',orange)
 mesh=bpy.data.meshes.new('Inner ear');mesh.from_pydata([(x-.09,-.575,1.52),(x+.09,-.575,1.52),(x,-.505,1.85)],[],[(0,1,2)]);o=bpy.data.objects.new('Inner ear',mesh);s.collection.objects.link(o);finish_obj(o,'Inner ear',pink)
 ico('Black eye',(side*.24,-.925,1.38),(.048,.028,.065),black,2);ico('Eye glint',(side*.235,-.951,1.403),(.015,.008,.018),cream,1)
head=list(assets[i:]);i=len(assets)
centers=[(0,.60,.8),(0,.96,.78),(0,1.28,.95),(0,1.55,1.28),(0,1.62,1.58)];radii=[.12,.27,.29,.21,.025];vs=[]
for c,r in zip(centers,radii):
 for j in range(8):a=j*math.tau/8;vs.append((c[0]+r*math.cos(a),c[1]+r*math.sin(a)*.5,c[2]+r*math.sin(a)))
fs=[]
for k in range(4):
 for j in range(8):fs.append((k*8+j,k*8+(j+1)%8,(k+1)*8+(j+1)%8,(k+1)*8+j))
fs += [tuple(range(7,-1,-1)),tuple(range(32,40))];mesh=bpy.data.meshes.new('Faceted tail');mesh.from_pydata(vs,[],fs);o=bpy.data.objects.new('Bushy tail',mesh);s.collection.objects.link(o);finish_obj(o,'Bushy tail',orange);mesh.materials.append(cream)
for f in mesh.polygons:
 if f.index>=24:f.material_index=1
tail=[o]
d=bpy.data.armatures.new('FoxRig');rig=bpy.data.objects.new('FoxRig',d);s.collection.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
for name,a,b in [('body',(0,0,.4),(0,0,1)),('head',(0,-.4,1),(0,-.7,1.5)),('tail',(0,.6,.8),(0,1.6,1.4))]:
 e=d.edit_bones.new(name);e.head=a;e.tail=b
 if name!='body':e.parent=d.edit_bones['body']
bpy.ops.object.mode_set(mode='OBJECT');bpy.ops.object.select_all(action='DESELECT')
for name,parts in [('body',body),('head',head),('tail',tail)]:
 for o in parts:
  o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);v=o.vertex_groups.new(name=name);v.add(list(range(len(o.data.vertices))),1,'REPLACE');m=o.modifiers.new('Idle rig','ARMATURE');m.object=rig;o.parent=rig;o.select_set(False)
for f,a in [(1,0),(4,.16),(7,0),(10,-.16),(13,0)]:
 for name,mult in [('head',.25),('tail',1)]:p=rig.pose.bones[name];p.rotation_mode='XYZ';p.rotation_euler.y=a*mult;p.keyframe_insert(data_path='rotation_euler',frame=f)
rig.animation_data.action.name='Fox_Idle';s.frame_start=1;s.frame_end=12;s.render.fps=12;s.frame_set(1);studio(5.2,(0,.15,1),(4,-6,3.3));seconds=render()
ground=next(o for o in s.objects if o.name.startswith('Studio floor'));ground.hide_render=True;s.render.film_transparent=True;s.cycles.samples=16;s.camera.data.ortho_scale=3.6
batch=time.perf_counter();frames=[]
for direction,a in [('front',0),('right',math.pi/2),('back',math.pi),('left',math.pi*1.5)]:
 s.camera.location=(6*math.sin(a),-6*math.cos(a),3.3);s.camera.rotation_euler=(Vector((0,.15,1))-s.camera.location).to_track_quat('-Z','Y').to_euler()
 for i,f in enumerate([1,4,7,10]):
  s.frame_set(f);name=f'sprites/{direction}-{i}.png';(OUT/'sprites').mkdir(exist_ok=True);render(name,(128,128));frames.append({'path':name,'direction':direction,'frame':f,'duration_ms':250,'pivot':[64,110]})
batch=time.perf_counter()-batch
(OUT/'sprites.json').write_text(json.dumps({'size':[128,128],'order':'rows front/right/back/left; columns idle frames 1/4/7/10','pivot_convention':'bottom-center canvas anchor; same across all directions','frames':frames},indent=2))
ground.hide_render=False;s.render.film_transparent=False;s.camera.data.ortho_scale=5.2;s.camera.location=(4,-6,3.3);s.camera.rotation_euler=(Vector((0,.15,1))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.frame_set(1);s.cycles.samples=32
result=save({'render_seconds':seconds,'batch_seconds':batch,'sprite_count':16,'sprite_size':[128,128],'frames_per_direction':4,'rig':'Head and tail idle; planted legs','seed':31})
