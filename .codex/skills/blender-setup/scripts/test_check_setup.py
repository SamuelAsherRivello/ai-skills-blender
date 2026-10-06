"""Regression tests for observable setup failures; never launch/change Blender."""
import asyncio
import contextlib
import ctypes
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

import check_setup as checker
import platform_checks

CFG = {'command': 'python', 'args': ['-m', 'blmcp', '--transport', 'stdio']}
SCENE = {'pid': 42, 'blender_version': '5.2.2 LTS', 'version_tuple': [5, 2, 2],
         'addons': [{'version': '1.0.3', 'minimum': '5.1.0'}],
         'scene': 'Test', 'object_count': 3}
NATIVE = {'agent_available': True, 'tool_count': 26, 'scene': SCENE}
DETAILS = {'python_version': '3.11.16', 'missing': [], 'package_version': '1.0.3'}
PROCESSES = [{'pid': 42, 'name': 'Blender'}]
WINDOWS = [{'pid': 42, 'visible': True, 'minimized': False}]
LISTENERS = [{'pid': 42, 'host': '127.0.0.1', 'port': 9876}]


class SetupTests(unittest.TestCase):
    def audit(self, cfg=None, native=None, processes=None, windows=None, listeners=None,
              platform='win32', config_error=None, process_error=None, window_error=None,
              python_info=None, allow_probe=False):
        with contextlib.ExitStack() as stack:
            stack.enter_context(patch.object(checker, 'config', return_value=CFG if cfg is None else cfg,
                                             side_effect=config_error))
            proc = stack.enter_context(patch.object(platform_checks, 'running_blender',
                return_value=PROCESSES if processes is None else processes, side_effect=process_error))
            win = stack.enter_context(patch.object(platform_checks, 'editor_windows',
                return_value=WINDOWS if windows is None else windows, side_effect=window_error))
            listen = stack.enter_context(patch.object(platform_checks, 'bridge_listeners',
                return_value=LISTENERS if listeners is None else listeners))
            stack.enter_context(patch.object(checker, 'resolve_interpreter', return_value=sys.executable))
            py = stack.enter_context(patch.object(checker, 'inspect_python', return_value=python_info or DETAILS))
            launch = stack.enter_context(patch.object(checker, 'run_windowless', side_effect=AssertionError('Unexpected launch')))
            report = checker.audit(native=NATIVE if native is None else native,
                                   platform=platform, allow_python_probe=allow_probe)
            launch.assert_not_called()
        return report, proc, win, listen, py

    def test_healthy_quick_pass_has_twelve_rows_and_no_second_client(self):
        report, _, _, listen, py = self.audit()
        self.assertTrue(report['all_passed'])
        self.assertEqual([r['step'].split('. ', 1)[1] for r in report['checks']], list(checker.STEPS))
        self.assertEqual(report['passes'], ['quick'])
        self.assertEqual(report['checks'][2]['evidence'], 'inferred')
        self.assertIn('not rechecked', report['checks'][2]['comment'])
        listen.assert_not_called()
        py.assert_not_called()

    def test_healthy_path_does_not_search_any_executable(self):
        with patch.object(Path, 'is_file', side_effect=AssertionError('Unexpected path check')):
            report, *_ = self.audit()
        self.assertTrue(report['all_passed'])

    def test_fresh_invocation_does_not_reuse_last_success(self):
        first, *_ = self.audit()
        second, proc, *_ = self.audit(native={'agent_available': True, 'tool_count': 26, 'scene_error': True},
                                     processes=[], listeners=[])
        self.assertTrue(first['all_passed'])
        self.assertEqual(second['mcp_readiness'], 'FAIL')
        self.assertEqual(second['checks'][5]['status'], 'FAIL')
        proc.assert_called_once()

    def test_closed_blender_is_not_reported_uninstalled(self):
        report, *_ = self.audit(native={'agent_available': True}, processes=[], listeners=[])
        self.assertEqual(report['checks'][4]['status'], 'BLOCKED')
        self.assertIn('unknown', report['checks'][4]['comment'])
        self.assertEqual(report['checks'][5]['comment'], 'Open Blender.')
        self.assertEqual(report['checks'][6]['status'], 'BLOCKED')

    def test_unknown_process_state_preserves_live_access(self):
        report, *_ = self.audit(process_error=PermissionError(5, 'secret'))
        self.assertEqual(report['checks'][4]['status'], 'BLOCKED')
        self.assertEqual(report['checks'][5]['status'], 'BLOCKED')
        self.assertEqual(report['mcp_readiness'], 'PASS')

    def test_minimized_editor_only_affects_editor_readiness(self):
        report, *_ = self.audit(windows=[{'pid': 42, 'visible': True, 'minimized': True}])
        self.assertEqual(report['mcp_readiness'], 'PASS')
        self.assertEqual(report['editor_readiness'], 'FAIL')
        self.assertIn('Restore Blender from the taskbar', report['checks'][6]['comment'])

    def test_no_visible_editor_is_not_an_open_editor(self):
        report, *_ = self.audit(windows=[])
        self.assertEqual(report['editor_readiness'], 'FAIL')
        self.assertEqual(report['mcp_readiness'], 'PASS')

    def test_visible_editor_does_not_require_foreground_or_maximization(self):
        report, *_ = self.audit(windows=[{'pid': 42, 'visible': True, 'minimized': False}])
        self.assertEqual(report['editor_readiness'], 'PASS')
        self.assertIn('behind other apps', report['checks'][6]['comment'])

    def test_window_permission_gap_is_unknown(self):
        report, *_ = self.audit(window_error=PermissionError(5, 'secret'))
        self.assertEqual(report['editor_readiness'], 'BLOCKED')
        self.assertEqual(report['mcp_readiness'], 'PASS')
        self.assertNotIn('secret', json.dumps(report))

    def test_wrong_instance_visible_window_does_not_pass(self):
        report, _, win, *_ = self.audit(processes=PROCESSES + [{'pid': 43, 'name': 'Blender'}],
                                       windows=[{'pid': 43, 'visible': True, 'minimized': False}])
        win.assert_called_once_with({42}, 'win32')
        self.assertEqual(report['target_pid'], 42)
        self.assertEqual(report['editor_readiness'], 'FAIL')

    def test_multiple_instances_known_live_pid_avoids_selection_prompt(self):
        report, _, win, *_ = self.audit(processes=PROCESSES + [{'pid': 43, 'name': 'Blender'}])
        win.assert_called_once_with({42}, 'win32')
        self.assertEqual(report['editor_readiness'], 'PASS')

    def test_multiple_instances_ambiguous_blocks_editor(self):
        report, _, win, *_ = self.audit(native={'agent_available': True, 'tool_count': 26},
            processes=PROCESSES + [{'pid': 43, 'name': 'Blender'}], listeners=[])
        win.assert_not_called()
        self.assertEqual(report['editor_readiness'], 'BLOCKED')
        self.assertIn('identify', report['checks'][6]['comment'])

    def test_bridge_owner_selects_instance_when_scene_query_fails(self):
        report, _, win, *_ = self.audit(native={'agent_available': True, 'tool_count': 26, 'scene_error': True},
            processes=PROCESSES + [{'pid': 43, 'name': 'Blender'}])
        win.assert_called_once_with({42}, 'win32')
        self.assertEqual(report['checks'][10]['status'], 'PASS')
        self.assertEqual(report['mcp_readiness'], 'FAIL')

    def test_remote_host_does_not_match_a_coincidentally_equal_local_pid(self):
        report, _, win, *_ = self.audit(cfg={**CFG, 'env': {'BLENDER_MCP_HOST': '192.0.2.1'}})
        win.assert_not_called()
        self.assertEqual(report['editor_readiness'], 'BLOCKED')
        self.assertEqual(report['mcp_readiness'], 'PASS')

    def test_pid_contradiction_has_one_bounded_recheck(self):
        report, proc, *_ = self.audit(processes=[{'pid': 43, 'name': 'Blender'}])
        self.assertEqual(proc.call_count, 2)
        self.assertEqual(report['passes'], ['quick', 'targeted'])
        self.assertEqual(report['editor_readiness'], 'BLOCKED')

    def test_missing_config_does_not_erase_native_success(self):
        report, *_ = self.audit(cfg={})
        self.assertEqual(report['checks'][1]['status'], 'FAIL')
        self.assertEqual(report['mcp_readiness'], 'PASS')

    def test_duplicate_toml_has_redacted_action(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / 'config.toml'
            path.write_text('[mcp_servers.blender]\ncommand="secret-token"\n[mcp_servers.blender]\n', encoding='utf-8')
            with patch.object(checker, 'collect_local', return_value={'processes': [], 'platform': 'win32'}):
                report = checker.audit(config_path=path)
        self.assertEqual(report['checks'][1]['status'], 'FAIL')
        self.assertIn('duplicate', report['checks'][1]['comment'])
        self.assertNotIn('secret-token', json.dumps(report))

    def test_unreadable_config_is_blocked_not_missing(self):
        report, *_ = self.audit(config_error=PermissionError(5, 'secret-token'))
        self.assertEqual(report['checks'][1]['status'], 'BLOCKED')
        self.assertEqual(report['mcp_readiness'], 'PASS')
        self.assertNotIn('secret-token', json.dumps(report))

    def test_python_exists_without_libraries_is_separate_failure(self):
        for version in ('3.14.7', '3.11.16'):
            with self.subTest(version=version):
                report, *_, py = self.audit(native={'agent_available': True},
                    python_info={**DETAILS, 'python_version': version, 'missing': ['blmcp']})
                self.assertEqual(report['checks'][2]['status'], 'PASS')
                self.assertIn(version, report['checks'][2]['comment'])
                self.assertEqual(report['checks'][3]['status'], 'FAIL')
                self.assertIn('configured interpreter', report['checks'][3]['comment'])
                py.assert_called_once()

    def test_externally_managed_missing_package_guides_to_venv(self):
        report, *_ = self.audit(native={}, python_info={**DETAILS, 'missing': ['blmcp'], 'externally_managed': True, 'venv': False})
        self.assertIn('dedicated venv', report['checks'][3]['comment'])
        self.assertNotIn('--break-system-packages', json.dumps(report))

    def test_uvx_limited_check_never_launches_or_probes_shell_python(self):
        report, *_, py = self.audit(cfg={'command': 'uvx', 'args': ['--python', '3.11', 'mcp-for-blender']})
        py.assert_not_called()
        self.assertEqual(report['checks'][2]['status'], 'BLOCKED')
        self.assertIn('isolated', report['checks'][2]['comment'])
        self.assertEqual(report['mcp_readiness'], 'PASS')

    def test_argument_variants_include_users_working_venv_entry(self):
        for tail in ([], ['--transport', 'stdio'], ['-t', 'stdio'], ['--transport=stdio']):
            cfg = {'command': 'C:/venv/Scripts/python.exe', 'args': ['-m', 'blmcp'] + tail}
            self.assertEqual(checker.config_kind(cfg)[0], 'PASS')
        self.assertEqual(checker.config_kind({'command': 'python3.11', 'args': ['-u', '-m', 'blmcp']})[0], 'PASS')

    def test_invalid_environment_is_actionable(self):
        report, *_ = self.audit(cfg={**CFG, 'env': {'token': 42}})
        self.assertEqual(report['checks'][1]['status'], 'FAIL')
        self.assertNotIn('42', report['checks'][1]['comment'])

    def test_configured_path_resolution_uses_effective_environment(self):
        with patch.object(checker.shutil, 'which', return_value='venv-python') as which:
            found = checker.resolve_interpreter({**CFG, 'env': {'PATH': 'configured-path'}})
        self.assertEqual(found, 'venv-python')
        which.assert_called_once_with('python', path='configured-path')

    def test_missing_configured_interpreter_has_separate_package_blocker(self):
        with patch.object(checker, 'config', return_value=CFG), patch.object(checker, 'collect_local', return_value={'processes': [], 'platform': 'win32'}), patch.object(checker, 'resolve_interpreter', return_value=None):
            report = checker.audit()
        self.assertEqual(report['checks'][2]['status'], 'FAIL')
        self.assertEqual(report['checks'][3]['status'], 'BLOCKED')

    def test_import_probe_requires_known_launch_boundary(self):
        with patch.object(checker, 'run_windowless') as launch:
            details = checker.inspect_python(sys.executable, CFG)
        launch.assert_not_called()
        self.assertIn('blocked', details)

    def test_import_probe_uses_exact_interpreter_and_bounded_owned_runner(self):
        cfg = {**CFG, 'env': {'BLENDER_MCP_PORT': '12345'}}
        with patch.object(checker, 'run_windowless', return_value=subprocess.CompletedProcess([], 0, json.dumps(DETAILS))) as launch:
            result = checker.inspect_python('C:/venv/Scripts/python.exe', cfg, True, 'win32')
        self.assertEqual(result['python_version'], DETAILS['python_version'])
        self.assertEqual(launch.call_args.args[0][0], 'C:/venv/Scripts/python.exe')
        self.assertEqual(launch.call_args.kwargs['timeout'], 15)
        self.assertEqual(launch.call_args.kwargs['env']['BLENDER_MCP_PORT'], '12345')

    def test_windows_store_alias_is_not_launched(self):
        with patch.object(checker, 'run_windowless') as launch:
            details = checker.inspect_python('C:/Users/user/AppData/Local/Microsoft/WindowsApps/python.exe', CFG, True, 'win32')
        launch.assert_not_called()
        self.assertIn('alias', details['blocked'])

    def test_owned_runner_blocker_has_no_unsafe_retry(self):
        with patch.object(checker, 'run_windowless', side_effect=checker.LaunchBlocked('secret-token')) as launch:
            details = checker.inspect_python(sys.executable, CFG, True, 'win32')
        launch.assert_called_once()
        self.assertIn('blocked', details)
        self.assertNotIn('secret-token', json.dumps(details))

    def test_stopped_bridge_is_distinct_from_successful_handshake(self):
        report, *_ = self.audit(native={'agent_available': True, 'tool_count': 26, 'scene_error': True}, listeners=[])
        self.assertEqual(report['checks'][9]['status'], 'FAIL')
        self.assertIn('cannot distinguish', report['checks'][9]['comment'])
        self.assertIn('browser page is not required', report['checks'][9]['comment'])
        self.assertEqual(report['checks'][10]['status'], 'PASS')

    def test_wrong_owner_and_wrong_address_do_not_prove_bridge(self):
        for listeners in ([{'pid': 99, 'port': 9876, 'host': '127.0.0.1'}],
                          [{'pid': 42, 'port': 9876, 'host': '192.0.2.1'}]):
            report, *_ = self.audit(native={}, listeners=listeners)
            self.assertEqual(report['checks'][9]['status'], 'FAIL')

    def test_configured_port_and_ipv6_are_honored(self):
        report, *_ = self.audit(cfg={**CFG, 'env': {'BLENDER_MCP_HOST': '::1', 'BLENDER_MCP_PORT': '12345'}},
            native={}, listeners=[{'pid': 42, 'host': '::1', 'port': 12345}])
        self.assertEqual(report['checks'][9]['status'], 'BLOCKED')
        self.assertIn('12345', report['checks'][9]['comment'])

    def test_invalid_port_is_not_silently_defaulted(self):
        report, *_ = self.audit(cfg={**CFG, 'env': {'BLENDER_MCP_PORT': '0'}}, native={})
        self.assertEqual(report['checks'][8]['status'], 'FAIL')

    def test_version_warning_does_not_erase_actual_scene_success(self):
        info = {'platform': 'win32', 'processes': PROCESSES, 'target_pid': 42, 'windows': WINDOWS}
        report = checker.build_report(CFG, NATIVE, info, {**DETAILS, 'package_version': '1.0.2'})
        self.assertEqual(report['mcp_readiness'], 'PASS')
        self.assertIn('differs', report['warnings'][0])

    def test_minimum_version_problem_does_not_erase_handshake(self):
        scene = {**SCENE, 'version_tuple': [4, 0, 0]}
        report, *_ = self.audit(native={**NATIVE, 'scene': scene})
        self.assertEqual(report['checks'][8]['status'], 'FAIL')
        self.assertEqual(report['checks'][10]['status'], 'PASS')

    def test_macos_unknown_window_state_does_not_invent_success(self):
        report, *_ = self.audit(platform='darwin', window_error=platform_checks.InspectionUnavailable())
        self.assertEqual(report['mcp_readiness'], 'PASS')
        self.assertEqual(report['editor_readiness'], 'BLOCKED')
        self.assertIn('untested live', report['warnings'][0])
        with patch.object(checker, 'run_windowless') as launch:
            details = checker.inspect_python(sys.executable, CFG, True, 'darwin')
        launch.assert_not_called()
        self.assertIn('blocked', details)

    def test_standalone_helper_does_not_claim_agent_session_availability(self):
        report, *_ = self.audit(native={})
        self.assertEqual(report['checks'][0]['status'], 'BLOCKED')
        self.assertEqual(report['checks'][10]['status'], 'BLOCKED')

    def test_sdk_fallback_remains_blocked(self):
        with patch.object(checker, 'run_windowless') as launch:
            result = asyncio.run(checker.probe(CFG))
        launch.assert_not_called()
        self.assertIn('probe_blocked', result)

    def test_markdown_has_required_headers_labels_and_separate_verdicts(self):
        report, *_ = self.audit()
        markdown = checker.render_report(report, 'markdown')
        self.assertIn('| Step | Status | Comment |', markdown)
        self.assertIn('| 1. AI Agent Available | ✅ Pass |', markdown)
        self.assertIn('| 12. Live Blender Communication | ✅ Pass |', markdown)
        self.assertIn('MCP Readiness:', markdown)
        self.assertIn('Editor Readiness:', markdown)
        self.assertNotIn('Codex configured', markdown)

    def test_exception_diagnostics_never_echo_secrets(self):
        for exc in (OSError(2, 'secret-token'), subprocess.CalledProcessError(7, ['secret-token'], stderr='secret-token'),
                    subprocess.TimeoutExpired(['secret-token'], 1), ValueError('secret-token')):
            self.assertNotIn('secret-token', checker.diagnostic(exc))

    def test_cli_native_stdin_is_current_evidence_not_a_cache_file(self):
        report, *_ = self.audit()
        output = io.StringIO()
        with patch.object(sys, 'argv', ['check_setup.py', '--native-stdin']), patch.object(sys, 'stdin', io.StringIO(json.dumps(NATIVE))), patch.object(checker, 'audit', return_value=report) as audit, contextlib.redirect_stdout(output):
            code = checker.main()
        self.assertEqual(code, 0)
        self.assertEqual(audit.call_args.args[1], NATIVE)
        self.assertEqual(len(json.loads(output.getvalue())['checks']), 12)


class PlatformTests(unittest.TestCase):
    def test_macos_process_api_returns_names_and_pids_only(self):
        lib = Mock()
        def listpids(kind, typeinfo, buffer, size):
            if buffer is None:
                return 4
            buffer[0] = 42
            return 4
        def name(pid, buffer, size):
            buffer.value = b'Blender'
            return 7
        lib.proc_listpids.side_effect = listpids
        lib.proc_name.side_effect = name
        with patch.object(ctypes, 'CDLL', return_value=lib):
            result = platform_checks.running_blender('darwin')
        self.assertEqual(result, PROCESSES)

    def test_macos_permission_gap_is_not_reported_closed(self):
        lib = Mock()
        def listpids(kind, typeinfo, buffer, size):
            if buffer is not None:
                buffer[0] = 42
            return 4
        lib.proc_listpids.side_effect = listpids
        lib.proc_name.return_value = 0
        with patch.object(ctypes, 'CDLL', return_value=lib), self.assertRaises(platform_checks.InspectionUnavailable):
            platform_checks.running_blender('darwin')

    def test_unsupported_window_adapter_is_explicit(self):
        with self.assertRaises(platform_checks.InspectionUnavailable):
            platform_checks.editor_windows({42}, 'darwin')

    @unittest.skipUnless(os.name == 'nt', 'Windows APIs')
    def test_windows_native_inspection_is_read_only_and_returns_no_paths(self):
        with patch.object(subprocess, 'Popen', side_effect=AssertionError('No subprocess allowed')):
            processes = platform_checks.running_blender('win32')
            listeners = platform_checks.bridge_listeners('win32')
            windows = platform_checks.editor_windows({p['pid'] for p in processes}, 'win32')
        self.assertTrue(all(set(p) == {'pid', 'name'} for p in processes))
        self.assertTrue(all(1 <= item['port'] <= 65535 for item in listeners))
        self.assertTrue(all(isinstance(item['visible'], bool) for item in windows))

    @unittest.skipUnless(os.name == 'nt', 'Windows console behavior')
    def test_reviewed_child_has_no_console(self):
        child = checker.run_windowless([sys.executable, '-c', 'import ctypes; print(bool(ctypes.windll.kernel32.GetConsoleWindow()))'], timeout=10, check=True)
        self.assertEqual(child.stdout.strip(), 'False')

    @unittest.skipUnless(os.name == 'nt', 'Reviewed Windows import probe')
    def test_standalone_import_probe_runs_selected_interpreter(self):
        details = checker.inspect_python(sys.executable, {}, True, 'win32')
        self.assertEqual(details.get('python_version'), sys.version.split()[0])
        self.assertEqual(details.get('executable'), sys.executable)
        self.assertIsInstance(details.get('missing'), list)

    @unittest.skipUnless(os.name == 'nt', 'Windows owned descendant cleanup')
    def test_timeout_cleans_owned_descendant_and_captures_diagnostics(self):
        # Every child boundary explicitly suppresses console creation.
        script = 'import subprocess,sys,time; p=subprocess.Popen([sys.executable,"-c","import time; time.sleep(30)"],creationflags=subprocess.CREATE_NO_WINDOW,stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); print(p.pid,flush=True); time.sleep(30)'
        with self.assertRaises(subprocess.TimeoutExpired) as caught:
            checker.run_windowless([sys.executable, '-c', script], timeout=1, check=True)
        pid = int(caught.exception.output.strip())
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.OpenProcess.argtypes = [ctypes.c_uint32, ctypes.c_int, ctypes.c_uint32]
        kernel.OpenProcess.restype = ctypes.c_void_p
        kernel.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        kernel.CloseHandle.argtypes = [ctypes.c_void_p]
        handle = kernel.OpenProcess(0x100000, False, pid)
        if handle:
            try:
                self.assertEqual(kernel.WaitForSingleObject(handle, 2000), 0)
            finally:
                kernel.CloseHandle(handle)


if __name__ == '__main__':
    unittest.main()
