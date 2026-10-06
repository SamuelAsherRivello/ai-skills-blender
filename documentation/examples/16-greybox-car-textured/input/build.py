"""Build the Slate-textured car greybox in the connected Blender editor."""
import importlib
import sys
from pathlib import Path

EXAMPLE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXAMPLE.parent / "_shared"))
import greybox_textured
importlib.reload(greybox_textured)
from greybox_textured import add_camera_and_lights, box, save_and_render, slate_material, start_scene, wheel, mesh

OUT = EXAMPLE / "output"
scene, collection = start_scene(
    "Greybox_Car_Textured", "16-greybox-car-textured",
    "Do the primary vehicle masses, wheel positions, and ground contact read as a car?",
    "No glazing, doors, lights, interior, trim, bevels, image textures, or UVs.",
)
floor = slate_material("Floor", (0.24, 0.29, 0.34))
vehicle = slate_material("Vehicle", (0.44, 0.50, 0.56))
wheels = slate_material("Wheels", (0.15, 0.19, 0.24))
mesh("Car_Textured_Ground_Plane", [(-5, -4, 0), (5, -4, 0), (5, 4, 0), (-5, 4, 0)], [(0, 1, 2, 3)], collection, floor)
box("Car_Textured_Chassis_Block", (0, 0, 1.0), (4.8, 2.0, 0.9), collection, vehicle)
box("Car_Textured_Cabin_Block", (-0.35, 0, 1.85), (2.3, 1.75, 0.9), collection, vehicle)
for name, center in (("Car_Textured_Wheel_Front_Left", (1.65, -1.05, 0.55)), ("Car_Textured_Wheel_Front_Right", (1.65, 1.05, 0.55)), ("Car_Textured_Wheel_Rear_Left", (-1.65, -1.05, 0.55)), ("Car_Textured_Wheel_Rear_Right", (-1.65, 1.05, 0.55))):
    wheel(name, center, 0.55, 0.35, collection, wheels)
add_camera_and_lights(scene, collection, "Car_Textured", (7.5, -9.0, 5.8), (0, 0, 1.0), 7.0)
source, render = save_and_render(scene, OUT)
result = {"source": str(source), "render": str(render), "objects": [obj.name for obj in collection.objects if obj.type == "MESH"]}
