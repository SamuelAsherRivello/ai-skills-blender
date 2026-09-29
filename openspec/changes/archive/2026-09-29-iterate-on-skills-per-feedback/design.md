# Design

## Context

See proposal.md for motivation. Example 02 has a 1280x720 Cycles output, editable source, and a technical review. Its broad stone trim, surface-mounted glazing, sparse context, and elevated camera weaken the requested realism. Eight user images mix photographs, a modern dusk visualization, and a dramatic isolated building render; they are cues, not a single reconstruction target. No main specs have been archived yet.

## Goals / Non-Goals

**Goals:** Test general decision guidance through five fresh-scene trials and two small transfer checks, with honest visual comparisons and traceable skill revisions.

**Non-Goals:** Exact reconstruction, adding trucks simply because references contain them, imposing photorealism on stylized prompts, replacing MCP, installing asset systems, completing add-examples milestone 2, or automatically publishing changes.

## Decisions

1. Keep original prompt and daytime two-bay brief stable. Add a separate feedback brief mapping reference cues to construction depth, scale, surface response, lighting, context, and visual acceptance. Do not blend incompatible night/day cues. Use original output as baseline zero.
2. Each attempt creates a new empty scene and new scene-owned geometry/materials. Construction scripts may evolve and be reused, but must execute from zero and embed their exact version in the resulting blend. Record script and skill hashes plus pre-build scene object count. This is a sequential learning exercise, not an independent statistical experiment.
3. Render then inspect then revise at least one skill after each attempt. Initially prioritize construction/proportions; subsequent priorities follow observed failures. Record a concrete observation and a portable decision rule. No predetermined claim that every iteration improves. Preserve rejected attempts.
4. Keep curated artifacts under input/ and output/. Leave the newly supplied feedback-target folder untouched; reference its files by relative paths and hashes. Store input/iterations/attempt-NN/build.py and skill snapshots; output/iterations/attempt-NN/{result.blend,result.png,editor.png,review.md,manifest.json}. Preserve output/baseline/ before changing main outputs. Record render and build times separately. Use genuine Blender screenshots, not composites presented as editor evidence.
5. Start with create-environment, create-model, materials, light-camera, render, review-optimize, and procedural-geometry. Update other skills only when evidence directly concerns their supported behavior. Keep mode-specific details concise or in linked references; synchronize generated client copies only from canonical sources.
6. Judge brief compliance, proportion/depth, material scale/response, light/exposure, camera/context, and artifacts against the actual images. Use descriptive findings rather than an invented objective realism score. A technically valid PNG is not visual success. Compare at final size as well as overview.
7. After attempt five's skill changes, render a realistic non-architectural prop and a stylized subject as small holdouts using final guidance. These verify limited transfer and style preservation, not all thirteen skills or all prompt types. Record any rule still untested; adjust unsupported guidance conservatively.
8. Select best attempt by visible quality and brief compliance, not attempt number. Promote its outputs to the established gallery paths with portable relative render paths; reopen and check the saved file. Preserve baseline and attempts so selection can be reversed.

## Risks / Trade-offs

- Procedural assets can remain visibly synthetic -> report the gap honestly; prioritize silhouettes, cavities, and material response before indiscriminate micro-noise or extra samples.
- Multiple coupled changes confound causality -> record intended change groups and observed results without attributing certainty to one parameter.
- Render budget competes with quality -> keep 30 seconds a soft goal, use bounded previews, record overruns rather than silently degrading the brief.
- Feedback images have unspecified licensing -> use them locally as user-provided comparison material; do not download or redistribute additional assets.
- Existing uncommitted edits -> preserve them and snapshot relevant skill bytes before iteration.
- UI screenshot may be unavailable when Blender is minimized -> report the exact issue, do not fabricate a capture or force foreground windows.

## Migration Plan

Snapshot existing outputs and canonical skill state, create independent attempts, synchronize clients, run validators, and replace only the main example output after selection. Baseline and per-attempt files support rollback. Leave milestone-approval task in add-examples pending.
