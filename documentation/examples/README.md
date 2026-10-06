[Back to README.md](../../README.md)

# Blender examples

Eleven integrated workflows, ready for visual review. Click a render to open it at full size. Examples 03–10 each use one creative iteration; review notes identify remaining artistic issues. Example 02 is the preserved baseline and examples 03, 07, and 08 have refresh candidates. Example 11 is the current showcase asset from a sketch input.

See the [style coverage map](style-coverage.md) for the intended and observed look of each example and the initial refresh candidates.

## Current visual review

[Open the side-by-side refresh gallery](human-review-2026-10-03.html) to review examples 02, 03, 07, and 08. It compares each selected refresh against its preserved baseline and states the visible differences.

| Name | Image | Files |
|---|---|---|
| [01 — School Morning Character](01-school-morning-character/) | <a href="01-school-morning-character/output/result.png"><img src="01-school-morning-character/output/result.png" width="100" alt="School Morning Character render" /></a> | [Prompt](01-school-morning-character/input/prompt.md) / [Result](01-school-morning-character/output/) |
| [02 — City-Corner Firehouse](02-city-corner-firehouse/) | <a href="02-city-corner-firehouse/output/result.png"><img src="02-city-corner-firehouse/output/result.png" width="100" alt="City-Corner Firehouse render" /></a> | [Prompt](02-city-corner-firehouse/input/prompt.md) / [Result](02-city-corner-firehouse/output/) |
| [03 — Game-Ready Treasure Chest](03-game-ready-treasure-chest/) | <a href="03-game-ready-treasure-chest/output/result.png"><img src="03-game-ready-treasure-chest/output/result.png" width="100" alt="Game-Ready Treasure Chest render" /></a> | [Prompt](03-game-ready-treasure-chest/input/prompt.md) / [Result](03-game-ready-treasure-chest/output/) |
| [04 — Robot Greeting](04-robot-greeting/) | <a href="04-robot-greeting/output/result.png"><img src="04-robot-greeting/output/result.png" width="100" alt="Robot Greeting render" /></a> | [Prompt](04-robot-greeting/input/prompt.md) / [Result](04-robot-greeting/output/) |
| [05 — Fox Sprite Sheet](05-fox-sprite-sheet/) | <a href="05-fox-sprite-sheet/output/result.png"><img src="05-fox-sprite-sheet/output/result.png" width="100" alt="Fox Sprite Sheet render" /></a> | [Prompt](05-fox-sprite-sheet/input/prompt.md) / [Result](05-fox-sprite-sheet/output/) |
| [06 — Desk Lamp from Image](06-desk-lamp-from-image/) | <a href="06-desk-lamp-from-image/output/result.png"><img src="06-desk-lamp-from-image/output/result.png" width="100" alt="Desk Lamp from Image render" /></a> | [Prompt](06-desk-lamp-from-image/input/prompt.md) / [Result](06-desk-lamp-from-image/output/) |
| [07 — Sunlit Reading Nook](07-sunlit-reading-nook/) | <a href="07-sunlit-reading-nook/output/result.png"><img src="07-sunlit-reading-nook/output/result.png" width="100" alt="Sunlit Reading Nook render" /></a> | [Prompt](07-sunlit-reading-nook/input/prompt.md) / [Result](07-sunlit-reading-nook/output/) |
| [08 — Modular Greenhouse](08-modular-greenhouse/) | <a href="08-modular-greenhouse/output/result.png"><img src="08-modular-greenhouse/output/result.png" width="100" alt="Modular Greenhouse render" /></a> | [Prompt](08-modular-greenhouse/input/prompt.md) / [Result](08-modular-greenhouse/output/) |
| [09 — Ceramic Tea Still Life](09-ceramic-tea-still-life/) | <a href="09-ceramic-tea-still-life/output/result.png"><img src="09-ceramic-tea-still-life/output/result.png" width="100" alt="Ceramic Tea Still Life render" /></a> | [Prompt](09-ceramic-tea-still-life/input/prompt.md) / [Result](09-ceramic-tea-still-life/output/) |
| [10 — Low-Poly Island](10-low-poly-island/) | <a href="10-low-poly-island/output/result.png"><img src="10-low-poly-island/output/result.png" width="100" alt="Low-Poly Island render" /></a> | [Prompt](10-low-poly-island/input/prompt.md) / [Result](10-low-poly-island/output/) |
| [11 — Floating Forest from Sketch](11-floating-forest-from-sketch/) | <a href="11-floating-forest-from-sketch/output/result.png"><img src="11-floating-forest-from-sketch/output/result.png" width="100" alt="Floating Forest from Sketch render" /></a> | [Prompt](11-floating-forest-from-sketch/input/prompt.md) / [Result](11-floating-forest-from-sketch/output/) |

## Layout and reproduction

Each numbered example stores prompts, build source and optional visual targets in `input/`, and Blender results, screenshots and review evidence in `output/`. Example 02 follows the same input/output pattern but is retained as a preserved baseline for comparison. Examples 03-10 each use a single creative iteration, while 11 demonstrates the sketch-based workflow. Example 11 is tracked with its preserved source, review notes and output renders.

`_shared/build_common.py` supplies common modeling, lighting and save helpers for examples 03–10. Open a result.blend to inspect its editable scene. To rebuild, use the verified official MCP with the example folder as context and the checked-in source assets. Saved scenes contain their required assets; helper source is separate from asset portability. Embedded build text records the original run; use the external input/build.py for the current checkout-integrated source.

## Skill coverage

All examples exercise setup, materials, lighting/camera, rendering and review. Model creation is shown by the character, chest, robot, fox, lamp and still life; environment creation by the firehouse, island and floating forest; greybox workflows are covered separately. See [verification.json](verification.json) for file and image checks. Reviews distinguish technical evidence from pending artistic approval. No target-engine compatibility is implied by Blender GLB or image export formatting.
