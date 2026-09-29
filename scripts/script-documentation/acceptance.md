# Validation and acceptance

The current fourteen-skill catalog adds [visual target acceptance](visual-target-acceptance.md). The original thirteen-skill technical exercise below is retained as its historical record.

Validated on 2026-09-29 with local Codex on Windows, Blender 5.2.2 LTS and official Blender Lab MCP add-on/server 1.0.3 (26 discovered tools). This is a small technical acceptance suite, not proof of production quality for every possible subject.

## Automated checks

- Thirteen skill entrypoints, names, ten-step workflows, metadata and local resources validate.
- Nine setup regression tests pass, including scene-only failure after successful handshake.
- Twelve local repository helper/installer/package tests pass, including invalid PNG/output conditions, metadata/resource failures, installation dry runs, conflicts/backups, legacy preservation and independently installed copies, overlapping gallery destination rejection and cache exclusion.
- The live diagnostic passes all six checks; native scene access is also confirmed.
- Twelve final PNG outputs pass manifest checks for 128x128 dimensions, RGBA channels, source existence and recorded settings.
- Blender sprite tests pass deterministic packing, size/missing-input rejection and existing-output preservation. Both packed tiles match source pixels exactly; alpha includes transparent and opaque pixels.
- No global skill installation, MCP configuration change or public release was performed.

## Live exercise matrix

The maintainer ran the local, Git-ignored `tests/blender_acceptance.py` through the official MCP with `REPO` set to this checkout and `OUTPUT` set to a fresh local run directory. The accepted local run was `.acceptance/run-05`; source is `acceptance.blend`, structured results are `evidence.json`, and output settings are `render-manifest.json`. These generated files are deliberately ignored by Git.

| Skill | Exercise and evidence | Observed result / limit |
|---|---|---|
| blender-setup | Read-only bridge diagnostic and native scene query | Six passes; original Scene has Cube, Light, Camera |
| blender-create-model | Editable beveled prop; model-environment.png and two sprite views | Dimensions 0.8 x 0.8 x 1.2; silhouette inspected; original scene preserved |
| blender-create-environment | Floor and three repeated modules; model-environment.png | Consistent scale and spacing; no game traversal claim |
| blender-procedural-geometry | Seed 7, counts 0/3/8, repeated generation and invalid count | Deterministic geometry; no accidental repeated output |
| blender-materials | Terracotta/blue surfaces under two light positions; material-comparison.png | Surface response inspected; constants need no external textures |
| blender-uv-bake | Selected-to-active color bake; bake.png, baked-target.png | 64x64 sRGB map, UV cross layout, four-pixel margin; target appearance reviewed |
| blender-light-camera | Orthographic camera, area light and alternate illumination | Framing, shadow direction and exposure inspected |
| blender-render | Twelve rendered PNGs plus manifest/source | PNG chunks and decoded scanlines pass; actual images separately inspected |
| blender-rig-animate | One-bone deformation at frames 1/5/9, 12 FPS | Visible bend and return; simple fixture does not certify complex character anatomy |
| blender-game-export | asset.glb reimport with prop, rig and skinned mesh | Two intended meshes, matching dimensions/pivots/material slots; animation duration 2/3 second preserved; target-engine import unverified |
| blender-review-optimize | optimize-before.png / optimize-after.png and mesh audit | 3,072 to 188 evaluated triangles; no visible silhouette change at 128x128 |
| blender-convert-3d-2d | Two fixed-scale views and packed/sheet.png + sheet.json | 256x128 sheet, documented centered pivot/directions, exact pixel preservation |
| blender-convert-2d-3d | Temporary rectangle reference; reconstruction-matching.png / reconstruction-oblique.png | Matching 1:1.5 silhouette; depth 0.2 explicitly inferred; no hidden-surface accuracy claim |

The source scene remained active after each fixture. Its original objects/transforms and unsaved filepath were preserved. Separate test scenes remain available for inspection. Checkpoints are local acceptance artifacts.

## Fixes learned from live execution

- Multi-scene glTF exports require both selected-object and active-scene scoping for this workflow.
- Skinned meshes need the intended armature hierarchy and origin normalization while preserving world geometry.
- Imported armatures create auxiliary display meshes; compare scene assets rather than every newly created mesh datablock.
- Restrict exported animations to intended active actions; unrelated actions can produce warnings.
- A subtle axial twist was a weak visual test. The fixture now uses an obvious bend and return.
- Compare clip duration in seconds: the source frames 1..9 at 12 FPS reimported as 2..18 at 24 FPS, preserving duration.

## Request behavior review

- “A boy getting ready for school, comic-book style” is accepted as a subject/style brief with stated defaults for an editable posed character and preview. This was an instruction-contract review; a full boy character was not generated as part of the technical fixture.
- “Render the current scene” reuses scene settings and does not require a new subject or reference PNG; the live fixture renders existing scene state.
- Empty or absent galleries do not block text-based style requests.
- Setup failures use Step / Status / Comment and solution text in the failed row; regression tests cover closed Blender, stopped bridge, missing configuration, inspection failure, version mismatch, handshake failure and scene failure.

## Reproduce

Install development requirements, run the commands in the root README, then execute the Blender fixture only against a verified official connection. Use a fresh output directory each time. It checkpoints before mutation and restores the original active scene in a finally block. It adds isolated test scenes; it does not delete arbitrary existing scenes.

Claude packaging and installation are tested; full Claude runtime execution remains unverified. Other platforms, complex assets, production animation rigs and game-engine imports need their own validation. The initial acceptance run used empty galleries. Afterward, 20 user-supplied reference PNGs were copied into the gallery and verified against their source SHA-256 hashes.
