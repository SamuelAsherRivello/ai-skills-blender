---
name: blender-review-optimize
description: Audit and optimize Blender asset cost while measuring appearance and downstream behavior.
---

# blender-review-optimize

## Inputs and scope

Accept target collection, budget and permitted changes; default to audit before edits. Honor supplied context, references, output specifications, and technical constraints. State assumptions; ask only when an answer materially changes the work. Textual style needs no reference; inspect an explicitly supplied or known-gallery image before relying on it, and never fetch one automatically.

## Operating boundaries

Read [operating boundaries](../blender-setup/references/operating-boundaries.md) before execution.

## Appearance preservation

Audit and optimization do not authorize redesign. Compare existing baselines or supplied references when visual fidelity is in scope; do not create a concept target unless the user specifically includes a visual revision.

## Workflow

1. Verify readiness and define scoped assets and optimization goals.
2. Capture baseline views and measured counts using the same camera/settings.
3. Audit evaluated geometry, materials, image sizes, modifiers and animation.
4. Rank findings by measured impact and visible risk. Separate technical validity, requested style fidelity, and runtime: a fast valid render can still miss the brief. Inspect the full image and a few final-resolution details, then fix the largest visible mismatch before adding samples or geometry indiscriminately.
5. Checkpoint the source before destructive optimization.
6. Apply focused fixes to the owned scope; preserve silhouette and deformation where required.
7. Remeasure using the baseline method.
8. Compare before/after renders at intended display size. Record which visible mismatch improved, stayed unchanged, or regressed; higher object counts are not evidence of better results. If small detail produces little improvement, revisit primary/secondary form and composition rather than continuing the same detail pass.
9. Check affected exports, modifiers and animation for regressions.
10. Deliver source, before/after measurements, visual evidence and unresolved findings. When feedback changes reusable guidance, state the supporting observation and its scope; test a different subject or style when practical. One improved example does not demonstrate general success, and architectural realism lessons must not erase intentional stylization.

## Execution notes


Use [scripts/audit_scene.py](scripts/audit_scene.py) inside Blender for selected-object counts; pass objects explicitly to audit(). Evaluated geometry can be much larger than base geometry. Texture memory estimates are estimates, not GPU profiler measurements.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.
