---
name: blender-game-export
description: Export Blender assets for a specified game engine with scale, pivot, material and animation checks.
---

# blender-game-export

## Inputs and scope

Accept target engine, format and budgets; ask when target differences materially affect output. Honor supplied context, references, output specifications, and technical constraints. State assumptions; ask only when an answer materially changes the work. Textual style needs no reference; inspect an explicitly supplied or known-gallery image before relying on it, and never fetch one automatically.

## Operating boundaries

Read [operating boundaries](../blender-setup/references/operating-boundaries.md) before execution.

## Appearance preservation

An export preserves the approved source appearance; do not launch visual-target work or redesign assets for an export-only request. If the user requests an appearance change as part of export preparation, handle and verify that change as a separately scoped visual task.

## Workflow

1. Verify readiness and choose the destination engine/format.
2. Inspect source geometry, transforms, materials and actions.
3. Set budgets from actual target constraints rather than universal polygon limits.
4. Create an export copy or isolate selection; preserve editable source.
5. Normalize units, orientation, pivots and transforms intentionally.
6. Adapt materials and texture channels to supported target features.
7. Prepare requested clips, collision proxies and LODs with explicit naming.
8. Export only scoped content to a fresh output path.
9. Reimport into an isolated collection/scene; compare size, pivot, materials and clips, then test target engine if available.
10. Deliver source/export files and separate structural verification from unavailable engine checks. For repository examples, follow the linked model-delivery contract; game-engine files do not replace the required browser GLB.

## Execution notes

GLB is a useful default only when the destination accepts glTF. Blender procedural shaders may need baking. Do not claim collision/LOD naming is engine-compatible without checking that engine's importer.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.


For glTF in a multi-scene file, use both selected-object and active-scene export scoping; verify the reimported object set. Parent skinned meshes to their armature while preserving world transforms before exporting, and review the exporter warnings.

Compare animation duration in seconds as well as clip names: reimport into a different scene FPS can change frame numbers while preserving timing. Distinguish imported scene meshes from auxiliary bone display shapes. Normalize the intended skinned-mesh origin to the rig root before export if the destination bakes mesh transforms.
