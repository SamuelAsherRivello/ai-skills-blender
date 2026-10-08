"""Build the fixed-palette car greybox in the connected Blender editor."""
import importlib
import sys
from pathlib import Path

EXAMPLE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXAMPLE.parent / "_shared"))
import greybox_textured
importlib.reload(greybox_textured)
from greybox_textured import add_camera_and_lights, add_grid_reference, box, mesh, palette_material, save_and_render, start_scene, wheel

OUT = EXAMPLE / "output"
scene, collection = start_scene(
    "Greybox_Car_Palette_Grid", "22-greybox-car-palette-grid",
    "Do the car's main mass, wheel placement, ground contact, and two primary groups read at a one-metre grid scale?",
    "No glazing, doors, lights, interior, trim, bevels, image textures, UVs, or modifiers.",
)
grid = add_grid_reference(collection, tile_size=1.0)
floor = palette_material("Floor", 0, grid, tile_size=1.0)
car = palette_material("Car", 1, grid, tile_size=1.0)
mesh("Car_Palette_Ground_Plane", [(-5, -4, 0), (5, -4, 0), (5, 4, 0), (-5, 4, 0)], [(0, 1, 2, 3)], collection, floor)
box("Car_Palette_Chassis_Block", (0, 0, 1.25), (4.8, 2.0, 0.9), collection, car)
box("Car_Palette_Cabin_Block", (-0.35, 0, 2.1), (2.3, 1.75, 0.9), collection, car)
for name, center in (
    ("Car_Palette_Wheel_Front_Left", (1.65, -1.05, 0.8)),
    ("Car_Palette_Wheel_Front_Right", (1.65, 1.05, 0.8)),
    ("Car_Palette_Wheel_Rear_Left", (-1.65, -1.05, 0.8)),
    ("Car_Palette_Wheel_Rear_Right", (-1.65, 1.05, 0.8)),
):
    wheel(name, center, 0.8, 0.35, collection, car)
add_camera_and_lights(scene, collection, "Car_Palette", (7.5, -9.0, 5.8), (0, 0, 1.0), 7.0)
source, render = save_and_render(scene, OUT)
result = {"source": str(source), "render": str(render), "palette": ["PowderBlue", "SoftSage"], "objects": [obj.name for obj in collection.objects if obj.type == "MESH"]}
