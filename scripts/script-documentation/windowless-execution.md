# Windowless execution verification

Verified on Windows on 2026-09-29. The priority is to create no auxiliary command windows, then keep existing skills and rules consistent with that requirement.

## Implemented behavior

- All 14 canonical skills, the Claude setup adapter, both generated client packages, and repository rules require full-chain suppression before launching. Unknown paths are blocked; existing MCP tools are preferred.
- The standalone setup package includes a captured runner using CREATE_NO_WINDOW for both its worker and reviewed command. Before starting the command, the worker joins a non-inheritable kill-on-close Windows Job with no breakaway permission. Job setup failure blocks the command. Worker exit removes owned descendants without process-name killing.
- Output is captured in temporary files so timeout diagnostics remain available even if a descendant inherits the output handles. Normal results retain exit status/stdout/stderr; startup failure and timeout remain distinct. Callers must not print secrets from captured streams.
- The optional SDK probe is blocked before starting any server process. MCP 1.30.0 has exception fallbacks without creationflags and permits missing Job ownership. No transport is currently approved by the helper. Existing native MCP access remains usable.
- Installer/package tests use the same runner. Current usage documentation explains the outer-launch prerequisite and why executable resolution does not prove suppression.

## Evidence

| Check | Result | Coverage |
|---|---|---|
| Setup regression suite | 16 passed | Existing six-row semantics, blocked probe without spawning, safe diagnostic summaries, direct runtime console state |
| Windows runner suite | 5 passed | Direct/nested console state, console-host show events, startup failure, nonzero exit, timeout output, descendant cleanup, no retry, Job failure |
| Policy checks | 3 passed | All distributed skills, packaged standalone helpers, unchanged editor capture prerequisites |
| Installer checks | 5 passed | Temporary installations, standalone setup tests, validation, conflicts/backups |
| Client-package checks | 3 passed | Source consistency, both clients, installed resource validation |
| Package synchronization and skill validation | Passed | 14 skills; generated Codex and Claude packages match canonical sources/adapters |
| Read-only helper chain | Expected blocked SDK probe | No observed console show events; configured Blender and visible editor checks passed; no unsafe SDK startup attempted |
| Existing native MCP connection | Passed | Blender 5.2.2 LTS, PID 40224, scene `Example_10-low-poly-island`, 63 objects; successful read-only tool response |
| Editor preservation | Passed | Two visible, non-minimized editor windows before and after the helper check, with equal recorded state; no focus/restore/capture calls |

Runtime checks used Python 3.14 and a .NET ProcessStartInfo outer launcher with UseShellExecute=false, CreateNoWindow=true, and redirected streams. Installed official environment metadata was blender-mcp 1.0.3, MCP 1.30.0, and AnyIO 4.15.1. Local machine evidence is retained in `.acceptance/windowless-runtime.json`; source tests for the setup runner ship with the setup skill.

## Scenario review and limits

Existing-tool work used native MCP without launching another server. Reviewed helper descendants passed console-state and show-event checks. Unknown SDK/client boundaries are blocked. Missing executables and nonzero exits produced captured errors; timeouts retained output and terminated the owned descendant while preserving the caller. Editor state and capture rules were preserved. Both client distributions carry the policy and Codex includes standalone helper dependencies.

This is evidence for the supported paths, not proof about every application or client. Window-event observation covered the current desktop and known console/terminal host classes, including hosts outside child PIDs. It cannot observe other sessions or unrecognized host classes; unrelated desktop activity could also cause a conservative failure. Code review and per-process console-state assertions supplement event observations. A restricted-process attempt could not enumerate editor windows; the same read-only check succeeded in the normal desktop context.

The client's original MCP launch flags remain unverified. No client restart, machine configuration change, SDK modification, global skill installation, or intentional visible failure case was attempted. The user's historical popup has not been attributed to a specific process. New or changed dependency launch behavior must be reviewed before it is enabled. Arbitrary application-created GUI windows are not suppressed by CREATE_NO_WINDOW; only reviewed console-only commands belong on this runner.
