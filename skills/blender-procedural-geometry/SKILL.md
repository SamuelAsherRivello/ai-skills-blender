---
name: blender-procedural-geometry
description: Create editable Geometry Nodes or Python generators in Blender with controlled parameters and reproducible output.
---

# blender-procedural-geometry

## Inputs and scope

Accept output geometry, exposed controls and ranges; choose Geometry Nodes for artist editing or Python for batch structure. Also accept optional setting, action/pose, composition, camera, lighting/mood, palette, user references, output specifications and technical constraints when relevant. State assumptions; ask only when a missing answer materially changes the work. A textual style works without reference images. The shared render-style gallery is optional: use an explicitly supplied path or known checkout, inspect a chosen PNG before drawing conclusions, and never fetch missing images automatically.

Use the separately configured official Blender Lab MCP connection. Discover its tools and confirm read-only scene access before mutations; report a connection blocker instead of switching servers. Preserve unrelated objects and settings, scope new content by named collection/run, and checkpoint before destructive edits. Repeated scripts must replace only owned output or create a separate named run. Do not start paid services without authorization.

## Workflow

1. Verify readiness and define the generated geometry contract.
2. Choose named parameters, units, safe ranges and output-size limits.
3. Select Geometry Nodes or Python based on editability and dependencies.
4. Prototype the simplest valid output inside an owned collection.
5. Expose useful controls and document interactions rather than every internal constant.
6. Make randomness explicit and record a seed.
7. Exercise minimum, normal and maximum supported inputs; reject invalid counts before allocating objects.
8. Inspect topology, evaluated bounds, instance realization and execution cost.
9. Rerun with the same parameters; replace only owned output or create a distinct named run, never accumulate accidental duplicates.
10. Deliver the editable node group/script, parameter examples, seed and validation results.

## Execution notes

Test zero/one counts if supported, negative dimensions, and very large requested counts. Preserve node sockets by identifiers where practical; inspect the installed Blender API before constructing version-sensitive nodes.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.
