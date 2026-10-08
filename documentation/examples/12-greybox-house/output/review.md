# Greybox house review

This house greybox asks whether a ground block, block house with a pyramid roof and chimney, and one blocky tree read as three distinct groups. The ground uses PowderBlue, all house parts use SoftSage, and both tree parts use SoftRose. Each category has one shared checker material with a one-scene-unit tile on axis-aligned faces; this example treats one scene unit as one metre.

The roof uses XY projection, so its sloped checker cells are stretched compared with the axis-aligned cubes. The scene intentionally omits doors, windows, a path, foliage detail, bevels, and realistic materials. The earlier two-plane scene remains in `../../25-greybox-2-5d-historical/` as a historical example.

## Verification

The saved 960×540 render was inspected visually. It shows the tree fully beside the house, the roof and chimney above the block body, and the three checker colors on their intended groups. Blender read the saved source as one isolated scene with six meshes, one camera, one light, and three packed checker images. The GLB has six meshes and three textured materials; its buffer, accessor, and embedded-image references are in bounds, and its hashes match the adjacent export report. Browser inspection is the final publication check.
