# Visual target skill acceptance

Tested 2026-09-29 for `blender-create-visual-target-2d`. The current catalog contains fourteen skills. The original thirteen-skill Blender technical exercise remains documented separately in acceptance.md.

| Path | Exercise | Observed result |
|---|---|---|
| Supplied image | User's generated firehouse target, preserved under examples/02-city-corner-firehouse/input/visual-targets/target-01 | Actual image inspected; 1672x941 PNG, byte-preserving copy and hash verified; original prompt/model recorded unknown. |
| Live generation | One built-in image_gen.imagegen call for a clean stylized waving toy robot | Actual 1254x1254 PNG inspected; full subject, grounded boots, readable pose and coherent palette. Narrow antenna headroom documented; no regeneration needed for useful direction. Exact prompt and provenance saved locally. |
| Missing tool | Manual scenario with no usable generator and no supplied image | Prompt-only package, missing-image status, null image, no visual-inspection claim. This was a simulated branch, not a live provider outage; no tools were disabled. |
| Comparison | Supplied firehouse target versus existing genuine Blender result | Separately labeled images, stable target identity, prioritized form/material/light/context gaps, no unperformed improvement claims. Render/blend hashes unchanged. |
| Packaging | Canonical, Codex and Claude package validation and sync check | Fourteen entries validate, resource links portable, client copies synchronized. Claude execution was not tested live. |

See [firehouse comparison](../../documentation/examples/02-city-corner-firehouse/output/target-comparison.md). Generated and prompt-only test evidence is local under ignored .acceptance/visual-target-2d/; it is not a shipped example asset or required skill dependency.

Boundary review also checked the spec scenarios: target-only work needs no Blender connection or scene edits; textual requests remain usable without targets; contradictory reference content is recorded rather than overriding the prompt; concept imagery cannot replace Blender output; changed targets are versioned; unknown model/seed metadata is not invented. These are manual behavior/instruction checks, not an independent or exhaustive benchmark.

No Blender rebuild, provider installation, global skill installation, gallery approval, commit or push was performed for this change.

## Parallel workflow instruction review

The default was subsequently expanded to all twelve 3D skills: one prompt-specific worker per top-level task, immediate main-thread progress, shared nested handoffs, exclusive target-directory ownership, and a bounded compare/correct/recheck loop. Setup checks, user opt-outs, existing-asset identity and scoped render/export/audit requests are covered. Delegation and generation fallbacks are explicit.

This addition was checked by reading the workflow and validating canonical/Codex/Claude packages and synchronization. The earlier live generation and supplied-image checks remain valid, and a subsequent Codex firehouse sky/color revision exercised parallel target generation while Blender renders proceeded. The parent inspected the returned target, rejected unrequested brightness/detail changes, and refined the procedural sky. The final render took 7.846 seconds; Claude remains statically validated only. This is an instruction-level workflow, not an installed background service. Finalization and publishing were authorized after the original acceptance exercise.
