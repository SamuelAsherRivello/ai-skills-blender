---
name: blender-render
description: Render existing Blender scenes to still images or frame sequences with preview checks and verified outputs.
---

# blender-render

## Inputs and scope

Accept existing scene, camera, output path/format/resolution; default to existing usable settings and bounded preview. Honor supplied context, references, output specifications, and technical constraints. State assumptions; ask only when an answer materially changes the work. Textual style needs no reference; inspect an explicitly supplied or known-gallery image before relying on it, and never fetch one automatically.

## Operating boundaries

Read [operating boundaries](../blender-setup/references/operating-boundaries.md) before execution.

## Appearance preservation

Render-only work preserves the source scene. Use a supplied visual reference to assess output when one exists; do not create a concept target or make design changes unless the user has included them in scope.

## Workflow

1. Verify readiness and identify still/sequence output requirements and source scene.
2. Preflight camera, visibility, missing assets, frame range and output destination.
3. Select a supported render engine/device and report any fallback.
4. Set a modest preview resolution/sample budget; cap requested frame batches.
5. Render the preview without overwriting unrelated outputs.
6. Inspect composition, noise, materials, transparency and exposure against the requested style and any supplied references. Identify the largest visible mismatch and route it to modeling, materials, or lighting before increasing render quality. Samples cannot repair missing construction depth, poor framing, or a mismatched visual treatment.
7. Record final settings, version, source path and expected files in a run manifest.
8. Render final output; resume only verified frames from the same source/settings and use a fresh run if settings changed.
9. Verify dimensions, format, alpha and complete frame coverage; inspect representative final images.
10. Deliver source, output paths, settings, evidence and any unverified quality/engine assumptions. For requested iteration studies, retain each attempt, select by inspected brief compliance rather than recency, and distinguish visual shortcomings from file-validation failures. Record build time separately from render time; treat a stated soft timing target as a trade-off, not permission to weaken the brief silently.

## Execution notes

Use [scripts/verify_outputs.py](scripts/verify_outputs.py) for PNG output manifests. It verifies structure and requested dimensions/channels, not artistic quality or alpha coverage. Run with --help. Actual image inspection remains required. Save the source before recording its path.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.
