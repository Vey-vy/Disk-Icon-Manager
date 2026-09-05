import os
import shutil
import ctypes


kernel32 = ctypes.windll.kernel32


def get_drives():
    drives = []

    bitmask = kernel32.GetLogicalDrives()

    for index in range(26):
        if bitmask & (1 << index):
            letter = chr(ord("A") + index)
            drive = f"{letter}:\\"

            drives.append(drive)

    return drives


def get_drive_usage(drive):
    return shutil.disk_usage(drive)


def drive_has_custom_icon(drive):
    desktop_ini = os.path.join(
        drive,
        "desktop.ini"
    )

    drive_icon = os.path.join(
        drive,
        "DriveIcon.ico"
    )

    return (
        os.path.isfile(desktop_ini)
        and os.path.isfile(drive_icon)
    )


def get_drive_type(drive):
    DRIVE_UNKNOWN = 0
    DRIVE_NO_ROOT_DIR = 1
    DRIVE_REMOVABLE = 2
    DRIVE_FIXED = 3
    DRIVE_REMOTE = 4
    DRIVE_CDROM = 5
    DRIVE_RAMDISK = 6

    drive_type = kernel32.GetDriveTypeW(
        drive
    )

    types = {
        DRIVE_UNKNOWN: "Unknown",
        DRIVE_NO_ROOT_DIR: "No root directory",
        DRIVE_REMOVABLE: "Removable",
        DRIVE_FIXED: "Fixed",
        DRIVE_REMOTE: "Network",
        DRIVE_CDROM: "CD/DVD",
        DRIVE_RAMDISK: "RAM Disk",
    }

    return types.get(
        drive_type,
        "Unknown"
    )


def is_drive_writable(drive):
    test_file = os.path.join(
        drive,
        ".disk_icon_maker_test"
    )

    try:
        with open(
            test_file,
            "w",
            encoding="utf-8"
        ) as file:
            file.write("test")

        os.remove(test_file)

        return True

    except (OSError, PermissionError):
        try:
            if os.path.exists(test_file):
                os.remove(test_file)
        except OSError:
            pass

        return False
