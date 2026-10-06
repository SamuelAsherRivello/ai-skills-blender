"""Build the minimal city greybox in the connected Blender editor."""
from pathlib import Path
import bpy
from mathutils import Vector

EXAMPLE = Path(__file__).resolve().parents[1]
OUT = EXAMPLE / "output"
OUT.mkdir(parents=True, exist_ok=True)
SCENE_NAME = "Greybox_City"
EXAMPLE_ID = "14-greybox-city"


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
        (bpy.data.materials, ("City_Ground_Grey", "City_Road_Grey", "City_Low_Building_Grey", "City_Mid_Building_Grey", "City_Tall_Building_Grey")),
        (bpy.data.worlds, ("City_Greybox_World",)),
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
    bsdf.inputs["Roughness"].default_value = 0.86
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
scene["greybox_question"] = "Do the road crossing, city blocks, and height hierarchy read at a glance?"
scene["intentional_omissions"] = "No facade, road-marking, streetscape, vehicle, tree, texture, UV, or bevel detail."
collection = bpy.data.collections.new(SCENE_NAME)
scene.collection.children.link(collection)

ground = mat("City_Ground_Grey", (0.31, 0.34, 0.38))
road = mat("City_Road_Grey", (0.12, 0.14, 0.16))
low = mat("City_Low_Building_Grey", (0.46, 0.51, 0.57))
mid = mat("City_Mid_Building_Grey", (0.58, 0.63, 0.68))
tall = mat("City_Tall_Building_Grey", (0.71, 0.75, 0.79))
plane("City_Ground_Plane", (0, 0), (24, 20), 0, collection, ground)
plane("City_Road_East_West", (0, 0), (24, 3.0), 0.02, collection, road)
plane("City_Road_North_South", (0, 0), (3.0, 20), 0.03, collection, road)
for name, center, size, material in (
    ("City_Building_A", (-7.0, -5.2, 2.0), (4.0, 3.2, 4.0), low),
    ("City_Building_B", (-6.4, 5.0, 4.0), (4.8, 3.8, 8.0), mid),
    ("City_Building_C", (6.6, -5.0, 5.0), (4.5, 3.5, 10.0), tall),
    ("City_Building_D", (6.7, 4.8, 2.8), (3.7, 4.0, 5.6), low),
    ("City_Building_E", (-2.7, 6.5, 3.3), (2.0, 2.5, 6.6), mid),
    ("City_Building_F", (2.9, -6.2, 3.6), (2.3, 2.5, 7.2), mid),
):
    box(name, center, size, collection, material)

camera_data = bpy.data.cameras.new("City_Greybox_Camera")
camera_data.type = "ORTHO"
camera_data.ortho_scale = 32.0
camera = bpy.data.objects.new("City_Greybox_Camera", camera_data)
collection.objects.link(camera)
camera.location = (25, -28, 25)
point_camera(camera, (0, 0, 3.5))
scene.camera = camera
sun_data = bpy.data.lights.new("City_Greybox_Key", "SUN")
sun_data.energy = 1.4
sun = bpy.data.objects.new("City_Greybox_Key", sun_data)
collection.objects.link(sun)
sun.rotation_euler = (0.5, -0.4, -0.55)
world = bpy.data.worlds.new("City_Greybox_World")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.045, 0.055, 0.07, 1.0)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.5
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
