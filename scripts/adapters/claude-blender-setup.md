---
name: blender-setup
description: Check the official Blender Lab MCP connection in Claude Code, diagnose missing prerequisites, and verify the open scene without modifying it.
---

# Blender Setup

Use /blender-setup for a read-only readiness check in Claude Code. Do not install or upgrade software, start apps, change configuration or mutate the scene unless the user also requests repairs.

Use the existing MCP connection whenever it can perform the operation. On Windows, auxiliary execution MUST remain windowless, including brief flashes, during setup, diagnostics, rendering, export, and verification. Before launching, establish suppression for the complete process chain, including client-owned and dependency-owned startup. Use explicit no-console creation (such as subprocess.CREATE_NO_WINDOW) and captured output for reviewed console-only commands. If any required boundary is unknown or unsupported, do not launch: report BLOCKED with the reason and next action, and continue independent safe work. Never retry through a visible terminal, toggle Blender's system console, or weaken suppression. An absolute executable path, cmd /c, Blender --background, or Start-Process -WindowStyle Hidden alone is not proof of no flashes. Keep exit status, bounded timeouts, useful diagnostics without secrets, and cleanup of owned descendants. Do not hide, minimize, restore, focus, or close the existing Blender editor to suppress auxiliary windows. Preserve fresh editor-readiness checks before screenshots.

## Workflow

1. Identify the platform and the official Blender MCP connection available to this Claude Code session.
2. Locate Blender and inspect its version using local process/executable evidence; do not assume a workstation path.
3. Check whether Blender is running with a visible, non-minimized editor window, matching the bridge-owning process when identifiable. Maximization is not required. Failed inspection means unknown, not closed.
4. Check official add-on evidence. An expanded Preferences entry is not proof that its enable checkbox is checked.
5. Check the configured bridge host/port and listener when local inspection is available. Socket refusal cannot distinguish a disabled add-on from a stopped bridge.
6. Inspect Claude's connection status using /mcp or the read-only claude mcp list / claude mcp get command when available. Report registration separately from runtime tool access. Never print configuration secrets.
7. Confirm the session's MCP connection initializes or exposes working tools. Do not launch an unrelated Codex registration to claim Claude is connected.
8. Discover actual tool names and honor the current tool policy. Preserve successful handshake/tool-discovery results if a later scene query fails.
9. Use an allowed official tool to read Blender version, enabled official add-on identity/version, active scene and object count. If execution is needed, query only; the official execution response requires a dictionary result. Inspect MCP and nested Blender errors.
10. Present the six-row report below, including observed evidence and the next action for every failed or blocked check.

## Report

Use exact headers Step, Status, Comment and these six rows:

| Step | Status | Comment |
|---|---|---|
| 1. Blender installed | observed status | Version/path evidence or install fix |
| 2. Blender open | observed status | Visible, non-minimized editor evidence or Open/Restore Blender. |
| 3. Official add-on / bridge | observed status | Identity/listener evidence or enable MCP and start its server |
| 4. Claude configured | observed status | Claude registration evidence or configure the official server in Claude |
| 5. MCP handshake / tools | observed status | Session tool evidence or reconnect using /mcp |
| 6. Live Blender communication | observed status | Scene/version evidence or resolve preceding prerequisites |

Replace status placeholders with ✅ Pass, ❌ Fail or ⛔ Blocked. Put the solution directly in failed-row comments. Missing dependent checks are blocked, not successful. If Blender is closed, step 2 fails with Open Blender.; steps 3 and 6 are blocked. A successful scene call can prove runtime access, but does not prove details of configuration that were not inspected.

Verify official add-on identity and version compatibility from available evidence. If package versions are unavailable through Claude's tools, label them unverified; do not invent a version or blindly upgrade. Retry once only for a clearly transient failure.

## Compatibility

This client-specific adapter intentionally does not use the Codex TOML diagnostic helper. Claude's MCP configuration and live tools are the authority for its connection.

Use [Blender's official setup](https://www.blender.org/lab/mcp-server/) and [official releases](https://projects.blender.org/lab/blender_mcp) when repairs are requested. Keep the official Python stdio server plus Blender add-on architecture. Llama.cpp is an alternative client, not a requirement. Do not replace it with a community server as a side effect.

## Editor readiness and screenshots

Step 2 requires Blender to be running with a visible editor window that is not minimized. A minimized editor is FAIL: **Restore Blender from the taskbar; leave its editor open and not minimized.** A background-only process is insufficient. Failed window-state inspection is BLOCKED, not PASS. Do not restore, focus, or maximize the window during a read-only audit. A minimized editor does not prevent independent bridge/handshake/scene checks from passing.

Screenshot capture is already authorized when part of requested Blender work, but authorization does not prove technical capability. Both official full-window and area captures returned black while minimized on this workstation. Prefer a restored editor, inspect actual pixels, and report failed captures honestly; a visible window is a readiness prerequisite, not a guarantee of a valid screenshot. Never present an old screenshot or a clean render as fresh editor evidence.

Before **every** Blender editor/window/area screenshot call, freshly check that the relevant Blender process has a visible, non-minimized editor window; do not reuse an earlier setup result. If Blender is closed, prompt the user to open it. If minimized or hidden, prompt the user to restore/show it (maximization is unnecessary). If inspection is unavailable, report the unknown state and ask the user to make the editor visible. Pause screenshot attempts until the issue is resolved, then repeat the window-state check before capturing. Do not automatically restore/focus the window. This prerequisite applies to editor screenshots, not saved render output. A passing check still requires inspection of the captured pixels; if the image is black or stale, report the failure and prompt the user to restore/show the editor before a fresh check and retry.
