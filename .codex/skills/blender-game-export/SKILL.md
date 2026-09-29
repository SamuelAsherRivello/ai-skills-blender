---
name: blender-game-export
description: Export Blender assets for a specified game engine with scale, pivot, material and animation checks.
---

# blender-game-export

## Inputs and scope

Accept target engine, format and budgets; ask when target differences materially affect output. Also accept optional setting, action/pose, composition, camera, lighting/mood, palette, user references, output specifications and technical constraints when relevant. State assumptions; ask only when a missing answer materially changes the work. A textual style works without reference images. The shared render-style gallery is optional: use an explicitly supplied path or known checkout, inspect a chosen PNG before drawing conclusions, and never fetch missing images automatically.

Use the separately configured official Blender Lab MCP connection. Discover its tools and confirm read-only scene access before mutations; report a connection blocker instead of switching servers. Preserve unrelated objects and settings, scope new content by named collection/run, and checkpoint before destructive edits. Repeated scripts must replace only owned output or create a separate named run. Do not start paid services without authorization.

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
10. Deliver source/export files and separate structural verification from unavailable engine checks.

## Execution notes

GLB is a useful default only when the destination accepts glTF. Blender procedural shaders may need baking. Do not claim collision/LOD naming is engine-compatible without checking that engine's importer.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.


For glTF in a multi-scene file, use both selected-object and active-scene export scoping; verify the reimported object set. Parent skinned meshes to their armature while preserving world transforms before exporting, and review the exporter warnings.

Compare animation duration in seconds as well as clip names: reimport into a different scene FPS can change frame numbers while preserving timing. Distinguish imported scene meshes from auxiliary bone display shapes. Normalize the intended skinned-mesh origin to the rig root before export if the destination bakes mesh transforms.
