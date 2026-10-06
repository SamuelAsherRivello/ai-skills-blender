---
name: blender-create-visual-target-2d
description: Generate or interpret a prompt-specific 2D visual target and concise 3D direction brief for visual development or reference-led Blender work.
---

# Blender Create Visual Target 2D

Before launching a helper, mutating Blender, capturing editor pixels, or changing an example `.blend`, read [operating boundaries](../blender-setup/references/operating-boundaries.md). A target-only request neither requires Blender nor authorizes a Blender connection or mutation.

## Inputs and scope

Accept a subject or supplied target image, intended 3D use, and optional style, setting, pose/action, camera, lighting, palette, aspect ratio, resolution, references and budget. State reasonable defaults; clarify only material ambiguity. Use this skill when a visual direction brief or a comparison target would materially help; technical-only work does not need it.

For parallel work, read [references/parallel-feedback.md](references/parallel-feedback.md). A parent may delegate a target while it continues independent construction; nested skills reuse the same task/target. A worker neither changes Blender nor recursively delegates. A direct invocation runs once.

Use an image tool actually available in the current session and follow its provider instructions. Codex or Claude being the client does not establish image-generation capability. Do not install a provider, switch to an unconfigured API, acquire credentials or start a paid service as a fallback. A supplied image can be analyzed without generation; otherwise deliver an explicit prompt-only result when generation is unavailable.

Targets are concept inputs for inspiration and comparison. Preserve genuine Blender renders, editor screenshots, meshes and textures. This skill does not reconstruct geometry, make billboards or project the image onto a model; `blender-convert-2d-3d` handles separately requested reconstruction.

## Workflow

1. Read the subject, intended 3D use and available images. Select new generation, supplied-target interpretation, or an explicitly requested revision.
2. Establish style, setting, pose, framing, lighting, palette and output constraints. When camera is unspecified, choose a clear diagnostic view that exposes the subject's important forms; preserve intentional stylization.
3. Inspect any references. Separate required content from inspiration and identify conflicts with explicit user choices; the image does not silently override the requested subject, lighting or layout.
4. Discover an available authorized image tool and relevant usage instructions. If none exists, use a supplied target or deliver the prompt-only path with missing-image status. Do not invent a successful tool call.
5. Compose and save the exact generation prompt, including essential forms, requested style and complete subject framing. For supplied imagery, identify the current interpretation request and mark the original generation prompt unknown unless provided.
6. Generate one target by default, or preserve the supplied image. Retain previous revisions and follow the requested variant budget. Save a project-bound image inside the project; record actual size/format rather than silently cropping or claiming unsupported dimensions.
7. Inspect the actual image for complete subjects, pose, style, camera, material cues and contradictory or implausible details. Record essential mismatches as needs-revision. Do not enter an unbounded generation loop or equate aesthetic polish with geometric accuracy.
8. Write a concise 3D direction brief: primary and secondary forms, relative proportions, material families, light/camera cues, prioritized visible details, inferred hidden geometry and budget-sensitive simplifications. Distinguish observations from assumptions and avoid promising photographic parity.
9. Save a versioned target package following [references/target-package.md](references/target-package.md). Deliver its image, prompt, brief and manifest with explicit readiness status. As a worker, return to the parent with prioritized cues and limitations; do not enter Blender creation skills yourself. A direct target-only request ends with this handoff.
10. The parent folds the completed target into the current 3D task: inspect it beside a genuine preview, rank visible gaps, make authorized corrections and compare again using the same target version. Follow the bounded feedback loop in parallel-feedback.md. Without a genuine preview, return criteria without claiming a 3D evaluation.

## Handoff

Use `blender-create-model` for props/characters and `blender-create-environment` for scenes. A target defines priorities, not a measurement survey: keep dimensions and unseen geometry editable. During a build/review cycle, freeze the chosen target; disclose a new target version as a changed comparison baseline. Match pose/view where useful, but assess style and structure rather than demand pixel identity.

The target may contain extra signage, objects or visual errors. Carry forward only cues consistent with the request. Keep generated concept imagery out of result.png and editor.png destinations reserved for real Blender output. A comparative report can show both with explicit labels and original links.
