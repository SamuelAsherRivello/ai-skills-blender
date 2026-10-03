---
name: blender-setup
description: Quickly check the official Blender Lab MCP connection using fresh Claude session evidence, deepen failed checks, and report AI agent, Python, Blender and editor readiness without scene changes.
---

# Blender Setup

Use /blender-setup to audit the active AI agent's official Blender Lab MCP connection. Default to a read-only check; repairs, installations, configuration edits and application startup require the user's requested scope.

Use the existing MCP connection whenever it can perform the operation. On Windows, auxiliary execution MUST remain windowless, including brief flashes, during setup, diagnostics, rendering, export, and verification. Before launching, establish suppression for the complete process chain, including client-owned and dependency-owned startup. Use explicit no-console creation (such as subprocess.CREATE_NO_WINDOW) and captured output for reviewed console-only commands. If any required boundary is unknown or unsupported, do not launch: report BLOCKED with the reason and next action, and continue independent safe work. Never retry through a visible terminal, toggle Blender's system console, or weaken suppression. An absolute executable path, cmd /c, Blender --background, or Start-Process -WindowStyle Hidden alone is not proof of no flashes. Keep exit status, bounded timeouts, useful diagnostics without secrets, and cleanup of owned descendants. Do not hide, minimize, restore, focus, or close the existing Blender editor to suppress auxiliary windows. Preserve fresh editor-readiness checks before screenshots.

## Workflow

1. Identify the platform and active Claude session. Check session availability directly; use client-neutral AI agent labels in the report.
2. Inspect the actual native tool catalog and perform one allowed read-only Blender query. Inspect MCP and nested Blender errors; a successful handshake remains separate from scene access.
3. Inspect Claude's registration through /mcp or safe read-only claude mcp list / claude mcp get when available. Never substitute Codex TOML/helper evidence for Claude's configuration. Print no secrets.
4. Report Python available and Python configured separately. Infer runtime readiness only from a fresh working official Python stdio connection, labeling the inference. Diagnose the configured interpreter on failure rather than unrelated terminal Python. Recognize uvx as limited/isolated; do not provision it during an audit.
5. Identify Blender only from currently running programs. Never search disk, registry, installation directories or PATH for its executable or use BLENDER_PATH discovery. With no running process, installation is unknown.
6. Target the Blender instance reached by MCP, using a read-only process ID query or verified bridge owner. Never substitute another instance's visible window; ask which is intended only when identity remains ambiguous.
7. Freshly inspect the target editor's visible/non-minimized state without restoring or focusing it. Maximization is unnecessary. Unavailable inspection is unknown/Blocked and does not erase a working MCP connection.
8. Verify enabled official add-on identity, minimum Blender version and bridge evidence at the effective host/port. A listener alone does not prove identity; an expanded Preferences entry does not prove enablement.
9. Begin each invocation with quick fresh evidence; deepen only failed, conflicting or necessary missing evidence in one bounded second pass. Preserve independent passes, retry once only for a clearly transient scene error, and never reuse saved/cached setup status or start another unreviewed client.
10. Display all ten rows plus separate MCP and editor verdicts, concrete solutions and platform limitations. Do not invent unobserved versions or save reports automatically.

## Report

Use exact headers **Step**, **Status**, **Comment** and these rows:

| Step | Status | Comment |
|---|---|---|
| 1. AI agent available | observed status | Current Claude session evidence |
| 2. AI agent configured | observed status | Claude official MCP registration |
| 3. Python available | observed status | Registered runtime available; label inference |
| 4. Python configured | observed status | Libraries in that runtime; label inference or unknown |
| 5. Blender installed | observed status | Running-program evidence; otherwise unknown |
| 6. Blender running | observed status | Current process evidence |
| 7. Blender open | observed status | Target editor visible and not minimized |
| 8. Official add-on / bridge | observed status | Official enabled identity and bridge evidence |
| 9. MCP handshake / tools | observed status | Current session initialization/tool discovery |
| 10. Live Blender communication | observed status | Fresh read-only scene query |

Replace placeholders with **✅ Pass**, **❌ Fail**, **⛔ Blocked**. Every failed row includes its solution; blocked rows identify unknown evidence and the next safe step. Label inferred passes. If Blender is absent from running programs, installed is Blocked/unknown, running fails with **Open Blender**, and editor open is Blocked.

Report **MCP readiness** and **Editor readiness** separately. A minimized editor requires **Restore Blender from the taskbar** before capture while live MCP access may still pass. Preserve handshake success when a scene query fails. A working scene query does not prove an unread persisted configuration, exact host interpreter/version, or visible window. Blender's embedded Python is not the host MCP server interpreter.

## Troubleshooting and compatibility

Check required libraries in the interpreter Claude actually launches. If PEP 668/externally managed Python rejects an installation, guide the user to a dedicated venv; do not bypass that protection. An environment can use the same host Python as hobby work and does not require another Blender version. Do not install, switch interpreters or rewrite a working registration as an audit side effect.

Inspect the checkbox beside MCP in supplied Preferences screenshots. Expanded details with an unchecked box mean installed but disabled: **Check the box beside MCP**, then start its bridge when authorized. An enabled entry showing **Start MCP Server** means the bridge is stopped. A refused socket alone cannot distinguish these cases. Do not recommend reinstalling a visibly installed add-on.

The local add-on TCP bridge need not serve a browser page at localhost:9876. Test MCP/live scene access instead. The architecture is AI client → official Python server over stdio → add-on inside Blender over local TCP. The AI client launches the host server; a separate LLM client inside Blender is unnecessary. Llama.cpp is optional. Use [official setup](https://www.blender.org/lab/mcp-server/) and [official releases](https://projects.blender.org/lab/blender_mcp) for compatibility research; do not replace the official server or automatically upgrade. Report version discrepancies without erasing actual live access.

Windows 10/11 share relevant Win32 inspection APIs; inspect the real desktop only through available supported read-only tools. Sandbox isolation or permission gaps can make visibility unknown. macOS support is limited and untested live in this repository's Windows validation: use available native MCP and running-program evidence, report unsupported editor/listener/interpreter diagnostics as Blocked, and do not grant permissions or invent platform support. The Claude package intentionally does not ship the Codex TOML helper.

## Editor readiness and screenshots

Before **every** editor/window/area screenshot, freshly check that the target process has a visible, non-minimized editor. If closed, ask the user to open Blender. If minimized/hidden, say **Restore Blender from the taskbar** or ask them to show it; maximization is unnecessary. If inspection is unavailable, report unknown and ask the user to make it visible. Pause attempts until resolved, then repeat the check. Do not restore, focus or maximize it automatically.

Inspect actual captured pixels. Minimized official captures have returned black on the observed Windows workstation. A visible window is not a guarantee: report black/stale captures, request show/restore, and recheck before retrying. Never substitute old screenshots or a clean render as fresh editor evidence. Saved render output does not need this editor prerequisite.

For supplied `.snagx`, inspect ZIP entries, extract/view the original full-resolution image temporarily, and preserve the original archive. Screenshots prove capture-time state only. Keep multiple/concatenated paths distinct and do not claim access to other AI chats that were not available.
