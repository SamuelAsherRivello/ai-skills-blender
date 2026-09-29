from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
exec(compile((ROOT/'documentation/examples/_shared/build_common.py').read_text(encoding='utf-8-sig'),'common','exec'))
begin('04-robot-greeting')
teal=mat('Enamel teal',(.018,.34,.36),.24,.25);yellow=mat('Butter yellow',(.95,.57,.07),.3,.12);dark=mat('Graphite joints',(.018,.026,.032),.4,.5);screen=mat('Dark screen',(.007,.025,.036),.16);eye=mat('Eye lights',(.5,.95,1),.2);p=eye.node_tree.nodes['Principled BSDF'];p.inputs['Emission Color'].default_value=(.2,.8,1,1);p.inputs['Emission Strength'].default_value=2
parts={}
def group(name,start):parts[name]=list(assets[start:])
i=len(assets);box('Rounded torso',(0,0,1.55),(1.1,.68,1.05),teal,.19);box('Chest yellow inset',(0,-.36,1.55),(.62,.055,.4),yellow,.08)
for x in [-.18,0,.18]:box('Speaker slit',(x,-.397,1.55),(.035,.01,.20),dark,.01)
sphere('Neck',(0,0,2.17),(.17,.17,.16),dark);group('body',i)
i=len(assets);box('Robot head',(0,0,2.62),(1.35,.80,.82),teal,.19);box('Face display',(0,-.407,2.65),(1.08,.08,.54),screen,.13)
for x in [-.28,.28]:sphere('Friendly eye',(x,-.46,2.72),(.09,.025,.12),eye)
curve('Smile',[(-.18,-.466,2.50),(0,-.48,2.46),(.18,-.466,2.50)],.018,eye)
for x in [-.77,.77]:sphere('Yellow ear',(x,0,2.62),(.12,.24,.23),yellow)
pipe('Antenna',(0,0,3.02),(.13,0,3.32),.026,dark);sphere('Antenna tip',(.13,0,3.36),(.10,.10,.10),yellow);group('head',i)
for side in [-1,1]:
 i=len(assets);x=side*.34;pipe('Leg',(x,0,1.12),(x,0,.47),.14,dark);box('Shin housing',(x,0,.66),(.34,.37,.43),teal,.07);box('Grounded boot',(x,-.14,.19),(.48,.7,.38),yellow,.10);group('leg'+str(side),i)
i=len(assets);sphere('Left shoulder',(-.65,0,1.97),(.21,.21,.21),yellow);pipe('Left arm',(-.67,0,1.95),(-.90,-.02,1.42),.12,dark);box('Left forearm',(-.92,-.02,1.32),(.32,.36,.42),teal,.08);sphere('Left hand',(-.94,-.02,1.05),(.19,.16,.17),yellow);group('left',i)
i=len(assets);sphere('Right shoulder',(.65,0,1.98),(.21,.21,.21),yellow);pipe('Upper raised arm',(.7,0,2),(1.01,0,2.38),.14,teal);sphere('Elbow',(1.02,0,2.39),(.16,.16,.16),dark);group('upper',i)
i=len(assets);pipe('Raised forearm',(1.03,0,2.41),(1.20,0,2.9),.14,teal);sphere('Wrist',(1.22,0,2.94),(.15,.15,.15),dark);box('Palm',(1.24,0,3.12),(.32,.20,.31),yellow,.06)
for j in range(4):pipe('Finger',(1.10+j*.095,0,3.24),(1.08+j*.105,0,3.48-(abs(j-1.5)*.04)),.035,yellow,12)
pipe('Thumb',(1.08,-.01,3.10),(.94,-.02,3.23),.055,yellow);group('wave',i)
# Rigid toy rig: each mechanical part has one full bone influence.
d=bpy.data.armatures.new('RobotRig');rig=bpy.data.objects.new('RobotRig',d);s.collection.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
def bone(name,a,b,parent=None):
 e=d.edit_bones.new(name);e.head=a;e.tail=b
 if parent:e.parent=d.edit_bones[parent]
bone('body',(0,0,.8),(0,0,2.1));bone('head',(0,0,2.1),(0,0,3),'body');bone('left',(-.65,0,2),(-.94,0,1.1),'body');bone('upper',(.65,0,2),(1.02,0,2.4),'body');bone('wave',(1.02,0,2.4),(1.24,0,3.4),'upper')
for side in [-1,1]:bone('leg'+str(side),(side*.34,0,1.1),(side*.34,0,.2),'body')
bpy.ops.object.mode_set(mode='OBJECT');bpy.ops.object.select_all(action='DESELECT')
for name,objs in parts.items():
 for o in objs:
  o.select_set(True);bpy.context.view_layer.objects.active=o
  if o.type=='CURVE':bpy.ops.object.convert(target='MESH');o=bpy.context.object
  bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);vg=o.vertex_groups.new(name=name);vg.add(list(range(len(o.data.vertices))),1,'REPLACE');mod=o.modifiers.new('Mechanical rig','ARMATURE');mod.object=rig;o.parent=rig;o.select_set(False)
wave=rig.pose.bones['wave'];wave.rotation_mode='XYZ';head=rig.pose.bones['head'];head.rotation_mode='XYZ'
for f,a in [(1,-.18),(6,.22),(12,-.22),(18,.22),(24,-.18)]:wave.rotation_euler.y=a;wave.keyframe_insert(data_path='rotation_euler',frame=f);head.rotation_euler.y=.04*math.sin(f/24*math.tau);head.keyframe_insert(data_path='rotation_euler',frame=f)
rig.animation_data.action.name='Greeting_Wave';s.frame_start=1;s.frame_end=24;s.render.fps=12;s.frame_set(6);studio(7.1,(.1,0,1.75),(5,-9,4.5));seconds=render()
bpy.ops.object.select_all(action='DESELECT');rig.select_set(True)
for o in s.objects:
 if o.parent==rig:o.select_set(True)
bpy.context.view_layer.objects.active=rig;bpy.ops.export_scene.gltf(filepath=str(OUT/'robot.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_animations=True)
frames=OUT/'frames';frames.mkdir(exist_ok=True);s.cycles.samples=12;batch=time.perf_counter()
for f in range(1,25):s.frame_set(f);render('frames/pose-%02d.png'%f,(480,270))
batch=time.perf_counter()-batch;s.frame_set(6);s.cycles.samples=32
result=save({'render_seconds':seconds,'batch_seconds':batch,'clip':'Greeting_Wave','frames':24,'fps':12,'duration_seconds':2,'rig':'Rigid mechanical parts, one bone per part; not soft skin'})
