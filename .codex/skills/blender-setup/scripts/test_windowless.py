"""Windows runtime regression checks; never launch a visible control process."""
import ctypes
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from windowless import LaunchBlocked, run


class WindowEvents:
    """Observe desktop show events, including console windows owned by a host.

    This conservative observer records all console/terminal show events during
    the check, not just child PIDs. Other user activity can therefore fail a
    check. It cannot observe another desktop/session or a nonstandard host.
    """
    def __enter__(self):
        self.events = []
        self.ready = threading.Event()
        self.stop = threading.Event()
        self.error = None
        self.thread = threading.Thread(target=self._watch, daemon=True)
        self.thread.start()
        if not self.ready.wait(5) or self.error:
            raise RuntimeError('Window observation unavailable')
        return self

    def _watch(self):
        from ctypes import wintypes as w
        u = ctypes.WinDLL('user32', use_last_error=True)
        callback_type = ctypes.WINFUNCTYPE(None, w.HANDLE, w.DWORD, w.HWND,
                                          w.LONG, w.LONG, w.DWORD, w.DWORD)
        u.SetWinEventHook.argtypes = [w.DWORD, w.DWORD, w.HMODULE,
                                     callback_type, w.DWORD, w.DWORD, w.DWORD]
        u.SetWinEventHook.restype = w.HANDLE
        u.UnhookWinEvent.argtypes = [w.HANDLE]
        u.GetClassNameW.argtypes = [w.HWND, w.LPWSTR, ctypes.c_int]
        u.GetWindowThreadProcessId.argtypes = [w.HWND, ctypes.POINTER(w.DWORD)]

        @callback_type
        def event(hook, event_id, hwnd, object_id, child_id, thread, timestamp):
            if object_id != 0 or child_id != 0:
                return
            name = ctypes.create_unicode_buffer(256)
            u.GetClassNameW(hwnd, name, 256)
            if name.value in ('ConsoleWindowClass', 'CASCADIA_HOSTING_WINDOW_CLASS', 'PseudoConsoleWindow'):
                pid = w.DWORD()
                u.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                self.events.append(dict(pid=pid.value, window_class=name.value,
                                        event=event_id, timestamp=timestamp))

        hook = u.SetWinEventHook(0x8002, 0x8002, None, event, 0, 0, 0)  # EVENT_OBJECT_SHOW
        if not hook:
            self.error = ctypes.get_last_error()
        self.ready.set()
        if not hook:
            return
        message = w.MSG()
        try:
            while not self.stop.is_set():
                while u.PeekMessageW(ctypes.byref(message), None, 0, 0, 1):
                    u.TranslateMessage(ctypes.byref(message))
                    u.DispatchMessageW(ctypes.byref(message))
                self.stop.wait(0.005)
        finally:
            u.UnhookWinEvent(hook)

    def __exit__(self, *args):
        time.sleep(0.05)  # Drain already queued events before stopping.
        self.stop.set()
        self.thread.join(5)


@unittest.skipUnless(os.name == 'nt', 'Windows execution contract')
class WindowlessTests(unittest.TestCase):
    def test_direct_and_nested_console_state_and_show_events(self):
        code = (
            'import ctypes,json,sys; from windowless import run; '
            'child=run([sys.executable,"-c",'
            '"import ctypes; print(bool(ctypes.windll.kernel32.GetConsoleWindow()))"]); '
            'print(json.dumps([bool(ctypes.windll.kernel32.GetConsoleWindow()),child.stdout.strip()]))'
        )
        with WindowEvents() as observed:
            result = run([sys.executable, '-c', code], cwd=Path(__file__).parent, check=True)
        self.assertEqual(json.loads(result.stdout), [False, 'False'])
        self.assertEqual(observed.events, [])

    def test_startup_failure_and_nonzero_exit_are_captured(self):
        with WindowEvents() as observed:
            with self.assertRaises(OSError):
                run([str(Path(tempfile.gettempdir()) / 'missing-windowless-fixture.exe')])
            result = run([sys.executable, '-c', 'import sys; print("failure evidence",file=sys.stderr); sys.exit(7)'])
        self.assertEqual(result.returncode, 7)
        self.assertIn('failure evidence', result.stderr)
        self.assertEqual(observed.events, [])

    def test_timeout_cleans_descendants_and_preserves_caller(self):
        with tempfile.TemporaryDirectory() as temp:
            pid_file = Path(temp) / 'pid.txt'
            child = 'import time; time.sleep(60)'
            code = ('import subprocess,sys,pathlib,time; '
                    f'p=subprocess.Popen([sys.executable,"-c",{child!r}],creationflags=subprocess.CREATE_NO_WINDOW); '
                    f'pathlib.Path({str(pid_file)!r}).write_text(str(p.pid)); '
                    'print("started",flush=True); time.sleep(60)')
            with WindowEvents() as observed:
                with self.assertRaises(subprocess.TimeoutExpired) as caught:
                    run([sys.executable, '-c', code], timeout=2)
            self.assertIn('started', caught.exception.stdout)
            self.assertEqual(observed.events, [])
            self.assertTrue(pid_file.is_file())
            from ctypes import wintypes as w
            k = ctypes.WinDLL('kernel32', use_last_error=True)
            k.OpenProcess.argtypes = [w.DWORD, w.BOOL, w.DWORD]
            k.OpenProcess.restype = w.HANDLE
            k.WaitForSingleObject.argtypes = [w.HANDLE, w.DWORD]
            k.CloseHandle.argtypes = [w.HANDLE]
            handle = k.OpenProcess(0x100000, False, int(pid_file.read_text()))
            if handle:
                try:
                    self.assertEqual(k.WaitForSingleObject(handle, 2000), 0)
                finally:
                    k.CloseHandle(handle)
            self.assertGreater(os.getpid(), 0)  # Parent test session survives.

    def test_worker_failure_never_retries_without_flags(self):
        with patch('windowless.subprocess.run', side_effect=OSError('blocked')) as launch:
            with self.assertRaises(OSError):
                run(['missing.exe'])
        self.assertEqual(launch.call_count, 1)
        self.assertEqual(launch.call_args.kwargs['creationflags'], subprocess.CREATE_NO_WINDOW)
        self.assertFalse(launch.call_args.kwargs['shell'])

    def test_job_failure_blocks_command(self):
        import io
        import windowless
        request = json.dumps(dict(args=['never.exe'], cwd=None, env=None, timeout=1))
        with patch('windowless._own_job', side_effect=LaunchBlocked('job unavailable')), patch('sys.stdin', io.StringIO(request)), patch('sys.stdout', new_callable=io.StringIO) as output, patch('windowless.subprocess.Popen') as launch:
            windowless._worker()
        launch.assert_not_called()
        self.assertEqual(json.loads(output.getvalue())['kind'], 'blocked')


if __name__ == '__main__':
    unittest.main()
