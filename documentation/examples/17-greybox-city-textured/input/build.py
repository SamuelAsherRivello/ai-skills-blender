"""Build the Slate-textured city greybox in the connected Blender editor."""
import importlib
import sys
from pathlib import Path

EXAMPLE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXAMPLE.parent / "_shared"))
import greybox_textured
importlib.reload(greybox_textured)
from greybox_textured import add_camera_and_lights, box, plane, save_and_render, slate_material, start_scene

OUT = EXAMPLE / "output"
scene, collection = start_scene(
    "Greybox_City_Textured", "17-greybox-city-textured",
    "Do the road crossing, city blocks, and height hierarchy read at a glance?",
    "No facade, road-marking, streetscape, vehicle, tree, image-texture, UV, or bevel detail.",
)
floor = slate_material("Floor", (0.28, 0.33, 0.38))
route = slate_material("Route", (0.16, 0.20, 0.25))
buildings = slate_material("Buildings", (0.50, 0.56, 0.62))
plane("City_Textured_Ground_Plane", (0, 0), (24, 20), 0, collection, floor)
plane("City_Textured_Road_East_West", (0, 0), (24, 3.0), 0.02, collection, route)
plane("City_Textured_Road_North_South", (0, 0), (3.0, 20), 0.03, collection, route)
for name, center, size in (
    ("City_Textured_Building_A", (-7.0, -5.2, 2.0), (4.0, 3.2, 4.0)),
    ("City_Textured_Building_B", (-6.4, 5.0, 4.0), (4.8, 3.8, 8.0)),
    ("City_Textured_Building_C", (6.6, -5.0, 5.0), (4.5, 3.5, 10.0)),
    ("City_Textured_Building_D", (6.7, 4.8, 2.8), (3.7, 4.0, 5.6)),
    ("City_Textured_Building_E", (-2.7, 6.5, 3.3), (2.0, 2.5, 6.6)),
    ("City_Textured_Building_F", (2.9, -6.2, 3.6), (2.3, 2.5, 7.2)),
):
    box(name, center, size, collection, buildings)
add_camera_and_lights(scene, collection, "City_Textured", (25, -28, 25), (0, 0, 3.5), 32.0)
source, render = save_and_render(scene, OUT)
result = {"source": str(source), "render": str(render), "objects": [obj.name for obj in collection.objects if obj.type == "MESH"]}
