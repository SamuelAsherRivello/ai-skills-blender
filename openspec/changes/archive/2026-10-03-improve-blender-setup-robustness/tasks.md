# Tasks

## 1. Report model and evidence rules

- [x] 1.1 Replace executable-path installation detection with running-process-only Blender evidence and verify unit cases show “unknown” when Blender is absent without invoking path, registry, or PATH discovery.
- [x] 1.2 Implement the ordered ten-row report with client-neutral “AI agent available” and “AI agent configured” labels, independent checks, and dependency-specific PASS, FAIL, and BLOCKED outcomes; verify fixtures cover unavailable session evidence, Blender closed, editor unknown, and checks continuing after earlier failures.
- [x] 1.3 Keep Blender process status separate from visible/non-minimized editor status; verify tests cover visible, minimized, background-only, and inspection-error cases without changing window state.
- [x] 1.4 Report separate MCP communication and editor-readiness verdicts; verify a successful live query remains usable when the editor is minimized or its visibility is unknown.
- [x] 1.5 Implement a fresh quick pass on every invocation with explicit direct/inferred/unknown evidence and no cached success; verify healthy native evidence avoids redundant SDK, package-import, install, and release-check launches.
- [x] 1.6 Add a bounded targeted second pass for failed, conflicting, or necessary missing evidence; verify only affected checks deepen and unsupported inspection does not retry indefinitely.

## 2. Codex and Python diagnostics

- [x] 2.1 Parse the active Codex server configuration and validate semantically supported command/argument forms, duplicate tables, enabled state, environment and working-directory fields; verify cases include the explicit venv Python with `-m blmcp --transport stdio` and avoid exposing secret values.
- [x] 2.2 Resolve and inspect the interpreter selected by the Codex entry, distinguishing interpreter availability from `blmcp` and required dependency readiness; verify fixtures model Python 3.14 on PATH, an unprovisioned Python 3.11, and a working dedicated venv.
- [x] 2.3 Add actionable PEP 668 guidance that recommends a dedicated venv and never suggests bypassing externally managed protections; verify the diagnostic points to the configured environment and performs no installation.
- [x] 2.4 Recognize `uvx` configurations with limited diagnostics and explicit unknown Python-environment evidence; verify no unrelated interpreter imports or environment-provisioning launches occur and the table uses “Python available” and “Python configured”.

## 3. Platform-aware Blender and bridge checks

- [x] 3.1 Refactor process, listener, and editor inspection behind platform adapters; verify Windows 10/11-compatible behavior through Windows tests and simulated macOS tests, without collecting Blender executable paths.
- [x] 3.2 On macOS, report unsupported or permission-limited editor visibility as BLOCKED/unknown and continue independent checks; verify simulated permission and unavailable-API cases and document the absence of live macOS validation.
- [x] 3.3 Verify bridge ownership and configured host/port evidence without assuming a browser page or overriding explicit settings; test wrong-owner, stopped-server, and browser-unavailable scenarios.
- [x] 3.4 Preserve bounded launches, captured diagnostics, secret redaction, Windows no-console guarantees, and owned-process cleanup; verify safety tests and keep MCP SDK probing blocked until its transport satisfies the documented process-safety review.
- [x] 3.5 Associate process/editor findings with the PID returned by the native Blender query or verified bridge ownership; test multiple-instance, wrong-window, known-target, and ambiguous-target cases without starting another connection.

## 4. Skill guidance and troubleshooting lessons

- [x] 4.1 Rewrite canonical `skills/blender-setup/SKILL.md` around the ten ordered report checks, native MCP evidence, no-executable-search rule, read-only behavior, and precise next actions; retain the ten-step workflow convention and verify client-neutral labels and statuses match helper output.
- [x] 4.2 Document macOS support as limited or missing wherever unverified, Windows 10/11 validation boundaries, and the fresh visible-window prerequisite for each editor screenshot; verify no claim of live cross-platform support exceeds available evidence.
- [x] 4.3 Add a concise diagnostic decision tree for wrong-interpreter imports, missing packages, PEP 668, duplicate TOML tables, bridge handshake versus scene-query failures, and local URLs that need not serve browser pages; verify each branch maps evidence to a distinct next action.
- [x] 4.4 Make troubleshooting guidance reusable across workstations; verify it contains no user-specific paths, permanently embedded conversation transcript, or claims of reviewing inaccessible sessions.
- [x] 4.5 Update `scripts/adapters/claude-blender-setup.md` to preserve common running-process discovery, visibility, safety, and platform-limit rules while retaining Claude configuration behavior; verify it never substitutes the Codex helper for Claude runtime evidence.
- [x] 4.6 Regenerate the Codex and Claude packages with `scripts/sync-client-skills.py`; verify `--check` and the existing canonical/client skill validators pass without editing generated copies directly.

## 5. Integration review

- [x] 5.1 Run the offline helper regression suite and static checks on the available Windows 11 host; confirm output schema, no-executable-search rule, and independent-check behavior.
- [x] 5.2 Review the final report against Windows 10 and macOS support statements; ensure untested platforms and permission-limited checks remain explicitly unverified, with no claim of live testing.
