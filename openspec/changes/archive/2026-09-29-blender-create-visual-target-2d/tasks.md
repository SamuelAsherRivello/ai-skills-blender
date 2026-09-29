# Tasks

## 1. Skill and handoff

- [x] 1.1 Create skills/blender-create-visual-target-2d/SKILL.md with the ten-step workflow, capability discovery, supplied-image and prompt-only paths, versioned artifact contract, and inspiration-only boundary; verify it against the spec scenarios and skill-creator validation.
- [x] 1.2 Add Codex UI metadata with display name "Blender Create Visual Target 2D" and concise supporting references only where needed for the package contract; verify metadata and all resource links are portable within the installed skill.
- [x] 1.3 Add default parallel target handoff guidance to all twelve 3D skills and stable comparison/correction guidance; statically verify one worker per top-level task, immediate main progress, nested reuse, scoped edits, explicit opt-outs, capability fallbacks and convert-2d-3d's separate reconstruction purpose.

## 2. Catalog and packaging

- [x] 2.1 Update the catalog validator for fourteen skills and current README badge/count/table/example plus relevant input and acceptance documentation; verify there are no stale current catalog claims while preserving historical records and README formatting.
- [x] 2.2 Generate both client packages with scripts/sync-client-skills.py; run canonical, Codex and Claude validators and the synchronization check successfully.

## 3. Behavioral acceptance

- [x] 3.1 Run supplied-image mode on the user's firehouse PNG, preserve it under example 02 input/visual-targets/ with its prompt status, brief and manifest; verify image hash/dimensions, inspected cues and honest unknown provenance.
- [x] 3.2 Run one live generated stylized-subject target through an available image tool into ignored acceptance storage; inspect the image and verify exact prompt, actual dimensions, style, status and known tool metadata are recorded.
- [x] 3.3 Exercise the missing-generator/no-image scenario without changing configured providers; verify the output is explicitly prompt-only with no fabricated image or completion claim, and document which client paths were tested live versus statically.
- [x] 3.4 Compare the supplied target with the existing example 02 Blender render in output/target-comparison.md; inspect both images, identify actionable gaps, label provenance, and verify existing render/blend hashes are unchanged.
- [x] 3.5 Record acceptance results and limitations, rerun affected validation, and strictly validate this OpenSpec change; verify no unrelated milestone approval, scene rebuild, commit or push occurred.
