"""Build the world-grid car greybox in the connected Blender editor."""
import importlib
import sys
from pathlib import Path

EXAMPLE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXAMPLE.parent / "_shared"))
import greybox_textured
importlib.reload(greybox_textured)
from greybox_textured import add_camera_and_lights, add_grid_reference, box, mesh, save_and_render, slate_material, start_scene, wheel

OUT = EXAMPLE / "output"
scene, collection = start_scene(
    "Greybox_Car_World_Grid", "19-greybox-car-world-grid",
    "Do the vehicle masses, wheel positions, and ground contact read as a car at a one-metre grid scale?",
    "No glazing, doors, lights, interior, trim, bevels, image textures, UVs, or modifiers.",
)
grid = add_grid_reference(collection, tile_size=1.0)
floor = slate_material("CarGround", (0.24, 0.29, 0.34), grid, tile_size=1.0)
vehicle = slate_material("CarBody", (0.44, 0.50, 0.56), grid, tile_size=1.0)
wheels = slate_material("CarWheels", (0.15, 0.19, 0.24), grid, tile_size=1.0)
mesh("Car_Grid_Ground_Plane", [(-5, -4, 0), (5, -4, 0), (5, 4, 0), (-5, 4, 0)], [(0, 1, 2, 3)], collection, floor)
box("Car_Grid_Chassis_Block", (0, 0, 1.0), (4.8, 2.0, 0.9), collection, vehicle)
box("Car_Grid_Cabin_Block", (-0.35, 0, 1.85), (2.3, 1.75, 0.9), collection, vehicle)
for name, center in (
    ("Car_Grid_Wheel_Front_Left", (1.65, -1.05, 0.55)),
    ("Car_Grid_Wheel_Front_Right", (1.65, 1.05, 0.55)),
    ("Car_Grid_Wheel_Rear_Left", (-1.65, -1.05, 0.55)),
    ("Car_Grid_Wheel_Rear_Right", (-1.65, 1.05, 0.55)),
):
    wheel(name, center, 0.55, 0.35, collection, wheels)
add_camera_and_lights(scene, collection, "Car_Grid", (7.5, -9.0, 5.8), (0, 0, 1.0), 7.0)
source, render = save_and_render(scene, OUT)
result = {"source": str(source), "render": str(render), "grid_tile_world_units": 1.0, "objects": [obj.name for obj in collection.objects if obj.type == "MESH"]}
