"""Build the minimal 2.5D greybox example in the connected Blender editor."""
from pathlib import Path
import bpy
from mathutils import Vector

EXAMPLE = Path(__file__).resolve().parents[1]
OUT = EXAMPLE / "output"
OUT.mkdir(parents=True, exist_ok=True)


def material(name, color):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    mat.use_nodes = True
    principled = mat.node_tree.nodes.get("Principled BSDF")
    principled.inputs["Base Color"].default_value = (*color, 1.0)
    principled.inputs["Roughness"].default_value = 0.82
    return mat


def plane(name, vertices, collection, mat):
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    mesh.from_pydata(vertices, [], [(0, 1, 2, 3)])
    mesh.materials.append(mat)
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    return obj


def point_camera(camera, target):
    camera.rotation_euler = (Vector(target) - camera.location).to_track_quat("-Z", "Y").to_euler()


owned_scene_name = "Greybox_2_5D"
owned_scene_id = "12-greybox-2-5d"
existing = bpy.data.scenes.get(owned_scene_name)
if existing:
    if existing.get("example_id") != owned_scene_id:
        raise RuntimeError(f"Refusing to replace non-owned scene: {owned_scene_name}")
    existing_collection = bpy.data.collections.get(owned_scene_name)
    fallback = next(scene for scene in bpy.data.scenes if scene != existing)
    bpy.context.window.scene = fallback
    bpy.data.scenes.remove(existing, do_unlink=True)
    if existing_collection and existing_collection.users == 0:
        for obj in list(existing_collection.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(existing_collection)
    for datablocks, names in (
        (bpy.data.meshes, ("Floor_Plane_Mesh", "Backdrop_Plane_Mesh")),
        (bpy.data.materials, ("Floor_Grey", "Backdrop_Grey")),
        (bpy.data.cameras, ("Greybox_Camera",)),
        (bpy.data.lights, ("Greybox_Key",)),
        (bpy.data.worlds, ("Greybox_World",)),
    ):
        for name in names:
            block = datablocks.get(name)
            if block and block.users == 0:
                datablocks.remove(block)

scene = bpy.data.scenes.new(owned_scene_name)
bpy.context.window.scene = scene
scene.unit_settings.system = "METRIC"
scene["example_id"] = owned_scene_id
scene["greybox_question"] = "How can two perpendicular planes communicate a 2.5D setup?"
scene["intentional_omissions"] = "No thickness, props, texture maps, UVs, bevels, interiors, or decorative detail."

collection = bpy.data.collections.new("Greybox_2_5D")
scene.collection.children.link(collection)

floor = plane(
    "Floor_Plane",
    [(-5.0, -4.0, 0.0), (5.0, -4.0, 0.0), (5.0, 4.0, 0.0), (-5.0, 4.0, 0.0)],
    collection,
    material("Floor_Grey", (0.30, 0.34, 0.39)),
)
backdrop = plane(
    "Backdrop_Plane",
    [(-5.0, 3.25, 0.0), (5.0, 3.25, 0.0), (5.0, 3.25, 6.0), (-5.0, 3.25, 6.0)],
    collection,
    material("Backdrop_Grey", (0.68, 0.72, 0.77)),
)

camera_data = bpy.data.cameras.new("Greybox_Camera")
camera_data.type = "ORTHO"
camera_data.ortho_scale = 12.5
camera = bpy.data.objects.new("Greybox_Camera", camera_data)
collection.objects.link(camera)
camera.location = (9.0, -11.0, 7.5)
point_camera(camera, (0.0, 0.8, 2.0))
scene.camera = camera

light_data = bpy.data.lights.new("Greybox_Key", "SUN")
light_data.energy = 2.0
light = bpy.data.objects.new("Greybox_Key", light_data)
collection.objects.link(light)
light.rotation_euler = (0.55, -0.35, -0.6)

world = bpy.data.worlds.new("Greybox_World")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.055, 0.065, 0.08, 1.0)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.28

scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGB"
scene.render.filepath = "//result.png"
scene.render.film_transparent = False

bpy.ops.wm.save_as_mainfile(filepath=str(OUT / "result.blend"), compress=True)
bpy.ops.render.render(write_still=True)
result = {
    "source": str(OUT / "result.blend"),
    "render": str(OUT / "result.png"),
    "objects": [floor.name, backdrop.name],
    "dimensions": {floor.name: list(floor.dimensions), backdrop.name: list(backdrop.dimensions)},
}
