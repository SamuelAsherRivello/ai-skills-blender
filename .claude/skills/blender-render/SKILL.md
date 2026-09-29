---
name: blender-render
description: Render existing Blender scenes to still images or frame sequences with preview checks and verified outputs.
---

# blender-render

## Inputs and scope

Accept existing scene, camera, output path/format/resolution; default to existing usable settings and bounded preview. Also accept optional setting, action/pose, composition, camera, lighting/mood, palette, user references, output specifications and technical constraints when relevant. State assumptions; ask only when a missing answer materially changes the work. A textual style works without reference images. The shared render-style gallery is optional: use an explicitly supplied path or known checkout, inspect a chosen PNG before drawing conclusions, and never fetch missing images automatically.

Use the separately configured official Blender Lab MCP connection. Discover its tools and confirm read-only scene access before mutations; report a connection blocker instead of switching servers. Preserve unrelated objects and settings, scope new content by named collection/run, and checkpoint before destructive edits. Repeated scripts must replace only owned output or create a separate named run. Do not start paid services without authorization.

## Workflow

1. Verify readiness and identify still/sequence output requirements and source scene.
2. Preflight camera, visibility, missing assets, frame range and output destination.
3. Select a supported render engine/device and report any fallback.
4. Set a modest preview resolution/sample budget; cap requested frame batches.
5. Render the preview without overwriting unrelated outputs.
6. Inspect composition, noise, materials, transparency and exposure.
7. Record final settings, version, source path and expected files in a run manifest.
8. Render final output; resume only verified frames from the same source/settings and use a fresh run if settings changed.
9. Verify dimensions, format, alpha and complete frame coverage; inspect representative final images.
10. Deliver source, output paths, settings, evidence and any unverified quality/engine assumptions.

## Execution notes

Use [scripts/verify_outputs.py](scripts/verify_outputs.py) for PNG output manifests. It verifies structure and requested dimensions/channels, not artistic quality or alpha coverage. Run with --help. Actual image inspection remains required. Save the source before recording its path.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.
