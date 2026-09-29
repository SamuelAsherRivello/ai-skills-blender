"""Run through official MCP with REPO and OUTPUT Paths supplied in globals.

Creates an isolated scene, restores the original active scene, writes only OUTPUT.
This is a bounded integration fixture, not a general asset creation script.
"""
import bpy
import json
import math
import random
import runpy
from pathlib import Path
from mathutils import Vector


def exercise(repo, output):
    repo, output = Path(repo), Path(output)
    output.mkdir(parents=True, exist_ok=False)
    original = bpy.context.window.scene
    original_objects = {o.name: list(o.matrix_world) for o in original.objects}
    previous_file = bpy.data.filepath
    bpy.ops.wm.save_as_mainfile(filepath=str(output/"checkpoint.blend"), copy=True)
    scene = bpy.data.scenes.new("SkillAcceptance-"+output.name)
    generated_collection = "AcceptanceGenerated-"+output.name
    bpy.context.window.scene = scene
    outputs, evidence = [], {}
    def render(name):
        scene.render.filepath = str(output/name)
        bpy.ops.render.render(write_still=True)
        outputs.append({"path":name,"width":128,"height":128,"alpha":True})
    def material(name, color):
        mat=bpy.data.materials.new(name); mat.use_nodes=True
        node=mat.node_tree.nodes.get("Principled BSDF")
        node.inputs["Base Color"].default_value=color
        node.inputs["Roughness"].default_value=0.55
        return mat
    def cube(name, location, scale, mat):
        bpy.ops.mesh.primitive_cube_add(size=1,location=location)
        obj=bpy.context.object; obj.name=name
        obj.scale=scale; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        obj.data.materials.append(mat)
        return obj
    try:
        scene.render.engine='CYCLES'; scene.cycles.device='CPU'; scene.cycles.samples=8
        scene.render.resolution_x=128; scene.render.resolution_y=128; scene.render.resolution_percentage=100
        scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGBA'
        scene.render.film_transparent=True
        scene.world=bpy.data.worlds.new("Acceptance World"); scene.world.use_nodes=True
        scene.world.node_tree.nodes["Background"].inputs[0].default_value=(0.25,0.25,0.25,1)
        red=material("Acceptance terracotta",(0.55,0.06,0.025,1))
        blue=material("Acceptance blue",(0.03,0.14,0.45,1))
        floor_mat=material("Acceptance floor",(0.3,0.3,0.3,1))
        prop=cube("AcceptanceProp",(0,0,0.6),(0.8,0.8,1.2),red)
        bevel=prop.modifiers.new("Editable bevel",'BEVEL'); bevel.width=0.08; bevel.segments=3
        prop.modifiers.new("Weighted normals",'WEIGHTED_NORMAL')
        floor=cube("AcceptanceFloor",(0,0,-0.08),(4,4,0.16),floor_mat)
        kit=[cube("AcceptanceModule"+str(i),(i-1,1.4,0.25),(0.8,0.2,0.5),blue) for i in range(3)]
        bpy.ops.object.camera_add(location=(3,-4,3))
        camera=bpy.context.object; camera.name="AcceptanceCamera"; camera.data.type='ORTHO'; camera.data.ortho_scale=4.5
        camera.rotation_euler=(Vector((0,0,0.5))-camera.location).to_track_quat('-Z','Y').to_euler()
        scene.camera=camera
        bpy.ops.object.light_add(type='AREA',location=(1,-2,4))
        light=bpy.context.object; light.data.energy=400; light.data.shape='DISK'; light.data.size=3
        light.rotation_euler=(Vector((0,0,0.4))-light.location).to_track_quat('-Z','Y').to_euler()
        render("model-environment.png")
        light.location=(-3,-1,2); render("material-comparison.png"); light.location=(1,-2,4)
        evidence["model"]={"dimensions":list(prop.dimensions),"objects": [prop.name]}
        evidence["environment"]={"module_count":len(kit),"module_width":0.8,"units":scene.unit_settings.system}
        evidence["materials"]={"roughness":0.55,"textures":"none required; procedural constant color","comparison":"material-comparison.png"}

        # A seeded, bounded generator replaces only its named collection.
        def generate(count, seed):
            if not isinstance(count,int) or not 0 <= count <= 8:
                raise ValueError("count outside 0..8")
            collection=bpy.data.collections.get(generated_collection)
            if collection:
                for obj in list(collection.objects): bpy.data.objects.remove(obj,do_unlink=True)
                bpy.data.collections.remove(collection)
            collection=bpy.data.collections.new(generated_collection); scene.collection.children.link(collection)
            rng=random.Random(seed)
            for i in range(count):
                obj=cube("Generated"+str(i),(-1.4+i*0.35,-0.6,0.15),(0.2,0.2,0.3+rng.random()*0.1),blue)
                for owner in list(obj.users_collection): owner.objects.unlink(obj)
                collection.objects.link(obj)
            return [(o.name,tuple(o.dimensions)) for o in collection.objects]
        assert generate(0,7)==[]
        assert len(generate(8,7))==8
        expected=generate(3,7); assert generate(3,7)==expected
        try: generate(-1,7)
        except ValueError: pass
        else: raise AssertionError("invalid generator count accepted")
        evidence["procedural"]={"seed":7,"bounds_tested":[0,3,8],"repeat_equal":True}

        # Selected-to-active bake from coincident duplicate source onto a UV target.
        target=cube("BakeTarget",(-1,0,0.5),(0.5,0.5,0.5),blue)
        source=target.copy(); source.data=target.data.copy(); scene.collection.objects.link(source); source.name="BakeSource"
        source.data.materials.clear(); source.data.materials.append(red)
        target_mat=blue.copy(); target_mat.name="Bake target material"; target.data.materials[0]=target_mat
        bake=bpy.data.images.new("AcceptanceBake",width=64,height=64,alpha=True)
        bake.colorspace_settings.name='sRGB'
        node=target_mat.node_tree.nodes.new("ShaderNodeTexImage"); node.image=bake
        target_mat.node_tree.nodes.active=node
        bpy.ops.object.select_all(action='DESELECT')
        source.select_set(True); target.select_set(True); bpy.context.view_layer.objects.active=target
        scene.render.bake.use_selected_to_active=True; scene.render.bake.cage_extrusion=0.05
        scene.render.bake.margin=4; scene.render.bake.use_pass_direct=False; scene.render.bake.use_pass_indirect=False
        scene.render.bake.use_pass_color=True
        bpy.ops.object.bake(type='DIFFUSE')
        bake.filepath_raw=str(output/"bake.png"); bake.file_format='PNG'; bake.save()
        target_mat.node_tree.links.new(node.outputs["Color"],target_mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"])
        source.hide_render=True; source.hide_set(True)
        render("baked-target.png")
        evidence["bake"]={"map":"bake.png","resolution":64,"margin":4,"color_space":bake.colorspace_settings.name,"uv_layers":len(target.data.uv_layers)}

        # One-bone deforming rig with a loop, plus extreme pose inspection.
        rig_mesh=cube("RiggedMesh",(1,0,0.7),(0.25,0.25,1.4),blue)
        bpy.ops.object.armature_add(location=(1,0,0))
        arm=bpy.context.object; arm.name="AcceptanceRig"
        bpy.context.view_layer.update()
        # Normalize skinned mesh origin to armature root while preserving world geometry.
        world=rig_mesh.matrix_world.copy()
        rig_mesh.data.transform(arm.matrix_world.inverted() @ world)
        rig_mesh.matrix_world=arm.matrix_world.copy()
        group=rig_mesh.vertex_groups.new(name="Bone"); group.add(list(range(len(rig_mesh.data.vertices))),1,'REPLACE')
        modifier=rig_mesh.modifiers.new("Armature",'ARMATURE'); modifier.object=arm
        world=rig_mesh.matrix_world.copy(); rig_mesh.parent=arm; rig_mesh.matrix_world=world
        bone=arm.pose.bones["Bone"]; bone.rotation_mode='XYZ'
        for frame,angle in [(1,0),(5,0.7),(9,0)]:
            bone.rotation_euler[0]=angle; bone.keyframe_insert(data_path="rotation_euler",frame=frame)
        arm.animation_data.action.name="AcceptanceSway"
        scene.frame_start=1; scene.frame_end=9; scene.render.fps=12
        for frame in [1,5,9]:
            scene.frame_set(frame); render(f"motion-{frame}.png")
        evidence["animation"]={"clip":arm.animation_data.action.name,"frames":[1,9],"fps":12,"review_frames":[1,5,9]}

        # Cost reduction without silhouette change: planar subdivision.
        audit=runpy.run_path(str(repo/"skills/blender-review-optimize/scripts/audit_scene.py"))["audit"]
        redundant=prop.modifiers.new("Redundant planar density",'SUBSURF'); redundant.subdivision_type='SIMPLE'; redundant.levels=2
        before=audit([prop]); render("optimize-before.png")
        prop.modifiers.remove(redundant); after=audit([prop]); render("optimize-after.png")
        assert after["triangles"] < before["triangles"]
        evidence["optimization"]={"before":before,"after":after}

        # Export the prop and animated asset only, then reimport in its own scene.
        bpy.ops.object.select_all(action='DESELECT')
        for obj in [prop,arm,rig_mesh]: obj.select_set(True)
        bpy.context.view_layer.objects.active=prop
        bpy.ops.export_scene.gltf(filepath=str(output/"asset.glb"),export_format='GLB',use_selection=True,use_active_scene=True,export_animations=True,export_animation_mode='ACTIVE_ACTIONS')
        imported=bpy.data.scenes.new("AcceptanceImport")
        bpy.context.window.scene=imported
        before_import=set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=str(output/"asset.glb"))
        new_objects=set(bpy.data.objects)-before_import
        exported_meshes=[o for o in imported.objects if o in new_objects and o.type=='MESH']
        assert len(exported_meshes)==2
        assert any(o.type=='ARMATURE' for o in imported.objects)
        for original_mesh, prefix in [(prop, "AcceptanceProp"), (rig_mesh, "RiggedMesh")]:
            restored=next(o for o in exported_meshes if o.name.startswith(prefix))
            assert max(abs(a-b) for a,b in zip(original_mesh.dimensions,restored.dimensions)) < 0.001
            assert (original_mesh.matrix_world.translation-restored.matrix_world.translation).length < 0.001
            assert len(restored.material_slots)==len(original_mesh.material_slots)
        imported_arm=next(o for o in imported.objects if o.type=='ARMATURE')
        assert imported_arm.animation_data and imported_arm.animation_data.action
        evidence["export"]={"meshes":[{"name":o.name,"dimensions":list(o.dimensions),"materials":len(o.material_slots)} for o in exported_meshes],
                            "actions":[imported_arm.animation_data.action.name],"pivot_and_dimensions_match":True,"engine_import":"unverified; Blender glTF reimport only"}
        bpy.context.window.scene=scene

        # Directional sprite frames from the same model/camera scale.
        hidden={o:o.hide_render for o in scene.objects if o not in [prop,camera,light]}
        for obj in hidden: obj.hide_render=True
        sprite_frames=[]
        for index,angle in enumerate([0,math.pi/2]):
            camera.location=(3*math.sin(angle),-3*math.cos(angle),2)
            camera.rotation_euler=(Vector((0,0,0.6))-camera.location).to_track_quat('-Z','Y').to_euler()
            name=f"sprite-{index}.png"; render(name)
            sprite_frames.append({"path":name,"direction":["front","right"][index],"frame":0})
        manifest={"width":128,"height":128,"columns":2,"pivot":[0.5,0.5],"frames":sprite_frames}
        (output/"sprites.json").write_text(json.dumps(manifest),encoding="utf-8")
        pack=runpy.run_path(str(repo/"skills/blender-convert-3d-2d/scripts/pack_sprites.py"))["pack"]
        sheet=pack(output/"sprites.json",output/"packed")
        evidence["sprites"]=sheet
        # Error paths and deterministic packing, without touching existing output.
        pack(output/"sprites.json",output/"packed-repeat")
        assert (output/"packed/sheet.png").read_bytes()==(output/"packed-repeat/sheet.png").read_bytes()
        for label,change in [("size",{"width":64}),("missing",{"frames":[{"path":"missing.png"}]}),("invalid",{"height":0})]:
            bad={**manifest,**change}; path=output/(label+".json"); path.write_text(json.dumps(bad))
            try: pack(path,output/("bad-"+label))
            except ValueError: pass
            else: raise AssertionError("packing accepted "+label)
        try: pack(output/"sprites.json",output/"packed")
        except ValueError: pass
        else: raise AssertionError("packing overwrote prior output")
        evidence["packing_tests"]=["deterministic","wrong size rejected","missing rejected","nonpositive rejected","existing output preserved"]
        for obj,state in hidden.items(): obj.hide_render=state

        # Synthetic reference is confined to this ignored acceptance run.
        image=bpy.data.images.new("Temporary geometric reference",width=32,height=32,alpha=True)
        pixels=[]
        for y in range(32):
            for x in range(32):
                pixels.extend((0.8,0.15,0.05,1) if 8<=x<24 and 4<=y<28 else (0,0,0,0))
        image.pixels.foreach_set(pixels); image.filepath_raw=str(output/"reference-fixture.png"); image.file_format='PNG'; image.save()
        evidence["reconstruction_input"]={"image":"reference-fixture.png","visible":"centered rectangle, width 16/32 and height 24/32","inferred":"depth 0.2, planar backside","mode":"rectangular relief"}
        reconstruction=cube("ReconstructedRelief",(0,-1.1,0.75),(1,0.2,1.5),red)
        evidence["reconstruction_input"]["dimensions"]=list(reconstruction.dimensions)
        reconstruction_hidden={o:o.hide_render for o in scene.objects if o not in [reconstruction,camera,light]}
        for obj in reconstruction_hidden: obj.hide_render=True
        camera.data.ortho_scale=2.0
        camera.location=(0,-4,0.75); camera.rotation_euler=(Vector(reconstruction.location)-camera.location).to_track_quat('-Z','Y').to_euler()
        render("reconstruction-matching.png")
        camera.location=(2,-4,2); camera.rotation_euler=(Vector(reconstruction.location)-camera.location).to_track_quat('-Z','Y').to_euler()
        render("reconstruction-oblique.png")
        for obj,state in reconstruction_hidden.items(): obj.hide_render=state
        evidence["original_preserved"]=all(o.name in original_objects and list(o.matrix_world)==original_objects[o.name] for o in original.objects) and len(original.objects)==len(original_objects)
        assert evidence["original_preserved"]
        bpy.ops.wm.save_as_mainfile(filepath=str(output/"acceptance.blend"),copy=True)
        assert bpy.data.filepath==previous_file
        (output/"render-manifest.json").write_text(json.dumps({"run_id":output.name,"source":"acceptance.blend","settings":{"engine":"CYCLES","samples":8,"blender":bpy.app.version_string},"outputs":outputs},indent=2),encoding="utf-8")
        (output/"evidence.json").write_text(json.dumps(evidence,indent=2),encoding="utf-8")
        return {"output":str(output),"renders":len(outputs),"evidence":evidence}
    finally:
        bpy.context.window.scene=original


if "REPO" in globals() and "OUTPUT" in globals():
    result=exercise(REPO,OUTPUT)
