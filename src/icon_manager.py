import os
import shutil

from .utils import set_file_attributes, refresh_explorer


ICON_NAME = "DriveIcon.ico"
INI_NAME = "desktop.ini"


def apply_icon(drive, source_icon):
    if not os.path.isfile(source_icon):
        raise FileNotFoundError(
            "The selected icon does not exist."
        )

    if not source_icon.lower().endswith(".ico"):
        raise ValueError(
            "The selected file must be an .ico file."
        )

    destination_icon = os.path.join(
        drive,
        ICON_NAME
    )

    desktop_ini = os.path.join(
        drive,
        INI_NAME
    )

    shutil.copy2(
        source_icon,
        destination_icon
    )

    content = (
        "[.ShellClassInfo]\n"
        "IconResource=DriveIcon.ico,0\n"
    )

    with open(
        desktop_ini,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(content)

    # Hidden + System
    set_file_attributes(
        desktop_ini,
        0x02 | 0x04
    )

    refresh_explorer()


def restore_icon(drive):
    desktop_ini = os.path.join(
        drive,
        INI_NAME
    )

    drive_icon = os.path.join(
        drive,
        ICON_NAME
    )

    if os.path.exists(desktop_ini):
        set_file_attributes(
            desktop_ini,
            0x80
        )
        os.remove(desktop_ini)

    if os.path.exists(drive_icon):
        set_file_attributes(
            drive_icon,
            0x80
        )
        os.remove(drive_icon)

    refresh_explorer()


def check_icon(drive):
    desktop_ini = os.path.join(
        drive,
        INI_NAME
    )

    drive_icon = os.path.join(
        drive,
        ICON_NAME
    )

    return {
        "desktop_ini": os.path.exists(desktop_ini),
        "drive_icon": os.path.exists(drive_icon),
        "customized": (
            os.path.exists(desktop_ini)
            and os.path.exists(drive_icon)
        )
    }
