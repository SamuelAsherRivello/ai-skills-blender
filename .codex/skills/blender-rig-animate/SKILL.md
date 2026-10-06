---
name: blender-rig-animate
description: Rig Blender assets and create named animation clips with deformation and motion checks.
---

# blender-rig-animate

## Inputs and scope

Accept mesh, movement requirements, frame rate, duration and target; clarify deformations that affect rig choice. Honor supplied context, references, output specifications, and technical constraints. State assumptions; ask only when an answer materially changes the work. Textual style needs no reference; inspect an explicitly supplied or known-gallery image before relying on it, and never fetch one automatically.

## Operating boundaries

Read [operating boundaries](../blender-setup/references/operating-boundaries.md) before execution.

## Visual direction

Use a supplied or prepared target only when pose and visual style are part of the animation brief. It guides silhouette and staging, not motion correctness, topology, or export compatibility; validate those independently.

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
