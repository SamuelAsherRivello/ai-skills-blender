"""Build the Slate-textured kitchen greybox in the connected Blender editor."""
import importlib
import sys
from pathlib import Path

EXAMPLE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXAMPLE.parent / "_shared"))
import greybox_textured
importlib.reload(greybox_textured)
from greybox_textured import add_camera_and_lights, box, plane, save_and_render, slate_material, start_scene, wall

OUT = EXAMPLE / "output"
scene, collection = start_scene(
    "Greybox_Kitchen_Textured", "18-greybox-kitchen-textured",
    "Does the open room shell, kitchen work zone, and central circulation read at a glance?",
    "No cabinet fronts, doors, windows, sink detail, furniture, image textures, UV, or bevel detail.",
)
floor = slate_material("Floor", (0.38, 0.44, 0.50))
walls = slate_material("Wall", (0.68, 0.73, 0.78))
counters = slate_material("Counter", (0.46, 0.52, 0.58))
appliance = slate_material("Appliance", (0.56, 0.62, 0.68))
plane("Kitchen_Textured_Floor_Plane", (0, 0), (10, 8), 0, collection, floor)
wall("Kitchen_Textured_Back_Wall", [(-5, 3.5, 0), (5, 3.5, 0), (5, 3.5, 5), (-5, 3.5, 5)], collection, walls)
wall("Kitchen_Textured_Left_Wall", [(-4.5, -4, 0), (-4.5, 3.5, 0), (-4.5, 3.5, 5), (-4.5, -4, 5)], collection, walls)
box("Kitchen_Textured_Back_Counter", (0.5, 2.8, 0.9), (6.0, 0.8, 1.8), collection, counters)
box("Kitchen_Textured_Side_Counter", (-3.6, 0.8, 0.9), (0.8, 3.2, 1.8), collection, counters)
box("Kitchen_Textured_Refrigerator", (3.8, 2.85, 1.65), (1.1, 0.85, 3.3), collection, appliance)
box("Kitchen_Textured_Island", (0.2, -0.65, 0.9), (2.6, 1.1, 1.8), collection, counters)
add_camera_and_lights(scene, collection, "Kitchen_Textured", (10.0, -12.0, 8.5), (0.0, 0.8, 1.8), 13.0, fill=True)
source, render = save_and_render(scene, OUT)
result = {"source": str(source), "render": str(render), "objects": [obj.name for obj in collection.objects if obj.type == "MESH"]}
