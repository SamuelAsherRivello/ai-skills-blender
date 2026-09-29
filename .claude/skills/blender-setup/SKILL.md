---
name: blender-setup
description: Check the official Blender Lab MCP connection in Claude Code, diagnose missing prerequisites, and verify the open scene without modifying it.
---

# Blender Setup

Use /blender-setup for a read-only readiness check in Claude Code. Do not install or upgrade software, start apps, change configuration or mutate the scene unless the user also requests repairs.

## Workflow

1. Identify the platform and the official Blender MCP connection available to this Claude Code session.
2. Locate Blender and inspect its version using local process/executable evidence; do not assume a workstation path.
3. Check whether Blender is running. Failed process inspection means unknown, not closed.
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
| 2. Blender open | observed status | Process evidence or Open Blender. |
| 3. Official add-on / bridge | observed status | Identity/listener evidence or enable MCP and start its server |
| 4. Claude configured | observed status | Claude registration evidence or configure the official server in Claude |
| 5. MCP handshake / tools | observed status | Session tool evidence or reconnect using /mcp |
| 6. Live Blender communication | observed status | Scene/version evidence or resolve preceding prerequisites |

Replace status placeholders with ✅ Pass, ❌ Fail or ⛔ Blocked. Put the solution directly in failed-row comments. Missing dependent checks are blocked, not successful. If Blender is closed, step 2 fails with Open Blender.; steps 3 and 6 are blocked. A successful scene call can prove runtime access, but does not prove details of configuration that were not inspected.

Verify official add-on identity and version compatibility from available evidence. If package versions are unavailable through Claude's tools, label them unverified; do not invent a version or blindly upgrade. Retry once only for a clearly transient failure.

## Compatibility

This client-specific adapter intentionally does not use the Codex TOML diagnostic helper. Claude's MCP configuration and live tools are the authority for its connection.

Use [Blender's official setup](https://www.blender.org/lab/mcp-server/) and [official releases](https://projects.blender.org/lab/blender_mcp) when repairs are requested. Keep the official Python stdio server plus Blender add-on architecture. Llama.cpp is an alternative client, not a requirement. Do not replace it with a community server as a side effect.
