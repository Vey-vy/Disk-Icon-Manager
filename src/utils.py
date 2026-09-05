import ctypes
import os
import subprocess


kernel32 = ctypes.windll.kernel32
shell32 = ctypes.windll.shell32


def is_admin():
    try:
        return bool(shell32.IsUserAnAdmin())
    except Exception:
        return False


def set_file_attributes(path, attributes):
    path = os.path.abspath(str(path))

    result = kernel32.SetFileAttributesW(
        path,
        attributes
    )

    if result == 0:
        raise ctypes.WinError()


def remove_file_attributes(path):
    if not os.path.exists(path):
        return

    set_file_attributes(
        path,
        0x80
    )


def refresh_explorer():
    SHCNE_ASSOCCHANGED = 0x08000000
    SHCNF_IDLIST = 0x0000

    shell32.SHChangeNotify(
        SHCNE_ASSOCCHANGED,
        SHCNF_IDLIST,
        None,
        None
    )


def require_admin():
    if not is_admin():
        raise PermissionError(
            "Administrator privileges are required."
        )