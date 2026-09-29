---
name: blender-setup
description: Check the official Blender Lab MCP setup in chronological order, verify a read-only connection to the open Blender scene, and report completed steps, missing steps, and exact next actions. Use for Blender connection setup checks and troubleshooting.
---

# Blender Setup

Audit the official Blender Lab add-on and MCP bridge used by Codex. Default to a read-only dry run: do not install, upgrade, start or stop apps, change configuration, create objects, switch scenes, or save files. If the user requests repairs too, repair within that scope and rerun affected checks.

Use the existing MCP connection whenever it can perform the operation. On Windows, auxiliary execution MUST remain windowless, including brief flashes, during setup, diagnostics, rendering, export, and verification. Before launching, establish suppression for the complete process chain, including client-owned and dependency-owned startup. Use explicit no-console creation (such as subprocess.CREATE_NO_WINDOW) and captured output for reviewed console-only commands. If any required boundary is unknown or unsupported, do not launch: report BLOCKED with the reason and next action, and continue independent safe work. Never retry through a visible terminal, toggle Blender's system console, or weaken suppression. An absolute executable path, cmd /c, Blender --background, or Start-Process -WindowStyle Hidden alone is not proof of no flashes. Keep exit status, bounded timeouts, useful diagnostics without secrets, and cleanup of owned descendants. Do not hide, minimize, restore, focus, or close the existing Blender editor to suppress auxiliary windows. Preserve fresh editor-readiness checks before screenshots.

## Run the checks

Use native session MCP tools first. Only when supplemental diagnostics are needed and the outer client launch is established as windowless, run [scripts/check_setup.py](scripts/check_setup.py) with Python 3.11 or newer. Its installed [windowless runner](scripts/windowless.py) captures output and owns helper cleanup. The SDK probe is blocked until its exact transport has reviewed suppression and cleanup support; MCP SDK 1.30.0 has an unsafe retry and is not supported for this fallback. It uses the current Codex home (`CODEX_HOME`, otherwise `~/.codex`), the configured `blender` MCP server, and a bounded MCP SDK probe. Use `--server NAME` when the connection has a different name. This helper targets Windows and the official Python stdio setup; report unsupported configurations rather than silently replacing them.

Use `python scripts/check_setup.py --format markdown` for a ready-to-present **Step / Status / Comment** table, or omit `--format` for JSON with `comment` fields. Resolve script paths relative to this skill directory. Exit code 0 means all checks passed; 1 means a failure or blocked check, not necessarily a script crash. The helper cannot inspect this conversation's native tool catalog; perform that check separately.

After changing the helper, run `python scripts/test_check_setup.py` (see [test helper](scripts/test_check_setup.py)). These offline regression tests simulate healthy, closed-Blender, stopped-bridge, missing-configuration, inspection-error, version-mismatch, and server-startup-failure states without altering Blender. Then use native MCP tools for a read-only live check once; never launch a blocked SDK probe to complete validation.

## Workflow

1. Identify Windows, the active Codex home and named server configuration.
2. Locate the configured or running Blender executable and inspect its version.
3. Inspect the Blender process and its editor window. Require a visible, non-minimized editor for the bridge-owning process when identifiable; maximization is not required. Failed inspection means unknown, not closed.
4. Check official add-on identity evidence; do not infer enablement from an expanded Preferences entry.
5. Probe the configured bridge listener and identify its owning process.
6. Validate the enabled official Python stdio registration and environment.
7. Initialize the MCP connection with a bounded timeout.
8. Discover tools and honor allowed/disabled tool policies.
9. Query Blender version, enabled add-on, active scene and object count read-only; preserve successful handshake status if this fails.
10. Present the six-row report below with observed evidence and actionable solutions, distinguishing helper access from native tools.

Report rows: Blender installed; Blender open; official add-on/bridge; Codex configured; MCP handshake/tools; live Blender communication. Verify minimum Blender version and matching add-on/server releases, reporting compatibility mismatches without automatic upgrades.

The helper continues independent checks after failures. Dependent checks become BLOCKED; they must not be marked successful. Status values are PASS, FAIL, and BLOCKED. Each non-PASS row needs a concrete next action, starting with the earliest missing prerequisite. Retry once only for a clearly transient connection error; do not loop indefinitely.

A refused connection cannot distinguish a disabled add-on from an enabled add-on with its server stopped. Report the observable failure, and use available UI evidence to identify which condition applies; otherwise explain both checks without claiming either as proven. A successful MCP initialization/tool listing stays PASS even when the subsequent Blender scene call fails.

When the user supplies a Preferences screenshot, inspect the checkbox beside **MCP**, not the disclosure arrow or the presence of its version/details. An expanded entry with an unchecked checkbox means **installed but disabled**. Report step 3 as FAIL with the next action **check the box beside MCP**; only then start its server if needed. An enabled checkbox with a **Start MCP Server** button instead indicates an enabled add-on with a stopped bridge. Treat screenshots as evidence at capture time, not proof of the current live state. Do not recommend reinstalling a visibly installed add-on for either case.

For a supplied `.snagx` capture, inspect its ZIP entries and extract the full-resolution image to a temporary location for viewing; use its metadata if multiple images or annotations need interpretation. Preserve the original capture.

## Interpret and report

Present an ordered table with the exact headers **Step**, **Status**, and **Comment**. Display statuses as **✅ Pass**, **❌ Fail**, and **⛔ Blocked**. In every red ❌ Fail row, put the concrete solution directly in the Comment cell (for example, **Open Blender**), rather than only describing the failure. For passing rows, give short evidence; for blocked rows, name the prerequisite to complete. If Blender is closed, step 2 is FAIL with **Open Blender**, and steps 3 and 6 are BLOCKED pending step 2. Include actual Blender/add-on/server versions and active scene when available. Do not promise every step will pass just because an earlier run did.

Distinguish **configured bridge verified by the helper** from **tools available directly in this conversation**. Inspect the session's actual tool catalog separately. If native Blender MCP tools are exposed, prefer a direct read-only scene tool call too. If absent but the helper passes, report the bridge as working and say that a new Codex thread/restart may be needed to expose native tools; do not describe the current conversation as natively connected.

For missing prerequisites, guide the user in order: install/open Blender, enable the official extension in Preferences and start its bridge, install a compatible official MCP Python package, register it with Codex, then retest. Use the configured host/port instead of assuming defaults. Discover the registered interpreter from the active configuration rather than assuming an installation directory.

Use [Blender's official MCP page](https://www.blender.org/lab/mcp-server/) and [official source/releases](https://projects.blender.org/lab/blender_mcp) when repair or compatibility research is needed. The working architecture is Codex → official Python MCP server over stdio → official Blender add-on over local TCP. Llama.cpp is an alternative client and is not required. Do not add community add-ons, other Blender workflows, or upgrade to an untagged development revision as a setup-check side effect. A known working version is evidence, not proof that it remains the latest release.

## Editor readiness and screenshots

Step 2 requires Blender to be running with a visible editor window that is not minimized. A minimized editor is FAIL: **Restore Blender from the taskbar; leave its editor open and not minimized.** A background-only process is insufficient. Failed window-state inspection is BLOCKED, not PASS. Do not restore, focus, or maximize the window during a read-only audit. A minimized editor does not prevent independent bridge/handshake/scene checks from passing.

Screenshot capture is already authorized when part of requested Blender work, but authorization does not prove technical capability. Both official full-window and area captures returned black while minimized on this workstation. Prefer a restored editor, inspect actual pixels, and report failed captures honestly; a visible window is a readiness prerequisite, not a guarantee of a valid screenshot. Never present an old screenshot or a clean render as fresh editor evidence.

Before **every** Blender editor/window/area screenshot call, freshly check that the relevant Blender process has a visible, non-minimized editor window; do not reuse an earlier setup result. If Blender is closed, prompt the user to open it. If minimized or hidden, prompt the user to restore/show it (maximization is unnecessary). If inspection is unavailable, report the unknown state and ask the user to make the editor visible. Pause screenshot attempts until the issue is resolved, then repeat the window-state check before capturing. Do not automatically restore/focus the window. This prerequisite applies to editor screenshots, not saved render output. A passing check still requires inspection of the captured pixels; if the image is black or stale, report the failure and prompt the user to restore/show the editor before a fresh check and retry.
