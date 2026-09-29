# Blender Visual Target 2D

## Purpose

Provide traceable AI-generated or supplied visual targets that guide genuine Blender construction and style-aware comparison without misrepresenting concept imagery as 3D output.

## Requirements

### Requirement: Target creation preserves intent
The skill SHALL accept a subject and optional style, setting, pose, camera, lighting, palette, reference images and output constraints. It SHALL preserve explicit user choices and support explicit opt-outs and capability-aware fallbacks.

#### Scenario: Stylized subject requested
- **WHEN** a user requests a comic-book character target
- **THEN** the prompt and visual criteria preserve that style rather than imposing architectural realism or photographic weathering.

#### Scenario: Reference conflicts with the brief
- **WHEN** a target depicts dusk but the requested scene is daytime
- **THEN** the brief identifies the conflict and preserves the requested daytime intent.

### Requirement: Capability-aware generation and fallback
The skill SHALL use an available authorized image-generation tool or inspect a supplied image, without requiring Blender to be open. It SHALL NOT claim generation from the harness name alone or install providers as a side effect.

#### Scenario: Image tool available
- **WHEN** a new target is requested and a usable tool is exposed
- **THEN** the skill saves the submitted prompt, generates one target by default, and inspects the actual result.

#### Scenario: Image tool unavailable
- **WHEN** no usable generator or supplied image exists
- **THEN** the skill delivers a ready-to-use prompt and explicit missing-image status, without fabricated image paths or a claim of generation success.

#### Scenario: Supplied image available
- **WHEN** the user provides an accessible target image
- **THEN** the skill can inspect and package it without regenerating it, attributing known provenance and marking unknown generation details as unknown.

### Requirement: Reviewable target package
The skill SHALL deliver the actual image when available, exact submitted prompt or honest supplied-image prompt status, a 3D interpretation brief, and provenance identifying target version, actual dimensions and known generation details. It SHALL preserve previous target revisions.

#### Scenario: Provider does not expose requested settings
- **WHEN** image dimensions differ from the request or model/seed metadata is absent
- **THEN** the package records actual dimensions and unknown metadata rather than inventing values or claiming exact reproducibility.

#### Scenario: Image contradicts essential requirements
- **WHEN** inspection finds missing subject parts, wrong framing, or conflicting content
- **THEN** the brief records those defects and marks the target as needing revision instead of silently presenting it as ready.

### Requirement: Targets remain inspiration and comparison inputs
The skill SHALL describe observed forms, proportions, materials, composition and lighting separately from inferred hidden geometry. It SHALL NOT replace a Blender render, editor screenshot, mesh or texture with the target. Reconstruction remains a separately requested workflow.

#### Scenario: Target appears more realistic than Blender output
- **WHEN** the actual Blender render falls short of the target
- **THEN** the comparison reports the gaps using separately labeled images and retains the genuine Blender output.

#### Scenario: Target-only invocation
- **WHEN** the user requests only a visual target
- **THEN** the skill delivers its target and handoff brief without modifying Blender scenes or beginning unrequested reconstruction.

### Requirement: Stable comparison and authorized handoff
Every top-level 3D task SHALL start one prompt-specific target subagent while the parent continues Blender work immediately when delegation is available. Nested skills SHALL reuse that worker. Pure setup and explicit user opt-outs SHALL bypass the default. The worker SHALL NOT mutate Blender or recursively delegate. The parent SHALL inspect the completed target and actual preview, prioritize visible gaps, apply authorized corrections and recheck, using the requested iteration budget or up to two focused correction passes. Existing asset identity and render/export/audit-only scope SHALL be preserved. Missing delegation SHALL use disclosed parent-side preparation; unavailable generation SHALL use a supplied target or explicit prompt-only fallback. Failed or unfinished comparisons SHALL be reported honestly. Comparisons SHALL use an identified target version and actual inspected Blender imagery; changing the target SHALL be disclosed as a baseline change.

#### Scenario: Target plus 3D work authorized
- **WHEN** a user requests a target followed by a Blender scene
- **THEN** the workflow can continue into the relevant creation skills using the target's priorities without adding an automatic approval gate.

#### Scenario: No Blender render exists
- **WHEN** only the target has been created
- **THEN** the handoff describes intended comparison criteria without claiming the 3D result has been tested.

### Requirement: Consistent client catalog and bounded validation
The repository SHALL expose the fourteenth skill in canonical, Codex and Claude packages with matching behavior and documentation. Validation SHALL cover supplied-image, generation, missing-tool and comparison behavior, distinguishing live tests from static checks.

#### Scenario: Only one client tested live
- **WHEN** Codex exercises generation and Claude's package is only statically validated
- **THEN** the acceptance record reports that distinction and does not claim live Claude image-generation success.

#### Scenario: Target finishes during construction
- **WHEN** a target worker completes while the parent builds the scene
- **THEN** the parent inspects the target, compares an actual preview and corrects in-scope gaps without starting another target worker.

#### Scenario: Nested skills or unavailable delegation
- **WHEN** multiple skills participate in one task or the harness cannot delegate
- **THEN** nested skills share one target job, and missing delegation is disclosed with parent-side preparation rather than a claimed background worker.
