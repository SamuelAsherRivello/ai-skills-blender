# Slate-textured city greybox review

This greybox answers whether a primary road crossing, four city blocks, and a varied-height building hierarchy read immediately. The selected hue is Slate; every material uses the same editable Object-coordinate checker graph with a mapping scale of 3.0 and restrained value contrast.

The category map is `Floor → Greybox_Slate_Floor`, `Route → Greybox_Slate_Route`, and `Buildings → Greybox_Slate_Buildings`; all six building masses share the exact `Buildings` datablock. It intentionally omits facades, road markings, sidewalks, vehicles, street furniture, trees, image textures, UVs, and modifiers.

## Verification

The saved render was inspected for the road crossing, height hierarchy, and readable checker grouping. The embedded-texture GLB passed the repository validator with zero errors (the generated tangent-space warning is expected for its baked normal atlas) and was inspected in the local Model Viewer. Anonymous public HTTP access remains unverified because this local repository has not been published.
