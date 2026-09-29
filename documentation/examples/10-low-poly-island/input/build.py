from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
exec(compile((ROOT/'documentation/examples/_shared/build_common.py').read_text(encoding='utf-8-sig'),'common','exec'))
begin('10-low-poly-island')
rock=mat('Slate cliffs',(.14,.20,.23),.95);rock2=mat('Pale strata',(.30,.35,.32),.95);grass=mat('Meadow',(.20,.38,.12),.95);sand=mat('Warm sand',(.67,.48,.22),.9);water=mat('Turquoise water',(.016,.36,.42),.22,.18);white=mat('Lighthouse ivory',(.82,.77,.57),.65);red=mat('Vermilion roof',(.55,.052,.021),.5);wood=mat('Pine trunks',(.16,.066,.025),.9);pine=mat('Pine green',(.036,.16,.08),.9);dark=mat('Lighthouse iron',(.025,.04,.04),.35,.65)
# Irregular layered island mesh; flat-shaded triangulation is intentional.
N=15;radii=[2.3+random.uniform(-.25,.25) for _ in range(N)];vs=[]
for radius_scale,z in [(1.04,.0),(1.0,.55),(.92,1.0)]:
 for i,r in enumerate(radii):a=i*math.tau/N;vs.append((r*radius_scale*math.cos(a),r*radius_scale*.75*math.sin(a),z+(.08*math.sin(i*3) if z else 0)))
vs.append((0,0,1.03));faces=[]
for layer in range(2):
 for i in range(N):j=(i+1)%N;faces.extend([(layer*N+i,layer*N+j,(layer+1)*N+j),(layer*N+i,(layer+1)*N+j,(layer+1)*N+i)])
for i in range(N):faces.append((45,30+i,30+(i+1)%N))
me=bpy.data.meshes.new('Faceted island strata');me.from_pydata(vs,[],faces);o=bpy.data.objects.new('Island cliffs and meadow',me);s.collection.objects.link(o);finish_obj(o,'Island cliffs and meadow',rock);me.materials.append(rock2);me.materials.append(grass)
for f in me.polygons:f.material_index=2 if f.index>=60 else (1 if f.index%4==0 else 0)
cone('Water disk',(0,0,-.16),3.7,3.7,.28,water,64)
# Sandy landing on the near side.
sphere('Beach',(-.75,-1.30,.55),(.95,.58,.12),sand,16,8)
curve('Winding sand path',[(-.75,-1.25,1.08),(-.6,-.65,1.08),(.1,-.25,1.08),(.25,.2,1.08),(.65,.48,1.08)],.115,sand)
# Lighthouse on island crown.
x,y=.65,.48
cone('Lighthouse tower',(x,y,1.86),.36,.27,1.6,white,16);cone('Red band',(x,y,1.96),.326,.315,.20,red,16);cone('Lantern balcony',(x,y,2.66),.46,.46,.10,dark,24)
lantern=mat('Lantern glass',(.26,.58,.61),.14,.3);cone('Lantern room',(x,y,2.89),.25,.25,.4,lantern,12)
for a in [i*math.tau/8 for i in range(8)]:pipe('Lantern frame',(x+.26*math.cos(a),y+.26*math.sin(a),2.7),(x+.26*math.cos(a),y+.26*math.sin(a),3.1),.018,dark,8)
cone('Red lantern roof',(x,y,3.21),.44,0,.30,red,16);sphere('Roof finial',(x,y,3.4),(.045,.045,.08),dark,12,6)
box('Lighthouse door',(x,y-.345,1.35),(.18,.035,.46),wood,.025)
for z in [1.83,2.30]:box('Tower window',(x,y-.31,z),(.11,.025,.17),dark,.02)
for tx,ty,h in [(-1.3,.25,1.1),(-1,.9,1.35),(-.4,1.1,.9),(1.45,-.4,.85),(1.3,.85,1.1)]:
 pipe('Pine trunk',(tx,ty,1),(tx,ty,1+h*.9),.065,wood,8)
 for z,r in [(h*.38,h*.34),(h*.62,h*.27),(h*.85,h*.2)]:cone('Pine tiers',(tx,ty,1+z),r,0,h*.55,pine,7)
for i in range(9):
 a=i*2.4;r=2.7+.3*math.sin(i);o=sphere('Sea rock',(r*math.cos(a),r*.8*math.sin(a),.02),(.20,.15,.14),rock,8,4)
foam=mat('Foam',(.61,.87,.82),.6)
for i in range(8):
 a=i*.65;curve('Sea ripple',[(2.85*math.cos(a+t),2.85*math.sin(a+t)*.85,.005) for t in [0,.08,.16]],.014,foam)
studio(9.4,(0,0,1.15),(7,-9,7));next(o for o in s.objects if o.name.startswith('Studio floor')).location.z=-.50
path=next(o for o in s.objects if o.name.startswith('Winding sand path'));path.scale.z=.10;path.location.z=.972
seconds=render();result=save({'render_seconds':seconds,'seed':31,'style':'Flat faceted island with stylized geometric vegetation','limitation':'Static illustrative water and inferred terrain; not navigation-tested.'})
