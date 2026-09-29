"""Bounded, captured execution for reviewed console-only commands.

This suppresses console creation, not application-created GUI windows. Callers
must audit the command and its descendants before use. No shell/visible retry.
The private Windows worker joins a kill-on-close Job before starting the command,
so even an outer timeout removes its owned descendants without PID/name killing.
"""
import ctypes
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


class LaunchBlocked(RuntimeError):
    pass


def _own_job():
    from ctypes import wintypes as w
    k = ctypes.WinDLL('kernel32', use_last_error=True)

    class Basic(ctypes.Structure):
        _fields_ = [('process_time', ctypes.c_int64), ('job_time', ctypes.c_int64),
                    ('flags', w.DWORD), ('min_ws', ctypes.c_size_t),
                    ('max_ws', ctypes.c_size_t), ('active', w.DWORD),
                    ('affinity', ctypes.c_size_t), ('priority', w.DWORD),
                    ('scheduling', w.DWORD)]

    class IO(ctypes.Structure):
        _fields_ = [(name, ctypes.c_uint64) for name in
                    ('reads', 'writes', 'other', 'read_bytes', 'write_bytes', 'other_bytes')]

    class Extended(ctypes.Structure):
        _fields_ = [('basic', Basic), ('io', IO), ('process_memory', ctypes.c_size_t),
                    ('job_memory', ctypes.c_size_t), ('peak_process', ctypes.c_size_t),
                    ('peak_job', ctypes.c_size_t)]

    k.CreateJobObjectW.argtypes = [ctypes.c_void_p, w.LPCWSTR]
    k.CreateJobObjectW.restype = w.HANDLE
    k.SetInformationJobObject.argtypes = [w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD]
    k.AssignProcessToJobObject.argtypes = [w.HANDLE, w.HANDLE]
    k.GetCurrentProcess.restype = w.HANDLE
    k.CloseHandle.argtypes = [w.HANDLE]
    job = k.CreateJobObjectW(None, None)
    if not job:
        raise LaunchBlocked('Job creation failed; no command was started.')
    info = Extended()
    info.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE; no breakaway
    if not k.SetInformationJobObject(job, 9, ctypes.byref(info), ctypes.sizeof(info)):
        k.CloseHandle(job)
        raise LaunchBlocked('Job configuration failed; no command was started.')
    if not k.AssignProcessToJobObject(job, k.GetCurrentProcess()):
        k.CloseHandle(job)
        raise LaunchBlocked('Job assignment failed; no command was started.')
    # Keep this non-inheritable handle until worker exit. Closing it here would
    # terminate the worker itself before its result can be returned.
    return job


def _worker():
    request = json.load(sys.stdin)
    try:
        job = _own_job()
        stdout_log = tempfile.TemporaryFile()
        stderr_log = tempfile.TemporaryFile()
        process = subprocess.Popen(request['args'], cwd=request['cwd'],
                                   env=request['env'], shell=False,
                                   stdin=subprocess.DEVNULL, stdout=stdout_log,
                                   stderr=stderr_log,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
        process.wait(timeout=request['timeout'])
        stdout_log.seek(0)
        stderr_log.seek(0)
        response = dict(kind='completed', returncode=process.returncode,
                        stdout=stdout_log.read().decode('utf-8', 'replace'),
                        stderr=stderr_log.read().decode('utf-8', 'replace'))
    except subprocess.TimeoutExpired:
        stdout_log.seek(0)
        stderr_log.seek(0)
        response = dict(kind='timeout', stdout=stdout_log.read().decode('utf-8', 'replace'),
                        stderr=stderr_log.read().decode('utf-8', 'replace'))
    except LaunchBlocked as exc:
        response = dict(kind='blocked', message=str(exc))
    except OSError as exc:
        # Do not include command arguments/environment in exception messages.
        response = dict(kind='startup', errno=exc.errno)
    print(json.dumps(response), flush=True)
    # Do not wait for inherited pipe handles on timeout. Worker exit closes the
    # Job, terminating all owned descendants atomically after diagnostics flush.
    if 'job' in locals():
        os._exit(0)


def run(args, *, capture_output=True, text=True, timeout=30, check=False,
        cwd=None, env=None):
    """subprocess.run subset: captured UTF-8 text, bounded, shell-free execution."""
    if isinstance(args, (str, bytes)) or not args or not capture_output or not text:
        raise ValueError('Use an argument list and captured text output.')
    if timeout is None or timeout <= 0:
        raise ValueError('A positive timeout is required.')
    args = [os.fspath(arg) for arg in args]
    if os.name != 'nt':
        return subprocess.run(args, capture_output=True, text=True, timeout=timeout,
                              check=check, cwd=cwd, env=env, shell=False)
    request = dict(args=args, cwd=os.fspath(cwd) if cwd else None,
                   env=env, timeout=timeout)
    worker = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--worker'],
                            input=json.dumps(request), capture_output=True, text=True,
                            encoding='utf-8', errors='replace', shell=False,
                            timeout=timeout + 5, creationflags=subprocess.CREATE_NO_WINDOW)
    if worker.returncode:
        raise LaunchBlocked('Windowless worker failed; inspect job support before retrying.')
    try:
        response = json.loads(worker.stdout)
    except ValueError as exc:
        raise LaunchBlocked('Windowless worker returned invalid diagnostics.') from exc
    if response['kind'] == 'blocked':
        raise LaunchBlocked(response['message'])
    if response['kind'] == 'startup':
        raise OSError(response['errno'], 'Command startup failed; verify executable and access.')
    if response['kind'] == 'timeout':
        raise subprocess.TimeoutExpired(args, timeout, response['stdout'], response['stderr'])
    result = subprocess.CompletedProcess(args, response['returncode'], response['stdout'], response['stderr'])
    if check:
        result.check_returncode()
    return result


if __name__ == '__main__':
    if sys.argv[1:] != ['--worker']:
        raise SystemExit('Import run() from a reviewed caller; this is a private worker.')
    _worker()
