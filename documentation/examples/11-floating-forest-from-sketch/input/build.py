"""Rebuild the floating forest example inside the official Blender MCP session.

Creates an independent scene; does not delete the user's other scenes.
All geometry and shaders are procedural, editable, and self-contained.
"""
import bpy
import math
import random
from pathlib import Path
from mathutils import Vector
from mathutils.noise import noise_vector

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'output'
OUT.mkdir(exist_ok=True)
SEED = 291126
rng = random.Random(SEED)
previous = bpy.data.scenes.get('EX11 Floating Forest')
if previous:
    owned_objects = list(previous.objects)
    bpy.data.scenes.remove(previous)
    for obj in owned_objects:
        bpy.data.objects.remove(obj, do_unlink=True)
for col in list(bpy.data.collections):
    if col.name.startswith('EX11 ') and col.users == 0:
        for obj in list(col.objects):
            if len(obj.users_collection) == 1:
                bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(col)
for old_text in list(bpy.data.texts):
    if old_text.name.startswith('EX11 build.py'):
        bpy.data.texts.remove(old_text)
scene = bpy.data.scenes.new('EX11 Floating Forest')
bpy.context.window.scene = scene
scene.unit_settings.system = 'METRIC'
scene['seed'] = SEED
scene['source_sketch'] = '../input/sketch.png'
scene['assumptions'] = 'Approx. 14 m square island; inferred roots, underside and tree backs. Artistic environment, no engine collision validation.'
collections = {}
for name in ['Terrain', 'Fractured geology', 'Exposed roots', 'Broadleaf trees', 'Pine trees', 'Meadow', 'Stream and cascade', 'Falling debris', 'Lighting']:
    col = bpy.data.collections.new('EX11 ' + name)
    scene.collection.children.link(col)
    collections[name] = col

def mesh(name, verts, faces, mats, collection, indices=None, smooth=False):
    data = bpy.data.meshes.new(name)
    data.from_pydata(verts, [], faces)
    data.update()
    obj = bpy.data.objects.new(name, data)
    collections[collection].objects.link(obj)
    for mat in mats:
        data.materials.append(mat)
    for p in data.polygons:
        p.use_smooth = smooth
        if indices:
            p.material_index = indices[p.index]
    return obj

def material(name, dark, light, scale=4, rough=.8, bump=.08):
    m = bpy.data.materials.new('EX11 ' + name)
    m.diffuse_color = (*light, 1)
    m.use_nodes = True
    n = m.node_tree.nodes
    l = m.node_tree.links
    bs = n.get('Principled BSDF')
    bs.inputs['Roughness'].default_value = rough
    tex = n.new('ShaderNodeTexNoise')
    tex.inputs['Scale'].default_value = scale
    tex.inputs['Detail'].default_value = 4
    ramp = n.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = .22
    ramp.color_ramp.elements[0].color = (*dark, 1)
    ramp.color_ramp.elements[1].position = .8
    ramp.color_ramp.elements[1].color = (*light, 1)
    coords = n.new('ShaderNodeTexCoord')
    l.new(coords.outputs['Generated'], tex.inputs['Vector'])
    l.new(tex.outputs['Fac'], ramp.inputs[0])
    l.new(ramp.outputs['Color'], bs.inputs['Base Color'])
    fine = n.new('ShaderNodeTexNoise')
    fine.inputs['Scale'].default_value = 95
    fine.inputs['Detail'].default_value = 3
    l.new(coords.outputs['Generated'], fine.inputs['Vector'])
    b = n.new('ShaderNodeBump')
    b.inputs['Strength'].default_value = .35
    b.inputs['Distance'].default_value = bump
    l.new(fine.outputs['Fac'], b.inputs['Height'])
    l.new(b.outputs['Normal'], bs.inputs['Normal'])
    return m

soil = material('Torn umber soil', (.07,.031,.014), (.26,.125,.042), 7, bump=.13)
stone = material('Fractured warm grey stone', (.095,.085,.061), (.33,.30,.22), 3, bump=.13)
stone_light = material('Fresh fracture surfaces', (.15,.13,.10), (.43,.39,.29), 4, bump=.08)
earth = material('Meadow undergrowth', (.028,.07,.006), (.18,.26,.037), 5, bump=.045)
bark = material('Rough ridged bark', (.036,.018,.009), (.17,.075,.028), 8, bump=.09)
grassmats = [material('Grass '+str(i), a, b, 3, bump=.003) for i,(a,b) in enumerate([
    ((.022,.071,.005),(.16,.31,.025)), ((.035,.12,.007),(.24,.43,.04)),
    ((.055,.095,.009),(.34,.37,.061)), ((.022,.089,.009),(.11,.24,.023))])]
leafmats = [material('Sunlit leaf '+str(i), a, b, 3, rough=.47, bump=.004) for i,(a,b) in enumerate([
    ((.027,.10,.006),(.20,.38,.035)), ((.047,.15,.007),(.32,.47,.054)),
    ((.014,.069,.006),(.11,.28,.017)), ((.032,.11,.008),(.22,.36,.039))])]
for mat in leafmats + grassmats:
    mat.node_tree.nodes.get('Principled BSDF').inputs['Subsurface Weight'].default_value = .055
    mat.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value = .82
    mat.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value = .18
pine_mats = [material('Pine needles '+str(i), (.008,.042,.018), c, 4, rough=.6, bump=.003)
             for i,c in enumerate([(.038,.16,.045),(.083,.22,.052),(.14,.28,.066)])]
water = material('Clear turquoise stream', (.012,.10,.15), (.035,.27,.32), 6, rough=.23, bump=.006)
bs = water.node_tree.nodes.get('Principled BSDF')
bs.inputs['Transmission Weight'].default_value = .08
bs.inputs['IOR'].default_value = 1.333
foam = material('White cascade glints', (.44,.66,.60), (.88,.97,.90), 9, rough=.27, bump=.01)

def tube(name, points, radii, mat, col, sides=8):
    vs=[]; faces=[]
    for i,p in enumerate(points):
        p=Vector(p)
        direction=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
        direction.normalize()
        u=direction.cross(Vector((0,0,1)))
        if u.length<.01: u=Vector((1,0,0))
        u.normalize(); v=direction.cross(u).normalized()
        for j in range(sides):
            a=j*math.tau/sides
            vs.append(p+radii[i]*(math.cos(a)*u+math.sin(a)*v))
        if i:
            for j in range(sides):
                k=(i-1)*sides+j; q=(j+1)%sides
                faces.append((k,(i-1)*sides+q,i*sides+q,i*sides+j))
    faces += [tuple(range(sides-1,-1,-1)),tuple((len(points)-1)*sides+j for j in range(sides))]
    return mesh(name,vs,faces,[mat],col,smooth=True)

def topz(x,y):
    return .12*math.sin(x*.72)*math.cos(y*.61)+.06*math.sin(y*1.8+x*.6)
def streamx(y):
    return 4.18+.62*math.sin(y*.7)+.16*math.sin(y*1.9)
def edgepoint(t):
    c=math.cos(t); s=math.sin(t)
    r=6.87/max(abs(c),abs(s))
    return r*c,r*s

# Continuous meadow grid, depressed under a winding shallow stream.
N=90
verts=[]
for j in range(N+1):
    y=-6.87+j*13.74/N
    for i in range(N+1):
        x=-6.87+i*13.74/N
        depression=.21*math.exp(-((x-streamx(y))/.52)**4)
        verts.append((x,y,topz(x,y)-depression))
faces=[]
for j in range(N):
    for i in range(N):
        q=j*(N+1)+i
        faces.append((q,q+1,q+N+2,q+N+1))
mesh('Living meadow surface',verts,faces,[earth],'Terrain',smooth=True)

# An irregular closed slab with a broken, tapered underside.
R=112; vs=[]
for layer in range(5):
    for k in range(R):
        a=k*math.tau/R; x,y=edgepoint(a)
        scales=[1,.998,.955,.86,.43]
        z=[topz(x,y)-.025,-.45,-1.25,-2.65,-3.7][layer]
        if layer: z+=rng.uniform(-.25,.25)*(1 if layer<3 else 2)
        sc=scales[layer]+(rng.uniform(-.05,.05) if layer>1 else 0)
        vs.append((x*sc,y*sc,z))
faces=[]; mids=[]
for layer in range(4):
    for k in range(R):
        q=layer*R+k; nxt=layer*R+(k+1)%R
        faces.extend([(q,nxt,nxt+R),(q,nxt+R,q+R)])
        mids.extend([0 if layer<1 else 1]*2)
faces.append(tuple(4*R+k for k in range(R-1,-1,-1))); mids.append(1)
mesh('Uprooted earth and rock core',vs,faces,[soil,stone],'Terrain',mids)

def rock(name,pos,scale,col,mat=stone):
    # Icosphere bmesh keeps every chunk a real editable mesh.
    import bmesh
    bm=bmesh.new(); bmesh.ops.create_icosphere(bm,subdivisions=2,radius=1)
    for v in bm.verts:
        v.co*=rng.uniform(.79,1.19)
    data=bpy.data.meshes.new(name); bm.to_mesh(data); bm.free()
    ob=bpy.data.objects.new(name,data); collections[col].objects.link(ob)
    ob.location=pos; ob.scale=scale
    ob.rotation_euler=(rng.random()*.9,rng.random()*.9,rng.random()*math.tau)
    data.materials.append(mat)
    return ob

for k in range(104):
    a=k*math.tau/104; x,y=edgepoint(a)
    # Vertical multi-planar fracture columns with varying broken ends.
    center=Vector((x*.95,y*.95,-1.52+rng.uniform(-.15,.15)))
    tang=Vector((-math.sin(a),math.cos(a),0)); normal=Vector((math.cos(a),math.sin(a),0))
    width=rng.uniform(.32,.60); depth=rng.uniform(.28,.62); height=rng.uniform(.8,1.6)
    v=[]
    for level in range(3):
        for j in range(7):
            ang=j*math.tau/7
            off=tang*(math.cos(ang)*width*rng.uniform(.82,1.2))+normal*(math.sin(ang)*depth*rng.uniform(.8,1.15))
            off.z=[height,rng.uniform(-.2,.25),-height][level]+rng.uniform(-.2,.2)
            if level==2: off-=normal*rng.uniform(.3,.8); off+=tang*rng.uniform(-.25,.25)
            v.append(center+off)
    f=[tuple(range(6,-1,-1)),tuple(range(14,21))]
    for level in range(2):
        for j in range(7): f.append((level*7+j,level*7+(j+1)%7,(level+1)*7+(j+1)%7,(level+1)*7+j))
    mesh('Angular fracture column %03d'%k,v,f,[stone,stone_light],'Fractured geology',[rng.randrange(2) for _ in f])
for k in range(230):
    a=rng.random()*math.tau; x,y=edgepoint(a)
    sz=rng.uniform(.055,.16)
    rock('Ragged soil lip %03d'%k,(x*.995,y*.995,-rng.uniform(.10,.52)),(sz,sz*.75,sz*2.4),'Fractured geology',soil)
for k in range(130):
    a=rng.random()*math.tau; x,y=edgepoint(a)
    rock('Embedded soil gravel %03d'%k,(x*.99,y*.99,rng.uniform(-.18,-1.2)),
         (rng.uniform(.045,.2),rng.uniform(.045,.17),rng.uniform(.055,.2)), 'Fractured geology')
for k in range(36):
    a=rng.random()*math.tau; x,y=edgepoint(a)
    size=rng.uniform(.065,.32)
    rock('Suspended falling fragment %02d'%k,(x*rng.uniform(.92,1.16),y*rng.uniform(.92,1.16),rng.uniform(-5.1,-3.6)),
         (size,size*.8,size*1.3),'Falling debris',stone if k%3 else soil)
for k in range(70):
    a=rng.random()*math.tau; x,y=edgepoint(a)
    z=topz(x,y)-.12; length=rng.uniform(.75,2.1)
    pts=[(x*.93,y*.93,z),(x*.996,y*.996,z-.3),(x*.99+.12,y*.99-.07,z-length*.62),(x*.965+.19,y*.965-.04,z-length)]
    tube('Torn dangling root %02d'%k,pts,[.06,.044,.023,.004],bark,'Exposed roots',6)

# Shallow stream ribbon, streambank stones and a narrow free-falling cascade.
vs=[]
for j in range(141):
    y=6.9-j*13.8/140; cx=streamx(y); width=.43+.06*math.sin(y*2)
    for dx in [-width,width]: vs.append((cx+dx,y,topz(cx,y)-.035))
mesh('Winding water surface',vs,[(2*j,2*j+1,2*j+3,2*j+2) for j in range(140)],[water],'Stream and cascade',smooth=True)
for j in range(160):
    y=rng.uniform(-6.8,6.8); sign=rng.choice([-1,1]); x=streamx(y)+sign*rng.uniform(.44,.66)
    sz=rng.uniform(.035,.14)
    rock('Streambank pebble %03d'%j,(x,y,topz(x,y)+.02),(sz*1.5,sz,sz*.65),'Stream and cascade',stone_light)
endx=streamx(-6.9)
vs=[]
for j in range(56):
    t=j/55; z=-.08-t*4.75; y=-6.92-.38*t-.08*math.sin(t*4)
    width=.45*(1-.58*t)
    for side in [-1,1]: vs.append((endx+side*width+.028*math.sin(t*32),y,z))
mesh('Waterfall sheet',vs,[(2*j,2*j+1,2*j+3,2*j+2) for j in range(55)],[water],'Stream and cascade',smooth=True)
for k in range(16):
    off=rng.uniform(-.4,.4)
    pts=[(endx+off*(1-.58*t)+.018*math.sin(t*30+k),-6.945-.38*t-.08*math.sin(t*4),-.08-t*4.75) for t in [i/28 for i in range(29)]]
    tube('Cascade silver thread %02d'%k,pts,[rng.uniform(.006,.016)]*29,foam,'Stream and cascade',4)

# Broadleaf trees: branched trunks and thousands of individual curved leaf blades.
trees=[(-5.5,-3.8,3.45),(-5.7,1.65,4.4),(-2.7,5.5,4.9),(2.25,5.55,4.15),(5.8,-3.15,3.5),(1.4,-5.55,3.3)]
tree_centers=[]
def leaf(vs,fs,mi,p,length,width,angle,tilt,matidx):
    p=Vector(p); u=Vector((math.cos(angle),math.sin(angle),tilt)).normalized()
    v=Vector((-math.sin(angle),math.cos(angle),0))
    q=len(vs)
    vs.extend([p-u*length*.48,p-v*width*.5,p+Vector((0,0,length*.12)),p+u*length*.52,p+v*width*.5])
    fs.extend([(q,q+1,q+2),(q+1,q+3,q+2),(q+3,q+4,q+2),(q+4,q,q+2)]); mi.extend([matidx]*4)
for ti,(x,y,h) in enumerate(trees):
    h *= .86
    z=topz(x,y); tree_centers.append((x,y))
    crown=Vector((x+.14,y,z+h*.73)); radius=h*.34
    tube('Oak %02d trunk'%ti,[(x,y,z),(x-.04,y+.04,z+h*.35),(x+.13,y,z+h*.72),(x+.24,y+.08,z+h*.96)],[.19,.15,.08,.014],bark,'Broadleaf trees',11)
    for k in range(6):
        a=k*math.tau/6+.3
        tube('Oak %02d spreading root %02d'%(ti,k),[(x+.68*math.cos(a),y+.68*math.sin(a),z+.025),(x+.27*math.cos(a),y+.27*math.sin(a),z+.08),(x,y,z+.38)],[.012,.07,.11],bark,'Broadleaf trees',7)
    lvs=[]; lfs=[]; lm=[]
    for k in range(44):
        az=k*2.39996+rng.uniform(-.25,.25)
        zz=rng.uniform(-.55,.76); rad=radius*math.sqrt(1-zz*zz)*rng.uniform(.4,1)
        center=crown+Vector((math.cos(az)*rad,math.sin(az)*rad,zz*radius*.85))
        branchstart=Vector((x,y,z+h*rng.uniform(.42,.70)))
        mid=branchstart.lerp(center,.58)+Vector((0,0,-.13))
        tube('Oak %02d bough %02d'%(ti,k),[branchstart,mid,center],[.055,.026,.005],bark,'Broadleaf trees',6)
        cluster_radius=radius*rng.uniform(.22,.36)
        for li in range(210):
            phi=rng.random()*math.tau; zz2=rng.uniform(-1,1); rr=cluster_radius*rng.random()**.32
            v=Vector((math.cos(phi)*math.sqrt(1-zz2*zz2),math.sin(phi)*math.sqrt(1-zz2*zz2),zz2*.76))*rr
            leaf(lvs,lfs,lm,center+v,rng.uniform(.13,.24),rng.uniform(.055,.095),rng.random()*math.tau,rng.uniform(-.6,.9),rng.choices(range(4),[4,2,3,2])[0])
    mesh('Oak %02d individual leaves'%ti,lvs,lfs,leafmats,'Broadleaf trees',lm)

# Pines built from radial woody branches and fine needle fans, not solid cones.
for ti,(x,y,h) in enumerate([(-5.8,-.9,4.5),(-5.2,4.6,5.45),(5.65,2.5,4.7)]):
    h *= .88
    z=topz(x,y); tree_centers.append((x,y))
    tube('Pine %02d trunk'%ti,[(x,y,z),(x+.04,y,z+h*.6),(x-.05,y,z+h)],[.15,.07,.008],bark,'Pine trees',9)
    vs=[]; ff=[]; ids=[]
    for tier in range(13):
        frac=.2+tier*.058; height=z+h*frac; reach=h*.275*(1-frac)**.82
        for j in range(9):
            a=j*math.tau/9+tier*.78+rng.uniform(-.15,.15)
            center=Vector((x,y,height)); tip=center+Vector((math.cos(a)*reach,math.sin(a)*reach,.08+reach*.13))
            tube('Pine %02d branch %02d %02d'%(ti,tier,j),[center,center.lerp(tip,.55)-Vector((0,0,.12)),tip],[.022,.015,.003],bark,'Pine trees',5)
            for spray in range(16):
                t=(spray+1)/17; mid=center.lerp(tip,t); spread=reach*.23*(1-t*.65)
                for side in [-1,1]:
                    b=a+side*.8
                    end=mid+Vector((math.cos(b)*spread,math.sin(b)*spread,.14))
                    for needle in range(16):
                        tt=rng.random(); p=mid.lerp(end,tt)
                        angle=b+rng.uniform(-1.6,1.6)
                        leaf(vs,ff,ids,p,rng.uniform(.065,.14),.012,angle,rng.uniform(.1,1.0),rng.randrange(3))
    mesh('Pine %02d needle sprays'%ti,vs,ff,pine_mats,'Pine trees',ids)

# A short living carpet with slightly longer meadow tufts.
vs=[]; ff=[]; ids=[]
for i in range(74000):
    x=rng.uniform(-6.86,6.86); y=rng.uniform(-6.86,6.86)
    if abs(x-streamx(y))<.52: continue
    if any((x-tx)**2+(y-ty)**2<.14 for tx,ty in tree_centers): continue
    z=topz(x,y)+.012; h=rng.uniform(.035,.13); w=rng.uniform(.009,.021); a=rng.random()*math.tau
    bend=rng.uniform(.025,.1); u=Vector((math.cos(a),math.sin(a),0)); v=Vector((-u.y,u.x,0)); p=Vector((x,y,z)); q=len(vs)
    vs.extend([p-v*w,p+v*w,p+u*bend*.4+Vector((0,0,h*.58))+v*w*.55,p+u*bend*.4+Vector((0,0,h*.58))-v*w*.55,p+u*bend+Vector((0,0,h))])
    ff.extend([(q,q+1,q+2,q+3),(q+3,q+2,q+4)]); ids.extend([rng.choices(range(4),[5,3,1,4])[0]]*2)
mesh('Individual meadow grass blades',vs,ff,grassmats,'Meadow',ids)
# A few taller grass clumps echo the sketch and break up the meadow carpet.
vs=[]; ff=[]; ids=[]
for k in range(75):
    x=rng.uniform(-6.5,6.5); y=rng.uniform(-6.5,6.5)
    if abs(x-streamx(y))<.68: continue
    for j in range(18):
        a=rng.random()*math.tau; h=rng.uniform(.15,.36); r=rng.uniform(0,.13)
        p=Vector((x+r*math.cos(a),y+r*math.sin(a),topz(x,y)))
        u=Vector((math.cos(a),math.sin(a),0)); v=Vector((-u.y,u.x,0))*.022; q=len(vs)
        vs.extend([p-v,p+v,p+u*h*.3+Vector((0,0,h*.65))+v*.6,p+u*h*.3+Vector((0,0,h*.65))-v*.6,p+u*h*.85+Vector((0,0,h))])
        ff.extend([(q,q+1,q+2,q+3),(q+3,q+2,q+4)]); ids.extend([1]*2)
mesh('Scattered meadow tufts',vs,ff,grassmats,'Meadow',ids)
for k in range(45):
    x=rng.uniform(-6.2,6.2); y=rng.uniform(-6.2,6.2)
    if abs(x-streamx(y))<.7: continue
    sz=rng.uniform(.06,.24)
    rock('Meadow scattered stone %02d'%k,(x,y,topz(x,y)+.02),(sz*1.4,sz,sz*.55),'Meadow',stone_light)

# Camera and lighting: neutral studio world, no ground plane or skybox.
world=bpy.data.worlds.new('EX11 Neutral backdrop; no skybox')
world.use_nodes=True
world.node_tree.nodes['Background'].inputs[0].default_value=(.72,.76,.78,1)
world.node_tree.nodes['Background'].inputs[1].default_value=.38
# A camera-only neutral background is not geometry or a skybox.
nodes=world.node_tree.nodes; links=world.node_tree.links
visible=nodes.new('ShaderNodeBackground'); visible.inputs[0].default_value=(.78,.71,.60,1); visible.inputs[1].default_value=.85
ray=nodes.new('ShaderNodeLightPath'); mix=nodes.new('ShaderNodeMixShader')
links.new(ray.outputs['Is Camera Ray'],mix.inputs[0]); links.new(nodes['Background'].outputs[0],mix.inputs[1]); links.new(visible.outputs[0],mix.inputs[2]); links.new(mix.outputs[0],nodes['World Output'].inputs['Surface'])
scene.world=world
def area(name,pos,power,size,color):
    data=bpy.data.lights.new(name,'AREA'); data.energy=power; data.shape='DISK'; data.size=size; data.color=color
    ob=bpy.data.objects.new(name,data); collections['Lighting'].objects.link(ob); ob.location=pos
    ob.rotation_euler=(Vector((0,0,0))-ob.location).to_track_quat('-Z','Y').to_euler()
area('EX11 warm broad sun',(-10,-8,17),2400,7,(1,.88,.70))
area('EX11 soft cool fill',(10,-4,10),1200,10,(.77,.88,1))
area('EX11 canopy rim',(-1,10,12),1900,6,(1,.96,.8))
camdata=bpy.data.cameras.new('EX11 Three-quarter camera'); camera=bpy.data.objects.new('EX11 Three-quarter camera',camdata)
collections['Lighting'].objects.link(camera)
camera.location=(20,-28,21)
look=Vector((0,0,-.1)); camera.rotation_euler=(look-camera.location).to_track_quat('-Z','Y').to_euler()
camdata.type='ORTHO'; camdata.ortho_scale=34.2; camdata.clip_end=200
scene.camera=camera
# Fit every mesh, including debris and the waterfall, with a visible margin.
bpy.context.view_layer.update()
inv=camera.matrix_world.inverted()
bounds=[inv @ (obj.matrix_world @ Vector(corner)) for obj in scene.objects if obj.type=='MESH' for corner in obj.bound_box]
minx,maxx=min(p.x for p in bounds),max(p.x for p in bounds)
miny,maxy=min(p.y for p in bounds),max(p.y for p in bounds)
camera.location += camera.rotation_euler.to_matrix() @ Vector(((minx+maxx)/2,(miny+maxy)/2,0))
camdata.ortho_scale=max(maxx-minx,(maxy-miny)*1920/1080)*1.09
scene.render.engine='CYCLES'
prefs=bpy.context.preferences.addons['cycles'].preferences
prefs.get_devices()
if any(d.type=='OPTIX' for d in prefs.devices):
    prefs.compute_device_type='OPTIX'
    for d in prefs.devices: d.use=(d.type=='OPTIX')
    scene.cycles.device='GPU'
else: scene.cycles.device='CPU'
scene.cycles.samples=96
scene.cycles.use_denoising=True
scene.cycles.max_bounces=8
scene.render.resolution_x=1920; scene.render.resolution_y=1080; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGBA'
scene.render.film_transparent=False
scene.view_settings.view_transform='AgX'
scene.view_settings.look='AgX - Medium High Contrast'
scene.view_settings.exposure=.55
scene.render.filepath=str(OUT/'result.png')
for screen in bpy.data.screens:
    for area_ in screen.areas:
        if area_.type=='VIEW_3D':
            area_.spaces.active.region_3d.view_perspective='CAMERA'
text=bpy.data.texts.new('EX11 build.py'); text.write(Path(__file__).read_text(encoding='utf-8'))
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'result.blend'),compress=True)
result={'scene':scene.name,'objects':len(scene.objects),'mesh_polygons':sum(len(o.data.polygons) for o in scene.objects if o.type=='MESH'),'source':str(OUT/'result.blend'),'seed':SEED}
