# Design

## Context

See proposal.md for motivation. Canonical sources live in skills/ and are copied into Codex and Claude packages by scripts/sync-client-skills.py. The validator explicitly enumerates thirteen skills and requires ten chronological workflow steps. Existing create-model, create-environment and review-optimize already accept references. Convert-2d-3d reconstructs from imagery and must retain its separate purpose.

The supplied target was visually inspected: clear building hierarchy, layered trim, varied brick, reflective glazing, human-scale street furniture, foliage, background depth and plausible daylight. Its richness provides useful direction, but inferred dimensions, hidden geometry, signage and exact construction are not authoritative. The target's original generation prompt and model metadata have not been supplied.

## Goals / Non-Goals

**Goals:** Make a visual target a portable, prompt-specific parallel input for any supported subject/style; preserve intent, provenance and comparison integrity; work with available capabilities in either harness.

**Non-Goals:** Image-to-mesh automation, generating final Blender render evidence, texture projection, installing providers, rebuilding example 02, making image generation mandatory, or promising photographic parity within a fixed render budget.

## Decisions

### Capability-based execution

Keep one provider-neutral canonical skill. Discover the session's image-generation tools and applicable provider instructions at execution time; use an already available authorized tool. Do not hard-code a model name, assume Claude or Codex itself produces raster images, or add credential management. An existing image can be analyzed without any generator or Blender connection. Missing generation capability produces a useful prompt and explicit prompt-only status. This is more portable than embedding a new image API client.

### Ten-step workflow

1. Read subject, intended 3D use and supplied images; identify generation versus supplied-target mode.
2. Establish requested style, setting, pose/action, camera, lighting, palette, aspect ratio and constraints; use reasonable stated defaults for omissions.
3. Inspect supplied references and distinguish required content from inspiration; preserve the textual brief when an image conflicts with it.
4. Discover usable image-generation capability or select the supplied-image/prompt-only path; no Blender setup prerequisite at this stage.
5. Compose and save the exact prompt, including framing, essential forms and explicit exclusions that matter to the brief.
6. Generate one target by default, or preserve the supplied target; use requested variants/revisions only and retain prior versions. Do not silently crop or relabel unsupported resolution output.
7. Inspect actual image pixels for subject completeness, style, framing and obvious contradictions. Record defects; no unbounded regeneration loop. An unusable result is reported as needing revision.
8. Write a concise 3D interpretation brief: primary/secondary forms, relative proportions, material families, lighting/composition cues, prioritized visible details, unknowns and simplifications needed for the user's budget.
9. Package the image, prompt and provenance with a stable target ID and explicit readiness status; hand off the chosen target to relevant modeling/environment skills when further work is authorized.
10. When a genuine Blender render is available, compare it against the same target version and requested brief, report visible gaps, and route them to the appropriate skill. Otherwise deliver the handoff without claiming a comparison or starting unrequested 3D work.

Every top-level 3D task starts one target subagent while the parent continues Blender work immediately; nested skills reuse it. The worker owns only its target directory and never modifies Blender or recursively delegates. On completion the parent inspects a genuine preview against the same target version, fixes in-scope gaps and rechecks, using the requested budget or up to two focused correction passes. Preserve existing asset identity and render/export/audit-only scope. Setup-only work and explicit opt-outs bypass this default. Missing delegation uses disclosed parent-side preparation; unavailable generation uses a supplied target or an explicit prompt-only fallback. Worker-only tool absence is not evidence of parent-side absence. This adds no approval gate. A request only for a target ends with the target; a request for target plus 3D construction can continue within that authorization. Explicit user review preferences remain controlling.

### Artifacts and provenance

Standalone default: visual-targets/target-01/. Inside an existing numbered example: input/visual-targets/target-01/. Use the next available ID for a new revision rather than replacing prior files.

- target.png, or target with its actual supported extension: an inspected generated or supplied image; absent in prompt-only mode.
- prompt.txt: exact submitted prompt for new generation, or the current interpretation brief with the original generation prompt marked unknown for supplied imagery.
- brief.md: concise 3D visual criteria and limitations, including reference conflicts and inferred details.
- manifest.json: target ID, generated/supplied/prompt-only mode, ready/needs-revision/missing-image status, relative artifact paths, image hash and actual dimensions when present, known tool/provider/model metadata (unknown when unavailable), requested versus actual aspect/resolution, reference origins and relationship to any prior target. Never invent seed/model details or reproducibility guarantees.

Targets remain concept inputs. Actual Blender sources and renders remain under output/. Comparisons link both sides with explicit labels; the generated image never occupies result.png or editor.png. Freeze the target during a build/review cycle; a new target version changes the comparison baseline and must be disclosed.

### Integration and packaging

Add the default parallel handoff and comparison loop to every 3D skill. Keep target generation capability-aware and report fallbacks honestly. Mention convert-2d-3d by name only to explain its different reconstruction purpose; avoid nonportable links outside an installed skill folder.

Use display name **Blender Create Visual Target 2D** and command slug `blender-create-visual-target-2d`. Keep dimensional suffixes at the end of this command. Add Codex agents/openai.yaml metadata, preserve normal implicit discovery, and use the existing sync mechanism for both client copies. Update the validator's catalog and count message plus README count/badge, skill table (Call Directly: Yes), a concise invocation example and relevant docs. The new skill's optional image tool dependency must be clear without making it a prerequisite for all existing skills. Historical acceptance records remain historical.

### Acceptance exercise

During apply, preserve the supplied PNG from C:/Users/srive/.codex/generated_images/01a0ed37-0eb0-7c30-816a-e6d51ad62c68/exec-27dedaf0-73aa-4747-bc98-43fc879eaa45.png as a versioned example 02 input. Record its original generation metadata as unknown except for the user's report that Codex generated it. Compare it with the existing example 02 render in an explicitly labeled report without modifying that render or scene.

Exercise new generation separately with one small target for a stylized subject using an available image tool; store temporary evidence under ignored .acceptance/. Inspect and record the actual output. Exercise missing-tool behavior through a bounded manual scenario that checks the prompt-only output contract without disabling configured tools. Validate both client packages statically; do not claim a live Claude execution if only Codex was available. No full new Blender build or gallery milestone advancement is required.

## Risks / Trade-offs

- Attractive imagery can depict impossible or ambiguous construction -> record inferred geometry and prioritize user requirements over invented detail.
- Target may exceed practical 3D budgets -> identify achievable priorities and remaining gaps; do not lower the target silently or guarantee a match.
- Generator lacks requested size/aspect/metadata -> record actual outputs and unknowns; preserve the image rather than claim unsupported controls.
- Model/provider capabilities differ by client -> discover tools at runtime and test the missing-tool path; package availability is not live-provider verification.
- Target regeneration can disguise a weak Blender result -> version and freeze targets during comparisons.

## Migration Plan

Add the canonical skill and targeted integration text, update current catalog documentation/validation, generate both client packages, then run acceptance and validators. Preserve existing uncommitted work, example outputs, reference directories and OpenSpec milestones. Rollback removes the added skill/catalog entry and scoped handoff text while leaving prior outputs intact. No publishing action is included.
