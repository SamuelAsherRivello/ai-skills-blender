[Back to README.md](../../../../README.md)

# 01 — School morning character

Status: technically verified; **awaiting human approval for milestone 2**.
Revision: pilot-v1, created 2026-09-29. No human approval has been recorded.

## Review the result

- [Final camera render](result.png)
- [Blender editor screenshot](editor.png)
- [Editable Blender scene](result.blend)
- [Exact initial prompt](../input/prompt.txt)
- [Front inspection](front-inspection.png), [side inspection](side-inspection.png), and [neutral-light comparison](neutral-light-comparison.png)

The character has a full-body silhouette, a hand wrapped around a backpack strap, a friendly face, blue clothing and a yellow backpack, and a compact bedroom setting. The final PNG was rendered in the open Blender application through the official MCP and saved directly from Render Result. The editor PNG is an actual full-window Blender screenshot, including the camera frame, scene hierarchy, and render settings.

## Inputs and construction

The prompt supplies the subject, pose, style, setting, palette, lighting, camera default, and output requirements. No external image reference or downloaded asset was used; the shared reference gallery was not changed or scanned. All geometry and materials were constructed in Blender. There were no additional user-facing creation prompts; technical refinements are recorded below.

Source repository revision: `fac7e7211955309049bd0869a33cf821157490be`. The example is an uncommitted local addition. README edits during this session are also local. The Blender file contains an embedded `BUILD_EXAMPLE_01.py` text block recording initial construction; the saved scene includes the subsequent refinements described here and is the authoritative final artifact. No random operations were used, so no seed applies.

The scene is `Example01_SchoolMorning`, organized into `01_Character`, `02_Bedroom`, and `03_Camera_and_Lights`. Named meshes, curves, editable bevels, and shader nodes remain available. The character is a static assembled illustration, not a rigged animation asset.

## Skills actually exercised

| Skill | Evidence |
|---|---|
| `blender-setup` | All six setup checks passed; direct native MCP scene access confirmed Blender 5.2.2 LTS and official add-on/server 1.0.3. |
| `blender-create-model` | Proportioned character, modeled face/limbs/backpack, readable grip, front/side/three-quarter inspections, organized editable parts. |
| `blender-materials` | Three-band Shader-to-RGB character materials, named color controls, neutral versus warm-light comparison, asset-path checks. |
| `blender-light-camera` | Orthographic three-quarter inspection camera, morning key/fill/rim lighting, exposure baseline, full-character framing checks. |
| `blender-render` | Bounded previews, saved source, timed final camera render, manifest-based PNG verification, actual image inspection. |
| `blender-review-optimize` | Scoped evaluated-geometry audit before/after, sample-cost assessment, before/after preview inspection, final counts and limitations. |

This pilot exercises six skills. Coverage of the other seven belongs to milestone 2 and is not claimed here.

## Render settings and measured cost

| Setting | Value |
|---|---|
| Blender | 5.2.2 LTS |
| Connection | Official Blender Lab MCP add-on/server 1.0.3 |
| Engine/device | EEVEE; NVIDIA GeForce RTX 4070 Laptop GPU |
| Final still | 1280×720 RGBA PNG, opaque background |
| Preview/comparison stills | 640×360 |
| Render samples | 128; first preview used 32 |
| Editor viewport samples | 128 |
| Camera | `Clinical_ThreeQuarter`, orthographic scale 5.7, position (4.4, -8, 4.3), looking at (0, 0.25, 1.28) |
| Color management | Standard, look None, exposure 0, gamma 1 |
| Initial preview | 17.542 s, including first-use shader compilation |
| Refined preview | 0.484 s with compiled shaders |
| Final still | **0.881 s** with compiled shaders |
| Front/side inspection | 0.639 s / 0.369 s |
| Neutral-light comparison | 0.476 s |

Times measure the synchronous Blender render call, including still output. They exclude modeling, inspection, saving/reopening, and screenshot capture. They describe this machine/session, not a portable performance guarantee. The final still met the soft 30-second target without lowering resolution.

## Verification and refinements

- Preserved the original scene and its cube, camera, and light. A full pre-pilot checkpoint is retained locally under the ignored `.acceptance/add-examples-pilot/` directory.
- Built in a separate owned scene. Exported only that scene and its dependencies into the deliverable, then reopened and saved it as a normal Blender project with its editor layout. No unrelated acceptance-test scenes or images remain in the deliverable.
- Reopened the saved project successfully: one scene, 159 objects, correct camera, 1280×720 output settings, and no external asset paths. Materials are procedural and Blender's built-in font is used, so no external texture/font package is needed.
- Inspected front, side, neutral-light, warm-light preview, and final images. The head and feet are visible in the final render; the backpack, strap grip, face, and bedroom props are readable.
- Corrected an overly tight temporary front/side inspection crop by widening those inspection cameras from orthographic scale 3.3 to 5.15. This did not change the final scene camera.
- Increased samples from 32 to 128 to reduce room-shadow grain. Compared the original and refined previews; geometry and intended shading remained unchanged.
- Audited **37,436 evaluated mesh triangles** before and after. No geometry reduction was necessary for this static still; retaining the editable parts was preferable. Curves are counted as scene objects but are not included in this helper's mesh-triangle total.
- Verified final PNG dimensions, alpha-channel presence, chunk checksums, and decoded pixel structure with the repository's `verify_outputs.py`, then visually inspected the image. Supporting evidence and manifests remain in the local ignored acceptance directory.
- Captured and inspected the genuine editor screenshot separately from the clean final render.
- A later screenshot returned black while Blender was minimized. Restored the existing Blender window, recaptured it, and visually verified the replacement before delivery.
- A reporting-only Python namespace error occurred after initial construction had already saved successfully; a direct scene query confirmed the result, and construction was not rerun or duplicated.

## Limitations and approval

The style is a rounded 3D comic interpretation with banded character shading and dark facial details, rather than a fully inked or halftone illustration. The room uses softer surface shading, and fine shadow grain can remain at close inspection. Facial features and hands are simplified; several parts intentionally overlap. This is not a watertight sculpt, deformation-ready character, or game export. EEVEE Shader-to-RGB materials are engine-specific. Animation, UV baking, and downstream engine compatibility were not requested or tested for this pilot.

Human approval: **pending**. Review the style, proportions, pose, render quality, and file layout. Any requested revisions remain in milestone 1. Examples 03–06 and final gallery integration await explicit approval of revised milestone 1. The user authorized the firehouse as example 02 before that approval.

## Folder migration

The user requested singular input/ and output/ directories. Original prompt bytes and visual results were preserved. This review and generated results now live in output/; the original prompt lives in input/. Blender uses //result.png relative to its relocated project. Shared references are unchanged. Migration is technical work, not human artistic approval.
