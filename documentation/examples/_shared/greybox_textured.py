"""Shared editable construction helpers for the textured greybox examples."""
from math import cos, pi, sin
from pathlib import Path
import bpy
from mathutils import Vector


def _remove_if_orphan(datablock):
    if datablock and datablock.users == 0:
        for collection in (bpy.data.meshes, bpy.data.cameras, bpy.data.lights, bpy.data.materials, bpy.data.worlds):
            if collection.get(datablock.name) == datablock:
                collection.remove(datablock)
                return


def start_scene(scene_name, example_id, question, omissions):
    existing = bpy.data.scenes.get(scene_name)
    if existing:
        if existing.get("example_id") != example_id:
            raise RuntimeError(f"Refusing to replace non-owned scene: {scene_name}")
        collection = bpy.data.collections.get(scene_name)
        owned_objects = list(collection.objects) if collection else []
        owned_data = list({obj.data.as_pointer(): obj.data for obj in owned_objects if obj.data}.values())
        owned_materials = list({mat.as_pointer(): mat for obj in owned_objects if hasattr(obj.data, "materials") for mat in obj.data.materials if mat}.values())
        world = existing.world
        bpy.context.window.scene = next(scene for scene in bpy.data.scenes if scene != existing)
        bpy.data.scenes.remove(existing, do_unlink=True)
        if collection and collection.users == 0:
            for obj in owned_objects:
                if all(owner == collection for owner in obj.users_collection):
                    bpy.data.objects.remove(obj, do_unlink=True)
            bpy.data.collections.remove(collection)
        for data in owned_data:
            _remove_if_orphan(data)
        for material in owned_materials:
            _remove_if_orphan(material)
        _remove_if_orphan(world)

    scene = bpy.data.scenes.new(scene_name)
    bpy.context.window.scene = scene
    scene.unit_settings.system = "METRIC"
    scene["example_id"] = example_id
    scene["greybox_question"] = question
    scene["intentional_omissions"] = omissions
    collection = bpy.data.collections.new(scene_name)
    scene.collection.children.link(collection)
    return scene, collection


def add_grid_reference(collection, tile_size=1.0):
    """Create the one world-aligned coordinate reference owned by this greybox."""
    reference = bpy.data.objects.new("Greybox_GridReference", None)
    reference.empty_display_type = "PLAIN_AXES"
    reference.empty_display_size = 0.6
    reference["grid_tile_world_units"] = tile_size
    reference["grid_coordinate_space"] = "world-aligned shared object coordinates"
    collection.objects.link(reference)
    return reference


def slate_material(category, base_color, grid_reference, tile_size=1.0):
    name = f"Greybox_Slate_{category}"
    existing = bpy.data.materials.get(name)
    if existing:
        if existing.users:
            raise RuntimeError(f"Material name is already in use outside this clean greybox: {name}")
        bpy.data.materials.remove(existing)
    if tile_size <= 0:
        raise ValueError("Grid tile size must be positive")
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    principled = nodes.new("ShaderNodeBsdfPrincipled")
    coordinates = nodes.new("ShaderNodeTexCoord")
    mapping = nodes.new("ShaderNodeMapping")
    checker = nodes.new("ShaderNodeTexChecker")
    mapping.inputs["Scale"].default_value = (1 / tile_size, 1 / tile_size, 1 / tile_size)
    coordinates.object = grid_reference
    checker.inputs["Color1"].default_value = (*base_color, 1.0)
    checker.inputs["Color2"].default_value = (*[min(1.0, component + 0.12) for component in base_color], 1.0)
    checker.inputs["Scale"].default_value = 1.0
    principled.inputs["Roughness"].default_value = 0.84
    links.new(coordinates.outputs["Object"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], checker.inputs["Vector"])
    links.new(checker.outputs["Color"], principled.inputs["Base Color"])
    links.new(principled.outputs["BSDF"], output.inputs["Surface"])
    material["greybox_hue"] = "Slate"
    material["grid_tile_world_units"] = tile_size
    material["grid_coordinate_space"] = "Greybox_GridReference Object coordinates"
    material["grid_mapping_scale"] = 1 / tile_size
    material["semantic_category"] = category
    return material


def mesh(name, vertices, faces, collection, material):
    data = bpy.data.meshes.new(f"{name}_Mesh")
    data.from_pydata(vertices, [], faces)
    data.materials.append(material)
    obj = bpy.data.objects.new(name, data)
    collection.objects.link(obj)
    return obj


def plane(name, center, size, z, collection, material):
    x, y = center
    dx, dy = (value / 2 for value in size)
    return mesh(name, [(x-dx, y-dy, z), (x+dx, y-dy, z), (x+dx, y+dy, z), (x-dx, y+dy, z)], [(0, 1, 2, 3)], collection, material)


def wall(name, points, collection, material):
    return mesh(name, points, [(0, 1, 2, 3)], collection, material)


def box(name, center, size, collection, material):
    x, y, z = center
    dx, dy, dz = (value / 2 for value in size)
    vertices = [(x + sx * dx, y + sy * dy, z + sz * dz) for sz in (-1, 1) for sy in (-1, 1) for sx in (-1, 1)]
    faces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    return mesh(name, vertices, faces, collection, material)


def wheel(name, center, radius, depth, collection, material, sides=12):
    x, y, z = center
    vertices = []
    for y_offset in (-depth / 2, depth / 2):
        vertices.extend((x + radius * cos(2 * pi * index / sides), y + y_offset, z + radius * sin(2 * pi * index / sides)) for index in range(sides))
    faces = [tuple(range(sides)), tuple(range(sides, 2 * sides))]
    faces.extend((index, (index + 1) % sides, sides + (index + 1) % sides, sides + index) for index in range(sides))
    return mesh(name, vertices, faces, collection, material)


def point_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def add_camera_and_lights(scene, collection, prefix, location, target, ortho_scale, fill=False):
    camera_data = bpy.data.cameras.new(f"{prefix}_Camera")
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = ortho_scale
    camera = bpy.data.objects.new(f"{prefix}_Camera", camera_data)
    collection.objects.link(camera)
    camera.location = location
    point_at(camera, target)
    scene.camera = camera
    key_data = bpy.data.lights.new(f"{prefix}_Key", "SUN")
    key_data.energy = 1.3
    key = bpy.data.objects.new(f"{prefix}_Key", key_data)
    collection.objects.link(key)
    key.rotation_euler = (0.6, -0.3, -0.55)
    if fill:
        fill_data = bpy.data.lights.new(f"{prefix}_Fill", "AREA")
        fill_data.energy = 420
        fill_data.shape = "DISK"
        fill_data.size = 5.0
        fill_obj = bpy.data.objects.new(f"{prefix}_Fill", fill_data)
        collection.objects.link(fill_obj)
        fill_obj.location = (1.5, -4.5, 6.0)
        point_at(fill_obj, target)
    world = bpy.data.worlds.new(f"{prefix}_World")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.045, 0.055, 0.07, 1.0)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.5
    scene.world = world


def save_and_render(scene, output_dir):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 960
    scene.render.resolution_y = 540
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.filepath = "//result.png"
    bpy.ops.wm.save_as_mainfile(filepath=str(output / "result.blend"), compress=True)
    bpy.ops.render.render(write_still=True)
    return output / "result.blend", output / "result.png"
