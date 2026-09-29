from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
exec(compile((ROOT/'documentation/examples/_shared/build_common.py').read_text(encoding='utf-8-sig'),'common','exec'))
begin('08-modular-greenhouse')
sage=mat('Sage enamel',(.16,.29,.20),.32,.4);brick=mat('Warm old brick',(.32,.12,.065),.8);stone=mat('Paving',(.45,.42,.33),.8);terra=mat('Terracotta pots',(.48,.19,.075),.7);leaf=mat('Green leaves',(.07,.23,.07),.68);soil=mat('Earth',(.055,.03,.014),1);glass=mat('Clear horticultural glass',(.83,.93,.91),.09);p=glass.node_tree.nodes['Principled BSDF'];p.inputs['Transmission Weight'].default_value=1;p.inputs['IOR'].default_value=1.45
owned=[]
def generate(bays=4,spacing=1.0):
 global owned
 if not isinstance(bays,int) or not 1<=bays<=6 or not .7<=spacing<=1.4:raise ValueError('bays 1..6, spacing .7..1.4m')
 for o in owned:bpy.data.objects.remove(o,do_unlink=True)
 owned=[];start=len(assets);length=bays*spacing
 box('Brick foundation',(0,0,.18),(3,length+.20,.36),brick,.025)
 box('Central stone path',(0,0,.38),(.75,length+.1,.045),stone,.01)
 for side in [-1,1]:
  box('Planting soil bed',(side*.95,0,.38),(.8,length-.18,.055),soil,.015)
  for i in range(bays+1):
   y=-length/2+i*spacing;pipe('Upright',(side*1.42,y,.35),(side*1.42,y,2.1),.035,sage);pipe('Roof rafter',(side*1.42,y,2.1),(0,y,2.95),.037,sage)
  for z in [.4,1.20,2.1]:pipe('Side rail',(side*1.42,-length/2,z),(side*1.42,length/2,z),.03,sage)
  for i in range(bays):
   y=-length/2+(i+.5)*spacing;box('Side glass',(side*1.42,y,1.25),(.015,spacing-.08,1.62),glass,.001)
   panel=box('Roof glass',(side*.71,y,2.525),(1.62,spacing-.08,.012),glass,.001);panel.rotation_euler.y=side*math.atan2(.85,1.42)
   cone('Terracotta pot',(side*.94,y,.64),.18,.24,.42,terra,24);cone('Pot rim',(side*.94,y,.86),.255,.255,.07,terra,24)
   for j in range(5):
    a=j*2.4;pt=(side*.94+math.cos(a)*.20,y+math.sin(a)*.18,1.07+(j%2)*.16);pipe('Plant stem',(side*.94,y,.86),pt,.012,leaf,8);o=sphere('Leaf',pt,(.12,.055,.22),leaf,12,6);o.rotation_euler=(math.sin(a)*.55,math.cos(a)*.55,a)
 pipe('Roof ridge',(0,-length/2,2.95),(0,length/2,2.95),.045,sage)
 for end in [-1,1]:
  y=end*length/2
  for x in [-.5,.5]:pipe('Door post',(x,y,.37),(x,y,2.15),.037,sage)
  pipe('Door lintel',(-.5,y,2.15),(.5,y,2.15),.035,sage)
  for x in [-.98,.98]:box('End glass',(x,y,1.24),(.85,.015,1.65),glass,.001)
  if end==1:box('Back door glazing',(0,y,1.22),(.94,.015,1.6),glass,.001)
  else:
   # Door leaf swung outward to show usable entrance.
   o=box('Open glass door',(.65,y-.35,1.23),(.014,.94,1.66),glass,.001)
   for yy in [y-.82,y+.12]:pipe('Open door vertical',(.65,yy,.4),(.65,yy,2.06),.028,sage)
   for z in [.4,2.06]:pipe('Open door rail',(.65,y-.82,z),(.65,y+.12,z),.028,sage)
 owned=list(assets[start:]);s['bay_count']=bays;s['bay_spacing']=spacing;return len(owned)
checks=[]
for b,sp in [(1,.7),(6,1.4),(4,1.)]:checks.append({'bays':b,'spacing':sp,'objects':generate(b,sp)})
for b,sp in [(0,1),(7,1),(4,-1)]:
 try:generate(b,sp);checks.append({'invalid_accepted':True})
 except ValueError:checks.append({'invalid_rejected':[b,sp]})
(OUT/'procedural-checks.json').write_text(json.dumps(checks,indent=2));control=bpy.data.texts.new('GREENHOUSE_CONTROLS.txt');control.write('Rebuild with input/build.py generate(bays=4, spacing=1.0). Valid bays 1..6; spacing .7..1.4 m. Only owned greenhouse objects are replaced; seed 31. Scene custom properties record current settings.')
base=mat('Garden base',(.15,.22,.10),.9);box('Garden diorama',(0,0,.04),(4.4,6.1,.16),base,.18)
for i in range(5):box('Approach stepping stone',(0,-2.7-i*.35,.14),(.75,.25,.10),stone,.035)
studio(9,(0,-.3,1.25),(7,-9,6));s.cycles.max_bounces=10;s.cycles.transmission_bounces=8;seconds=render();result=save({'render_seconds':seconds,'controls':{'bays':4,'spacing':1.0},'procedural_checks':checks,'limitation':'Thin modeled panes; simplified greenery and no climate simulation.'})
