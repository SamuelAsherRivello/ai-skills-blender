# World-grid car greybox review

This greybox answers whether the wheel placement, ground contact, and two main masses read as a car. The selected hue is Slate. Major tiles are fixed one-scene-unit squares; this example records the deliberate convention that one scene unit equals one metre.

Every category material samples Object coordinates from the single owned `Greybox_GridReference` Empty through a uniform XYZ Mapping scale of `(1.0, 1.0, 1.0)`. This keeps the 3D checker square and world-aligned on the stretched chassis, cabin, wheels, and floor. The category map is `CarGround → Greybox_Slate_CarGround`, `CarBody → Greybox_Slate_CarBody`, and `CarWheels → Greybox_Slate_CarWheels`. It intentionally omits all vehicle surface detail, glazing, interiors, trim, image textures, UVs, and modifiers.

## Verification

The saved Blender render and the browser-rendered GLB were inspected: the ground, stretched chassis, cabin, and wheels retain square, same-size major tiles. The GLB passed the repository validator with zero errors; its generated tangent-space warning is expected for the baked normal atlas. Anonymous public HTTP access remains unverified because this local repository has not been published.
