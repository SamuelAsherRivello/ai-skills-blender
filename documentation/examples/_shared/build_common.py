import bpy, math, random, time, json
from pathlib import Path
from mathutils import Vector
# ROOT is supplied by the example's build.py.
def begin(slug):
 global s,OUT,INPUT,assets
 OUT=ROOT/'documentation/examples'/slug/'output';INPUT=OUT.parent/'input';assets=[]
 s=bpy.data.scenes.new('Example_'+slug);bpy.context.window.scene=s;s.unit_settings.system='METRIC'
 s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=True
 prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
 for d in prefs.devices:d.use=d.type=='OPTIX'
 s.cycles.device='GPU';s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA'
 s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=.3
 w=bpy.data.worlds.new(slug+'_world');w.use_nodes=True;w.node_tree.nodes['Background'].inputs[0].default_value=(.24,.3,.42,1);w.node_tree.nodes['Background'].inputs[1].default_value=.35;s.world=w
 random.seed(31);return s

def mat(name,color,rough=.45,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;return m

def finish_obj(o,name,material,bevel=0):
 o.name=name
 if material:o.data.materials.append(material)
 if bevel:
  m=o.modifiers.new('Soft manufactured edges','BEVEL');m.width=bevel;m.segments=3
  o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
 assets.append(o);return o

def box(name,loc,size,m,bevel=.025):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return finish_obj(o,name,m,bevel)
def sphere(name,loc,scale,m,segments=24,rings=12):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=rings,location=loc);o=bpy.context.object;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 for f in o.data.polygons:f.use_smooth=True
 return finish_obj(o,name,m)
def cone(name,loc,r1,r2,depth,m,vertices=32):
 bpy.ops.mesh.primitive_cone_add(vertices=vertices,radius1=r1,radius2=r2,depth=depth,location=loc);return finish_obj(bpy.context.object,name,m,.012)
def pipe(name,a,b,r,m,vertices=16):
 a,b=Vector(a),Vector(b);o=cone(name,(a+b)/2,r,r,(b-a).length,m,vertices);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o

def curve(name,points,r,m):
 d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.resolution_u=16;d.bevel_depth=r;d.bevel_resolution=3;p=d.splines.new('BEZIER');p.bezier_points.add(len(points)-1)
 for b,co in zip(p.bezier_points,points):b.co=co;b.handle_left_type='AUTO';b.handle_right_type='AUTO'
 o=bpy.data.objects.new(name,d);s.collection.objects.link(o);d.materials.append(m);assets.append(o);return o

def area(name,loc,power,color,size,target=(0,0,1)):
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.color=color;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
def studio(scale=6,target=(0,0,1),cam=(6,-8,5),floor=True):
 if floor:box('Studio floor',(0,0,-.09),(200,200,.16),mat('Warm studio',(.19,.22,.23)),0)
 area('Large warm key',(-3,-4,7),1000,(1,.85,.67),5,target);area('Cool fill',(5,-1,4),650,(.65,.82,1),4,target);area('Edge softbox',(1,5,6),1100,(1,.94,.82),3,target)
 d=bpy.data.cameras.new('Presentation camera');o=bpy.data.objects.new('Presentation camera',d);s.collection.objects.link(o);o.location=cam;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=scale;s.camera=o

def render(name='result.png',resolution=None):
 if resolution:s.render.resolution_x,s.render.resolution_y=resolution
 s.render.filepath=str(OUT/name);t=time.perf_counter();bpy.ops.render.render(write_still=True);return time.perf_counter()-t

def save(manifest):
 s.render.resolution_x=1280;s.render.resolution_y=720;s.render.filepath='//result.png'
 text=bpy.data.texts.new('BUILD.py');text.write((INPUT/'build.py').read_text(encoding='utf-8'))
 common=bpy.data.texts.new('COMMON.py');common.write((ROOT/'documentation/examples/_shared/build_common.py').read_text(encoding='utf-8'))
 for img in bpy.data.images:
  if img.type=='IMAGE' and img.filepath and not img.packed_file:
   try:img.pack()
   except:pass
 bpy.data.libraries.write(str(OUT/'result.blend'),{s,text,common},fake_user=True,path_remap='RELATIVE_ALL',compress=True)
 manifest.update(scene=s.name,objects=len(s.objects),blender=bpy.app.version_string,engine='Cycles',device='OptiX',samples=s.cycles.samples,resolution=[1280,720],iteration=1)
 (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2));return manifest
