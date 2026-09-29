# blender-visual-feedback Specification

## Purpose

Improve reusable Blender skill decisions through inspected reference feedback, traceable fresh-scene trials, and style-preserving transfer checks.

## Requirements

### Requirement: Reference feedback preserves requested intent
The workflow SHALL inspect supplied targets and record relevant visual cues separately from the original prompt, preserving its subject, daylight, camera intent, and deliverables unless the user changes them.

#### Scenario: Targets include conflicting styles
- **WHEN** photographic daytime, dusk, and isolated dramatic targets are supplied for a daytime architectural scene
- **THEN** the brief identifies transferable quality cues without silently changing the requested scene to dusk or adding unrelated subjects.

### Requirement: Five traceable fresh builds
The workflow SHALL produce five new example 02 scenes from empty owned scenes, preserving original outputs and each attempt's editable source, clean render, genuine editor screenshot, settings, timings, construction source, and skill revision provenance.

#### Scenario: A new attempt starts
- **WHEN** the preceding attempt has been reviewed
- **THEN** the next attempt reconstructs its scene from zero using the current guidance, without reopening or incrementally modifying the previous scene, and records the empty starting state.

#### Scenario: Screenshot unavailable
- **WHEN** the editor cannot supply a genuine usable screenshot
- **THEN** the workflow reports the missing evidence and does not substitute a render or fabricated UI image.

### Requirement: Evidence-led reusable skill changes
After each attempt the workflow SHALL inspect its actual render and update one or more canonical skills with a lesson supported by observed behavior. Changes SHALL preserve non-realistic styles and avoid universal architectural or firehouse-specific prescriptions.

#### Scenario: Glazing looks like an opaque painted panel
- **WHEN** image inspection reveals missing depth or believable reflection
- **THEN** the recorded lesson addresses relevant geometry, material, and environment conditions, and the next attempt tests that guidance rather than merely raising samples.

### Requirement: Quality and runtime are reported independently
The workflow SHALL distinguish technical validity from visual acceptance and measure render time separately from scene construction. Final stills SHALL be 1280x720, previews 640x360, with under 30 seconds a target rather than a hard failure threshold.

#### Scenario: Fast output remains visibly synthetic
- **WHEN** a render meets file and time checks but misses the reference quality
- **THEN** its review records the visual shortcomings and does not call it photorealistic solely because validation passed.

### Requirement: Transfer and package consistency
The final guidance SHALL be exercised on a small realistic non-architectural prop and a stylized subject, and canonical skills SHALL synchronize to both supported client packages with validation.

#### Scenario: Realism guidance is used for a stylized subject
- **WHEN** the requested style intentionally simplifies materials and forms
- **THEN** the workflow preserves that intent and checks readability instead of forcing photographic noise, weathering, or camera choices.

### Requirement: Reviewable final selection
The workflow SHALL provide a comparative report linking all five attempts and their lessons, promote the best inspected compliant attempt to main example outputs, and preserve baseline and rejected attempts without automatically approving the existing gallery milestone or committing changes.

#### Scenario: Latest attempt regresses
- **WHEN** an earlier attempt better satisfies the brief
- **THEN** the earlier attempt may be selected with an explicit rationale and all attempts remain available for human review.
