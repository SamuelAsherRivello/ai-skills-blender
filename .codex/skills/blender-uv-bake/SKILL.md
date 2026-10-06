---
name: blender-uv-bake
description: Unwrap Blender meshes and bake source detail into target texture maps; use for UV layout and texture baking.
---

# blender-uv-bake

## Inputs and scope

Accept source and target, map types, texture resolution and target engine; clarify source/target ambiguity. Honor supplied context, references, output specifications, and technical constraints. State assumptions; ask only when an answer materially changes the work. Textual style needs no reference; inspect an explicitly supplied or known-gallery image before relying on it, and never fetch one automatically.

## Operating boundaries

Read [operating boundaries](../blender-setup/references/operating-boundaries.md) before execution.

## Appearance preservation

UV and baking work preserves the approved asset look. Use supplied references to judge map fidelity where relevant, but do not create concept-target work for a technical unwrap or bake.

## Workflow

1. Verify readiness and explicitly identify source meshes and target mesh.
2. Choose map types, resolution and texel density appropriate to final usage.
3. Save a checkpoint and make an isolated bake target when changing existing UVs.
4. Choose seams from visibility/deformation needs and unwrap.
5. Inspect distortion and unintended overlaps with a checker.
6. Pack islands with scale consistency and resolution-aware margins.
7. Configure the supported bake engine, selected-to-active order, cage/ray distance, active UV and active target image nodes.
8. Bake a small test and inspect projection errors, seams and channel conventions.
9. Bake final maps; apply them to the target and inspect at intended viewing size.
10. Deliver target/source blend, maps, UV information and bake settings.

## Execution notes

Normal/roughness maps use data color space; confirm tangent basis and green-channel convention for the destination. Do not bake onto a source image in use. Verify selection and active object immediately before a bake.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.
