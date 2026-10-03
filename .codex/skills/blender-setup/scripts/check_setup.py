"""Fresh read-only setup evidence with a targeted diagnostic second pass.

The configuration adapter is Codex-specific; displayed labels are client-neutral.
Native session evidence must be collected by the agent during THIS invocation.
Never start Blender, install packages, or start another MCP client/server.
"""
import argparse
import importlib
import importlib.metadata
import inspect
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import sysconfig
import tomllib

import platform_checks
from windowless import LaunchBlocked, run as run_windowless

STEPS = ('AI agent available', 'AI agent configured', 'Python available',
         'Python configured', 'Blender installed', 'Blender running',
         'Blender open', 'Official add-on / bridge', 'MCP handshake / tools',
         'Live Blender communication')

# Use only with an allowed native execute tool; it queries the existing scene.
QUERY = '''import bpy, os, sys, pathlib, tomllib
addons = []
for key in bpy.context.preferences.addons.keys():
    module = sys.modules.get(key)
    if module is None or not getattr(module, '__file__', None):
        continue
    manifest_path = pathlib.Path(module.__file__).parent / 'blender_manifest.toml'
    if manifest_path.is_file():
        try:
            manifest = tomllib.loads(manifest_path.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            continue
        if manifest.get('id') == 'mcp' and manifest.get('maintainer') == 'Blender Lab':
            addons.append({'version': manifest.get('version'), 'minimum': manifest.get('blender_version_min')})
result = {'pid': os.getpid(), 'blender_version': bpy.app.version_string, 'version_tuple': list(bpy.app.version), 'addons': addons, 'scene': bpy.context.scene.name, 'object_count': len(bpy.context.scene.objects)}
'''


def sdk_launch_support():
    return False, 'SDK fallback launch is not verified windowless. Use the existing session MCP tools; review transport suppression and owned cleanup before enabling another client.'


async def probe(cfg):
    # Fail closed: never import/spawn the SDK, even on a healthy workstation.
    return {'probe_blocked': sdk_launch_support()[1]}


def diagnostic(exc):
    # Arbitrary exception text/stderr/arguments/environment can contain secrets.
    if isinstance(exc, LaunchBlocked):
        return 'Safe launch/owned cleanup unavailable; use native tools or establish the launch boundary before retrying.'
    if isinstance(exc, subprocess.TimeoutExpired):
        return 'Timed out; owned probe processes were stopped. Check responsiveness before retrying.'
    if isinstance(exc, subprocess.CalledProcessError):
        return f'Helper exited with status {exc.returncode}; check the configured interpreter and libraries.'
    if isinstance(exc, OSError):
        return f'Inspection/startup failed (OS error {exc.errno}); verify access and rerun.'
    return f'Evidence unavailable ({type(exc).__name__}); rerun the affected check.'


def config(name, path=None):
    root = Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex')
    with (Path(path) if path else root / 'config.toml').open('rb') as handle:
        servers = tomllib.load(handle).get('mcp_servers', {})
    if not isinstance(servers, dict) or not isinstance(servers.get(name, {}), dict):
        raise ValueError('Invalid server configuration')
    return servers.get(name, {})


def config_kind(cfg):
    """Validate structure without running the command or printing secret values."""
    if not cfg or cfg.get('enabled', True) is False:
        return 'FAIL', 'missing', 'Enable one official Blender MCP registration in the active AI client.'
    command, args, env, cwd = (cfg.get('command'), cfg.get('args', []),
                               cfg.get('env', {}), cfg.get('cwd'))
    if (not isinstance(command, str) or not command.strip()
            or not isinstance(args, list) or not all(isinstance(a, str) for a in args)
            or not isinstance(env, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in env.items())
            or (cwd is not None and (not isinstance(cwd, str) or not Path(cwd).is_dir()))
            or not isinstance(cfg.get('enabled', True), bool)):
        return 'FAIL', 'invalid', 'Correct the server command, arguments, environment or working directory in the active client configuration.'
    name = re.split(r'[/\\]', command)[-1].casefold()
    if name in ('uvx', 'uvx.exe') or (name in ('uv', 'uv.exe') and args[:2] == ['tool', 'run']):
        return 'BLOCKED', 'uvx', 'Launcher registration recognized; uvx environment diagnostics are limited. Verify official package identity with current native tools.'
    if not re.fullmatch(r'python(?:w)?(?:\d+(?:\.\d+)*)?(?:\.exe)?', name):
        return 'BLOCKED', 'unsupported', 'This configuration adapter supports direct Python stdio and recognizes uvx. Inspect this launcher with client-native evidence.'
    module_args = list(args)
    while module_args and module_args[0] in ('-u', '-B'):
        module_args.pop(0)
    if module_args[:2] != ['-m', 'blmcp']:
        return 'FAIL', 'invalid', 'Use the official Python module entry: -m blmcp, optionally followed by --transport stdio.'
    if module_args[2:] not in ([], ['--transport', 'stdio'], ['-t', 'stdio'], ['--transport=stdio']):
        return 'BLOCKED', 'unsupported', 'This helper supports official stdio arguments. Inspect other transports/options with active-client tools; do not replace a working registration.'
    return 'PASS', 'python', 'Enabled official blmcp stdio registration; interpreter execution is checked separately.'


def resolve_interpreter(cfg):
    """Resolve only configured Python, never any Blender executable."""
    env = dict(os.environ)
    env.update(cfg.get('env', {}))
    command = cfg['command']
    if '/' in command or '\\' in command:
        path = Path(command)
        if not path.is_absolute():
            path = Path(cfg.get('cwd') or Path.cwd()) / path
        return str(path.resolve()) if path.is_file() else None
    if cfg.get('cwd'):
        candidate = Path(cfg['cwd']) / command
        if candidate.is_file():
            return str(candidate.resolve())
    return shutil.which(command, path=env.get('PATH', os.defpath))


def python_details():
    """Reviewed import-only check; never calls blmcp.main or an MCP client."""
    missing = []
    for module in ('blmcp', 'mcp', 'yaml'):
        try:
            importlib.import_module(module)
        except Exception:
            missing.append(module)
    try:
        version = importlib.metadata.version('blender-mcp')
    except importlib.metadata.PackageNotFoundError:
        version = None
    return {'python_version': sys.version.split()[0], 'executable': sys.executable, 'missing': missing,
            'package_version': version,
            'externally_managed': (Path(sysconfig.get_path('stdlib')) / 'EXTERNALLY-MANAGED').is_file(),
            'venv': sys.prefix != sys.base_prefix}


def inspect_python(executable, cfg, allow_launch=False, platform=None):
    if not allow_launch:
        return {'blocked': 'Establish a reviewed no-console outer launch and owned cleanup before the import-only second pass; do not probe unrelated shell Python.'}
    if (platform or sys.platform) != 'win32':
        return {'blocked': 'Import subprocess diagnostics are limited on this platform; live macOS validation is unavailable.'}
    if '\\microsoft\\windowsapps\\' in executable.replace('/', '\\').casefold():
        return {'blocked': 'Python resolves to a Windows app alias. Configure a real installed/venv interpreter; do not launch the alias.'}
    env = dict(os.environ)
    env.update(cfg.get('env', {}))
    # Standalone preflight: the server interpreter need not meet the helper's
    # Python 3.11+ tomllib requirement just to report its own version.
    code = ('import importlib, importlib.metadata, json, sys, sysconfig\n'
            'from pathlib import Path\n' + inspect.getsource(python_details)
            + '\nprint(json.dumps(python_details()))\n')
    try:
        completed = run_windowless([executable, '-B', '-c', code],
                                   cwd=cfg.get('cwd'), env=env, timeout=15, check=True)
        details = json.loads(completed.stdout)
        if not isinstance(details.get('missing'), list) or not isinstance(details.get('python_version'), str):
            raise ValueError('Invalid interpreter evidence')
        return details
    except Exception as exc:
        return {'blocked' if isinstance(exc, LaunchBlocked) else 'error': diagnostic(exc)}


def endpoint(cfg):
    env = dict(os.environ)
    override = cfg.get('env', {})
    if isinstance(override, dict):
        env.update(override)
    host = env.get('BLENDER_MCP_HOST', 'localhost')
    try:
        port = int(env.get('BLENDER_MCP_PORT', 9876))
        if not 1 <= port <= 65535 or not isinstance(host, str) or not re.fullmatch(r'[A-Za-z0-9_.:-]+', host):
            raise ValueError('Invalid bridge endpoint')
    except (ValueError, TypeError):
        return None
    return host, port


def local_host(host):
    return host.casefold() in ('localhost', '127.0.0.1', '::1')


def listener_matches(listener, bridge):
    host, port = bridge
    addresses = {'127.0.0.1', '::1'} if host.casefold() == 'localhost' else {host}
    return listener.get('port') == port and listener.get('host') in addresses | {'0.0.0.0', '::'}


def choose_target(processes, listeners, bridge, scene_pid=None):
    pids = {p['pid'] for p in processes}
    if bridge and not local_host(bridge[0]):
        return None, 'Bridge host is not local; local windows cannot prove remote editor visibility.'
    if scene_pid is not None:
        if scene_pid in pids:
            return scene_pid, None
        return None, 'Live Blender PID is absent from local running programs; recheck process state and bridge host.'
    owners = {x['pid'] for x in listeners or [] if bridge and listener_matches(x, bridge)} & pids
    if len(owners) == 1:
        return next(iter(owners)), None
    if len(pids) == 1:
        return next(iter(pids)), None
    if not pids:
        return None, 'Open Blender.'
    return None, 'Multiple Blender instances are running; identify the intended MCP-connected process before editor checks.'


def collect_local(platform, scene_pid=None, bridge=None):
    info = {'platform': platform, 'processes': None, 'listeners': None, 'windows': None}
    try:
        info['processes'] = platform_checks.running_blender(platform)
    except Exception as exc:
        info['process_error'] = diagnostic(exc)
    if scene_pid is None and bridge and local_host(bridge[0]):
        try:
            info['listeners'] = platform_checks.bridge_listeners(platform)
        except Exception as exc:
            info['listener_error'] = diagnostic(exc)
    if info['processes'] is not None:
        target, reason = choose_target(info['processes'], info['listeners'], bridge, scene_pid)
        info['target_pid'], info['target_error'] = target, reason
        if target is not None:
            try:
                info['windows'] = platform_checks.editor_windows({target}, platform)
            except Exception as exc:
                info['window_error'] = diagnostic(exc)
    return info


def build_report(cfg, native, info, python_info=None, config_error=None):
    """Combine this invocation's evidence; no persistent state or subprocesses."""
    rows = []
    def row(index, status, comment, evidence='direct'):
        rows.append({'step': f'{index + 1}. {STEPS[index]}', 'status': status,
                     'comment': comment, 'evidence': evidence if status != 'BLOCKED' else 'unknown'})
    available = native.get('agent_available')
    row(0, 'PASS' if available is True else ('FAIL' if available is False else 'BLOCKED'),
        'Current AI agent session responds.' if available is True else 'Use the active AI agent to collect fresh session evidence; a standalone helper cannot verify it.')
    cfg_status, kind, cfg_comment = config_kind(cfg)
    if config_error:
        cfg_status, cfg_comment = config_error
    row(1, cfg_status, cfg_comment)
    scene = native.get('scene') if isinstance(native.get('scene'), dict) and not native.get('scene_error') else None
    live = bool(scene and isinstance(scene.get('blender_version'), str) and isinstance(scene.get('scene'), str))
    tool_count = native.get('tool_count')
    tools_ok = isinstance(tool_count, int) and not isinstance(tool_count, bool) and tool_count > 0
    python_info = python_info or {}
    if kind == 'python' and live and not config_error:
        row(2, 'PASS', 'Inferred from fresh official stdio communication; exact server interpreter/version not rechecked.', 'inferred')
        row(3, 'PASS', 'Inferred: official Python server operating; package/environment metadata not rechecked.', 'inferred')
    elif python_info.get('python_version'):
        row(2, 'PASS', f"Configured interpreter runs Python {python_info['python_version']}" + (f" at {python_info['executable']}" if python_info.get('executable') else '') + '.')
        missing = python_info.get('missing', [])
        if missing:
            managed = python_info.get('externally_managed') and not python_info.get('venv')
            row(3, 'FAIL', ('Create a dedicated venv and install the official package there; this base Python is externally managed. ' if managed else 'Install the official MCP package into the configured interpreter/venv. ') + 'Missing imports: ' + ', '.join(missing) + '. Register that same interpreter; do not bypass managed-environment protection.')
        else:
            row(3, 'PASS', f"Required imports available; official package {python_info.get('package_version') or 'version unverified'}.")
    elif python_info.get('missing_interpreter'):
        row(2, 'FAIL', 'Configure an existing Python/venv interpreter accessible in the AI client environment; the registered command could not be resolved.')
        row(3, 'BLOCKED', 'Resolve the configured interpreter first, then check libraries in that environment.')
    else:
        detail = python_info.get('blocked') or python_info.get('error') or ('uvx uses an isolated environment; dedicated diagnostics are limited. Do not test unrelated shell Python.' if kind == 'uvx' else 'Inspect the configured interpreter with a supported safe second pass.')
        row(2, 'FAIL' if python_info.get('error') else 'BLOCKED', detail)
        row(3, 'BLOCKED', 'Python package readiness is unknown. ' + detail)

    processes = info.get('processes')
    if processes is None:
        row(4, 'BLOCKED', 'Installation unknown; restore running-program inspection. No executable search is performed.')
        row(5, 'BLOCKED', 'Running state unknown. ' + info.get('process_error', 'Use supported running-program inspection.'))
    elif processes:
        row(4, 'PASS', 'Blender present in currently running programs; no executable path searched.', 'inferred')
        row(5, 'PASS', 'Running Blender PID(s): ' + ', '.join(str(p['pid']) for p in processes) + '.')
    else:
        row(4, 'BLOCKED', 'Installation unknown without a running Blender process. Open Blender if installed; no executable search is performed.')
        row(5, 'FAIL', 'Open Blender.')
    windows = info.get('windows')
    if processes == []:
        row(6, 'BLOCKED', 'Open Blender, then check its editor window.')
    elif info.get('target_pid') is None or windows is None:
        row(6, 'BLOCKED', info.get('target_error') or 'Editor visibility is unknown or unsupported; show Blender and use a supported fresh window-state check. ' + info.get('window_error', ''))
    elif any(w.get('pid') == info['target_pid'] and w.get('visible') and not w.get('minimized') for w in windows):
        row(6, 'PASS', f"Connected editor visible and not minimized (PID {info['target_pid']}); maximization unnecessary.")
    elif any(w.get('pid') == info['target_pid'] and w.get('minimized') for w in windows):
        row(6, 'FAIL', 'Restore Blender from the taskbar; leave the connected editor visible and not minimized.')
    else:
        row(6, 'FAIL', 'Show the connected Blender editor; a background process or another instance\'s window is insufficient.')

    bridge = endpoint(cfg)
    addons = scene.get('addons', []) if live else []
    if live and addons:
        minimum_ok = None
        try:
            minimum_ok = any(tuple(scene['version_tuple']) >= tuple(int(x) for x in a['minimum'].split('.')) for a in addons)
        except (KeyError, TypeError, ValueError):
            pass
        if minimum_ok is False:
            row(7, 'FAIL', 'Use a Blender version meeting the enabled official add-on\'s minimum; review compatible releases before any upgrade.')
        elif minimum_ok is None:
            row(7, 'BLOCKED', 'Bridge responds; inspect the official add-on manifest to verify identity/minimum version.')
        else:
            versions = ', '.join(str(a.get('version') or 'unknown') for a in addons)
            row(7, 'PASS', f'Enabled official Blender Lab add-on {versions}; bridge answered the fresh query.')
    elif bridge is None:
        row(7, 'FAIL', 'Correct BLENDER_MCP_HOST / BLENDER_MCP_PORT in the effective client environment; port must be 1..65535.')
    elif live:
        row(7, 'BLOCKED', 'Live Blender responds; official add-on identity/version unverified. Inspect its enabled manifest or Preferences checkbox.')
    elif processes == [] or processes is None:
        row(7, 'BLOCKED', 'Inspect running Blender first, then verify the official add-on checkbox and bridge.')
    elif info.get('listeners') is None:
        row(7, 'BLOCKED', 'Bridge ownership unknown or unsupported; inspect the official MCP checkbox and bridge status in Blender.')
    else:
        owned = [x for x in info['listeners'] if listener_matches(x, bridge) and x['pid'] in {p['pid'] for p in processes}]
        if owned:
            row(7, 'BLOCKED', f'Blender owns a listener at {bridge[0]}:{bridge[1]}; official add-on identity still needs native/UI evidence.')
        else:
            row(7, 'FAIL', f'Check the official MCP enable checkbox, then Start MCP Server at {bridge[0]}:{bridge[1]}. Absence cannot distinguish disabled add-on from stopped bridge; a browser page is not required.')
    row(8, 'PASS' if tools_ok else ('FAIL' if native.get('handshake_error') else 'BLOCKED'),
        f'{tool_count} official native tools exposed in the current session; tool discovery is separate from scene access.' if tools_ok else 'Reconnect the official server in the active AI agent and inspect its current tool catalog. ' + sdk_launch_support()[1])
    row(9, 'PASS' if live else ('FAIL' if native.get('scene_error') else 'BLOCKED'),
        f"Blender {scene['blender_version']}; scene {scene['scene']!r}, {scene.get('object_count', 'unknown')} object(s)." if live else 'Run an allowed read-only native scene query; inspect the official add-on and configured bridge if it fails. Preserve a successful handshake result.')
    warnings = []
    version = python_info.get('package_version')
    if version and addons and all(a.get('version') != version for a in addons):
        warnings.append(f'Server package {version} differs from add-on version; review official release compatibility. Observed communication remains separate.')
    if info.get('platform') == 'darwin':
        warnings.append('macOS support limited: process adapter untested live; editor/listener and import-subprocess diagnostics unsupported here.')
    return {'transport': 'Native-session evidence plus read-only local inspection; no helper MCP connection.',
            'checks': rows, 'mcp_readiness': rows[9]['status'], 'editor_readiness': rows[6]['status'],
            'all_passed': all(r['status'] == 'PASS' for r in rows), 'warnings': warnings,
            'target_pid': info.get('target_pid')}


def audit(name='blender', native=None, config_path=None, allow_python_probe=False, platform=None):
    native = native or {}
    platform = platform or sys.platform
    config_error = None
    try:
        cfg = config(name, config_path)
    except tomllib.TOMLDecodeError:
        cfg = {}
        config_error = ('FAIL', 'Fix TOML syntax or duplicate server tables; keep one entry per MCP server. Do not paste competing command/args examples together.')
    except FileNotFoundError:
        cfg = {}
        config_error = ('FAIL', 'Configure the official MCP server in the active AI client; the selected configuration file is missing.')
    except Exception as exc:
        cfg = {}
        config_error = ('BLOCKED', 'Configuration unverified. ' + diagnostic(exc))
    scene = native.get('scene') if isinstance(native.get('scene'), dict) and not native.get('scene_error') else {}
    bridge = endpoint(cfg)
    info = collect_local(platform, scene.get('pid'), bridge)
    targeted = False
    if scene.get('pid') is not None and info['processes'] is not None and scene['pid'] not in {p['pid'] for p in info['processes']}:
        info = collect_local(platform, scene['pid'], bridge)
        targeted = True  # Bounded recheck of contradictory local/live PID evidence.
    kind = config_kind(cfg)[1]
    details = None
    healthy = isinstance(scene.get('blender_version'), str) and isinstance(scene.get('scene'), str)
    if kind == 'python' and not healthy and not config_error:
        executable = resolve_interpreter(cfg)
        details = inspect_python(executable, cfg, allow_python_probe, platform) if executable else {'missing_interpreter': True}
        targeted = True
    report = build_report(cfg, native, info, details, config_error)
    report['passes'] = ['quick'] + (['targeted'] if targeted else [])
    return report


def render_report(report, output_format):
    if output_format == 'json':
        return json.dumps(report, indent=2, ensure_ascii=False)
    labels = {'PASS': '✅ Pass', 'FAIL': '❌ Fail', 'BLOCKED': '⛔ Blocked'}
    def cell(value):
        return str(value).replace('|', '\\|').replace('\r', ' ').replace('\n', ' ')
    lines = ['| Step | Status | Comment |', '|---|---|---|']
    for item in report['checks']:
        comment = item['comment']
        if item['evidence'] == 'inferred' and not comment.startswith('Inferred'):
            comment = 'Inferred: ' + comment
        lines.append(f"| {cell(item['step'])} | {labels[item['status']]} | {cell(comment)} |")
    lines += ['', f"MCP readiness: {labels[report['mcp_readiness']]}. Editor readiness: {labels[report['editor_readiness']]}."]
    lines += ['\n' + cell(w) for w in report['warnings']]
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--server', default='blender')
    parser.add_argument('--config', help='Explicit client TOML path; project/CLI overrides are not inferred.')
    parser.add_argument('--format', choices=['json', 'markdown'], default='json')
    parser.add_argument('--native-stdin', action='store_true', help='Fresh normalized native evidence from THIS invocation, as JSON on stdin; never reuse a saved report.')
    parser.add_argument('--allow-python-probe', action='store_true', help='Allow the reviewed Windows import-only second pass after the outer launch is established as windowless.')
    parser.add_argument('--python-details', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--probe', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.python_details:
        print(json.dumps(python_details()))
        return 0
    if args.probe:
        print(json.dumps({'probe_blocked': sdk_launch_support()[1]}))
        return 1
    try:
        native = json.load(sys.stdin) if args.native_stdin else {}
        if not isinstance(native, dict):
            raise ValueError('Invalid evidence')
        report = audit(args.server, native, args.config, args.allow_python_probe)
    except Exception as exc:
        print(json.dumps({'error': diagnostic(exc)}))
        return 1
    print(render_report(report, args.format))
    return 0 if report['all_passed'] else 1


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
