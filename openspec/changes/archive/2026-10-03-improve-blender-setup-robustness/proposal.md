# Proposal

## Why

The setup audit can misdiagnose a working Blender MCP connection because it mixes installation, Python environment, transport, and editor visibility evidence. Repeated setup attempts showed the need for precise next actions and honest platform limits without disturbing the running Blender editor.

## What Changes

- **Report useful evidence:** Display ten checks using client-neutral labels, starting with “AI agent available” and “AI agent configured,” followed by Python, Blender, bridge, and connection checks. Present separate MCP readiness and editor readiness verdicts, preserving a working connection when the editor is minimized or unverified.
- **Start fast on every invocation:** Run a fresh quick pass through the current session, live Blender connection, and lightweight local evidence. Automatically deepen only failed, conflicting, or necessary missing evidence in one targeted second pass, without caching prior setup results.
- **Respect the workstation:** Identify Blender only through running programs; never search for its executable. Keep the default audit read-only and preserve the existing rules for Windows process creation and fresh screenshot prerequisites.
- **Target the connected instance:** Associate the report with the Blender process reached by MCP; use verified bridge ownership where available, and ask for clarification only if the target remains ambiguous.
- **Diagnose the configured environment:** Report “Python available” and “Python configured” separately. Fully diagnose direct Python and venv launches, recognize `uvx` with limited checks, handle configuration errors clearly, and guide externally managed Python users toward a dedicated environment.
- **Explain recurring failures:** Turn wrong-interpreter imports, missing packages, PEP 668, duplicate TOML tables, disabled add-ons, stopped bridges, and browser-endpoint confusion into reusable troubleshooting guidance.
- **State compatibility precisely:** Design Windows checks for Windows 10/11. Document macOS checks as limited, unavailable, or unverified according to actual evidence; do not infer live support from simulated tests.
- **Maintain the published skill packages:** Make changes in canonical sources, preserve common safety and evidence rules in the Claude adapter, regenerate client packages, and validate the behavioral failure cases.

## Capabilities

### New Capabilities
- `blender-setup`: Read-only, evidence-based auditing and troubleshooting of the active AI agent's official Blender MCP connection.

### Modified Capabilities

None.

## Impact

- Canonical `skills/blender-setup/SKILL.md` and its diagnostic helper/tests.
- `scripts/adapters/claude-blender-setup.md` for common discovery, visibility, platform, and evidence rules, retaining Claude-specific configuration behavior.
- Generated `.codex/skills/blender-setup/` and `.claude/skills/blender-setup/`, regenerated through `scripts/sync-client-skills.py`.
- New OpenSpec capability spec for Blender setup readiness.
- No automatic installs, config edits, application startup, window focus/restore, or Blender scene changes are introduced. Windows 10 and 11 are design targets; macOS can only receive static/simulated validation here and must be labeled accordingly.
