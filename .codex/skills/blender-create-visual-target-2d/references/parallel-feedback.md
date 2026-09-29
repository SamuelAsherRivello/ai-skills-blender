# Parallel target and 3D feedback

At the start of each top-level 3D task, the parent launches one target worker using this skill. This includes modeling, scene creation, materials, UV/baking, lighting, rendering, rigging/animation, procedural work, export, optimization and dimensional conversions. Pure connection diagnostics, documentation and skill maintenance are not 3D tasks. An explicit user opt-out overrides the default.

## Dispatch without blocking construction

Give the worker the exact user request, subject/style, output constraints, requested changes, parts that must remain unchanged, relevant supplied references or an existing-scene preview, and an exclusive target output directory. Include a task ID and the instruction that it is the target worker. Use the harness's available delegation mechanism; do not assume a particular tool name exists in both clients.

The worker generates a prompt-specific target, or prepares the supplied target when the user has already chosen one. Generic gallery sheets may supplement it but do not replace the prompt-specific brief. For an existing asset, preserve its identity, layout, proportions and unrequested features; generation must depict only the authorized change. An export-only task uses an appearance-preservation target, not a redesign. Animation/sprite targets express the requested pose, silhouette and style; they do not prove motion, topology, export compatibility or hidden geometry.

The parent immediately continues authorized Blender readiness checks, inspection, setup and construction. Do not wait for image generation before starting independent 3D work. Only the parent mutates the shared Blender session or scene/output files. The worker writes only its assigned target package and never calls Blender mutation tools, edits skills or spawns another target worker.

Carry the task ID, worker ID and target package path through nested skill calls. Reuse a pending or completed target job for the same task; invoking materials then render must not create duplicate workers. Launch a new job only for a new top-level task or a materially revised user brief, and record that revision.

## Return contract

The worker returns task/target IDs, package paths, readiness status, actual inspected image, prioritized visual cues, reference conflicts, assumptions and limitations. Publish the final manifest only after its referenced files are fully written; the parent reads the package after a completion message rather than inspecting partially written files. Missing-image and needs-revision outcomes must be explicit.

If the worker lacks an image tool but the parent has one, return the exact prompt for parent-side generation; this is a capability fallback, not proof that generation is unavailable everywhere. If delegation is unavailable, the parent executes target preparation itself and reports that it was not parallel. If neither can generate or inspect an existing target, continue authorized 3D work with a prompt-only brief and state that image comparison was unavailable. Do not install providers or invent a worker/result to satisfy the default.

## Incorporate, compare, correct

When the target completes, the parent inspects its pixels and brief, reconciles any conflict with the user's request, and freezes that target version. Compare a genuine current Blender preview at a useful matching view. Rank the largest visible differences in form, proportion, materials, lighting, composition and relevant pose; distinguish plausible causes from proven ones.

Apply in-scope corrections and inspect a new preview against the same target. Use the requested iteration budget; otherwise perform up to two focused correction passes, stopping earlier if no meaningful in-scope gap remains. Report remaining gaps instead of claiming fidelity or silently changing the target. For audit-only, render-only or export-only requests, do not redesign or modify unauthorized scene properties: report out-of-scope findings and retain the task's technical checks.

Complete the comparison before declaring visual work finished when the target is available. If target generation fails or remains unavailable within the task's practical budget, disclose that limitation and deliver actual work/evidence without claiming a comparison. A target is an additional source of direction, never a replacement for the user's brief, geometric validation, animation checks or real Blender renders.
