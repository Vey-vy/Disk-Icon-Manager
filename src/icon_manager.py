import os
import shutil

from .utils import (
    set_file_attributes,
    remove_file_attributes,
    refresh_explorer
)


ICON_NAME = "icon.ico"
AUTORUN_NAME = "autorun.inf"
DESKTOP_INI_NAME = "desktop.ini"


FILE_ATTRIBUTE_HIDDEN = 0x02
FILE_ATTRIBUTE_SYSTEM = 0x04
FILE_ATTRIBUTE_NORMAL = 0x80


def _path(drive, filename):
    return os.path.join(
        os.path.abspath(drive),
        filename
    )


def _remove_file(path):

    if not os.path.exists(path):
        return

    try:
        remove_file_attributes(path)
    except Exception:
        pass

    try:
        os.remove(path)
    except PermissionError as error:
        raise PermissionError(
            f"Windows refused access to:\n{path}"
        ) from error


def _write_text(path, content):

    try:
        with open(
            path,
            "w",
            encoding="utf-8",
            newline="\r\n"
        ) as file:
            file.write(content)

    except PermissionError as error:
        raise PermissionError(
            f"Windows refused access to:\n{path}"
        ) from error


def _hide_system(path):

    set_file_attributes(
        path,
        FILE_ATTRIBUTE_HIDDEN
        | FILE_ATTRIBUTE_SYSTEM
    )


def _make_normal(path):

    if os.path.exists(path):
        set_file_attributes(
            path,
            FILE_ATTRIBUTE_NORMAL
        )


def apply_icon(
    drive,
    source_icon,
    use_autorun=True,
    use_desktop_ini=True,
    hide_files=True
):

    drive = os.path.abspath(drive)

    if not os.path.isdir(drive):
        raise FileNotFoundError(
            f"Drive not found:\n{drive}"
        )

    if not os.path.isfile(source_icon):
        raise FileNotFoundError(
            "The selected icon does not exist."
        )

    if not source_icon.lower().endswith(".ico"):
        raise ValueError(
            "The selected file must be an .ico file."
        )

    if not use_autorun and not use_desktop_ini:
        raise ValueError(
            "At least one icon method must be enabled."
        )

    destination_icon = _path(
        drive,
        ICON_NAME
    )

    autorun_file = _path(
        drive,
        AUTORUN_NAME
    )

    desktop_ini = _path(
        drive,
        DESKTOP_INI_NAME
    )

    _remove_file(autorun_file)
    _remove_file(desktop_ini)
    _remove_file(destination_icon)

    try:
        shutil.copyfile(
            source_icon,
            destination_icon
        )
    except PermissionError as error:
        raise PermissionError(
            f"Windows refused access to:\n"
            f"{destination_icon}\n\n"
            f"The drive may be read-only or protected."
        ) from error

    if use_autorun:
        autorun_content = (
            "[Autorun]\n"
            "ICON=icon.ico\n"
        )

        _write_text(
            autorun_file,
            autorun_content
        )

    if use_desktop_ini:
        desktop_content = (
            "[.ShellClassInfo]\n"
            "IconResource=icon.ico,0\n"
        )

        _write_text(
            desktop_ini,
            desktop_content
        )

    if hide_files:
        if os.path.exists(destination_icon):
            _hide_system(destination_icon)

        if use_autorun and os.path.exists(autorun_file):
            _hide_system(autorun_file)

        if use_desktop_ini and os.path.exists(desktop_ini):
            _hide_system(desktop_ini)

    else:
        if os.path.exists(destination_icon):
            _make_normal(destination_icon)

        if os.path.exists(autorun_file):
            _make_normal(autorun_file)

        if os.path.exists(desktop_ini):
            _make_normal(desktop_ini)

    refresh_explorer()


def restore_icon(drive):

    drive = os.path.abspath(drive)

    files = [
        _path(drive, ICON_NAME),
        _path(drive, AUTORUN_NAME),
        _path(drive, DESKTOP_INI_NAME),
    ]

    for path in files:
        _remove_file(path)

    refresh_explorer()


def check_icon(drive):

    drive = os.path.abspath(drive)

    icon = _path(
        drive,
        ICON_NAME
    )

    autorun = _path(
        drive,
        AUTORUN_NAME
    )

    desktop_ini = _path(
        drive,
        DESKTOP_INI_NAME
    )

    autorun_valid = False
    desktop_valid = False

    if os.path.isfile(autorun):
        try:
            with open(
                autorun,
                "r",
                encoding="utf-8"
            ) as file:
                content = file.read().lower()

            autorun_valid = (
                "[autorun]" in content
                and "icon=icon.ico" in content
            )
        except Exception:
            autorun_valid = False

    if os.path.isfile(desktop_ini):
        try:
            with open(
                desktop_ini,
                "r",
                encoding="utf-8"
            ) as file:
                content = file.read().lower()

            desktop_valid = (
                "[.shellclassinfo]" in content
                and "iconresource=icon.ico,0" in content
            )
        except Exception:
            desktop_valid = False

    return {
        "icon": os.path.isfile(icon),
        "autorun": os.path.isfile(autorun),
        "desktop_ini": os.path.isfile(desktop_ini),

        "autorun_valid": autorun_valid,
        "desktop_valid": desktop_valid,

        "customized": (
            os.path.isfile(icon)
            and (
                autorun_valid
                or desktop_valid
            )
        )
    }
