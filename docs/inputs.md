# Request conventions

Commands accept natural language. Subject and render style are useful for creation; the current scene is a valid subject for rendering, review, animation or export.

Optional inputs: deliverable, setting, action/pose, composition, camera, lighting/mood, palette, user-provided references, output specifications, and technical constraints.

State reasonable defaults before execution; ask only when ambiguity changes the result materially. Do not require every field.

Example: `$blender-create-model A boy getting ready for school, comic-book style.`
A reasonable brief is a stylized posed character with a backpack, editable source, and modest preview. State inferred age/proportions, pose and material treatment; clarify if the intended deliverable could change the modeling approach substantially. This example is not a built-in asset generator.

Example: `$blender-render Render the current scene.`
Reuse the existing usable camera/output settings, select a bounded preview, inspect it, and render the requested final. No new subject or PNG is required.

Text-only comic-book style can use strong silhouettes, grouped tones, restrained palette and deliberate outlines appropriate to the chosen engine. Never claim a gallery image was inspected when none exists.
