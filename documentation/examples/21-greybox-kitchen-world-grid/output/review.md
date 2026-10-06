# World-grid kitchen greybox review

This greybox answers whether an open room shell, L-shaped work zone, refrigerator mass, and central circulation path read immediately at a one-metre grid scale. The selected hue is Slate. Major tiles are fixed one-scene-unit squares; this example records the deliberate convention that one scene unit equals one metre.

Every category material samples Object coordinates from the single owned `Greybox_GridReference` Empty through a uniform XYZ Mapping scale of `(1.0, 1.0, 1.0)`. This keeps the 3D checker square and world-aligned across the floor, vertical walls, long counters, shallow island, and tall refrigerator. The category map is `KitchenFloor → Greybox_Slate_KitchenFloor`, `KitchenWall → Greybox_Slate_KitchenWall`, `KitchenCounter → Greybox_Slate_KitchenCounter`, and `KitchenAppliance → Greybox_Slate_KitchenAppliance`; both counter runs and the island share the exact `KitchenCounter` datablock. It intentionally omits cabinet fronts, doors, windows, sink details, furniture, decor, image textures, UVs, and modifiers.

## Verification

The saved Blender render and the browser-rendered GLB were inspected: the floor, vertical walls, long/shallow counter masses, island, and refrigerator retain square, same-size major tiles. The GLB passed the repository validator with zero errors; its generated tangent-space warning is expected for the baked normal atlas. Anonymous public HTTP access remains unverified because this local repository has not been published.
