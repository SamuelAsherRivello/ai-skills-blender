# Fixed-palette city greybox review

This greybox answers whether the road/ground network and the varied-height building set read as two immediately distinct groups. The one-scene-unit tile convention is deliberately treated as one metre.

The ordered palette map is `Floor → PowderBlue → Greybox_PowderBlue_Floor`, then `Buildings → SoftSage → Greybox_SoftSage_Buildings`. The ground and both road planes share the first material; all six building masses share the second. Every material samples the same `Greybox_GridReference` with uniform `(1.0, 1.0, 1.0)` mapping, keeping all major checker squares the same size. Omitted: facades, markings, sidewalks, vehicles, streetscape, trees, image textures, UVs, and modifiers.

## Verification

The saved render and browser-rendered GLB were inspected. PowderBlue unifies ground and routes while SoftSage groups every building, and the wide, tall, and narrow primitives retain the same square grid scale. The GLB passed the repository validator with zero errors; its generated tangent-space warning is expected for the baked normal atlas. Anonymous public HTTP access remains unverified because this local repository has not been published.
