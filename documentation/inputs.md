[Back to README.md](../README.md)

# Request conventions

Commands accept natural language. Subject and render style are useful for creation; the current scene is a valid subject for rendering, review, animation or export.

Optional inputs: deliverable, setting, action/pose, composition, camera, lighting/mood, palette, user-provided references, output specifications, and technical constraints.

State reasonable defaults before execution; ask only when ambiguity changes the result materially. Do not require every field.

Example: `$blender-create-model A boy getting ready for school, comic-book style.`
A reasonable brief is a stylized posed character with a backpack, editable source, and modest preview. State inferred age/proportions, pose and material treatment; clarify if the intended deliverable could change the modeling approach substantially. This example is not a built-in asset generator.

Example: `$blender-render Render the current scene.`
Reuse the existing usable camera/output settings, select a bounded preview, inspect it, and render the requested final. No new subject or PNG is required.

Text-only comic-book style can use strong silhouettes, grouped tones, restrained palette and deliberate outlines appropriate to the chosen engine. Never claim a gallery image was inspected when none exists.

## Automatic parallel visual targets

Every new 3D task launches one subagent using `$blender-create-visual-target-2d` (or `/blender-create-visual-target-2d` in Claude) with the exact prompt, subject, style, camera, lighting and relevant references. Main Blender work starts immediately; nested skills share the same target job. When the target arrives, compare a genuine preview, make authorized corrections and inspect again. You can also call the skill directly for a target-only request. An available image tool is needed only for new generation; a supplied target can be interpreted without it or Blender. Without either, the result is explicitly prompt-only.

The versioned package contains an image when available, prompt.txt, brief.md and manifest.json. In examples it lives under input/visual-targets/. Keep actual Blender renders in output/ and freeze the target version for a build/review cycle. This is inspiration and comparison; image reconstruction remains the separate blender-convert-2d-3d workflow.

The target worker owns only its assigned target directory; the parent alone mutates Blender. Preserve existing-scene features outside the requested change. Export/render/audit tasks still receive appearance direction without authorization to redesign the scene. Use up to two focused correction passes by default, or the user's stated budget. Pure connection diagnostics are excluded and explicit opt-outs are respected. If delegation is unavailable, report serial target preparation; if no image can be obtained, report prompt-only evidence rather than imply a completed visual comparison.
