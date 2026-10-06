"""Run in a disposable Blender background process, with autoexec disabled.

Never saves a .blend. Exports the active scene, and bakes procedural surface
color/normal into a shared atlas. See documentation/models/README.md.
"""
import bpy
import hashlib
import json
import sys
import time
import math
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
EXPORTER_VERSION = 4


def browser_materials(objects):
    converted = []
    for mat in {m for o in objects if hasattr(o.data, 'materials') for m in o.data.materials if m}:
        if not mat.use_nodes or principled(mat):
            continue
        nodes = mat.node_tree.nodes
        ramp = next((n for n in nodes if n.type == 'VALTORGB'), None)
        if ramp and any(n.type == 'SHADERTORGB' for n in nodes):
            # glTF cannot express Eevee Shader-to-RGB lighting. Retain its
            # authored lit palette color, letting the viewer supply lighting.
            color = tuple(ramp.color_ramp.elements[-1].color)
            nodes.clear()
            p = nodes.new('ShaderNodeBsdfPrincipled')
            p.inputs['Base Color'].default_value = color
            p.inputs['Roughness'].default_value = .8
            out = nodes.new('ShaderNodeOutputMaterial')
            mat.node_tree.links.new(p.outputs['BSDF'], out.inputs['Surface'])
            converted.append(mat.name)
        else:
            raise RuntimeError('Unsupported surface requires an explicit adapter: '+mat.name)
    return ['Eevee toon ramps approximated with their authored lit palette colors and neutral PBR shading: '+', '.join(sorted(converted))] if converted else []


def source_view(scene):
    cam = scene.camera
    if not cam:
        return None
    eye = cam.matrix_world.translation
    forward = cam.matrix_world.to_quaternion() @ Vector((0,0,-1))
    distance = max(eye.length, 1)
    target = eye + forward * distance
    aspect = scene.render.resolution_x * scene.render.pixel_aspect_x / (scene.render.resolution_y * scene.render.pixel_aspect_y)
    height = cam.data.ortho_scale / max(1, aspect) if cam.data.type == 'ORTHO' else 2 * distance * math.tan(cam.data.angle_y/2)
    return {'position':[eye.x,eye.z,-eye.y], 'target':[target.x,target.z,-target.y], 'frameHeight':height, 'aspect':aspect}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def select(objects):
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        obj.hide_set(False)
        obj.hide_select = False
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]


def principled(mat):
    return next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None) if mat and mat.use_nodes else None


def bake_procedural(objects, resolution=2048):
    candidates = []
    for obj in objects:
        if obj.type != 'MESH':
            continue
        if any(principled(m) and any(principled(m).inputs[k].is_linked and principled(m).inputs[k].links[0].from_node.type not in ('TEX_IMAGE', 'NORMAL_MAP') for k in ('Base Color', 'Normal', 'Roughness')) for m in obj.data.materials):
            candidates.append(obj)
    if not candidates:
        return objects, []
    # Preserve object/generated coordinates before joining the static bake copy.
    select(candidates)
    bpy.ops.object.convert(target='MESH')
    mats = {m for o in candidates for m in o.data.materials if m}
    # A greybox may deliberately use one Empty as a world-aligned texture
    # coordinate reference. Bake that coordinate frame rather than silently
    # falling back to each stretched primitive's local space.
    object_refs = {
        node.object
        for mat in mats if mat.use_nodes
        for node in mat.node_tree.nodes
        if node.type == 'TEX_COORD' and node.object and node.outputs['Object'].is_linked
    }
    if len(object_refs) > 1:
        raise RuntimeError('Multiple shared object texture-coordinate references require an explicit bake adapter.')
    object_ref = next(iter(object_refs), None)
    object_ref_inverse = object_ref.matrix_world.inverted() if object_ref else None
    for obj in candidates:
        obj.data = obj.data.copy()
        verts = obj.data.vertices
        low = Vector(tuple(min(v.co[i] for v in verts) for i in range(3)))
        high = Vector(tuple(max(v.co[i] for v in verts) for i in range(3)))
        for name in ('viewer_generated', 'viewer_object'):
            attr = obj.data.attributes.get(name) or obj.data.attributes.new(name, 'FLOAT_VECTOR', 'POINT')
            for v, item in zip(verts, attr.data):
                if name.endswith('generated'):
                    item.vector = tuple((v.co[i]-low[i])/max(high[i]-low[i],1e-9) for i in range(3))
                elif object_ref_inverse:
                    item.vector = object_ref_inverse @ (obj.matrix_world @ v.co)
                else:
                    item.vector = v.co
    for mat in mats:
        if not mat.use_nodes:
            continue
        nt = mat.node_tree
        attrs = {}
        for key in ('Generated','Object'):
            node = nt.nodes.new('ShaderNodeAttribute')
            node.attribute_name = 'viewer_' + key.lower()
            attrs[key] = node
        for node in list(nt.nodes):
            if node.type == 'TEX_COORD':
                for key in attrs:
                    if key == 'Object' and node.object and node.object != object_ref:
                        raise RuntimeError('Referenced object texture coordinates require an explicit bake adapter: '+mat.name)
                    for link in list(node.outputs[key].links):
                        nt.links.new(attrs[key].outputs['Vector'], link.to_socket)
            if node.type.startswith('TEX_') and node.type not in ('TEX_IMAGE','TEX_COORD') and 'Vector' in node.inputs and not node.inputs['Vector'].is_linked:
                nt.links.new(attrs['Generated'].outputs['Vector'], node.inputs['Vector'])
    select(candidates)
    bpy.ops.object.join()
    atlas_obj = bpy.context.object
    atlas_obj.name = 'Viewer baked procedural surfaces'
    if len(atlas_obj.data.polygons) > 250000:
        # Millions of tiny foliage faces cannot share a useful texture atlas.
        # Bake their procedural palette at corners without dropping geometry.
        scene=bpy.context.scene
        scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=1
        color=atlas_obj.data.color_attributes.new(name='ViewerColor',type='FLOAT_COLOR',domain='CORNER')
        atlas_obj.data.color_attributes.active_color=color
        scene.render.bake.target='VERTEX_COLORS'
        scene.render.bake.use_selected_to_active=False
        restore=[]
        for mat in mats:
            nt=mat.node_tree;bsdf=principled(mat)
            output=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL' and n.is_active_output)
            old=output.inputs['Surface'].links[0].from_socket
            emission=nt.nodes.new('ShaderNodeEmission');base=bsdf.inputs['Base Color']
            if base.is_linked:nt.links.new(base.links[0].from_socket,emission.inputs['Color'])
            else:emission.inputs['Color'].default_value=base.default_value
            nt.links.new(emission.outputs[0],output.inputs['Surface'])
            restore.append((nt,bsdf,output,old,emission))
        bpy.ops.object.bake(type='EMIT')
        for nt,bsdf,output,old,emission in restore:
            nt.links.new(old,output.inputs['Surface']);nt.nodes.remove(emission)
            node=nt.nodes.new('ShaderNodeVertexColor');node.layer_name='ViewerColor'
            nt.links.new(node.outputs['Color'],bsdf.inputs['Base Color'])
            for link in list(bsdf.inputs['Normal'].links):nt.links.remove(link)
        return [o for o in scene.objects if o.type not in ('CAMERA','LIGHT') and not o.hide_render], ['Dense procedural scene uses per-corner baked colors to preserve foliage palettes without texture-atlas loss. Geometry is retained; sub-vertex color variation and procedural bump microdetail are not represented.']
    # Make a dedicated atlas without changing source files or image coordinates.
    uv = atlas_obj.data.uv_layers.new(name='ViewerAtlas')
    atlas_obj.data.uv_layers.active = uv
    uv.active_render = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=1.151917, island_margin=0.004)
    bpy.ops.object.mode_set(mode='OBJECT')
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 1
    scene.render.bake.margin = 8
    scene.render.bake.use_clear = True
    scene.render.bake.use_selected_to_active = False
    targets = {}
    baked = {}
    for channel in ('Normal', 'Base Color'):
        img = bpy.data.images.new('Viewer '+channel, resolution, resolution, alpha=False)
        img.colorspace_settings.name = 'Non-Color' if channel=='Normal' else 'sRGB'
        restore = []
        for mat in mats:
            nt = mat.node_tree
            bsdf = principled(mat)
            if not bsdf:
                raise RuntimeError('Bake requires Principled material: '+mat.name)
            for n in nt.nodes:
                n.select = False
            target = nt.nodes.new('ShaderNodeTexImage')
            target.image = img
            target.select = True
            nt.nodes.active = target
            targets[mat] = target
            if channel == 'Base Color':
                output = next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL' and n.is_active_output)
                old = output.inputs['Surface'].links[0].from_socket
                emission = nt.nodes.new('ShaderNodeEmission')
                color = bsdf.inputs['Base Color']
                if color.is_linked:
                    nt.links.new(color.links[0].from_socket, emission.inputs['Color'])
                else:
                    emission.inputs['Color'].default_value = color.default_value
                nt.links.new(emission.outputs[0],output.inputs['Surface'])
                restore.append((nt,output,old,emission))
        bpy.ops.object.bake(type='NORMAL' if channel=='Normal' else 'EMIT')
        img.pack()
        baked[channel] = img
        for nt, output, old, emission in restore:
            nt.links.new(old,output.inputs['Surface'])
            nt.nodes.remove(emission)
    for mat in mats:
        nt=mat.node_tree
        bsdf=principled(mat)
        for channel,img in baked.items():
            node=nt.nodes.new('ShaderNodeTexImage'); node.image=img
            uvnode=nt.nodes.new('ShaderNodeUVMap'); uvnode.uv_map='ViewerAtlas'
            nt.links.new(uvnode.outputs['UV'],node.inputs['Vector'])
            socket=node.outputs['Color']
            if channel=='Normal':
                normal=nt.nodes.new('ShaderNodeNormalMap'); normal.uv_map='ViewerAtlas'
                nt.links.new(socket,normal.inputs['Color']); socket=normal.outputs['Normal']
            nt.links.new(socket,bsdf.inputs[channel])
    survivors=[o for o in bpy.context.scene.objects if o.type not in ('CAMERA','LIGHT') and not o.hide_render]
    return survivors, [f'Procedural base color and tangent normals baked to {resolution}px atlas; microdetail is resolution-limited.']


def export(source):
    started=time.time()
    before=digest(source)
    report=source.with_suffix('.export.json')
    if report.exists() and source.with_suffix('.glb').exists():
        old=json.loads(report.read_text())
        if old.get('exporterVersion')==EXPORTER_VERSION and old.get('sourceSha256')==before and old.get('glbSha256')==digest(source.with_suffix('.glb')):
            print('VIEWER_UNCHANGED '+str(source),flush=True)
            return
    bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False)
    scene=bpy.context.scene
    scene.frame_set(scene.frame_start)
    warnings=['Blender world, compositor, and studio lighting are replaced by viewer lighting.']
    # Existing game exports are separately verified and retained; source scene
    # export remains complete and includes stage geometry and relevant clips.
    objects=[o for o in scene.objects if o.type not in ('CAMERA','LIGHT') and not o.hide_render]
    warnings += browser_materials(objects)
    view = source_view(scene)
    curves=[o for o in objects if o.type in ('CURVE','FONT','SURFACE','META')]
    if curves:
        select(curves); bpy.ops.object.convert(target='MESH')
    objects,w=bake_procedural(objects); warnings+=w
    select(objects)
    out=source.with_suffix('.glb')
    actions=sorted({o.animation_data.action.name for o in objects if o.animation_data and o.animation_data.action})
    bpy.ops.export_scene.gltf(filepath=str(out),export_format='GLB',use_selection=True,use_active_scene=True,export_apply=True,export_tangents=False,export_animations=True,export_animation_mode='ACTIVE_ACTIONS',export_nla_strips_merged_animation_name=' + '.join(actions) or 'Scene',export_frame_range=True,export_force_sampling=True,export_cameras=False,export_lights=False,export_draco_mesh_compression_enable=False,export_yup=True)
    assert digest(source)==before,'Source file changed'
    info={'sourcePath':source.relative_to(ROOT).as_posix(),'sourceSha256':before,'glbPath':out.relative_to(ROOT).as_posix(),'glbSha256':digest(out),'byteSize':out.stat().st_size,'warnings':warnings,'blenderVersion':bpy.app.version_string,'seconds':round(time.time()-started,2)}
    info.update(exporterVersion=EXPORTER_VERSION, view=view)
    out.with_suffix('.export.json').write_text(json.dumps(info,indent=2)+'\n',encoding='utf-8')
    print('VIEWER_EXPORT '+json.dumps(info),flush=True)


if __name__=='__main__':
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    paths=[ROOT/args[0]] if args else sorted((ROOT/'documentation/examples').rglob('*.blend'))
    for path in paths:
        export(path)
