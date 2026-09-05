import ctypes


def is_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def set_file_attributes(path, attributes):
    result = ctypes.windll.kernel32.SetFileAttributesW(
        str(path),
        attributes
    )

    if result == 0:
        raise ctypes.WinError()


def refresh_explorer():
    SHCNE_ASSOCCHANGED = 0x08000000
    SHCNF_IDLIST = 0x0000

    ctypes.windll.shell32.SHChangeNotify(
        SHCNE_ASSOCCHANGED,
        SHCNF_IDLIST,
        None,
        None
    )
