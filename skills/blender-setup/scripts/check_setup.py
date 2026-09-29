"""Read-only Windows readiness check for the official Blender Lab MCP bridge."""
import argparse
import asyncio
import json
import os
from pathlib import Path
import subprocess
import sys
import tomllib
from windowless import LaunchBlocked, run as run_windowless


def sdk_launch_support():
    """Fail closed: no installed SDK transport has full-chain approval yet.

    MCP 1.30.0 retries without creationflags on both Windows spawn paths and
    treats Job assignment as optional. Do not infer safety from a version bump
    or a substring check. Supporting a transport requires source review and
    runtime evidence for startup, fallback, cancellation and owned cleanup.
    """
    return False, ('SDK fallback launch is not verified windowless. Use the existing '
                   'session MCP tools; review transport suppression and cleanup before enabling a helper probe.')


def diagnostic(exc):
    # Exception text and arbitrary stderr can contain configuration secrets.
    if isinstance(exc, LaunchBlocked):
        return 'BLOCKED: windowless process ownership unavailable; review Job support before retrying.'
    if isinstance(exc, subprocess.TimeoutExpired):
        return 'Timed out; owned helper processes were stopped. Check responsiveness before retrying.'
    if isinstance(exc, subprocess.CalledProcessError):
        return f'Helper exited with status {exc.returncode}; check interpreter and dependencies.'
    if isinstance(exc, OSError):
        return f'Startup failed (OS error {exc.errno}); verify executable path and access.'
    return f'Invalid helper response ({type(exc).__name__}); check the configured interpreter.'

QUERY = '''import bpy
addons = []
for key in bpy.context.preferences.addons.keys():
    module = __import__('sys').modules.get(key)
    if module is None or not getattr(module, '__file__', None):
        continue
    path = __import__('pathlib').Path(module.__file__).parent / 'blender_manifest.toml'
    if path.is_file():
        manifest = __import__('tomllib').loads(path.read_text(encoding='utf-8'))
        if manifest.get('id') == 'mcp' and manifest.get('maintainer') == 'Blender Lab':
            addons.append({'version': manifest.get('version'), 'minimum': manifest.get('blender_version_min')})
result = {'blender_version': bpy.app.version_string, 'version_tuple': list(bpy.app.version), 'addons': addons, 'scene': bpy.context.scene.name, 'object_count': len(bpy.context.scene.objects)}
'''


def config(name):
    root = Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex')
    with (root / 'config.toml').open('rb') as handle:
        return tomllib.load(handle).get('mcp_servers', {}).get(name, {})


async def probe(cfg):
    supported, reason = sdk_launch_support()
    if not supported:
        return {'probe_blocked': reason}
    from importlib.metadata import version
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    result = {'package_version': version('blender-mcp')}
    env = dict(os.environ)
    env.update(cfg.get('env', {}))
    params = StdioServerParameters(command=cfg['command'], args=cfg.get('args', []), env=env, cwd=cfg.get('cwd'))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            catalog = await session.list_tools()
            result['tool_count'] = len(catalog.tools)
            tool_names = {tool.name for tool in catalog.tools}
            name = 'execute_blender_code'
            if name not in tool_names:
                result['scene_error'] = 'Official execution tool is unavailable; check the registered server capabilities.'
                return result
            allowed = cfg.get('enabled_tools')
            if name in cfg.get('disabled_tools', []) or (allowed is not None and name not in allowed):
                result['scene_error'] = 'Read-only execution probe is excluded by tool policy; use an allowed scene-summary tool.'
                return result
            try:
                response = await session.call_tool(name, {'code': QUERY})
            except Exception as exc:
                result['scene_error'] = 'Scene query failed ({}). Check the Blender bridge and rerun.'.format(type(exc).__name__)
                return result
            if response.isError:
                result['scene_error'] = 'The MCP server responds, but the Blender scene query failed. Check that the add-on is enabled and its server is started at the configured host/port.'
                return result
            data = response.structuredContent
            if data is None:
                try:
                    data = json.loads(next(c.text for c in response.content if c.type == 'text'))
                except (ValueError, StopIteration):
                    result['scene_error'] = 'The scene response was invalid. Check official add-on/server compatibility and rerun.'
                    return result
            if response.isError or data.get('status') != 'ok' or data.get('result', {}).get('status') == 'error':
                result['scene_error'] = 'Blender returned an error; confirm the official add-on is enabled and its bridge is started.'
            else:
                result['scene'] = data['result']
    return result


def render_report(report, output_format):
    if output_format == 'json':
        return json.dumps(report, indent=2)
    labels = {'PASS': '✅ Pass', 'FAIL': '❌ Fail', 'BLOCKED': '⛔ Blocked'}
    def cell(value):
        return str(value).replace('|', '\\|').replace('\n', ' ')
    lines = ['| Step | Status | Comment |', '|---|---|---|']
    for row in report['checks']:
        lines.append('| {} | {} | {} |'.format(cell(row['step']), labels[row['status']], cell(row['comment'])))
    return '\n'.join(lines)


def inspect_editor_windows(process_ids):
    """Read window state without restoring, focusing, or changing Blender."""
    import ctypes
    from ctypes import wintypes
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    callback_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows.argtypes = [callback_type, wintypes.LPARAM]
    user32.EnumWindows.restype = wintypes.BOOL
    user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    user32.IsWindowVisible.argtypes = [wintypes.HWND]
    user32.IsIconic.argtypes = [wintypes.HWND]
    user32.GetClassNameW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
    windows = []
    @callback_type
    def visit(hwnd, _):
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        if pid.value in process_ids:
            cls = ctypes.create_unicode_buffer(256)
            user32.GetClassNameW(hwnd, cls, len(cls))
            if cls.value == 'GHOST_WindowClass':
                windows.append({'pid': pid.value, 'visible': bool(user32.IsWindowVisible(hwnd)),
                                'minimized': bool(user32.IsIconic(hwnd))})
        return True
    if not user32.EnumWindows(visit, 0):
        raise ctypes.WinError(ctypes.get_last_error())
    return windows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', default='blender')
    parser.add_argument('--format', choices=['json', 'markdown'], default='json')
    parser.add_argument('--probe', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        cfg = config(args.server)
    except (OSError, ValueError):
        cfg = {}
    if args.probe:
        try:
            print(json.dumps(asyncio.run(asyncio.wait_for(probe(cfg), 40))))
        except Exception as exc:
            print(json.dumps({'probe_error': type(exc).__name__}))
            sys.exit(1)
        return

    rows = []
    def row(step, status, comment):
        rows.append({'step': step, 'status': status, 'comment': comment})

    if os.name != 'nt':
        print(json.dumps({'error': 'This helper targets Windows. Perform the six skill checks with platform-native tools.'}))
        return 1
    inspection_error = False
    command = "$ErrorActionPreference='Stop'; @{processes=@(Get-CimInstance Win32_Process -Filter \"Name='blender.exe'\" | Select-Object ProcessId,ExecutablePath);listeners=@(Get-NetTCPConnection -State Listen | Select-Object OwningProcess,LocalPort)} | ConvertTo-Json -Depth 4 -Compress"
    try:
        info = json.loads(run_windowless(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', command], timeout=20, check=True).stdout)
    except Exception as exc:
        inspection_error = True
        inspection_detail = diagnostic(exc)
        info = {'processes': [], 'listeners': []}
    processes = info['processes']
    executable = cfg.get('env', {}).get('BLENDER_PATH') or next((p['ExecutablePath'] for p in processes if p.get('ExecutablePath')), '')
    installed = bool(executable and Path(executable).is_file())
    row('1. Blender installed', 'PASS' if installed else 'FAIL', executable if installed else 'Install Blender or correct BLENDER_PATH to an existing Blender executable.')
    # Window readiness is checked after identifying the bridge-owning process.
    try:
        port = int(cfg.get('env', {}).get('BLENDER_MCP_PORT', 9876))
    except (TypeError, ValueError):
        port = -1
    owned = any(x['LocalPort'] == port and x['OwningProcess'] in [p['ProcessId'] for p in processes] for x in info['listeners'])
    if inspection_error:
        window_status, window_comment = 'BLOCKED', 'Blender state is unknown. ' + inspection_detail
    elif not processes:
        window_status, window_comment = 'FAIL', 'Open Blender.'
    else:
        try:
            owners = {x['OwningProcess'] for x in info['listeners'] if x['LocalPort'] == port}
            blender_pids = {p['ProcessId'] for p in processes}
            windows = inspect_editor_windows((owners & blender_pids) or blender_pids)
            ready = [w for w in windows if w['visible'] and not w['minimized']]
            if ready:
                window_status, window_comment = 'PASS', f"Blender editor visible and not minimized (PID {ready[0]['pid']}); maximization is not required."
            elif any(w['minimized'] for w in windows):
                window_status, window_comment = 'FAIL', 'Restore Blender from the taskbar; leave its editor open and not minimized. Maximization is not required.'
            else:
                window_status, window_comment = 'FAIL', 'Open a visible Blender editor window; a background process alone is insufficient.'
        except Exception:
            window_status, window_comment = 'BLOCKED', 'Restore access to Windows window-state inspection and rerun; editor visibility is unknown.'
    row('2. Blender open', window_status, window_comment)
    row('3. Official add-on / bridge', 'BLOCKED' if not processes or inspection_error else ('PASS' if owned else 'FAIL'), 'Complete step 2 first.' if not processes or inspection_error else (f'Blender listening on port {port}; identity checked in step 6.' if owned else f'In Blender Preferences, check the MCP box if disabled, then click Start MCP Server for port {port}.'))
    valid = cfg.get('enabled', True) and Path(cfg.get('command', '')).is_file() and cfg.get('args', []) == ['-m', 'blmcp']
    row('4. Codex configured', 'PASS' if valid else 'FAIL', f'Enabled official blmcp stdio registration: {args.server}' if valid else 'Register the official Python MCP bridge with codex mcp add; this helper expects python -m blmcp.')
    if not valid:
        if owned:
            rows[2]['status'] = 'BLOCKED'
            rows[2]['comment'] = 'Blender port is listening; restore step 4 to verify official add-on identity.'
        row('5. MCP handshake / tools', 'BLOCKED', 'Complete step 4, then rerun.')
        row('6. Live Blender communication', 'BLOCKED', 'Complete preceding connection steps, then rerun.')
    else:
        supported, reason = sdk_launch_support()
        if not supported:
            result = {'probe_blocked': reason}
        else:
            try:
                run = run_windowless([cfg['command'], str(Path(__file__).resolve()), '--server', args.server, '--probe'], timeout=50, check=True)
                result = json.loads(run.stdout.strip().splitlines()[-1])
            except Exception as exc:
                result = {'probe_error': diagnostic(exc)}
        ok = 'tool_count' in result
        row('5. MCP handshake / tools', 'PASS' if ok else ('BLOCKED' if 'probe_blocked' in result else 'FAIL'), f"{result['tool_count']} tools; official package {result['package_version']}" if ok else result.get('probe_blocked', result.get('probe_error', 'Check the registered Python environment and official MCP dependencies; handshake failed.')))
        scene = result.get('scene')
        if scene:
            addons = scene.get('addons', [])
            matching = any(a['version'] == result['package_version'] and tuple(scene['version_tuple']) >= tuple(map(int, a['minimum'].split('.'))) for a in addons)
            if not matching:
                rows[2]['status'] = 'FAIL'
                rows[2]['comment'] = 'Review official add-on identity, minimum Blender version, and add-on/server version compatibility.'
            else:
                rows[2]['comment'] = f"Official add-on {result['package_version']}; port {port}."
            row('6. Live Blender communication', 'PASS' if matching else 'FAIL', f"Blender {scene['blender_version']}; scene {scene['scene']!r}, {scene['object_count']} object(s)." if matching else 'Check official release compatibility and use compatible Blender, add-on, and server versions.')
        else:
            if owned:
                rows[2]['status'] = 'BLOCKED'
                rows[2]['comment'] = 'Blender port is listening, but the official add-on identity could not be verified.'
            row('6. Live Blender communication', 'FAIL' if ok and owned else 'BLOCKED', 'Complete step 2 first.' if not processes or inspection_error else result.get('probe_blocked', result.get('scene_error', 'Restore the MCP connection and rerun the read-only scene query.')))
    print(render_report({'transport': 'configured stdio diagnostic subprocess; native session tools must be checked separately', 'checks': rows, 'all_passed': all(r['status'] == 'PASS' for r in rows)}, args.format))
    return 0 if all(r['status'] == 'PASS' for r in rows) else 1


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
