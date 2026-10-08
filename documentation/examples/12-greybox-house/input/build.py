"""Build example 12 in the connected Blender editor without replacing its file.

The scene uses packed checker images so the source and direct GLB export retain
the same three category textures. Run through the official Blender Lab MCP.
"""
from array import array
import hashlib
import json
from pathlib import Path
import time

import bpy
from mathutils import Vector


EXAMPLE = Path(__file__).resolve().parents[1]
ROOT = EXAMPLE.parents[2]
OUT = EXAMPLE / "output"
OUT.mkdir(parents=True, exist_ok=True)

PALETTE = (
    ("PowderBlue", (0.46, 0.61, 0.74), "Ground"),
    ("SoftSage", (0.52, 0.70, 0.60), "House"),
    ("SoftRose", (0.76, 0.56, 0.62), "Tree"),
)
TILE_SIZE = 1.0
CAMERA_TARGET = Vector((-0.25, 0.0, 2.0))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def checker_image(name, base):
    """Two one-metre checks per repeat, packed into the source scene."""
    size = 128
    image = bpy.data.images.new(name, width=size, height=size, alpha=False)
    image.file_format = "PNG"
    image.colorspace_settings.name = "sRGB"
    lighter = tuple(min(1.0, component + 0.10) for component in base)
    pixels = array("f")
    for y in range(size):
        for x in range(size):
            color = base if ((x // 64) + (y // 64)) % 2 == 0 else lighter
            pixels.extend((*color, 1.0))
    image.pixels.foreach_set(pixels)
    image.update()
    image.pack()
    return image


def category_material(palette_name, base, category):
    image = checker_image(f"House12_{palette_name}_Checker", base)
    material = bpy.data.materials.new(f"Greybox_{palette_name}_{category}")
    material.use_nodes = True
    material.diffuse_color = (*base, 1.0)
    nodes = material.node_tree.nodes
    nodes.clear()
    texture = nodes.new("ShaderNodeTexImage")
    texture.image = image
    texture.interpolation = "Closest"
    texture.extension = "REPEAT"
    principled = nodes.new("ShaderNodeBsdfPrincipled")
    principled.inputs["Roughness"].default_value = 0.84
    output = nodes.new("ShaderNodeOutputMaterial")
    material.node_tree.links.new(texture.outputs["Color"], principled.inputs["Base Color"])
    material.node_tree.links.new(principled.outputs["BSDF"], output.inputs["Surface"])
    material["greybox_palette_entry"] = palette_name
    material["semantic_category"] = category
    material["texture_tile_world_units"] = TILE_SIZE
    material["texture_projection"] = "world-axis UV; sloped roof uses XY projection"
    return material


def add_mesh(collection, name, vertices, faces, material):
    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.materials.append(material)
    mesh.update()
    uv = mesh.uv_layers.new(name="WorldMeterGrid")
    for polygon in mesh.polygons:
        normal = polygon.normal
        for loop_index in polygon.loop_indices:
            vertex = mesh.vertices[mesh.loops[loop_index].vertex_index].co
            if abs(normal.z) >= max(abs(normal.x), abs(normal.y)):
                u, v = vertex.x, vertex.y
            elif abs(normal.y) >= abs(normal.x):
                u, v = vertex.x, vertex.z
            else:
                u, v = vertex.y, vertex.z
            uv.data[loop_index].uv = (u / (2 * TILE_SIZE), v / (2 * TILE_SIZE))
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    return obj


def box(collection, name, center, size, material):
    x, y, z = center
    dx, dy, dz = (value / 2 for value in size)
    vertices = [(x + sx * dx, y + sy * dy, z + sz * dz)
                for sz in (-1, 1) for sy in (-1, 1) for sx in (-1, 1)]
    faces = [(0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4),
             (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)]
    return add_mesh(collection, name, vertices, faces, material)


def point_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def build():
    started = time.monotonic()
    previous_scene = bpy.context.window.scene
    scene = bpy.data.scenes.new("Greybox_House_12")
    scene["example_id"] = "12-greybox-house"
    scene["greybox_question"] = "Do house, ground, and tree read as three clear forms?"
    scene["intentional_omissions"] = "No doors, windows, paths, leaf detail, bevels, or realistic materials."
    scene.unit_settings.system = "METRIC"
    collection = bpy.data.collections.new("Greybox_House_12_Objects")
    scene.collection.children.link(collection)
    ground, house, tree = [category_material(*entry) for entry in PALETTE]
    objects = [
        box(collection, "House12_Ground", (0, 0, -0.12), (12, 10, 0.24), ground),
        box(collection, "House12_Main_Block", (0, 0, 1.6), (4.2, 3.6, 3.2), house),
    ]
    roof_vertices = [(-2.35, -2.05, 3.2), (2.35, -2.05, 3.2),
                     (2.35, 2.05, 3.2), (-2.35, 2.05, 3.2), (0, 0, 5.2)]
    objects.append(add_mesh(collection, "House12_Pyramid_Roof", roof_vertices,
                            [(3, 2, 1, 0), (0, 1, 4), (1, 2, 4),
                             (2, 3, 4), (3, 0, 4)], house))
    objects.extend((
        box(collection, "House12_Chimney", (1.15, 0.75, 4.5), (0.55, 0.55, 2.1), house),
        box(collection, "House12_Tree_Trunk", (-4.3, -2.2, 1.05), (0.45, 0.45, 2.1), tree),
        box(collection, "House12_Tree_Canopy", (-4.3, -2.2, 2.75), (1.9, 1.9, 1.9), tree),
    ))
    camera_data = bpy.data.cameras.new("House12_Camera")
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = 14.0
    camera = bpy.data.objects.new("House12_Camera", camera_data)
    collection.objects.link(camera)
    camera.location = (8.0, -11.0, 8.0)
    point_at(camera, CAMERA_TARGET)
    scene.camera = camera
    sun_data = bpy.data.lights.new("House12_Key", "SUN")
    sun_data.energy = 1.8
    sun = bpy.data.objects.new("House12_Key", sun_data)
    collection.objects.link(sun)
    sun.rotation_euler = (0.55, -0.3, -0.55)
    world = bpy.data.worlds.new("House12_World")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.08, 0.09, 0.11, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.8
    scene.world = world
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 960
    scene.render.resolution_y = 540
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    source = OUT / "result.blend"
    preview = OUT / "result.png"
    exported = OUT / "result.glb"
    try:
        bpy.context.window.scene = scene
        scene.render.filepath = str(preview)
        bpy.ops.render.render(write_still=True)
        scene.render.filepath = "//result.png"
        bpy.data.libraries.write(str(source), {scene}, compress=True)
        bpy.ops.object.select_all(action="DESELECT")
        for obj in objects:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = objects[0]
        bpy.ops.export_scene.gltf(
            filepath=str(exported), export_format="GLB", use_selection=True,
            use_active_scene=True, export_apply=True, export_cameras=False,
            export_lights=False, export_animations=False,
            export_draco_mesh_compression_enable=False,
        )
    finally:
        bpy.context.window.scene = previous_scene
    aspect = scene.render.resolution_x / scene.render.resolution_y
    report = {
        "sourcePath": source.relative_to(ROOT).as_posix(),
        "sourceSha256": digest(source),
        "glbPath": exported.relative_to(ROOT).as_posix(),
        "glbSha256": digest(exported),
        "byteSize": exported.stat().st_size,
        "warnings": [
            "Blender world and studio lighting are replaced by viewer lighting.",
            "Checker images are packed; world-axis UVs keep one-metre tiles square on axis-aligned faces, while roof slopes use XY projection.",
            "Packed-image direct export replaces the standard procedural atlas bake for this scene.",
        ],
        "blenderVersion": bpy.app.version_string,
        "exportMethod": "Direct glTF export of packed checker images from an isolated scene",
        "seconds": round(time.monotonic() - started, 2),
        "view": {
            "position": [camera.location.x, camera.location.z, -camera.location.y],
            "target": [CAMERA_TARGET.x, CAMERA_TARGET.z, -CAMERA_TARGET.y],
            "frameHeight": camera_data.ortho_scale / max(1, aspect),
            "aspect": aspect,
        },
    }
    (OUT / "result.export.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return {"source": str(source), "render": str(preview), "glb": str(exported),
            "objects": [obj.name for obj in objects], "materials": [item.name for item in (ground, house, tree)]}


result = build()
