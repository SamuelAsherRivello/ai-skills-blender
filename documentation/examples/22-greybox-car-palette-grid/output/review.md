# Fixed-palette car greybox review

This greybox answers whether the ground plane and complete vehicle read as two distinct groups while wheel placement and contact remain clear. The one-scene-unit tile convention is deliberately treated as one metre.

The ordered palette map is `Floor → PowderBlue → Greybox_PowderBlue_Floor`, then `Car → SoftSage → Greybox_SoftSage_Car`. The chassis, cabin, and every wheel face—including each circular cap—use the exact shared `Greybox_SoftSage_Car` datablock. Every material samples the same `Greybox_GridReference` with uniform `(1.0, 1.0, 1.0)` mapping, keeping all major checker squares the same size. Omitted: vehicle surface detail, glazing, interiors, trim, image textures, UVs, and modifiers.

## Verification

The saved render and browser-rendered GLB were inspected. PowderBlue clearly separates the floor from SoftSage vehicle masses; the enlarged circular wheel caps visibly retain the same SoftSage checker material as the chassis and cabin. The GLB passed the repository validator with zero errors; its generated tangent-space warning is expected for the baked normal atlas. Anonymous public HTTP access remains unverified because this local repository has not been published.
