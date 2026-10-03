# Design

## Context

Canonical setup sources are in `skills/blender-setup/`; `.codex/skills/` is generated. The Claude setup skill is generated separately from `scripts/adapters/claude-blender-setup.md` and intentionally does not run the Codex helper. Source changes must be synchronized with `scripts/sync-client-skills.py`. The existing skill validator requires one ten-step numbered workflow; preserve this convention alongside the ten-row report.

See [proposal.md](proposal.md) for motivation. The current audit helper is Windows-only, treats a Blender executable path as installation evidence, combines editor visibility with other checks, assumes a narrow Codex command/argument form, and has its MCP SDK fallback explicitly blocked. The current setup skill already prioritizes native MCP tools and requires read-only behavior, safe Windows child launches, fresh editor visibility checks before screenshots, and honest reporting of failed evidence.

The only setup history available for this plan is the current conversation. It records Python 3.14 on PATH without `blmcp`, a separate uv-managed Python 3.11 that also lacked the package, PEP 668 preventing base-environment installation, a dedicated venv that successfully imported `blmcp`, a TOML example with duplicate `[mcp_servers.blender]` tables, and confusion over whether the local bridge URL should render in a browser. It also records the user's rule to identify Blender only through running programs, not by searching for its executable.

## Goals / Non-Goals

**Goals:**
- Make each report row traceable to a specific observation, with PASS, FAIL, BLOCKED, and explicit unknown evidence.
- Cover Windows 10 and 11 using shared Windows inspection behavior, while describing the macOS workflow as limited or unavailable wherever the helper cannot verify it.
- Give practical, environment-specific guidance for Python, Codex TOML, MCP stages, and Blender editor visibility.
- Preserve safe, read-only operation and avoid disturbing the user's Blender window or scene.

**Non-Goals:**
- Installing Blender, Python, packages, or add-ons; editing Codex configuration; starting/stopping servers or applications; or changing Blender scenes.
- Claiming official macOS MCP support without an official platform statement or live macOS validation.
- Scanning for Blender executables, substituting another MCP implementation, or treating a browser page as a required MCP capability.
- Enabling the SDK subprocess probe unless its exact transport, startup, cancellation, and descendant cleanup behavior is reviewed and validated against process-safety requirements.

## Decisions

### Use client-neutral report labels with client-specific evidence

Start the table with “AI agent available” (the active client/session is accessible) and “AI agent configured” (its official Blender MCP registration is enabled and valid). These are distinct from MCP tool discovery and live Blender access. The Codex helper must not claim to inspect another client's configuration; each adapter contributes its own evidence. An independent helper cannot prove session availability and must mark that observation unknown unless supplied by the running agent.

### Report MCP and editor readiness separately

The report will give separate verdicts for MCP communication and editor/screenshot readiness. Each verdict must come from its own observed evidence. A minimized editor can require restoration for capture while the live MCP connection remains usable. A single aggregate `all_passed` flag may describe checklist completion but must not be presented as the sole answer to whether Codex can communicate with Blender.

**Alternative considered:** Require every report row to pass for one overall Ready verdict. Rejected in the planning interview because editor visibility and live communication serve different needs.

### Prefer native connection evidence and keep diagnostic stages separate

Every invocation begins with a fresh quick pass. Inspect the current session/tool availability, perform one bounded read-only live Blender query when allowed, and collect lightweight process/window and configuration evidence where safely available. Display all ten rows. A prerequisite may be described as inferred only when the fresh runtime evidence actually entails it; successful scene access does not verify an unread configuration file, an exact server interpreter path/version, or editor visibility. Blender's embedded Python must not be presented as the host MCP server's Python.

Trigger a targeted second pass for failed, contradictory, or missing evidence needed to diagnose a problem or decide readiness. Recheck only affected prerequisites using the safe helper or other read-only evidence. Preserve successful unrelated results. Unsupported platform/launcher inspection remains BLOCKED with a useful explanation; it must not cause an unbounded diagnostic loop. A healthy native connection must not trigger a redundant SDK connection, package-import subprocess, installer, or release lookup merely to repeat facts the runtime already establishes.

No prior report, stored success flag, or cached setup state substitutes for fresh invocation evidence. Historical reports, if separately authorized later, cannot determine current readiness.

The supplemental helper cannot inspect the conversation's native tool catalog. Session runtime evidence is supplied by the active agent; helper configuration and process findings cannot substitute for it. Preserve successful initialization/tool discovery if the later scene query fails.

**Alternative considered:** Always launch a new MCP SDK client from the helper. Rejected because the current SDK fallback is blocked for Windows process-safety reasons and a second connection can disagree with the already-established native session.

### Discover Blender only from the running-process list

Use process enumeration that returns process identity and PID without collecting the executable path. Never search disk, PATH, registry, or install locations. If Blender is absent, report the running check as FAIL (“Open Blender”) and installation as unknown/BLOCKED; process absence cannot establish that Blender is uninstalled.

**Alternative considered:** Infer installation from configured paths or executable discovery. Rejected because it conflicts with the user's explicit discovery rule and risks reporting a stale path as current installation evidence.

### Resolve and inspect the effective Codex interpreter

The two Python report rows are “Python available” (the configured interpreter can run) and “Python configured” (the MCP package and required libraries are available in that environment). Full automated checks cover direct Python and venv launches. Recognize `uvx` without launching it to provision an environment or importing its package from unrelated shell Python; missing environment evidence is BLOCKED with a limited-support explanation. Dedicated `uvx` environment discovery is deferred.

Parse the active `mcp_servers.<name>` TOML entry and inspect the interpreter represented by its command, resolving a bare command using the environment lookup rules of the current platform. Validate package imports and metadata in that environment, not in whichever `python` happens to be first in an interactive shell. Accept semantically valid command/argument forms, including a virtual-environment Python with `-m blmcp` and optional `--transport stdio`. Detect duplicate tables and report only redacted, relevant configuration details. Do not install packages; recommend a dedicated venv when an externally managed interpreter rejects global installs.

**Alternative considered:** Match only one literal argument list or run `python` from the current terminal. Rejected because the user's working configuration used an explicit venv path and arguments differed from the original example; shell Python versions also differed from the configured environment.

### Separate process state from editor-window state with platform adapters

Keep independent checks for Blender running and Blender editor open. On Windows 10/11, use the existing read-only Windows window-enumeration approach for a visible non-minimized Blender editor, without restoring or focusing it. For macOS, provide only checks that can be made safely and reliably; if process, Accessibility, or window-state APIs are unavailable or permission-limited, mark that row BLOCKED/unknown and continue unrelated checks. Do not prompt the user to grant broad permissions automatically or claim macOS visibility verification works without live validation.

**Alternative considered:** Treat an active process as proof that the editor is open on all platforms. Rejected because background/headless processes and minimized editors do not meet the user's screenshot prerequisite.

### Match the Blender instance reached by MCP

A native read-only query can return Blender's process ID alongside scene/version information. Match that PID against the currently running Blender programs, then inspect only its editor windows. Verified bridge-listener ownership is a fallback association when the live query is unavailable. Never accept a visible window from a different Blender instance as evidence for the connected one. If ownership remains ambiguous, preserve proven MCP access, block instance-specific visibility checks, and ask the user which process is intended.

**Alternative considered:** Inspect any visible Blender editor or require a selection whenever multiple processes exist. Rejected because the former can misidentify readiness and the latter interrupts an already identifiable connection.

### Keep the audit safe and side-effect free

Use bounded, captured helper execution only after the full launch boundary is known. On Windows, preserve the repository's no-console rule for the outer launcher and descendants, with explicit suppression, timeouts, diagnostics that omit secrets, and cleanup of owned processes. If the required suppression or cleanup boundary is unsupported, block that probe rather than retrying visibly. Never manipulate the user's Blender window. Do not use MCP bridge port defaults when the active configuration supplies a value.

**Alternative considered:** Add a generic fallback shell command for unsupported platforms. Rejected because it would make process visibility, secret handling, and descendant cleanup less predictable.

### Make troubleshooting follow observed failure states

The skill should distinguish: interpreter missing; interpreter available but package absent; package installed in a different Python; externally managed base Python; duplicate/inconsistent Codex config; Blender process absent; editor minimized/unknown; add-on disabled versus bridge stopped when UI evidence supports that distinction; handshake failure; and live scene query failure. A local port URL need not serve a browser page, so browser reachability is not an acceptance condition. When evidence cannot distinguish add-on-disabled from server-stopped, report both possibilities without claiming either.

**Alternative considered:** Keep one generic “MCP setup failed” instruction. Rejected because the recorded troubleshooting showed distinct causes with different remedies and because a generic message can send users back to reinstall a working component.

## Risks / Trade-offs

- [macOS window inspection may require permissions or native APIs unavailable to the helper] → Mark visibility as limited/blocked and continue checks; document that live macOS validation was not performed.
- [Windows 10/11 behavior could differ in process visibility or API permissions] → Use shared documented APIs and run Windows-specific tests on the available Windows 11 machine; label Windows 10 compatibility as designed but not live-tested unless a Windows 10 test environment is available.
- [TOML command interpretation may vary by Codex version] → Validate effective fields and clearly report unsupported forms instead of rewriting config or guessing.
- [Configured Python may itself require launching a child process for package checks] → Keep the operation bounded and read-only, apply platform launch rules, and mark it blocked if safe launch/cleanup cannot be established.
- [A port listener can be a different process or a stale service] → Associate listener PID with the running Blender PID where supported and keep bridge identity separate from handshake and scene evidence.

## Migration Plan

1. Update the skill workflow and report format, retaining its existing read-only and screenshot requirements.
2. Refactor the helper around testable platform/evidence adapters and the ten ordered checks; preserve safe Windows execution and leave unsafe MCP SDK launching disabled.
3. Add offline regression tests for platform adapters, Python/configuration cases, missing processes, unknown editor visibility, independent-check continuation, and the recorded troubleshooting scenarios.
4. Run the helper's offline tests and static checks on Windows. Confirm actual Windows 11 behavior where safe. For macOS, run simulated platform tests only and report live support as unverified. Do not claim Windows 10 or macOS live verification without such a host.
5. Rollback by reverting the skill/helper/test changes; no user configuration or Blender state is migrated.

## Deferred Work and Validation Limits

- Saved diagnostic reports were not decided before the user ended the interview. This change retains displayed JSON/Markdown output and adds no automatic report persistence or readiness cache.
- Dedicated `uvx` environment discovery is deferred; recognized wrappers retain explicit limited-support diagnostics.
- macOS live validation and native window inspection remain unavailable here. This change must document limited or missing support, not require a complete untested macOS adapter. Windows 10 compatibility is a design target; only the available Windows host can receive live validation.
- Troubleshooting guidance describes reusable failure states without embedding user-specific paths or a chat transcript. Other inaccessible Codex sessions were not reviewed.
