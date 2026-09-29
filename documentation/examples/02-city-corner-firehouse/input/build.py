"""Fresh scene builder, run through official Blender Lab MCP. No external assets."""
import bpy, math, random, time, json, pathlib, hashlib
from mathutils import Vector
START=time.perf_counter()
SOURCE=pathlib.Path(__file__).resolve()
ROOT=SOURCE.parents[3]
EX=SOURCE.parents[1]
ATTEMPT=5
OUT=EX/'output'
OUT.mkdir(parents=True,exist_ok=True)
NAME=f'Feedback_Firehouse_{ATTEMPT:02}'
if bpy.data.scenes.get(NAME): raise RuntimeError('Attempt already exists; preserve it and inspect before retry')
s=bpy.data.scenes.new(NAME);bpy.context.window.scene=s
assert len(s.objects)==0
s['fresh_start_objects']=0;s.unit_settings.system='METRIC'
random.seed(27)
col=bpy.data.collections.new(NAME+'_geometry');s.collection.children.link(col)

def own(obj):
 for c in list(obj.users_collection):c.objects.unlink(obj)
 col.objects.link(obj);return obj
def box(name,loc,dim,mat,bevel=.015):
 x,y,z=[v/2 for v in dim]
 verts=[(-x,-y,-z),(x,-y,-z),(x,y,-z),(-x,y,-z),(-x,-y,z),(x,-y,z),(x,y,z),(-x,y,z)]
 faces=[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
 o=bpy.data.objects.new(name,mesh);col.objects.link(o);o.location=loc
 if mat:mesh.materials.append(mat)
 if bevel:
  m=o.modifiers.new('Small edge radius','BEVEL');m.width=bevel;m.segments=2
  o.modifiers.new('Weighted surface normals','WEIGHTED_NORMAL')
 return o
def pipe(name,a,b,r,mat):
 a,b=Vector(a),Vector(b)
 bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=r,depth=(b-a).length,location=(a+b)/2)
 o=own(bpy.context.object);o.name=name;o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();o.data.materials.append(mat)
 for p in o.data.polygons:p.use_smooth=True
 return o
def extruded_profile(name,points,yfront,yback,mat):
 count=len(points);verts=[(x,y,z) for y in [yfront,yback] for x,z in points]
 faces=[tuple(reversed(range(count))),tuple(range(count,2*count))]
 faces += [(i,(i+1)%count,(i+1)%count+count,i+count) for i in range(count)]
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();mesh.materials.append(mat)
 obj=bpy.data.objects.new(name,mesh);col.objects.link(obj);return obj
def material(name,color,rough=.6,metal=0,noise=0):
 m=bpy.data.materials.new(NAME+'_'+name);m.diffuse_color=(*color,1);m.use_nodes=True
 n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
 p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 if noise:
  g=n.new('ShaderNodeNewGeometry');t=n.new('ShaderNodeTexNoise');t.inputs['Scale'].default_value=38;t.inputs['Detail'].default_value=3;l.new(g.outputs['Position'],t.inputs[0])
  b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.22;b.inputs['Distance'].default_value=noise;l.new(t.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal'])
 return m
stone=material('aged limestone',(.37,.34,.29),.78,noise=.004)
concrete=material('paving concrete',(.27,.28,.26),.82,noise=.006)
asphalt=material('aggregate asphalt',(.035,.041,.047),.87,noise=.004)
red=material('oxblood enamel',(.21,.016,.009),.3,noise=.0004)
dark=material('painted iron',(.023,.028,.027),.38)
zinc=material('zinc',(.4,.42,.43),.32,.85)
black=material('rubber',(.009,.011,.01),.8)
inside=material('interior plaster',(.26,.25,.21),.87)
wood=material('timber',(.11,.047,.018),.64)
white=material('aged road paint',(.64,.62,.54),.86)
glass=material('window glass',(.89,.94,.98),.065)
p=glass.node_tree.nodes['Principled BSDF'];p.inputs['Transmission Weight'].default_value=1;p.inputs['IOR'].default_value=1.46
def brickmat(name,side=False):
 m=material(name,(.22,.066,.034),.8);n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
 geo=n.new('ShaderNodeNewGeometry');sep=n.new('ShaderNodeSeparateXYZ');v=n.new('ShaderNodeCombineXYZ');l.new(geo.outputs['Position'],sep.inputs[0]);l.new(sep.outputs['Y' if side else 'X'],v.inputs['X']);l.new(sep.outputs['Z'],v.inputs['Y'])
 t=n.new('ShaderNodeTexBrick');t.inputs['Scale'].default_value=1;t.inputs['Brick Width'].default_value=.235;t.inputs['Row Height'].default_value=.078;t.inputs['Mortar Size'].default_value=.0035;t.inputs['Mortar Smooth'].default_value=.001
 t.inputs['Color1'].default_value=(.17,.052,.027,1);t.inputs['Color2'].default_value=(.30,.105,.058,1);t.inputs['Mortar'].default_value=(.24,.22,.185,1);l.new(v.outputs[0],t.inputs[0]);l.new(t.outputs['Color'],p.inputs['Base Color'])
 b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.45;b.inputs['Distance'].default_value=.006;b.invert=True;l.new(t.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal']);return m
brick=brickmat('running bond');sidebrick=brickmat('side running bond',True)

def wallbox(name,u,z,w,h,depth,mat,side=False,offset=0):
 return box(name,(7-offset,u,z) if side else (u,offset,z),(depth,w,h) if side else (w,depth,h),mat)
def wall_with_holes(side,umin,umax,zmin,zmax,holes):
 # Partition masonry into non-overlapping cells; genuine cavities, no glass over solid wall.
 us=sorted(set([umin,umax]+[v for a,b,c,d in holes for v in (a,b)]));zs=sorted(set([zmin,zmax]+[v for a,b,c,d in holes for v in (c,d)]))
 for a,b in zip(us,us[1:]):
  for c,d in zip(zs,zs[1:]):
   mid=((a+b)/2,(c+d)/2)
   if not any(x<=mid[0]<=y and lo<=mid[1]<=hi for x,y,lo,hi in holes):wallbox('Masonry wall',(a+b)/2,(c+d)/2,b-a,d-c,.38,sidebrick if side else brick,side,.19)
WIN=[-5.45,-2.8,-.15,2.5,5.15]
front_holes=[(x-.66,x+.66,5.85,7.95) for x in WIN]+[(-6.05,-2.45,.24,4.38),(-1.85,1.75,.24,4.38),(4.18,5.65,.24,3.0)]
side_holes=[(y-.65,y+.65,z,z+2.1) for y in [1.5,4.2,6.9,9.5] for z in [1.3,5.85]]
wall_with_holes(False,-7,7,.24,9.05,front_holes);wall_with_holes(True,0,11,.24,9.05,side_holes)
box('Rear wall',(0,10.85,4.65),(14,.3,8.8),brick)
box('Left wall',(-6.85,5.5,4.65),(.3,11,8.8),sidebrick)
box('Ground floor slab',(0,5.5,.23),(14,11,.16),concrete)
box('Upper floor',(0,5.5,4.85),(14,11,.23),wood)
box('Upper interior rear wall',(0,9.9,6.4),(13,.15,3.0),inside)
for z,h,d in [(.48,.34,.42),(4.65,.18,.51),(8.65,.13,.46),(9.07,.20,.7),(9.27,.12,.85)]:
 wallbox('Front limestone course',0,z,14.2,h,d,stone,False,.07)
 wallbox('Side limestone course',5.5,z,11,h,d,stone,True,.07)
box('Roof',(0,5.5,9.05),(14,11,.20),dark)

# Front-facing assemblies; side orientation uses the same local construction.
def window(u,z,side=False,tag='Window'):
 objs=[]
 def wb(name,du,dz,w,h,depth,mat,offset):
  o=wallbox(tag+' '+name,u+du,z+dz,w,h,depth,mat,side,offset);objs.append(o);return o
 wb('glass',0,0,1.15,1.93,.016,glass,.22)
 for du in [-.625,.625]:wb('outer jamb',du,0,.09,2.14,.13,dark,.13)
 for dz in [-1.035,1.035]:wb('frame',0,dz,1.32,.075,.13,dark,.13)
 wb('center sash',0,-.03,1.22,.048,.12,dark,.09);wb('vertical mullion',0,0,.035,2.0,.09,dark,.09)
 wb('sill',0,-1.11,1.48,.12,.59,stone,.11);wb('brick head',0,1.15,1.49,.21,.43,sidebrick if side else brick,.16)
 wb('interior ceiling',0,.98,1.27,.08,1.7,inside,1.03)
 # Visible interior behind glass, not a flat tinted insert.
 wb('interior back',0,0,1.29,1.95,.06,inside,1.8)
 blind=wb('blind',0,.73,1.12,.42,.025,white,.38)
 for dz in [.56,.65,.74,.83,.92]:wb('blind slat',0,dz,1.13,.018,.03,stone,.365)
 return objs
groups=[]
for j,x in enumerate(WIN):groups.append(window(x,6.90,tag=f'FrontWindow{j+1}'))
# Reversible, scoped facade controls keep all associated parts and infill coherent.
control=bpy.data.objects.new('Facade Controls',None);col.objects.link(control)
control['window_count']=5;control['blind_height']=.42
for j,(x,parts) in enumerate(zip(WIN,groups)):
 for obj in parts:obj['front_window_index']=j+1
 fill=wallbox('Unused window infill',x,6.9,1.32,2.10,.38,brick,offset=.19);fill['front_infill_index']=j+1;fill.hide_render=True;fill.hide_viewport=True
control_source='''import bpy
def set_facade(window_count=5, blind_height=.42):
    if type(window_count) is not int or not 1 <= window_count <= 5:
        raise ValueError("window_count must be an integer from 1 to 5")
    if type(blind_height) not in (int, float) or not .2 <= blind_height <= 1.2:
        raise ValueError("blind_height must be between .2 and 1.2 meters")
    scene=bpy.context.scene
    for obj in scene.objects:
        index=obj.get("front_window_index")
        if index:
            obj.hide_render=index>window_count;obj.hide_viewport=index>window_count
            if obj.name.startswith("FrontWindow") and " blind" in obj.name:
                if "slat" in obj.name:
                    obj.hide_render=True;obj.hide_viewport=True
                else:
                    obj.scale.z=blind_height/.42;obj.location.z=7.84-blind_height/2
        index=obj.get("front_infill_index")
        if index:obj.hide_render=index<=window_count;obj.hide_viewport=index<=window_count
    ctrl=next(o for o in scene.objects if o.type=="EMPTY" and "window_count" in o)
    ctrl["window_count"]=window_count;ctrl["blind_height"]=blind_height
    bpy.context.view_layer.update()
    return {"window_count":window_count,"blind_height":blind_height}
'''
controls_text=bpy.data.texts.new('EDIT_FACADE_FEEDBACK.py');controls_text.write(control_source)
control_namespace={};exec(control_source,control_namespace);control_namespace['set_facade']()
for y in [1.5,4.2,6.9,9.5]:
 for z in [2.35,6.90]:window(y,z,True,'Side window')
def text(body,loc,size,mat=stone):
 d=bpy.data.curves.new('Sign','FONT');d.body=body;d.align_x='CENTER';d.size=size;d.extrude=.004
 o=bpy.data.objects.new('Sign '+body,d);col.objects.link(o);o.location=loc;o.rotation_euler=(math.pi/2,0,0);d.materials.append(mat);return o
for j,x in enumerate([-4.25,-.05]):
 for xx in [x-1.9,x+1.9]:wallbox('Bay stone jamb',xx,2.33,.19,4.25,.49,stone,offset=.03)
 # Segmental arch is genuine opening geometry rather than a curve drawn over a wall.
 for k in range(24):
  a=math.pi*k/24+.004;b=math.pi*(k+1)/24-.004
  pts=[(x+1.82*math.cos(a),3.57+.79*math.sin(a)),(x+1.82*math.cos(b),3.57+.79*math.sin(b)),(x+2.0*math.cos(b),3.57+1.0*math.sin(b)),(x+2.0*math.cos(a),3.57+1.0*math.sin(a))]
  extruded_profile('Arch voussoir',pts,-.09,.35,stone)
 for k in range(32):
  a=-1.8+3.6*k/32;b=-1.8+3.6*(k+1)/32
  za=3.57+.79*math.sqrt(max(0,1-(a/1.82)**2));zb=3.57+.79*math.sqrt(max(0,1-(b/1.82)**2))
  extruded_profile('Masonry above arch',[(x+a,za),(x+b,zb),(x+b,4.38),(x+a,4.38)],0,.38,brick)
 # Panels and glazed upper door rows leave real visual depth into the bay.
 for z in [.56,1.13,1.70,2.27,2.84,3.41]:
  for dx in [-1.31,-.435,.435,1.31]:
   glazed=z>2.5
   wallbox('Door glass' if glazed else 'Door inset panel',x+dx,z,.81,.49,.025,glass if glazed else red,offset=.29)
  wallbox('Door cross rail',x,z+.275,3.60,.065,.10,red,offset=.24)
 for dx in [-1.78,-.88,0,.88,1.78]:wallbox('Door upright',x+dx,1.92,.065,3.34,.10,red,offset=.24)
 pts=[(x+1.75*math.cos(math.pi*k/32),3.56+.73*math.sin(math.pi*k/32)) for k in range(33)]
 extruded_profile('Arched transom glass',pts,.28,.296,glass)
 for k in range(32):
  a=math.pi*k/32;b=math.pi*(k+1)/32
  pipe('Curved transom frame',(x+1.77*math.cos(a),.235,3.56+.76*math.sin(a)),(x+1.77*math.cos(b),.235,3.56+.76*math.sin(b)),.027,red)
 for dx in [-.9,0,.9]:
  h=.72*math.sqrt(1-(dx/1.75)**2)
  wallbox('Transom division',x+dx,3.57+h/2,.038,h,.06,red,offset=.24)
 for dx in [-.12,.12]:wallbox('Door pull',x+dx,1.55,.035,.24,.06,zinc,offset=.17)
 box('Bay interior back',(x,6.0,2.4),(3.65,.12,4.2),inside)
 for dx in [-1.4,1.4]:box('Equipment cabinet',(x+dx,3,1.25),(.5,.6,1.9),red)
 text(str(j+1),(x,.13,4.85),.22,dark)
wallbox('Entry door',4.915,1.60,1.4,2.67,.12,red,offset=.21)
wallbox('Entry glass',4.915,1.93,1.12,1.55,.018,glass,offset=.135)
wallbox('Entry handle',5.43,1.55,.03,.48,.11,zinc,offset=.08)
text('F I R E   S T A T I O N   0 7',(-.5,-.04,5.20),.31,dark)
box('Sign stone inset',(-.5,.012,5.33),(8.35,.08,.48),stone,.015)
text('EST. 1924',(4.92,-.04,3.28),.15,dark)
for x in [-6.56,2.45,6.65]:
 pipe('Rain pipe',(x,-.09,.4),(x,-.09,8.55),.044,dark)
 for z in [1,3,5,7]:wallbox('Pipe bracket',x,z,.16,.028,.21,zinc,offset=.02)
for x in [-6.5,2.65,6.0]:
 pipe('Lamp arm',(x,-.05,3.75),(x,-.5,3.75),.025,dark)
 box('Lantern',(x,-.5,3.57),(.18,.18,.30),dark)
 box('Lantern face',(x,-.60,3.57),(.13,.012,.19),white)
# Hose-drying tower is a separate mass with restrained cornice and vent depth.
tower=box('Tower',(4.8,8.5,10.7),(2.7,3.2,5),sidebrick)
tower.data.materials.append(brick)
for face in tower.data.polygons:
 if abs(face.normal.y)>.5:face.material_index=1
box('Tower cap',(4.8,8.5,13.27),(3.06,3.56,.22),stone)
for x in [-6.8+i*.24 for i in range(58)]:box('Cornice dentil',(x,-.09,8.87),(.12,.30,.17),stone,.008)
for y in [.1+i*.24 for i in range(46)]:box('Side cornice dentil',(7.07,y,8.87),(.30,.12,.17),stone,.008)
for y in [2.85,5.55,8.25]:
 box('Side pilaster',(7.01,y,4.7),(.14,.28,8.0),sidebrick,.008)
box('Electrical meter',(6.25,-.08,1.5),(.32,.22,.43),zinc)
pipe('Service conduit',(6.25,.01,1.3),(6.25,.01,.3),.012,zinc)
for x in [3.95,4.8,5.65]:
 box('Tower vent recess',(x,6.87,11.72),(.40,.05,1.5),black)
 for z in [11.05+i*.13 for i in range(11)]:box('Tower louvers',(x,6.8,z),(.42,.14,.035),dark,.005)

# Street geometry and neighboring scale cues.
box('Continuous street',(0,0,-.15),(220,220,.20),asphalt,0)
box('Sidewalk',(0,5.0,.065),(18,16,.23),concrete)
box('Continuous west sidewalk',(-26,5,.065),(34,16,.23),concrete)
box('Continuous north sidewalk',(0,34,.065),(18,42,.23),concrete)
for x in [i*1.4-8.4 for i in range(13)]:box('Pavement joint',(x,-1.4,.184),(.012,2.85,.005),dark,0)
for y in [-2.4,-1.0,.4,1.8,3.2,4.6,6,7.4,8.8,10.2,11.6]:box('Side paving joint',(8,y,.184),(1.9,.01,.005),dark,0)
for x in [i-8.5 for i in range(18)]:box('Front curb',(x,-3.0,.075),(.98,.22,.30),stone,.012)
for y in range(-2,13):box('Side curb',(9.0,y,.075),(.22,.98,.30),stone,.012)
for i in range(8):
 box('Crosswalk front',(7.45,-4.0-i*.68,-.039),(2,.35,.013),white,.001)
 box('Crosswalk side',(10.0+i*.68,-1.9,-.039),(.35,2,.013),white,.001)
for x in range(-45,45,6):box('Lane dash',(x,-7.0,-.04),(2.8,.09,.012),white,.001)
for y in range(-30,60,6):box('Lane dash',(13.5,y,-.04),(.09,2.8,.012),white,.001)
for x,y in [(-8,-1.8),(8.2,11)]:
 pipe('Streetlight pole',(x,y,.2),(x,y,5.4),.055,dark);pipe('Streetlight arm',(x,y,5.4),(x-.8,y,5.5),.032,dark);box('Streetlight head',(x-.85,y,5.5),(.55,.22,.10),dark)
pipe('Hydrant body',(8,-1.85,.25),(8,-1.85,1.1),.13,red)
pipe('Hydrant crossbar',(7.75,-1.85,.8),(8.25,-1.85,.8),.075,red)
pipe('Hydrant top',(8,-1.85,1.08),(8,-1.85,1.16),.17,red)
for i in range(9):box('Drain grate',(8.75,-2.7+i*.065,-.016),(.32,.025,.022),dark,0)
facade=material('neighbor buff brick',(.24,.21,.16),.8,noise=.003)
def neighbor(x,y,w,d,h):
 finish=facade if x<0 else brick
 shell=box('Urban neighbor',(x,y,h/2),(w,d,h),finish)
 shell.data.materials.append(sidebrick)
 for face in shell.data.polygons:
  if abs(face.normal.x)>.5 and x>=0:face.material_index=1
 for z in [2.2+i*3.1 for i in range(int(h/3.1))]:
  for u in [x-w/2+1.2+i*2.2 for i in range(int(w/2.2))]:
   box('Neighbor window recess',(u,y-d/2-.025,z),(1.1,.06,1.6),dark)
   box('Neighbor reflective pane',(u,y-d/2-.07,z),(.95,.015,1.45),glass)
   box('Neighbor lintel',(u,y-d/2-.11,z+.86),(1.27,.23,.13),stone)
   box('Neighbor sill',(u,y-d/2-.14,z-.85),(1.25,.32,.10),stone)
   for xx in [u-.5,u,u+.5]:box('Neighbor sash',(xx,y-d/2-.09,z),(.035,.035,1.5),stone,.004)
   box('Neighbor transom',(u,y-d/2-.095,z),(1,.035,.045),stone,.004)
  box('Neighbor floor course',(x,y-d/2-.06,z+1.25),(w,.22,.15),stone)
 box('Neighbor cornice',(x,y,h),(w+.25,d+.2,.2),stone)
 # Side elevations are visible in the actual camera; complete the secondary facade.
 for yy in [y-d/2+1.4+i*2.5 for i in range(int(d/2.5))]:
  for z in [2.2+i*3.1 for i in range(int(h/3.1))]:
   box('Context side recess',(x+w/2+.01,yy,z),(.06,1.1,1.6),dark)
   box('Context side pane',(x+w/2+.05,yy,z),(.018,.97,1.44),glass)
   box('Context side sill',(x+w/2+.09,yy,z-.85),(.32,1.24,.10),stone)
   box('Context side sash',(x+w/2+.065,yy,z),(.04,.035,1.48),stone,.005)
 for xx in [x-w/2+.18,x+w/2-.18]:box('Context pilaster',(xx,y-d/2-.04,h/2),(.23,.22,h),stone)
neighbor(-14,5,10,12,13.5);neighbor(-25,8,10,15,17);neighbor(0,25,16,10,15);neighbor(24,24,12,10,19)
# Opposite street geometry is outside the camera but provides real reflections.
neighbor(-9,-54,15,8,11);neighbor(11,-55,13,9,15)
for x in [-18,-12,-6,0,6,12,18]:
 box('Opposite shop light facade',(x,-49.8,3),(3.6,.12,4),inside)
 box('Opposite shop glazing',(x,-49.7,2.6),(3.3,.05,2.9),glass)
# Large-scale surface variation supplements, rather than replaces, fine bump.
for mat,lo,hi,scale in [(asphalt,(.031,.034,.038),(.044,.048,.052),2.8),(concrete,(.23,.24,.225),(.30,.31,.29),3.4),(stone,(.30,.28,.235),(.40,.37,.31),5.6)]:
 n=mat.node_tree.nodes;l=mat.node_tree.links;p=n['Principled BSDF'];g=n.new('ShaderNodeNewGeometry');tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=scale;tex.inputs['Detail'].default_value=4;l.new(g.outputs['Position'],tex.inputs[0]);r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(*lo,1);r.color_ramp.elements[1].color=(*hi,1);l.new(tex.outputs['Fac'],r.inputs[0]);l.new(r.outputs['Color'],p.inputs['Base Color'])

# Lighting deliberately starts with a simple stable daylight baseline.
# Localized base darkening is driven by height, with noise breaking up its boundary.
for mat in [brick,sidebrick]:
 n=mat.node_tree.nodes;l=mat.node_tree.links;p=n['Principled BSDF'];old=p.inputs['Base Color'].links[0].from_socket
 g=n.new('ShaderNodeNewGeometry');sep=n.new('ShaderNodeSeparateXYZ');l.new(g.outputs['Position'],sep.inputs[0]);r=n.new('ShaderNodeMapRange');r.inputs['From Min'].default_value=.15;r.inputs['From Max'].default_value=1.3;r.inputs['To Min'].default_value=.45;r.inputs['To Max'].default_value=1.0;l.new(sep.outputs['Z'],r.inputs['Value'])
 mult=n.new('ShaderNodeMixRGB');mult.blend_type='MULTIPLY';mult.inputs[0].default_value=1;l.new(old,mult.inputs[1]);l.new(r.outputs['Result'],mult.inputs[2]);l.new(mult.outputs[0],p.inputs['Base Color'])
# Thin street repairs and runoff at curb contact add scale without a uniform dirt layer.
repair=material('asphalt repair',(.022,.025,.028),.91,noise=.003)
for x,y,w,d in [(-4,-6,1.5,.55),(4,-4.2,.8,.3),(11,4,.35,2.1),(-10,-5,.25,3)]:box('Subtle road repair',(x,y,-.04),(w,d,.009),repair,.018)
grit=material('joint grit',(.045,.037,.022),.96)
for i in range(75):
 x=random.uniform(-8.5,8.5);y=-2.83+random.uniform(-.04,.07)
 box('Curb debris',(x,y,.19),(random.uniform(.01,.04),random.uniform(.015,.05),.005),grit,0)
for y in [2.7,6.1,10.3]:
 for i in range(8):box('Curb runoff trace',(9.14,y+i*.018,-.038),(.18+random.random()*.20,.012,.003),repair,0)
# One leafless street tree: branch hierarchy avoids a blob-shaped foliage placeholder.
bark=material('tree bark',(.065,.043,.023),.9,noise=.009)
tx,ty=-9,-1.8
pipe('Tree trunk',(tx,ty,.2),(tx+.12,ty,3.4),.11,bark)
for k in range(9):
 a=k*2.399;start=Vector((tx+.07,ty,1.9+k*.16));end=start+Vector((math.cos(a)*1.1,math.sin(a)*1.0,1.6))
 pipe('Tree bough',start,end,.042,bark)
 for j in range(3):
  mid=start.lerp(end,.48+j*.18);tip=mid+Vector((math.cos(a+j)*.55,math.sin(a+j)*.55,.65));pipe('Tree twig',mid,tip,.013,bark)
box('Tree planting bed',(-9,-1.8,.19),(.85,.85,.06),grit,.04)
for z in [.53,.69,.85]:box('Bench timber slat',(7.8,8,z),(.07,1.8,.065),wood,.012)
for y in [7.3,8.7]:pipe('Bench frame',(7.8,y,.2),(7.8,y,.95),.022,dark)
world=bpy.data.worlds.new(NAME+'_world');world.use_nodes=True;s.world=world
bg=world.node_tree.nodes['Background'];sky=world.node_tree.nodes.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(40);sky.sun_rotation=math.radians(220);sky.sun_disc=False;sky.altitude=100;world.node_tree.links.new(sky.outputs[0],bg.inputs[0]);bg.inputs[1].default_value=.18
d=bpy.data.lights.new('Daylight','SUN');d.energy=2.5;d.angle=math.radians(1.5);o=bpy.data.objects.new('Daylight',d);col.objects.link(o);o.rotation_euler=Vector((.55,.75,-1)).to_track_quat('-Z','Y').to_euler()
d=bpy.data.cameras.new('Street architectural camera');cam=bpy.data.objects.new('Street architectural camera',d);col.objects.link(cam);cam.location=(22,-32,3.4);cam.rotation_euler=(Vector((0,3.8,3.4))-cam.location).to_track_quat('-Z','Y').to_euler();d.lens=51;d.shift_y=.09;d.clip_end=400;s.camera=cam
s.render.engine='CYCLES';s.cycles.samples=64;s.cycles.use_denoising=True;s.cycles.max_bounces=8
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
for device in prefs.devices:device.use=device.type=='OPTIX'
s.cycles.device='GPU';s.view_settings.view_transform='AgX';s.view_settings.exposure=.5
s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(OUT/'result.png')
s['attempt']=ATTEMPT;s['seed']=27
bpy.context.view_layer.update()
# Final blue-sky and color treatment.
w=s.world; n=w.node_tree.nodes;l=w.node_tree.links
bg=n['Background'];wo=n['World Output']
def node(kind,name,x,y):
 a=n.new(kind);a.name=name;a.label=name;a.location=(x,y);return a
tex=node('ShaderNodeTexCoord','Sky directions',-1000,0)
noise=node('ShaderNodeTexNoise','Soft cloud banks',-750,0);noise.inputs['Scale'].default_value=7;noise.inputs['Detail'].default_value=5;noise.inputs['Roughness'].default_value=.57
l.new(tex.outputs['Normal'],noise.inputs['Vector'])
ramp=node('ShaderNodeValToRGB','Cloud coverage',-510,0);ramp.color_ramp.elements[0].position=.50;ramp.color_ramp.elements[1].position=.64
l.new(noise.outputs['Fac'],ramp.inputs[0])
mix=node('ShaderNodeMixRGB','Blue sky and white clouds',-230,0);mix.inputs[1].default_value=(.10,.32,.68,1);mix.inputs[2].default_value=(.9,.94,1,1)
l.new(ramp.outputs['Color'],mix.inputs[0])
b=node('ShaderNodeBackground','Visible cloud sky',0,0);b.inputs['Strength'].default_value=.8;l.new(mix.outputs[0],b.inputs['Color'])
ray=node('ShaderNodeLightPath','Preserve daylight illumination',-220,-300)
m=node('ShaderNodeMath','Camera and glossy sky',0,-300);m.operation='MAXIMUM';l.new(ray.outputs['Is Camera Ray'],m.inputs[0]);l.new(ray.outputs['Is Glossy Ray'],m.inputs[1])
sh=node('ShaderNodeMixShader','Cloud appearance with existing daylight',250,0);l.new(m.outputs[0],sh.inputs[0]);l.new(bg.outputs[0],sh.inputs[1]);l.new(b.outputs[0],sh.inputs[2]);l.new(sh.outputs[0],wo.inputs['Surface'])
g=s.compositing_node_group
if g is None:
 g=bpy.data.node_groups.new('Firehouse_SkyColor_Compositor','CompositorNodeTree')
 g.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
 g.nodes.new('CompositorNodeRLayers');g.nodes.new('CompositorNodeHueSat');g.nodes.new('NodeGroupOutput');s.compositing_node_group=g
r=next(x for x in g.nodes if x.bl_idname=='CompositorNodeRLayers');h=next(x for x in g.nodes if x.bl_idname=='CompositorNodeHueSat');o=next(x for x in g.nodes if x.bl_idname=='NodeGroupOutput')
h.inputs['Saturation'].default_value=1.10;h.label='10% saturation lift';g.links.new(r.outputs['Image'],h.inputs['Image']);g.links.new(h.outputs['Image'],o.inputs['Image'])

build_seconds=time.perf_counter()-START
t=bpy.data.texts.new(f'BUILD_ATTEMPT_{ATTEMPT:02}.py');t.write(SOURCE.read_text(encoding='utf-8'))
manifest={'run_id':NAME,'source':'result.blend','fresh_start_objects':0,'build_seconds':build_seconds,'blender_version':bpy.app.version_string,'objects':len(s.objects),'script_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'settings':{'engine':'CYCLES','device':'OPTIX','samples':64,'seed':27,'resolution':[1280,720]},'outputs':[{'path':'result.png','width':1280,'height':720,'alpha':True}]}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
bpy.data.libraries.write(str(OUT/'result.blend'),{s,t,controls_text},path_remap='RELATIVE_ALL',fake_user=True,compress=True)
result=manifest
