[Back to examples](README.md)

# Example style coverage

This baseline visual audit compares each saved Blender render with its prompt and existing review. The intended look comes from the prompt; the observed look comes from the actual `output/result.png`, inspected on 2026-10-03. The full file and source-revision inventory is in [baseline-inventory.md](baseline-inventory.md). “Refresh” means the current evidence identifies missing required content, incorrect framing, style drift, or another major visible gap. “Retain” means the visible quality gate passed for the current deliverable. This is a review aid, not human approval.

| Example | Intended look | Observed look | Initial disposition |
|---|---|---|---|
| [01 — School Morning Character](01-school-morning-character/) | Stylized storybook character illustration in a bedroom | Faceted friendly character, warm pastel room, softly shaded diorama | Retain; style and requested pose read clearly. |
| [02 — City-Corner Firehouse](02-city-corner-firehouse/) | Realistic architectural visualization, daytime city corner | Detailed brick façade and street context, but clean procedural surfaces and simplified surroundings | Refresh; increase architectural realism while preserving the daytime brief. |
| [03 — Game-Ready Treasure Chest](03-game-ready-treasure-chest/) | Stylized game asset with readable walnut, iron and brass | Strong wood/metal palette, but the visible right end is open; the existing review also records missing lid end panels | Refresh; close and inspect the container from all sides, then retain the game-ready constraints. |
| [04 — Robot Greeting](04-robot-greeting/) | Friendly rounded toy robot, animated greeting | Clear teal-and-yellow toy design with a readable raised-hand pose and soft studio light | Retain; intended toy style is legible. |
| [05 — Fox Sprite Sheet](05-fox-sprite-sheet/) | Low-poly fox supporting sprite conversion | Strong angular silhouette and color blocks, presented as a single 3D hero render | Retain as a style example; inspect sprite-sheet deliverables separately from this hero image. |
| [06 — Desk Lamp from Image](06-desk-lamp-from-image/) | Plausible 3D reconstruction of a supplied lamp image | Dark metal articulated arms and yellow shade read as a product reconstruction in a warm studio | Retain with documented proportion and landmark differences from the source. |
| [07 — Sunlit Reading Nook](07-sunlit-reading-nook/) | Scandinavian interior with warm afternoon light and architectural perspective | Soft pastel diorama in an orthographic view; the existing review records cropped room edges and camera mismatch | Refresh; satisfy the requested perspective and keep the room/platform fully framed. |
| [08 — Modular Greenhouse](08-modular-greenhouse/) | Victorian-inspired glasshouse diorama with transparent glazing and procedural controls | The walls and roof transmit enough light to reveal plants, but the roof has a strong pale reflection; the render also omits the requested benches and brick masonry joints | Refresh; keep the readable modular glasshouse while adding the missing required content and controlling roof reflection. |
| [09 — Ceramic Tea Still Life](09-ceramic-tea-still-life/) | Refined product still life with glazed ceramic, wood and linen | Clean softly lit arrangement; the existing review says the surfaces are simpler and more stylized than the photographic target | Retain provisionally; prioritize more convincing material response if other evidence identifies a major gap. |
| [10 — Low-Poly Island](10-low-poly-island/) | Whimsical faceted island diorama | Strong low-poly terrain and simple saturated colors, distinct from the more naturalistic environment in example 11 | Retain; the requested faceted style is clear. |
| [11 — Floating Forest from Sketch](11-floating-forest-from-sketch/) | Detailed stylized natural environment reconstructed from a sketch | Lush foliage, exposed cliffs, water and debris with substantially more surface detail than the other dioramas | Retain with the documented differences from the frozen target; do not claim exact reconstruction. |

## Gallery-level finding

The subject and modeling workflows already vary. The visual finish is less evenly varied: examples 01, 03–05 and 07–10 often use soft studio or diorama lighting and simplified smooth forms; examples 02 and 06 provide architectural and product-reconstruction counterpoints, while example 11 has the richest natural surface detail. The refresh should preserve these intended styles and improve the weaker examples instead of applying one universal realism treatment.

## Quality gate used for refresh selection

**Final 2026-10-03 decision:** examples 02, 03, 07 and 08 require refresh. Examples 01, 04, 05, 06, 09, 10 and 11 pass the visible gate and remain documented as retained deliverables. The greenhouse decision follows review of the material and current render: glazing transmits the interior, while required benches and brick masonry detail are still absent.

An example passes when its required content and framing are present, the requested style remains legible, and no major visible gap remains. Technical file validity is a separate check. The initial refresh set is 02, 03 and 07; 08 needs scene/material reinspection before a final decision. All other examples remain subject to the same gate during implementation, and smaller target differences stay documented.
