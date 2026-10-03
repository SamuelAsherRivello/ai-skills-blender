"""Read-only native inspection of running programs; never locate Blender binaries.

Windows 10/11 use shared Win32 APIs without launching PowerShell or another app.
macOS process inspection uses libproc; editor/listener inspection is explicitly
limited. macOS has not been tested live on the development workstation.
"""
import ctypes
import socket
import struct
import sys


class InspectionUnavailable(RuntimeError):
    pass


def running_blender(platform=None):
    platform = platform or sys.platform
    if platform == 'win32':
        return _windows_processes()
    if platform == 'darwin':
        return _mac_processes()
    raise InspectionUnavailable('Running-program inspection is unsupported here.')


def _windows_processes():
    from ctypes import wintypes as w
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)

    class Entry(ctypes.Structure):
        _fields_ = [('size', w.DWORD), ('usage', w.DWORD), ('pid', w.DWORD),
                    ('heap', ctypes.c_size_t), ('module', w.DWORD),
                    ('threads', w.DWORD), ('parent', w.DWORD),
                    ('priority', w.LONG), ('flags', w.DWORD),
                    ('name', w.WCHAR * 260)]

    kernel.CreateToolhelp32Snapshot.argtypes = [w.DWORD, w.DWORD]
    kernel.CreateToolhelp32Snapshot.restype = w.HANDLE
    kernel.Process32FirstW.argtypes = [w.HANDLE, ctypes.POINTER(Entry)]
    kernel.Process32NextW.argtypes = [w.HANDLE, ctypes.POINTER(Entry)]
    kernel.CloseHandle.argtypes = [w.HANDLE]
    handle = kernel.CreateToolhelp32Snapshot(2, 0)
    if handle == ctypes.c_void_p(-1).value:
        raise ctypes.WinError(ctypes.get_last_error())
    processes = []
    try:
        entry = Entry()
        entry.size = ctypes.sizeof(Entry)
        found = kernel.Process32FirstW(handle, ctypes.byref(entry))
        while found:
            if entry.name.casefold() == 'blender.exe':
                processes.append({'pid': int(entry.pid), 'name': 'Blender'})
            found = kernel.Process32NextW(handle, ctypes.byref(entry))
        if ctypes.get_last_error() != 18:  # ERROR_NO_MORE_FILES
            raise ctypes.WinError(ctypes.get_last_error())
    finally:
        kernel.CloseHandle(handle)
    return processes


def _mac_processes():
    # Inspect process names, not bundle paths or installed applications.
    lib = ctypes.CDLL('/usr/lib/libproc.dylib', use_errno=True)
    lib.proc_listpids.argtypes = [ctypes.c_uint32, ctypes.c_uint32,
                                ctypes.c_void_p, ctypes.c_int]
    lib.proc_listpids.restype = ctypes.c_int
    lib.proc_name.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_uint32]
    lib.proc_name.restype = ctypes.c_int
    count_bytes = lib.proc_listpids(1, 0, None, 0)
    if count_bytes <= 0:
        raise InspectionUnavailable('macOS process inspection is unavailable.')
    pids = (ctypes.c_int * (count_bytes // ctypes.sizeof(ctypes.c_int) + 64))()
    used = lib.proc_listpids(1, 0, pids, ctypes.sizeof(pids))
    if used <= 0:
        raise InspectionUnavailable('macOS process inspection is unavailable.')
    processes = []
    for pid in pids[:used // ctypes.sizeof(ctypes.c_int)]:
        if pid <= 0:
            continue
        name = ctypes.create_string_buffer(1024)
        if lib.proc_name(pid, name, len(name)) <= 0:
            # Permission gaps prevent a reliable "Blender is closed" verdict.
            raise InspectionUnavailable('macOS process-name inspection is incomplete.')
        if name.value.decode('utf-8', 'replace').casefold() == 'blender':
            processes.append({'pid': int(pid), 'name': 'Blender'})
    return processes


def editor_windows(process_ids, platform=None):
    if (platform or sys.platform) != 'win32':
        raise InspectionUnavailable('Editor visibility support is missing on this platform; show Blender and use a supported fresh window check.')
    from ctypes import wintypes as w
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    dwm = ctypes.WinDLL('dwmapi', use_last_error=True)
    callback_type = ctypes.WINFUNCTYPE(w.BOOL, w.HWND, w.LPARAM)
    user32.EnumWindows.argtypes = [callback_type, w.LPARAM]
    user32.EnumWindows.restype = w.BOOL
    user32.GetWindowThreadProcessId.argtypes = [w.HWND, ctypes.POINTER(w.DWORD)]
    user32.IsWindowVisible.argtypes = [w.HWND]
    user32.IsIconic.argtypes = [w.HWND]
    user32.GetClassNameW.argtypes = [w.HWND, w.LPWSTR, ctypes.c_int]
    dwm.DwmGetWindowAttribute.argtypes = [w.HWND, w.DWORD, ctypes.c_void_p, w.DWORD]
    windows, errors = [], []

    @callback_type
    def visit(hwnd, _):
        pid = w.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        if pid.value in process_ids:
            cls = ctypes.create_unicode_buffer(256)
            if not user32.GetClassNameW(hwnd, cls, len(cls)):
                errors.append(True)
            elif cls.value == 'GHOST_WindowClass':
                cloaked = w.DWORD()
                if dwm.DwmGetWindowAttribute(hwnd, 14, ctypes.byref(cloaked), ctypes.sizeof(cloaked)) != 0:
                    errors.append(True)
                else:
                    windows.append({'pid': int(pid.value),
                                    'visible': bool(user32.IsWindowVisible(hwnd)) and not bool(cloaked.value),
                                    'minimized': bool(user32.IsIconic(hwnd))})
        return True

    if not user32.EnumWindows(visit, 0):
        raise ctypes.WinError(ctypes.get_last_error())
    if errors:
        raise InspectionUnavailable('Window-state inspection is incomplete.')
    return windows


def bridge_listeners(platform=None):
    if (platform or sys.platform) != 'win32':
        raise InspectionUnavailable('Listener ownership inspection is unsupported on this platform.')
    from ctypes import wintypes as w
    helper = ctypes.WinDLL('iphlpapi', use_last_error=True)
    helper.GetExtendedTcpTable.argtypes = [ctypes.c_void_p, ctypes.POINTER(w.DWORD),
                                          w.BOOL, w.ULONG, ctypes.c_int, w.ULONG]
    helper.GetExtendedTcpTable.restype = w.DWORD

    class IPv4Row(ctypes.Structure):
        _fields_ = [(key, w.DWORD) for key in
                    ('state', 'address', 'port', 'remote_address', 'remote_port', 'pid')]

    class IPv6Row(ctypes.Structure):
        _fields_ = [('address', ctypes.c_ubyte * 16), ('scope', w.DWORD),
                    ('port', w.DWORD), ('remote_address', ctypes.c_ubyte * 16),
                    ('remote_scope', w.DWORD), ('remote_port', w.DWORD),
                    ('state', w.DWORD), ('pid', w.DWORD)]

    listeners = []
    for family, row_type in ((socket.AF_INET, IPv4Row), (socket.AF_INET6, IPv6Row)):
        size = w.DWORD()
        error = helper.GetExtendedTcpTable(None, ctypes.byref(size), False, family, 3, 0)
        if error not in (0, 122):
            raise OSError(error, 'Listener inspection unavailable.')
        # Bounded retry only for the native table growing between two reads.
        for _ in range(2):
            buffer = ctypes.create_string_buffer(max(size.value, 4))
            error = helper.GetExtendedTcpTable(buffer, ctypes.byref(size), False, family, 3, 0)
            if error != 122:
                break
        if error:
            raise OSError(error, 'Listener inspection unavailable.')
        count = w.DWORD.from_buffer(buffer).value
        if 4 + count * ctypes.sizeof(row_type) > len(buffer):
            raise InspectionUnavailable('Invalid listener inspection response.')
        for index in range(count):
            row = row_type.from_buffer_copy(buffer, 4 + index * ctypes.sizeof(row_type))
            raw = struct.pack('=I', row.address) if family == socket.AF_INET else bytes(row.address)
            listeners.append({'pid': int(row.pid), 'host': socket.inet_ntop(family, raw),
                              'port': socket.ntohs(row.port & 0xffff)})
    return listeners
