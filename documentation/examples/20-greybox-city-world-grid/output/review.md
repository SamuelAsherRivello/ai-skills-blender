# World-grid city greybox review

This greybox answers whether a primary road crossing, varied-height blocks, and their relative one-metre scale read immediately. The selected hue is Slate. Major tiles are fixed one-scene-unit squares; this example records the deliberate convention that one scene unit equals one metre.

Every category material samples Object coordinates from the single owned `Greybox_GridReference` Empty through a uniform XYZ Mapping scale of `(1.0, 1.0, 1.0)`. This keeps the 3D checker square and world-aligned across the wide roads, flat ground, and tall or narrow building masses. The category map is `CityGround → Greybox_Slate_CityGround`, `CityRoute → Greybox_Slate_CityRoute`, and `CityBuildings → Greybox_Slate_CityBuildings`; all six building masses share the exact `CityBuildings` datablock. It intentionally omits facades, road markings, sidewalks, vehicles, street furniture, trees, image textures, UVs, and modifiers.

## Verification

The saved Blender render and the browser-rendered GLB were inspected: the road, ground, and varied-width/height building masses retain square, same-size major tiles. The GLB passed the repository validator with zero errors; its generated tangent-space warning is expected for the baked normal atlas. Anonymous public HTTP access remains unverified because this local repository has not been published.
