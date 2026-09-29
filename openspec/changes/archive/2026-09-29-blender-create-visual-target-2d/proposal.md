# Proposal

## Why

The firehouse iterations improved the Blender result but lacked a single, coherent visual target. The user's generated firehouse image demonstrates how concept imagery can establish composition, material response, detail hierarchy and atmosphere before construction, while remaining separate from evidence of actual 3D output.

## What Changes

- Add **Blender Create Visual Target 2D** (`blender-create-visual-target-2d`) as a default parallel, directly callable fourteenth skill, packaged for Codex and Claude Code.
- Turn subject, style, setting, camera, lighting, palette and output constraints into one inspected image target and a concise 3D interpretation brief. Support a user-supplied target as well as generation through an available authorized image tool.
- Detect actual image-generation capability at runtime; do not assume an AI harness or language model can generate images. When unavailable, deliver a ready-to-use prompt with an explicit missing-image status or analyze a supplied image.
- Record the exact generation prompt, known provenance, actual image dimensions, reference inputs and target version. Preserve targets between iterations rather than silently replacing the comparison baseline.
- Start one prompt-specific target subagent per top-level 3D task while Blender work continues. Nested skills share that worker. Inspect the completed target and use a bounded comparison-and-correction loop, respecting explicit opt-outs and reporting unavailable capabilities. Use targets purely for inspiration and comparison; do not substitute them for Blender renders, create billboards, project textures, or reconstruct meshes through this skill.
- Integrate the new catalog entry, metadata, documentation, client packages and validator count. Validate supplied-image, live-generation, missing-tool and downstream-comparison paths.

## Capabilities

### New Capabilities

- `blender-visual-target-2d`: Generate or interpret a traceable 2D target and hand off style-aware visual criteria for genuine Blender construction and comparison.

### Modified Capabilities

None. No archived main specs exist; related in-flight changes remain separate.

## Impact

New canonical skill and UI metadata; generated `.codex/skills/` and `.claude/skills/` packages; parallel target and feedback guidance in all twelve 3D skills; README and relevant input/acceptance documentation; catalog validator updates. Target generation requires no live Blender connection and adds no image provider, MCP server, paid service, or automatic installation. The supplied firehouse target can be captured under example 02 inputs and compared against its existing render without replacing its 3D output. No commit, push, or gallery milestone approval is included.
