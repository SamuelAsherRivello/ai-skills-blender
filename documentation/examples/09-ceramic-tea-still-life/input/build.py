from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
exec(compile((ROOT/'documentation/examples/_shared/build_common.py').read_text(encoding='utf-8-sig'),'common','exec'))
begin('09-ceramic-tea-still-life')
ceramic=mat('Seafoam glaze',(.13,.44,.38),.19);p=ceramic.node_tree.nodes['Principled BSDF'];p.inputs['Coat Weight'].default_value=.35;p.inputs['Coat Roughness'].default_value=.15
oak=mat('Honey wood',(.43,.23,.065),.4);linen=mat('Natural linen',(.67,.6,.43),.92);orange=mat('Citrus peel',(.95,.34,.016),.55);green=mat('Citrus leaf',(.04,.18,.025),.55);tea=mat('Tea',(.08,.025,.005),.13)
def lathe(name,loc,profile,material):
 vs=[]
 for r,z in profile:
  for j in range(64):a=j*math.tau/64;vs.append((loc[0]+r*math.cos(a),loc[1]+r*math.sin(a),loc[2]+z))
 fs=[]
 for k in range(len(profile)-1):
  for j in range(64):fs.append((k*64+j,k*64+(j+1)%64,(k+1)*64+(j+1)%64,(k+1)*64+j))
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);o=bpy.data.objects.new(name,me);s.collection.objects.link(o);finish_obj(o,name,material)
 for f in me.polygons:f.use_smooth=True
 return o
box('Wood serving tray',(0,0,.12),(3.6,2.25,.14),oak,.13)
for y in [-1.1,1.1]:box('Tray raised rim',(0,y,.25),(3.58,.065,.18),oak,.035)
for x in [-1.75,1.75]:box('Tray end rail',(x,0,.25),(.075,2.1,.18),oak,.035)
basez=.2
lathe('Teapot body',(-.35,.25,basez),[(0,0),(.32,0),(.4,.07),(.56,.28),(.59,.48),(.52,.70),(.35,.85),(.26,.88),(.24,.83),(.32,.80)],ceramic)
lathe('Teapot lid',(-.35,.25,basez),[(0,.90),(.29,.9),(.30,.94),(.23,.98),(0,1.01)],ceramic);sphere('Lid knob',(-.35,.25,basez+1.06),(.08,.08,.075),ceramic)
curve('Arched teapot handle',[(-.78,.25,.43),(-1.23,.25,.47),(-1.36,.25,.91),(-1.16,.25,1.17),(-.76,.25,1.02)],.067,ceramic)
# Swept hollow spout with a real opening at its tip.
cs=[Vector((.12,.25,.60)),Vector((.42,.25,.70)),Vector((.65,.25,.95)),Vector((.82,.25,1.16))];rs=[.18,.15,.105,.075];vs=[]
for inner in [False,True]:
 for k,(c,r) in enumerate(zip(cs,rs)):
  direction=(cs[min(k+1,3)]-cs[max(k-1,0)]).normalized();u=Vector((0,1,0));v=direction.cross(u).normalized()
  for j in range(32):a=j*math.tau/32;vs.append(c+(r-(.025 if inner else 0))*(math.cos(a)*u+math.sin(a)*v))
fs=[]
for offset in [0,128]:
 for k in range(3):
  for j in range(32):f=(offset+k*32+j,offset+k*32+(j+1)%32,offset+(k+1)*32+(j+1)%32,offset+(k+1)*32+j);fs.append(f if offset==0 else tuple(reversed(f)))
for j in range(32):fs.append((96+j,96+(j+1)%32,224+(j+1)%32,224+j))
me=bpy.data.meshes.new('Spout');me.from_pydata(vs,[],fs);o=bpy.data.objects.new('Hollow curved spout',me);s.collection.objects.link(o);finish_obj(o,'Hollow curved spout',ceramic)
for f in me.polygons:f.use_smooth=True
for x,y in [(.55,-.52),(1.13,.36)]:
 lathe('Cup',(x,y,basez),[(0,0),(.14,0),(.17,.04),(.23,.31),(.23,.35),(.208,.35),(.20,.29),(.145,.06),(0,.06)],ceramic)
 curve('Cup handle',[(x+.20,y,.47),(x+.36,y,.48),(x+.37,y,.32),(x+.18,y,.28)],.027,ceramic)
 cone('Tea surface',(x,y,.48),.197,.197,.005,tea,64)
box('Folded linen',(-.63,-.65,.23),(.9,.57,.04),linen,.018);box('Linen fold',(-.64,-.50,.26),(.88,.27,.027),linen,.015)
for i in range(4):box('Linen weave stripe',(-.93+i*.055,-.64,.257),(.014,.52,.003),oak,.001)
sphere('Citrus',(1.24,-.53,.42),(.23,.23,.22),orange,32,16);o=sphere('Citrus leaf',(1.30,-.5,.63),(.14,.05,.017),green,16,8);o.rotation_euler.z=.5
studio(6.5,(0,0,.6),(5,-7,4));seconds=render();result=save({'render_seconds':seconds,'geometry':'Hollow cups and swept open spout; editable lathed ceramic bodies','limitation':'Stylized clean glaze and linen; no micro-crackle or cloth simulation.'})
