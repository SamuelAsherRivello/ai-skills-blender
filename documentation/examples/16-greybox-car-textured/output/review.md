# Slate-textured car greybox review

This greybox answers whether the wheel placement, ground contact, and two main masses read as a car. The selected hue is Slate; every material uses the same editable Object-coordinate checker graph with a mapping scale of 3.0 and restrained value contrast.

The category map is `Floor → Greybox_Slate_Floor`, `Vehicle → Greybox_Slate_Vehicle`, and `Wheels → Greybox_Slate_Wheels`. It intentionally omits all vehicle surface detail, glazing, interiors, trim, image textures, UVs, and modifiers.

## Verification

The saved render was inspected for silhouette, wheel placement, ground contact, and readable checker grouping. The embedded-texture GLB passed the repository validator with zero errors (the generated tangent-space warning is expected for its baked normal atlas) and was inspected in the local Model Viewer. Anonymous public HTTP access remains unverified because this local repository has not been published.
