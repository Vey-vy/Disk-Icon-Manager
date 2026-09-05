import os
import shutil

from .utils import (
    set_file_attributes,
    refresh_explorer
)


ICON_NAME = "DriveIcon.ico"
INI_NAME = "desktop.ini"

FILE_ATTRIBUTE_READONLY = 0x01
FILE_ATTRIBUTE_HIDDEN = 0x02
FILE_ATTRIBUTE_SYSTEM = 0x04
FILE_ATTRIBUTE_NORMAL = 0x80


def remove_attributes(path):
    if os.path.exists(path):
        try:
            set_file_attributes(
                path,
                FILE_ATTRIBUTE_NORMAL
            )
        except Exception:
            pass


def apply_icon(drive, source_icon):
    if not os.path.isfile(source_icon):
        raise FileNotFoundError(
            "The selected icon does not exist."
        )

    if not source_icon.lower().endswith(".ico"):
        raise ValueError(
            "The selected file must be an .ico file."
        )

    drive = os.path.abspath(drive)

    destination_icon = os.path.join(
        drive,
        ICON_NAME
    )

    desktop_ini = os.path.join(
        drive,
        INI_NAME
    )

    remove_attributes(destination_icon)
    remove_attributes(desktop_ini)

    if os.path.exists(destination_icon):
        os.remove(destination_icon)

    if os.path.exists(desktop_ini):
        os.remove(desktop_ini)

    try:
        shutil.copyfile(
            source_icon,
            destination_icon
        )
    except PermissionError as error:
        raise PermissionError(
            f"Windows refused access to:\n"
            f"{destination_icon}\n\n"
            f"Make sure the selected drive is writable."
        ) from error

    content = (
        "[.ShellClassInfo]\n"
        "IconResource=DriveIcon.ico,0\n"
    )

    try:
        with open(
            desktop_ini,
            "w",
            encoding="utf-8",
            newline="\r\n"
        ) as file:
            file.write(content)

    except PermissionError as error:
        remove_attributes(destination_icon)

        try:
            os.remove(destination_icon)
        except OSError:
            pass

        raise PermissionError(
            f"Windows refused access to:\n"
            f"{desktop_ini}\n\n"
            f"Make sure the selected drive is writable."
        ) from error

    set_file_attributes(
        desktop_ini,
        FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM
    )

    refresh_explorer()


def restore_icon(drive):
    drive = os.path.abspath(drive)

    desktop_ini = os.path.join(
        drive,
        INI_NAME
    )

    drive_icon = os.path.join(
        drive,
        ICON_NAME
    )

    if os.path.exists(desktop_ini):
        remove_attributes(desktop_ini)

        try:
            os.remove(desktop_ini)
        except PermissionError as error:
            raise PermissionError(
                f"Unable to remove:\n{desktop_ini}"
            ) from error

    if os.path.exists(drive_icon):
        remove_attributes(drive_icon)

        try:
            os.remove(drive_icon)
        except PermissionError as error:
            raise PermissionError(
                f"Unable to remove:\n{drive_icon}"
            ) from error

    refresh_explorer()


def check_icon(drive):
    drive = os.path.abspath(drive)

    desktop_ini = os.path.join(
        drive,
        INI_NAME
    )

    drive_icon = os.path.join(
        drive,
        ICON_NAME
    )

    return {
        "desktop_ini": os.path.isfile(desktop_ini),
        "drive_icon": os.path.isfile(drive_icon),
        "customized": (
            os.path.isfile(desktop_ini)
            and os.path.isfile(drive_icon)
        )
    }
