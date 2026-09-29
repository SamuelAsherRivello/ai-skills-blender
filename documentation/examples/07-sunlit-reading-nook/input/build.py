from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
exec(compile((ROOT/'documentation/examples/_shared/build_common.py').read_text(encoding='utf-8-sig'),'common','exec'))
begin('07-sunlit-reading-nook')
oak=mat('Honey oak',(.36,.20,.085),.55);plaster=mat('Warm plaster',(.73,.69,.59),.85);rust=mat('Rust upholstery',(.43,.10,.04),.88);linen=mat('Cream linen',(.72,.66,.5),.9);green=mat('Leaf green',(.075,.22,.075),.62);terra=mat('Terracotta',(.4,.14,.065),.75);dark=mat('Dark bronze',(.03,.027,.023),.4,.7);rug=mat('Oatmeal weave',(.38,.33,.23),.95)
for x in range(16):
 for y in range(5):box('Oak floor plank',(-1.9+x*.25,-1.6+y*.78,.02),(.244,.77,.06),oak,.008)
box('Room foundation',(0,0,-.12),(4.3,4.3,.2),plaster)
# Window opening is actual missing wall, not glazing over opaque plaster.
box('Back wall below window',(0,1.98,.48),(4.1,.16,.85),plaster);box('Back wall lintel',(0,1.98,2.94),(4.1,.16,.36),plaster)
box('Back left pier',(-1.85,1.98,1.82),(.4,.16,1.85),plaster);box('Back right pier',(1.4,1.98,1.82),(1.35,.16,1.85),plaster)
box('Side wall',(-2.04,0,1.55),(.16,4.1,3.1),plaster)
for x in [-1.6,.7]:box('Window jamb',(x,1.85,1.8),(.075,.24,1.85),oak)
for z in [.88,2.72]:box('Window frame',(-.45,1.85,z),(2.38,.24,.08),oak)
box('Window sill',(-.45,1.72,.85),(2.55,.48,.10),oak);box('Window mullion',(-.45,1.87,1.8),(.055,.1,1.8),oak)
# Soft sky beyond aperture provides a readable window backdrop.
sky=mat('Window daylight',(.52,.73,.9),1);p=sky.node_tree.nodes['Principled BSDF'];p.inputs['Emission Color'].default_value=(.4,.65,.9,1);p.inputs['Emission Strength'].default_value=.4;box('Distant sky',(-.45,2.4,1.8),(3,.04,2),sky,0)
for y in [-1.95,1.86]:box('Oak skirting',(0,y,.16),(4,.06,.18),oak,.005)
box('Woven rug',(.12,-.50,.072),(2.75,2.1,.035),rug,.12)
for x in [-1.2,1.35]:
 for i in range(28):pipe('Rug fringe',(x,-1.5+i*.073,.092),(x+(-.10 if x<0 else .1),-1.5+i*.073,.092),.005,linen,6)
for x in [-.55,.55]:
 for y in [-.52,.48]:pipe('Chair oak leg',(x,y,.09),(x*.9,y*.85,.50),.045,oak)
box('Chair seat',(0,-.08,.66),(1.15,1.08,.25),rust,.13);back=box('Chair back',(0,.40,1.13),(1.17,.28,1.05),rust,.16);back.rotation_euler.x=math.radians(-8)
for x in [-.62,.62]:box('Chair upholstered arm',(x,-.02,.87),(.22,1.06,.36),rust,.095)
pillow=box('Linen cushion',(.03,.17,1.04),(.65,.22,.48),linen,.09);pillow.rotation_euler=(math.radians(-12),0,math.radians(-9))
for x in [-.2,0,.2]:sphere('Cushion tuft',(x,.043,1.06),(.02,.012,.02),rug)
cone('Round side table',(1.25,-.02,.66),.47,.47,.075,oak,64)
for a in [0,2.1,4.2]:pipe('Table leg',(1.25+.34*math.cos(a),-.02+.34*math.sin(a),.09),(1.25+.25*math.cos(a),-.02+.25*math.sin(a),.62),.026,dark)
bookcolors=[mat('Book sage',(.15,.24,.18)),mat('Book ochre',(.55,.30,.05)),mat('Book red',(.31,.06,.035))]
for i,m in enumerate(bookcolors[:2]):box('Table book',(1.3,.06,.72+i*.065),(.43,.30,.055),m,.008)
mug=mat('Ceramic ivory',(.8,.73,.57),.2);cone('Mug',(1.04,-.15,.86),.09,.105,.19,mug);curve('Mug handle',[(1.14,-.15,.93),(1.22,-.15,.9),(1.22,-.15,.80),(1.14,-.15,.79)],.02,mug)
cone('Plant pot',(-1.25,.87,.28),.23,.31,.42,terra);soil=mat('Pot soil',(.035,.022,.012),.95);cone('Soil',(-1.25,.87,.5),.28,.28,.025,soil)
for j in range(9):
 a=j*2.4;end=Vector((-1.25+math.cos(a)*.36,.87+math.sin(a)*.32,.85+(j%3)*.18));pipe('Plant stem',(-1.25,.87,.5),end,.012,green,8);o=sphere('Broad leaf',end,(.13,.055,.30),green,16,8);o.rotation_euler=(.5*math.sin(a),.6*math.cos(a),a)
box('Small wall shelf',(-1.87,-.45,1.9),(.35,1.2,.065),oak)
for j in range(6):box('Shelf book',(-1.81,-.9+j*.15,2.08),(.19,.11,.30+(j%2)*.06),bookcolors[j%3],.008)
studio(7.5,(0,0,1.3),(7,-9,6),floor=True);area('Window soft sun',(-.4,1.6,3),550,(1,.79,.51),1.4,(0,-1,.5))
seconds=render();result=save({'render_seconds':seconds,'seed':31,'layout':'4m open-corner room with a real window opening','limitation':'Studio-assisted window lighting and simplified textiles; no cloth simulation.'})
