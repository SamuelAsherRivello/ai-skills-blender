# Blender Setup Specification

## Purpose

Give users an evidence-based, read-only way to diagnose whether their active AI agent can reach the official Blender MCP server and the live Blender editor, with actionable next steps and honest platform limitations.

## Requirements

### Requirement: Ordered setup report separates prerequisites
The audit SHALL report ten checks in order: AI agent available, AI agent configured, Python available, Python configured, Blender installed, Blender running, Blender open, official add-on / bridge, MCP handshake / tools, and live Blender communication. Each check SHALL report PASS, FAIL, or BLOCKED with evidence and a next action for non-passing results. Independent checks SHALL continue after a failure.

#### Scenario: Client-neutral labels use actual client evidence
- **WHEN** a Codex or Claude setup adapter renders the report
- **THEN** it uses the common AI agent labels and validates that client's availability and configuration without substituting evidence from another client

#### Scenario: Python is installed but lacks the package
- **WHEN** the configured Python interpreter exists but cannot import the official MCP package
- **THEN** Python available is PASS, Python configured is FAIL, and the report identifies that configured interpreter's environment as the installation target

#### Scenario: Blender is not running
- **WHEN** process inspection succeeds and finds no Blender process
- **THEN** Blender running is FAIL with the action to open Blender, while Blender installed evidence is BLOCKED or unknown rather than claiming Blender is absent

### Requirement: Each invocation starts with a fresh quick pass
The audit SHALL begin with fresh lightweight evidence and a bounded native read-only Blender query when available. It SHALL display all ten rows, identify direct, inferred, and unknown evidence, and perform a targeted second pass for failed, conflicting, or necessary missing evidence. Previous reports SHALL NOT act as a readiness cache.

#### Scenario: Setup is already working
- **WHEN** fresh session and live Blender evidence confirm the connection is healthy
- **THEN** the audit reports that evidence without redundantly launching another MCP client, package-import subprocesses, installers, or release searches

#### Scenario: Quick evidence contradicts a prerequisite
- **WHEN** a fresh quick check fails or leaves necessary evidence unresolved
- **THEN** the audit deepens only the relevant checks in a bounded second pass and preserves successful unrelated observations

#### Scenario: Runtime does not prove a configuration detail
- **WHEN** live scene access succeeds but an exact server interpreter version, persisted configuration field, or editor visibility has not been inspected
- **THEN** the audit does not claim those details were verified and distinguishes the server interpreter from Blender's embedded Python

### Requirement: MCP readiness and editor readiness have separate verdicts
The audit SHALL present separate MCP communication and editor-readiness verdicts, each derived from its own evidence. A failing or unknown editor-visibility check SHALL NOT invalidate an observed working MCP connection.

#### Scenario: Working connection with a minimized editor
- **WHEN** the live Blender query succeeds while the editor is minimized
- **THEN** the report states that MCP communication is working and separately instructs the user to restore Blender before editor screenshots

#### Scenario: Working connection with unknown visibility
- **WHEN** MCP communication succeeds but editor visibility cannot be inspected
- **THEN** the MCP verdict remains successful while editor readiness is blocked as unknown

### Requirement: Blender discovery uses running-process evidence only
The audit SHALL NOT search disks, registries, installation directories, or PATH for a Blender executable. It SHALL identify Blender only from currently running-program evidence and SHALL describe installation as unknown when that evidence is unavailable.

#### Scenario: Blender process is found
- **WHEN** the platform process inspector identifies a Blender process
- **THEN** the audit reports Blender as running without reading or presenting its executable path as an installation check

#### Scenario: Process inspection is unavailable
- **WHEN** permissions or platform support prevent reliable process inspection
- **THEN** Blender running and installed evidence are BLOCKED as unknown, and the report gives a safe next step without scanning for the executable

### Requirement: Python checks follow the active client's configured environment
When deeper Python diagnostics are needed, the audit SHALL inspect the interpreter selected by the active client's MCP configuration, distinguish interpreter availability from package readiness, and validate supported command forms without requiring one literal spelling. It SHALL NOT install packages or modify environments. Quick-pass runtime inferences SHALL be explicitly labeled.

#### Scenario: Configured virtual environment is ready
- **WHEN** the active client's configuration points to a virtual-environment interpreter and the official MCP package and required imports are available there
- **THEN** Python available and Python configured pass using that interpreter's evidence

#### Scenario: Base interpreter is externally managed
- **WHEN** package installation guidance or diagnostics encounter an externally managed Python environment
- **THEN** the audit recommends a dedicated virtual environment and does not recommend bypassing the environment protection

#### Scenario: Configuration has duplicate or inconsistent server entries
- **WHEN** the active Codex TOML contains duplicate server tables or the configured interpreter differs from the inspected interpreter
- **THEN** AI agent configured or Python configured fails with the conflicting entry identified without exposing secrets

#### Scenario: Launcher environment cannot be inspected
- **WHEN** the configuration uses `uvx` and the managed interpreter or package environment cannot be inspected safely
- **THEN** the Python checks report limited evidence as BLOCKED, do not test imports in unrelated shell Python, and do not run `uvx` to download or install dependencies

### Requirement: Blender process and editor visibility are distinct
The audit SHALL report Blender running separately from whether a visible, non-minimized Blender editor window is verified. It SHALL never restore, focus, minimize, hide, or close a user's Blender window during a read-only audit.

#### Scenario: Blender runs with a visible editor
- **WHEN** the process and window inspectors can associate a visible, non-minimized editor with a running Blender process
- **THEN** Blender running and Blender editor open pass

#### Scenario: Blender is minimized or visibility cannot be inspected
- **WHEN** the editor is minimized or platform permissions prevent visibility inspection
- **THEN** the editor-open result fails with a restore/show instruction or is blocked as unknown, while independent MCP checks continue

### Requirement: MCP stages preserve separate evidence
The audit SHALL distinguish active-client registration, official add-on/bridge evidence, MCP initialization and tool discovery, and a read-only live Blender query. A successful MCP handshake SHALL remain successful if the later scene query fails.

#### Scenario: MCP handshake succeeds but scene query fails
- **WHEN** the active client initializes the server and discovers tools but a read-only Blender query fails
- **THEN** MCP handshake and tools pass while live Blender communication fails or is blocked with the observed cause

#### Scenario: Local bridge URL has no browser page
- **WHEN** the user expects a local bridge address to render a browser page
- **THEN** the audit explains that browser-page availability is not proof of MCP readiness and diagnoses the configured MCP transport and bridge evidence instead

### Requirement: Instance checks target the Blender process reached by MCP
The audit SHALL associate instance-specific process and editor checks with the Blender instance reached by MCP or verified bridge ownership. It SHALL NOT substitute a different instance's visible window. If target identity remains ambiguous, instance-specific checks SHALL be blocked pending clarification while proven connection results are preserved.

#### Scenario: Other Blender instance has a visible editor
- **WHEN** MCP reaches one Blender process but only another process has a visible editor
- **THEN** the connected instance's editor check does not pass based on the unrelated window

#### Scenario: Connected instance is identifiable
- **WHEN** multiple Blender processes exist and the native query identifies its process ID
- **THEN** the audit targets that process without asking the user to choose

#### Scenario: Target cannot be associated
- **WHEN** several Blender processes exist and neither the live query nor bridge evidence identifies the target
- **THEN** the audit asks for clarification and blocks instance-specific visibility checks without erasing independent successful connection evidence

### Requirement: Platform limitations and evidence freshness are explicit
The setup guidance SHALL describe Windows 10/11 and macOS support according to verified capability, mark untested or permission-limited checks as limited or unknown, and require a fresh visible-window check before every editor screenshot. It SHALL not claim macOS support based only on architectural portability.

#### Scenario: macOS window inspection is unavailable
- **WHEN** the macOS helper cannot verify editor visibility, including because required permissions are unavailable
- **THEN** it reports that check as blocked or unsupported, continues independent safe checks, and documents that live macOS behavior is unverified

#### Scenario: Screenshot prerequisite fails
- **WHEN** Blender is closed, minimized, hidden, or window visibility is unknown before an editor screenshot
- **THEN** screenshot capture pauses and the user is asked to open or show the editor before a fresh readiness check

### Requirement: Client packages preserve shared setup rules
The distributed Codex and Claude setup skills SHALL preserve common discovery, editor-readiness, safety, and platform-limit rules from canonical sources. Client-specific configuration and runtime evidence SHALL remain specific to the client being audited.

#### Scenario: Setup guidance changes
- **WHEN** canonical setup guidance is revised and client packages are regenerated
- **THEN** the packages retain the common rules and Claude's audit uses Claude connection evidence rather than launching the Codex diagnostic registration
