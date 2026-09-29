"""Offline regression tests; never launch or change Blender."""
import contextlib
import io
import json
import subprocess
import sys
import unittest
from unittest.mock import patch

import check_setup as checker


class SetupTests(unittest.TestCase):
    def run_case(self, *, running=True, listening=True, configured=True, inspection_error=False, scene=True, version='1.0.3', probe_error=False):
        cfg = {'command': sys.executable, 'args': ['-m', 'blmcp'], 'env': {'BLENDER_PATH': sys.executable}} if configured else {}
        info = {'processes': [{'ProcessId': 42, 'ExecutablePath': sys.executable}] if running else [], 'listeners': [{'OwningProcess': 42, 'LocalPort': 9876}] if listening else []}
        result = {'package_version': '1.0.3', 'tool_count': 26}
        if scene:
            result['scene'] = {'blender_version': '5.2.2 LTS', 'version_tuple': [5, 2, 2], 'addons': [{'version': version, 'minimum': '5.1.0'}], 'scene': 'Test', 'object_count': 1}
        else:
            result['scene_error'] = 'Enable the add-on and start its bridge.'
        if probe_error:
            result = {'probe_error': 'ImportError'}
        outcomes = [subprocess.TimeoutExpired('inspection', 20) if inspection_error else subprocess.CompletedProcess([], 0, json.dumps(info)), subprocess.CompletedProcess([], 0, json.dumps(result))]
        output = io.StringIO()
        with patch.object(checker, 'config', return_value=cfg), patch.object(checker.subprocess, 'run', side_effect=outcomes), patch.object(sys, 'argv', ['check_setup.py']), contextlib.redirect_stdout(output):
            code = checker.main()
        report = json.loads(output.getvalue())
        return code, report, [row['status'] for row in report['checks']]

    def test_healthy(self):
        code, report, statuses = self.run_case()
        self.assertEqual(code, 0)
        self.assertEqual(statuses, ['PASS'] * 6)
        self.assertTrue(report['all_passed'])

    def test_blender_closed(self):
        code, report, statuses = self.run_case(running=False, listening=False, scene=False)
        self.assertEqual(code, 1)
        self.assertEqual(statuses, ['PASS', 'FAIL', 'BLOCKED', 'PASS', 'PASS', 'BLOCKED'])
        self.assertEqual(report['checks'][1]['comment'], 'Open Blender.')

    def test_bridge_stopped_keeps_handshake_success(self):
        _, _, statuses = self.run_case(listening=False, scene=False)
        self.assertEqual(statuses, ['PASS', 'PASS', 'FAIL', 'PASS', 'PASS', 'BLOCKED'])

    def test_missing_configuration(self):
        _, _, statuses = self.run_case(configured=False, scene=False)
        self.assertEqual(statuses[3:], ['FAIL', 'BLOCKED', 'BLOCKED'])

    def test_process_inspection_failure_is_unknown_not_closed(self):
        _, report, statuses = self.run_case(inspection_error=True, scene=False)
        self.assertEqual(statuses[1:3], ['BLOCKED', 'BLOCKED'])
        self.assertIn('unknown', report['checks'][1]['comment'])

    def test_version_mismatch(self):
        _, _, statuses = self.run_case(version='0.3.0')
        self.assertEqual(statuses[2], 'FAIL')
        self.assertEqual(statuses[4:], ['PASS', 'FAIL'])

    def test_bridge_environment_failure(self):
        _, _, statuses = self.run_case(probe_error=True)
        self.assertEqual(statuses[4:], ['FAIL', 'BLOCKED'])

    def test_scene_failure_preserves_handshake(self):
        code, report, statuses = self.run_case(scene=False)
        self.assertEqual(code, 1)
        self.assertEqual(statuses[4:], ['PASS', 'FAIL'])
        self.assertIn('subprocess', report['transport'])

    def test_markdown(self):
        _, report, _ = self.run_case(running=False, listening=False, scene=False)
        output = checker.render_report(report, 'markdown')
        self.assertIn('| Step | Status | Comment |', output)
        self.assertIn('| 2. Blender open | ❌ Fail | Open Blender. |', output)


if __name__ == '__main__':
    unittest.main()
