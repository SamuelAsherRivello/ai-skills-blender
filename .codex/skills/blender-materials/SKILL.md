---
name: blender-materials
description: Create and tune Blender materials and shader nodes for requested surfaces or render styles.
---

# blender-materials

## Inputs and scope

Accept target objects, surface/style, physical scale and render engine; use neutral comparison lighting. Honor supplied context, references, output specifications, and technical constraints. State assumptions; ask only when an answer materially changes the work. Textual style needs no reference; inspect an explicitly supplied or known-gallery image before relying on it, and never fetch one automatically.

## Operating boundaries

Read [operating boundaries](../blender-setup/references/operating-boundaries.md) before execution.

## Visual direction

For a style-led material task, use one supplied or prepared visual target to assess only authorized surface changes. Reuse it across nested work and inspect genuine material previews. Do not create a concept target for a color-space, missing-path, or export-compatibility repair.

## Workflow

1. Verify readiness and identify the requested surface and target engine.
2. Inspect existing materials and make unique copies when shared users must not change.
3. Set a neutral comparison view with stable exposure.
4. Establish base color, roughness, metallic/transmission response before adding detail.
5. Load available textures with correct color spaces: color inputs versus Non-Color data maps.
6. Set texture scale and restrained bump/normal strength in scene units. Inspect every visible face for stretched or rotated mapping. Separate broad color variation, material grain, and joints; avoid making all three the same noise scale or adding large cloudy patches to otherwise uniform surfaces.
7. Name and organize nodes; keep important controls editable.
8. Compare the material under neutral and intended production lighting. For glass, inspect the whole optical setup: real opening, surface thickness, plausible interior/backing, and something meaningful to reflect. Do not compensate for an opaque backing or empty environment by tinting glass or making it metallic.
9. Check missing paths, packed assets when needed, material slots, shader cost and export compatibility.
10. Save the material/source and inspected comparison renders with limitations.

## Execution notes

Do not label a material physically accurate solely from a pleasing render. Avoid metallic response on ordinary dielectrics. Shader-to-RGB/outline techniques can be engine-specific; verify the selected engine and downstream export.

For worn realistic surfaces, tie variation to a cause: rain paths below ledges, handling at grips, contact near a base, or grain following manufacture. Keep the underlying material readable. Uniform dirt and random noise across every surface can make a scene less plausible; clean, stylized, and diagrammatic requests may need none.

## Delivery and evidence

Provide editable source and requested outputs, relevant settings/seed/version, observed checks and remaining limitations. Inspect actual images for visual claims. File existence alone is not proof of quality. Prefer previews before expensive batches; do not overwrite unrelated files. Report unavailable downstream checks as unverified.
