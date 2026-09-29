---
name: blender-materials
description: Create and tune Blender materials and shader nodes for requested surfaces or render styles.
---

# blender-materials

## Inputs and scope

Accept target objects, surface/style, physical scale and render engine; use neutral comparison lighting. Also accept optional setting, action/pose, composition, camera, lighting/mood, palette, user references, output specifications and technical constraints when relevant. State assumptions; ask only when a missing answer materially changes the work. A textual style works without reference images. The shared render-style gallery is optional: use an explicitly supplied path or known checkout, inspect a chosen PNG before drawing conclusions, and never fetch missing images automatically.

Use the separately configured official Blender Lab MCP connection. Discover its tools and confirm read-only scene access before mutations; report a connection blocker instead of switching servers. Preserve unrelated objects and settings, scope new content by named collection/run, and checkpoint before destructive edits. Repeated scripts must replace only owned output or create a separate named run. Do not start paid services without authorization.

## Workflow

1. Verify readiness and identify the requested surface and target engine.
2. Inspect existing materials and make unique copies when shared users must not change.
3. Set a neutral comparison view with stable exposure.
4. Establish base color, roughness, metallic/transmission response before adding detail.
5. Load available textures with correct color spaces: color inputs versus Non-Color data maps.
6. Set texture scale and restrained bump/normal strength in scene units.
7. Name and organize nodes; keep important controls editable.
8. Compare the material under neutral and intended production lighting.
9. Check missing paths, packed assets when needed, material slots, shader cost and export compatibility.
10. Save the material/source and inspected comparison renders with limitations.

## Execution notes

Do not label a material physically accurate solely from a pleasing render. Avoid metallic response on ordinary dielectrics. Shader-to-RGB/outline techniques can be engine-specific; verify the selected engine and downstream export.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.
