# Windows execution priority

## Browser model deliverables

When adding or changing any example `.blend`, maintain a matching self-contained
GLB alongside it and update `documentation/models/index.json`. Follow
`documentation/models/README.md` and the export/catalog scripts in `scripts/`.
Retain all source scenes, including historical variants. Embed required textures,
preserve applicable animation, and bake procedural surfaces when glTF cannot
represent them directly. Validate the GLB structure and inspect it in the browser;
file existence is not sufficient. Record export limitations in `.export.json`
and catalog warnings. Metadata must cite the actual source manifest/review/prompt;
do not invent missing fields or confuse AI visual-target metadata with model data.
Regenerate exports when source hashes change, commit the catalog with its assets,
and verify anonymous public HTTP access after publication. The independent Model
Viewer consumes these files remotely and must never bundle them in its releases.

## Process execution

1. Create no auxiliary command windows, including transient flashes. Prefer the existing MCP connection. Before any helper launch, establish no-console creation for the outer launcher and every descendant. If a required boundary is unknown or unsupported, do not launch it: report the operation as blocked and continue independent safe work. Never retry without suppression or open a terminal to work around a failure.
2. Keep existing Blender skills, setup adapters, helper scripts, and generated client rules consistent with this priority. Preserve captured diagnostics, bounded execution, and cleanup of owned processes. An absolute executable path, `cmd /c`, Blender `--background`, or hidden-window styling alone does not establish no-console execution. Do not hide, restore, focus, or close the user's existing Blender editor to satisfy this rule.

# Blender editor capture preference

Editor screenshots are authorized as part of requested Blender work. Check that Blender is running with a visible, non-minimized editor before capturing; maximization is not required. Both official full-window and area captures have returned black while minimized on this workstation, so minimized capture is not a verified capability. Report "Restore Blender from the taskbar" when this prerequisite fails. Read-only setup checks must not restore or focus windows themselves. Always inspect captured pixels; report capture failures honestly and never substitute a clean render or old screenshot for fresh editor evidence.

Before **every** Blender editor/window/area screenshot call, freshly check that the relevant Blender process has a visible, non-minimized editor window; do not reuse an earlier setup result. If Blender is closed, prompt the user to open it. If minimized or hidden, prompt the user to restore/show it (maximization is unnecessary). If inspection is unavailable, report the unknown state and ask the user to make the editor visible. Pause screenshot attempts until the issue is resolved, then repeat the window-state check before capturing. Do not automatically restore/focus the window. This prerequisite applies to editor screenshots, not saved render output. A passing check still requires inspection of the captured pixels; if the image is black or stale, report the failure and prompt the user to restore/show the editor before a fresh check and retry.
