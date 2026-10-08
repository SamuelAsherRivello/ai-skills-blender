# Fixed-palette kitchen greybox review

This greybox answers whether the floor, enclosing room surfaces, and repeated kitchen fixtures read as three intentional groups. The one-scene-unit tile convention is deliberately treated as one metre.

The ordered palette map is `Floor → PowderBlue → Greybox_PowderBlue_Floor`, `Walls → SoftSage → Greybox_SoftSage_Walls`, then `Furniture → SoftRose → Greybox_SoftRose_Furniture`. Both walls share the second material; the counters, island, and refrigerator all share the third. Every material samples the same `Greybox_GridReference` with uniform `(1.0, 1.0, 1.0)` mapping, keeping all major checker squares the same size. Omitted: cabinet fronts, doors, windows, sink detail, stools, decor, image textures, UVs, and modifiers.

## Verification

The saved render and browser-rendered GLB were inspected. The three light palette entries separate floor, enclosing walls, and repeated furnishings without assigning semantic color meaning; stretched walls and furniture retain the same square grid scale. The GLB passed the repository validator with zero errors; its generated tangent-space warning is expected for the baked normal atlas. Anonymous public HTTP access remains unverified because this local repository has not been published.
