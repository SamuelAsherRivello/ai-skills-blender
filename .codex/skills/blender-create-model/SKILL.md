---
name: blender-create-model
description: Create or refine a Blender mesh from a subject and dimensions; use for individual props or characters, not whole environment assembly.
---

# blender-create-model

## Inputs and scope

Accept subject, scale, silhouette, intended use; default to editable source plus preview. Honor supplied context, references, output specifications, and technical constraints. State assumptions; ask only when an answer materially changes the work. Textual style needs no reference; inspect an explicitly supplied or known-gallery image before relying on it, and never fetch one automatically.

## Operating boundaries

Read [operating boundaries](../blender-setup/references/operating-boundaries.md) before execution.

## Visual direction

For a new or restyled model with visual direction, prepare one target with `blender-create-visual-target-2d`. Reuse it across nested work, compare genuine previews against the frozen target, and correct only authorized visible gaps. Do not require a target for topology, dimension, repair, or export-only work.

## Workflow

1. Establish official MCP readiness and turn the subject/style into a brief; identify what already exists.
2. Choose units, dimensions and proportion landmarks before detail.
3. Create a named task collection; record existing objects and checkpoint before replacing geometry.
4. Block out primary masses with primitives or a low-resolution mesh.
5. Inspect front, side and three-quarter views; resolve proportion errors before topology detail. For a grounded pose or placed prop, verify the actual lowest visible contact against its support surface; nominal centers or bounding boxes can leave rounded feet or bases floating. Preserve intentional hovering or airborne poses.
6. Refine silhouette and secondary forms; choose modifiers for editable construction.
7. Add only detail visible at the intended viewing distance; separate reusable parts. Check how secondary forms meet: supports, frames, trim, and accessories must not accidentally cross openings or conceal defining features. For containers and enclosed props, inspect the end panels, interior walls, lid closure and all sides after assembly; a hero angle can hide missing surfaces. Judge thickness and contact at final image size, not only in a close viewport.
8. Check normals, accidental internal faces, transforms and topology appropriate to deformation/export. Ngons are not universally invalid.
9. Render modest final views and inspect them against the brief at intended display size.
10. Save the editable blend and provide object names, dimensions, previews and unresolved limitations.

## Execution notes


Prefer scale-aware bevels and intentional shading. For characters, establish facial/body landmarks and pose requirements before adding accessories. A render-ready static model is not automatically animation-ready.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.
