"""Build the minimal car greybox in the connected Blender editor."""
from math import cos, pi, sin
from pathlib import Path
import bpy
from mathutils import Vector

EXAMPLE = Path(__file__).resolve().parents[1]
OUT = EXAMPLE / "output"
OUT.mkdir(parents=True, exist_ok=True)
SCENE_NAME = "Greybox_Car"
EXAMPLE_ID = "13-greybox-car"


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


def mat(name, color):
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.82
    return material


def mesh(name, vertices, faces, collection, material):
    data = bpy.data.meshes.new(f"{name}_Mesh")
    data.from_pydata(vertices, [], faces)
    data.materials.append(material)
    obj = bpy.data.objects.new(name, data)
    collection.objects.link(obj)
    return obj


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


def point_camera(camera, target):
    camera.rotation_euler = (Vector(target) - camera.location).to_track_quat("-Z", "Y").to_euler()


clear_previous_run()
scene = bpy.data.scenes.new(SCENE_NAME)
bpy.context.window.scene = scene
scene.unit_settings.system = "METRIC"
scene["example_id"] = EXAMPLE_ID
scene["greybox_question"] = "Do the primary vehicle masses and wheel positions read as a car?"
scene["intentional_omissions"] = "No windows, doors, lights, interior, trim, bevels, textures, or UVs."
collection = bpy.data.collections.new(SCENE_NAME)
scene.collection.children.link(collection)

ground = mat("Car_Ground_Grey", (0.24, 0.28, 0.32))
body = mat("Car_Body_Grey", (0.46, 0.52, 0.58))
cabin = mat("Car_Cabin_Grey", (0.68, 0.73, 0.78))
rubber = mat("Car_Wheel_Grey", (0.10, 0.12, 0.14))
mesh("Car_Ground_Plane", [(-5, -4, 0), (5, -4, 0), (5, 4, 0), (-5, 4, 0)], [(0, 1, 2, 3)], collection, ground)
box("Car_Chassis_Block", (0, 0, 1.0), (4.8, 2.0, 0.9), collection, body)
box("Car_Cabin_Block", (-0.35, 0, 1.85), (2.3, 1.75, 0.9), collection, cabin)
for name, center in (("Car_Wheel_Front_Left", (1.65, -1.05, 0.55)), ("Car_Wheel_Front_Right", (1.65, 1.05, 0.55)), ("Car_Wheel_Rear_Left", (-1.65, -1.05, 0.55)), ("Car_Wheel_Rear_Right", (-1.65, 1.05, 0.55))):
    wheel(name, center, 0.55, 0.35, collection, rubber)

camera_data = bpy.data.cameras.new("Car_Greybox_Camera")
camera_data.type = "ORTHO"
camera_data.ortho_scale = 7.0
camera = bpy.data.objects.new("Car_Greybox_Camera", camera_data)
collection.objects.link(camera)
camera.location = (7.5, -9.0, 5.8)
point_camera(camera, (0, 0, 1.0))
scene.camera = camera
sun_data = bpy.data.lights.new("Car_Greybox_Key", "SUN")
sun_data.energy = 2.0
sun = bpy.data.objects.new("Car_Greybox_Key", sun_data)
collection.objects.link(sun)
sun.rotation_euler = (0.5, -0.3, -0.6)
world = bpy.data.worlds.new("Car_Greybox_World")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.045, 0.055, 0.07, 1.0)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.3
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
