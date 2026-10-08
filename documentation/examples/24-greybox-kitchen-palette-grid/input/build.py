"""Build the fixed-palette kitchen greybox in the connected Blender editor."""
import importlib
import sys
from pathlib import Path

EXAMPLE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXAMPLE.parent / "_shared"))
import greybox_textured
importlib.reload(greybox_textured)
from greybox_textured import add_camera_and_lights, add_grid_reference, box, palette_material, plane, save_and_render, start_scene, wall

OUT = EXAMPLE / "output"
scene, collection = start_scene(
    "Greybox_Kitchen_Palette_Grid", "24-greybox-kitchen-palette-grid",
    "Do the floor, room boundary, and grouped kitchen furnishings read as three clear categories at a one-metre grid scale?",
    "No cabinet fronts, doors, windows, sink detail, furniture detail, image textures, UV, or bevel detail.",
)
grid = add_grid_reference(collection, tile_size=1.0)
floor = palette_material("Floor", 0, grid, tile_size=1.0)
walls = palette_material("Walls", 1, grid, tile_size=1.0)
furniture = palette_material("Furniture", 2, grid, tile_size=1.0)
plane("Kitchen_Palette_Floor_Plane", (0, 0), (10, 8), 0, collection, floor)
wall("Kitchen_Palette_Back_Wall", [(-5, 3.5, 0), (5, 3.5, 0), (5, 3.5, 5), (-5, 3.5, 5)], collection, walls)
wall("Kitchen_Palette_Left_Wall", [(-4.5, -4, 0), (-4.5, 3.5, 0), (-4.5, 3.5, 5), (-4.5, -4, 5)], collection, walls)
box("Kitchen_Palette_Back_Counter", (0.5, 2.8, 0.9), (6.0, 0.8, 1.8), collection, furniture)
box("Kitchen_Palette_Side_Counter", (-3.6, 0.8, 0.9), (0.8, 3.2, 1.8), collection, furniture)
box("Kitchen_Palette_Refrigerator", (3.8, 2.85, 1.65), (1.1, 0.85, 3.3), collection, furniture)
box("Kitchen_Palette_Island", (0.2, -0.65, 0.9), (2.6, 1.1, 1.8), collection, furniture)
add_camera_and_lights(scene, collection, "Kitchen_Palette", (10.0, -12.0, 8.5), (0.0, 0.8, 1.8), 13.0, fill=True)
source, render = save_and_render(scene, OUT)
result = {"source": str(source), "render": str(render), "palette": ["PowderBlue", "SoftSage", "SoftRose"], "objects": [obj.name for obj in collection.objects if obj.type == "MESH"]}
