[Back to README.md](../../../../README.md)

# 02 — City-Corner Firehouse

Selected version: attempt 05 with the final blue-sky and color pass. Earlier attempts were compared visually and removed during cleanup. This version has the most complete facade, arched apparatus bays, readable glazing, and coherent city context.

- [Prompt](../input/prompt.txt) and [build source](../input/build.py)
- [Visual target](../input/visual-targets/target-01/target.png) and [direction brief](../input/visual-targets/target-01/brief.md)
- [Final render](result.png), [editable Blender scene](result.blend), [GLB export](result.glb), and [editor screenshot](editor.png)
- [Settings](manifest.json), [facade control checks](control-checks.json), and [source reopening checks](reopen-check.json)

## Scene and settings

Blender 5.2.2 LTS, Cycles/OptiX, 64 samples, denoising, AgX, 1280×720. Final render: 7.846 seconds; original construction: 13.256 seconds. Camera: 51 mm, level three-quarter perspective, vertical shift 0.09. Procedural seed 27, Cycles seed 0.

The editable scene Feedback_Firehouse_05 contains 2,611 objects, a 14 m frontage, 11 m depth, approximately 9.3 m cornice and 13.3 m tower. Genuine window and bay cavities, glazed apparatus doors, shallow interiors, sidewalks, crosswalks, streetlights, a hydrant and neighboring buildings establish the city corner. Materials are procedural and require no external textures.

The world provides blue clouds to camera and glossy rays while preserving original daylight illumination. Compositor saturation is 1.10; this is not an exact 10% increase in displayed pixel saturation after AgX.

## Editing and reproduction

The embedded EDIT_FACADE_FEEDBACK.py exposes set_facade(window_count=5, blind_height=.42). Supported counts: 1–5; blind height: 0.2–1.2 metres. Bounds, invalid values and default restoration were checked. Embedded scripts do not execute automatically.

Use the consolidated external input/build.py through the official MCP context, with __file__ set to its path, in a session without its owned scene name. It creates the scene and final sky/color treatment and saves output/result.blend. Render afterward to produce output/result.png. This relocated source passed syntax checking; a fresh rebuild was not performed during folder cleanup. The saved scene and final render were preserved unchanged.

## Evidence and limitations

The selected render was visually inspected during cleanup. It is a clean procedural architectural visualization, not a claim of hyperrealism: city activity, surface wear and neighboring detail remain simplified. The concept target is inspiration, not the delivered render.

The retained editor.png is a genuine earlier screenshot of the selected geometry and predates the sky/color revision. A prior refresh produced a black frame; this cleanup did not take or claim a new editor capture.

Existing reopening evidence records the expected scene, camera, relative render destination and no external image or library dependencies. The GLB uses baked materials and viewer lighting; its appearance does not include Blender world/compositor effects. Cleanup verification checks retained file hashes and PNG dimensions without claiming a new export or render.
