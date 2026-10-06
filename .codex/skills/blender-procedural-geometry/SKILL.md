---
name: blender-procedural-geometry
description: Create editable Geometry Nodes or Python generators in Blender with controlled parameters and reproducible output.
---

# blender-procedural-geometry

## Inputs and scope

Accept output geometry, exposed controls and ranges; choose Geometry Nodes for artist editing or Python for batch structure. Honor supplied context, references, output specifications, and technical constraints. State assumptions; ask only when an answer materially changes the work. Textual style needs no reference; inspect an explicitly supplied or known-gallery image before relying on it, and never fetch one automatically.

## Operating boundaries

Read [operating boundaries](../blender-setup/references/operating-boundaries.md) before execution.

## Visual direction

For a generator whose requested look matters, use a single target or supplied reference to check representative output at the intended camera. Do not use target generation to distract from parameter, topology, repeatability, or performance validation.

## Workflow

1. Verify readiness and define the generated geometry contract.
2. Choose named parameters, units, safe ranges and output-size limits.
3. Select Geometry Nodes or Python based on editability and dependencies.
4. Prototype the simplest valid output inside an owned collection.
5. Expose useful controls and document interactions rather than every internal constant.
6. Make randomness explicit and record a seed.
7. Exercise minimum, normal and maximum supported inputs; reject invalid counts before allocating objects.
8. Inspect topology, evaluated bounds, instance realization and execution cost. Inspect the generated result at the actual camera too: valid parameter ranges can still produce repetitive silhouettes, intersecting assemblies, or detail below the pixel scale. Keep construction rules separate from style choices so reusable generators do not impose one visual treatment.
9. Rerun with the same parameters; replace only owned output or create a distinct named run, never accumulate accidental duplicates.
10. Deliver the editable node group/script, parameter examples, seed and validation results.

## Execution notes

Test zero/one counts if supported, negative dimensions, and very large requested counts. Preserve node sockets by identifiers where practical; inspect the installed Blender API before constructing version-sensitive nodes.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.
