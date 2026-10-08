"""Build the fixed-palette city greybox in the connected Blender editor."""
import importlib
import sys
from pathlib import Path

EXAMPLE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXAMPLE.parent / "_shared"))
import greybox_textured
importlib.reload(greybox_textured)
from greybox_textured import add_camera_and_lights, add_grid_reference, box, palette_material, plane, save_and_render, start_scene

OUT = EXAMPLE / "output"
scene, collection = start_scene(
    "Greybox_City_Palette_Grid", "23-greybox-city-palette-grid",
    "Do the shared ground/road network and all building blocks read as two clear groups at a one-metre grid scale?",
    "No facade, road-marking, streetscape, vehicle, tree, image-texture, UV, or bevel detail.",
)
grid = add_grid_reference(collection, tile_size=1.0)
floor = palette_material("Floor", 0, grid, tile_size=1.0)
buildings = palette_material("Buildings", 1, grid, tile_size=1.0)
plane("City_Palette_Ground_Plane", (0, 0), (24, 20), 0, collection, floor)
plane("City_Palette_Road_East_West", (0, 0), (24, 3.0), 0.02, collection, floor)
plane("City_Palette_Road_North_South", (0, 0), (3.0, 20), 0.03, collection, floor)
for name, center, size in (
    ("City_Palette_Building_A", (-7.0, -5.2, 2.0), (4.0, 3.2, 4.0)),
    ("City_Palette_Building_B", (-6.4, 5.0, 4.0), (4.8, 3.8, 8.0)),
    ("City_Palette_Building_C", (6.6, -5.0, 5.0), (4.5, 3.5, 10.0)),
    ("City_Palette_Building_D", (6.7, 4.8, 2.8), (3.7, 4.0, 5.6)),
    ("City_Palette_Building_E", (-2.7, 6.5, 3.3), (2.0, 2.5, 6.6)),
    ("City_Palette_Building_F", (2.9, -6.2, 3.6), (2.3, 2.5, 7.2)),
):
    box(name, center, size, collection, buildings)
add_camera_and_lights(scene, collection, "City_Palette", (25, -28, 25), (0, 0, 3.5), 32.0)
source, render = save_and_render(scene, OUT)
result = {"source": str(source), "render": str(render), "palette": ["PowderBlue", "SoftSage"], "objects": [obj.name for obj in collection.objects if obj.type == "MESH"]}
