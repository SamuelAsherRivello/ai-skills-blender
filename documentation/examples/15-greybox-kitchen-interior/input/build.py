"""Build the minimal kitchen-interior greybox in the connected Blender editor."""
from pathlib import Path
import bpy
from mathutils import Vector

EXAMPLE = Path(__file__).resolve().parents[1]
OUT = EXAMPLE / "output"
OUT.mkdir(parents=True, exist_ok=True)
SCENE_NAME = "Greybox_Kitchen_Interior"
EXAMPLE_ID = "15-greybox-kitchen-interior"


def clear_previous_run():
    scene = bpy.data.scenes.get(SCENE_NAME)
    if not scene:
        return
    if scene.get("example_id") != EXAMPLE_ID:
        raise RuntimeError(f"Refusing to replace non-owned scene: {SCENE_NAME}")
    collection = bpy.data.collections.get(SCENE_NAME)
    bpy.context.window.scene = next(s for s in bpy.data.scenes if s != scene)
    bpy.data.scenes.remove(scene, do_unlink=True)
    if collection and collection.users == 0:
        for obj in list(collection.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(collection)
    for datablocks, names in (
        (bpy.data.materials, ("Kitchen_Floor_Grey", "Kitchen_Wall_Grey", "Kitchen_Counter_Grey", "Kitchen_Appliance_Grey")),
        (bpy.data.cameras, ("Kitchen_Greybox_Camera",)),
        (bpy.data.lights, ("Kitchen_Greybox_Key", "Kitchen_Greybox_Fill")),
        (bpy.data.worlds, ("Kitchen_Greybox_World",)),
    ):
        for name in names:
            block = datablocks.get(name)
            if block and block.users == 0:
                datablocks.remove(block)


def mat(name, color):
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.84
    return material


def mesh(name, vertices, faces, collection, material):
    data = bpy.data.meshes.new(f"{name}_Mesh")
    data.from_pydata(vertices, [], faces)
    data.materials.append(material)
    obj = bpy.data.objects.new(name, data)
    collection.objects.link(obj)
    return obj


def plane(name, vertices, collection, material):
    return mesh(name, vertices, [(0, 1, 2, 3)], collection, material)


def box(name, center, size, collection, material):
    x, y, z = center
    dx, dy, dz = (value / 2 for value in size)
    vertices = [(x + sx * dx, y + sy * dy, z + sz * dz) for sz in (-1, 1) for sy in (-1, 1) for sx in (-1, 1)]
    faces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    return mesh(name, vertices, faces, collection, material)


def point_camera(camera, target):
    camera.rotation_euler = (Vector(target) - camera.location).to_track_quat("-Z", "Y").to_euler()


clear_previous_run()
scene = bpy.data.scenes.new(SCENE_NAME)
bpy.context.window.scene = scene
scene.unit_settings.system = "METRIC"
scene["example_id"] = EXAMPLE_ID
scene["greybox_question"] = "Does the open room shell, kitchen work zone, and central circulation read at a glance?"
scene["intentional_omissions"] = "No cabinet fronts, doors, windows, sink detail, furniture, texture, UV, or bevel detail."
collection = bpy.data.collections.new(SCENE_NAME)
scene.collection.children.link(collection)

floor_mat = mat("Kitchen_Floor_Grey", (0.39, 0.43, 0.47))
wall_mat = mat("Kitchen_Wall_Grey", (0.78, 0.81, 0.84))
counter_mat = mat("Kitchen_Counter_Grey", (0.46, 0.53, 0.60))
appliance_mat = mat("Kitchen_Appliance_Grey", (0.63, 0.68, 0.73))
plane("Kitchen_Floor_Plane", [(-5, -4, 0), (5, -4, 0), (5, 4, 0), (-5, 4, 0)], collection, floor_mat)
plane("Kitchen_Back_Wall_Plane", [(-5, 3.5, 0), (5, 3.5, 0), (5, 3.5, 5), (-5, 3.5, 5)], collection, wall_mat)
plane("Kitchen_Left_Wall_Plane", [(-4.5, -4, 0), (-4.5, 3.5, 0), (-4.5, 3.5, 5), (-4.5, -4, 5)], collection, wall_mat)
box("Kitchen_Back_Counter_Block", (0.5, 2.8, 0.9), (6.0, 0.8, 1.8), collection, counter_mat)
box("Kitchen_Side_Counter_Block", (-3.6, 0.8, 0.9), (0.8, 3.2, 1.8), collection, counter_mat)
box("Kitchen_Refrigerator_Block", (3.8, 2.85, 1.65), (1.1, 0.85, 3.3), collection, appliance_mat)
box("Kitchen_Island_Block", (0.2, -0.65, 0.9), (2.6, 1.1, 1.8), collection, counter_mat)

camera_data = bpy.data.cameras.new("Kitchen_Greybox_Camera")
camera_data.type = "ORTHO"
camera_data.ortho_scale = 13.0
camera = bpy.data.objects.new("Kitchen_Greybox_Camera", camera_data)
collection.objects.link(camera)
camera.location = (10.0, -12.0, 8.5)
point_camera(camera, (0.0, 0.8, 1.8))
scene.camera = camera
sun_data = bpy.data.lights.new("Kitchen_Greybox_Key", "SUN")
sun_data.energy = 1.2
sun = bpy.data.objects.new("Kitchen_Greybox_Key", sun_data)
collection.objects.link(sun)
sun.rotation_euler = (0.6, -0.25, -0.55)
fill_data = bpy.data.lights.new("Kitchen_Greybox_Fill", "AREA")
fill_data.energy = 450
fill_data.shape = "DISK"
fill_data.size = 5.0
fill = bpy.data.objects.new("Kitchen_Greybox_Fill", fill_data)
collection.objects.link(fill)
fill.location = (1.5, -4.5, 6.0)
point_camera(fill, (0.0, 1.0, 1.5))
world = bpy.data.worlds.new("Kitchen_Greybox_World")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.045, 0.055, 0.07, 1.0)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.55
scene.world = world
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = "//result.png"
bpy.ops.wm.save_as_mainfile(filepath=str(OUT / "result.blend"), compress=True)
bpy.ops.render.render(write_still=True)
result = {"source": str(OUT / "result.blend"), "render": str(OUT / "result.png"), "objects": [obj.name for obj in collection.objects if obj.type == "MESH"]}
