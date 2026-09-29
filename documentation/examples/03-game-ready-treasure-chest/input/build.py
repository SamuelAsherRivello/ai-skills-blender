from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
exec(compile((ROOT/'documentation/examples/_shared/build_common.py').read_text(encoding='utf-8-sig'),'common','exec'))
begin('03-game-ready-treasure-chest')
wood=mat('Walnut',(.22,.072,.022),.42);iron=mat('Forged iron',(.026,.039,.047),.34,.7);gold=mat('Antique brass',(.48,.29,.07),.28,.78)
n=wood.node_tree.nodes;l=wood.node_tree.links;p=n['Principled BSDF'];tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=4;tex.inputs['Detail'].default_value=3;coords=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(2,35,35);l.new(coords.outputs['Generated'],mapping.inputs[0]);l.new(mapping.outputs[0],tex.inputs[0]);r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(.055,.014,.004,1);r.color_ramp.elements[1].color=(.38,.16,.045,1);l.new(tex.outputs['Fac'],r.inputs[0]);l.new(r.outputs[0],p.inputs['Base Color']);b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.17;b.inputs['Distance'].default_value=.025;l.new(tex.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal'])
for z in [.35,.59,.83,1.07]:
 for y in [-.57,.57]:box('Walnut side plank',(0,y,z),(2.4,.12,.22),wood,.018)
 for x in [-1.14,1.14]:box('End plank',(x,0,z),(.12,1.05,.22),wood,.018)
box('Base',(0,0,.21),(2.4,1.22,.16),wood)
# Curved lid: separate longitudinal wooden staves.
for i in range(10):
 a=(i+.5)*math.pi/10;y=.62*math.cos(a);z=1.18+.47*math.sin(a);o=box('Curved lid stave',(0,y,z),(2.4,.20,.09),wood,.012);o.rotation_euler.x=a-math.pi/2
for x in [-.86,.86]:
 for y in [-.65,.65]:box('Iron strap',(x,y,.72),(.15,.07,1.04),iron,.014)
 pts=[(x,.66*math.cos(i*math.pi/24),1.18+.51*math.sin(i*math.pi/24)) for i in range(25)];curve('Lid iron band',pts,.058,iron)
 for y in [-.694,.694]:
  for z in [.3,.59,.88,1.13]:sphere('Brass rivet',(x,y,z),(.043,.02,.043),gold,12,6)
for x in [-1,1]:
 for y in [-.45,.45]:box('Brass foot',(x,y,.10),(.23,.25,.20),gold)
box('Clasp plate',(0,-.69,1.04),(.27,.075,.38),gold,.028);box('Lock body',(0,-.76,.86),(.25,.13,.25),gold,.035);box('Keyhole',(0,-.832,.88),(.035,.007,.072),iron,.008)
# Join evaluated parts into a compact target, retaining a detailed source.
parts=list(assets);bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.convert(target='MESH');bpy.ops.object.join();target=bpy.context.object;target.name='Chest_export_target'
# Triangulated measured budget; decimate curved hardware conservatively.
mod=target.modifiers.new('Budget reduction','DECIMATE');mod.ratio=.45;bpy.ops.object.modifier_apply(modifier=mod.name)
source=target.copy();source.data=target.data.copy();source.name='Chest_detail_source';s.collection.objects.link(source)
# Source bevel gives a real selected-to-active normal-map contribution.
bev=source.modifiers.new('Source edge detail','BEVEL');bev.width=.009;bev.segments=3
bpy.ops.object.select_all(action='DESELECT');target.select_set(True);bpy.context.view_layer.objects.active=target;bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(island_margin=.025);bpy.ops.object.mode_set(mode='OBJECT')
tri=sum(len(f.vertices)-2 for f in target.data.polygons);assert tri<12000,tri
maps=OUT/'maps';maps.mkdir(exist_ok=True);s.cycles.samples=8;s.render.bake.use_selected_to_active=True;s.render.bake.cage_extrusion=.04;s.render.bake.margin=12
baked={};t=time.perf_counter()
for label,kind in [('base-color','DIFFUSE'),('normal','NORMAL')]:
 img=bpy.data.images.new('Chest_'+label,1024,1024,alpha=False)
 if kind=='NORMAL':img.colorspace_settings.name='Non-Color'
 for material in target.data.materials:
  node=material.node_tree.nodes.new('ShaderNodeTexImage');node.image=img;material.node_tree.nodes.active=node
 bpy.ops.object.select_all(action='DESELECT');source.select_set(True);target.select_set(True);bpy.context.view_layer.objects.active=target
 if kind=='DIFFUSE':s.render.bake.use_pass_direct=False;s.render.bake.use_pass_indirect=False;s.render.bake.use_pass_color=True
 bpy.ops.object.bake(type=kind);img.filepath_raw=str(maps/(label+'.png'));img.file_format='PNG';img.save();img.pack();baked[label]=img
bake_seconds=time.perf_counter()-t
m=mat('Baked walnut and hardware',(1,1,1),.42);n=m.node_tree.nodes;l=m.node_tree.links;p=n['Principled BSDF'];c=n.new('ShaderNodeTexImage');c.image=baked['base-color'];l.new(c.outputs[0],p.inputs['Base Color']);no=n.new('ShaderNodeTexImage');no.image=baked['normal'];nm=n.new('ShaderNodeNormalMap');l.new(no.outputs[0],nm.inputs['Color']);l.new(nm.outputs[0],p.inputs['Normal']);target.data.materials.clear();target.data.materials.append(m)
source.hide_render=True;source.hide_set(True)
s.render.bake.use_selected_to_active=False;s.cycles.samples=32;studio(5.4,(0,0,.85),(5,-7,4));seconds=render()
bpy.ops.object.select_all(action='DESELECT');target.select_set(True);bpy.context.view_layer.objects.active=target
bpy.ops.export_scene.gltf(filepath=str(OUT/'chest.glb'),export_format='GLB',use_selection=True,use_active_scene=True)
# UV layout and checker diagnostic.
bpy.ops.uv.export_layout(filepath=str(OUT/'uv-layout.png'),size=(1024,1024),opacity=.35)
checker=mat('UV diagnostic',(1,1,1));n=checker.node_tree.nodes;l=checker.node_tree.links;uv=n.new('ShaderNodeTexCoord');ch=n.new('ShaderNodeTexChecker');ch.inputs['Scale'].default_value=24;l.new(uv.outputs['UV'],ch.inputs[0]);l.new(ch.outputs[0],n['Principled BSDF'].inputs['Base Color']);target.data.materials[0]=checker;render('uv-checker.png',(640,360));target.data.materials[0]=m
source.hide_render=False;target.hide_render=True;render('source-comparison.png',(640,360));source.hide_render=True;target.hide_render=False
result=save({'render_seconds':seconds,'bake_seconds':bake_seconds,'target_triangles':tri,'bake':'selected-to-active color and tangent normal, 1024, margin 12, cage .04m','limitation':'Single baked material uses uniform roughness; metallic map not baked.'})
