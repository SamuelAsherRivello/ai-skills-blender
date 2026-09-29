---
name: blender-rig-animate
description: Rig Blender assets and create named animation clips with deformation and motion checks.
---

# blender-rig-animate

## Inputs and scope

Accept mesh, movement requirements, frame rate, duration and target; clarify deformations that affect rig choice. Also accept optional setting, action/pose, composition, camera, lighting/mood, palette, user references, output specifications and technical constraints when relevant. State assumptions; ask only when a missing answer materially changes the work. A textual style works without reference images. The shared render-style gallery is optional: use an explicitly supplied path or known checkout, inspect a chosen PNG before drawing conclusions, and never fetch missing images automatically.

Use the separately configured official Blender Lab MCP connection. Discover its tools and confirm read-only scene access before mutations; report a connection blocker instead of switching servers. Preserve unrelated objects and settings, scope new content by named collection/run, and checkpoint before destructive edits. Repeated scripts must replace only owned output or create a separate named run. Do not start paid services without authorization.

## Workflow

1. Verify readiness and define intended motions, clip names and deliverable.
2. Inspect topology, rest pose, mesh transforms and scale.
3. Choose a minimal bone/control hierarchy and deformation axes.
4. Create the rig in an owned scope with predictable names.
5. Bind weights and inspect influence isolation.
6. Test extreme poses for collapsing joints and unwanted deformation.
7. Create named clips with explicit frame ranges and frame rate.
8. Refine timing, interpolation, contacts and loop transitions.
9. Review playback or a representative frame sequence plus root motion and clip metadata.
10. Save the editable rig/actions and provide previews and known deformation limits.

## Execution notes

Do not infer animation correctness from a single still. Check action slots and channel APIs against the installed Blender version. Preserve rest pose and distinguish object-level animation from bone deformation.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.
