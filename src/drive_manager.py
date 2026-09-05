import os
import shutil


def get_drives():
    drives = []

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        drive = f"{letter}:\\"

        if os.path.exists(drive):
            drives.append(drive)

    return drives


def get_drive_usage(drive):
    return shutil.disk_usage(drive)


def drive_has_custom_icon(drive):
    desktop_ini = os.path.join(drive, "desktop.ini")
    drive_icon = os.path.join(drive, "DriveIcon.ico")

    return os.path.exists(desktop_ini) and os.path.exists(drive_icon)
