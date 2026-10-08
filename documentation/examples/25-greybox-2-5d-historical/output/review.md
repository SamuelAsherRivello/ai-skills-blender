# 2.5D Greybox review

This deliberately minimal scene answers one question: can a ground plane and a perpendicular upright plane communicate a 2.5D spatial setup? The answer is evaluated from its orthographic three-quarter camera view. Floor and backdrop use neutral greys only to separate their roles.

The source intentionally omits thickness, props, texture maps, UV work, bevels, interiors, architecture, and decorative detail. Those are possible next fidelity steps only if the user asks for a more specific concept.

## Verification

The saved 960×540 render was inspected visually: the two planes meet at a clear right angle, with the floor receding to the vertical backdrop. The adjacent GLB has two exported meshes, no external buffers or textures, and passed the repository validator with zero errors and warnings. This source is preserved as a historical variant after the textured house replaced it at example 12; the public Model Viewer keeps it available as the final catalog entry.
