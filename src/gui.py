import os
import subprocess
import tkinter as tk

from tkinter import (
    filedialog,
    messagebox,
    ttk
)

from .drive_manager import (
    get_drives,
    get_drive_usage,
    get_drive_type,
    is_drive_writable
)

from .icon_manager import (
    apply_icon,
    restore_icon,
    check_icon
)

from .utils import (
    is_admin,
    refresh_explorer,
    restart_explorer,
    reboot_windows
)


class DiskIconMaker:

    def __init__(self):
        self.root = tk.Tk()

        self.root.title(
            "Disk Icon Maker"
        )

        self.root.geometry(
            "760x700"
        )

        self.root.resizable(
            False,
            False
        )

        self.drive_var = tk.StringVar()
        self.icon_var = tk.StringVar()

        # Options
        self.autorun_var = tk.BooleanVar(
            value=True
        )

        self.desktop_ini_var = tk.BooleanVar(
            value=True
        )

        self.hide_files_var = tk.BooleanVar(
            value=True
        )

        self.restart_after_apply_var = tk.BooleanVar(
            value=False
        )

        self.create_ui()
        self.refresh_drives()

    # ========================================================
    # UI
    # ========================================================

    def create_ui(self):

        main = ttk.Frame(
            self.root,
            padding=25
        )

        main.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        ttk.Label(
            main,
            text="Disk Icon Maker",
            font=(
                "Segoe UI",
                22,
                "bold"
            )
        ).pack(
            anchor="w"
        )

        ttk.Label(
            main,
            text=(
                "Customize Windows drive icons "
                "using multiple supported methods."
            )
        ).pack(
            anchor="w",
            pady=(0, 20)
        )

        # ----------------------------------------------------
        # Administrator status
        # ----------------------------------------------------

        admin_text = (
            "Administrator mode"
            if is_admin()
            else
            "WARNING: Standard mode"
        )

        admin_label = ttk.Label(
            main,
            text=admin_text
        )

        admin_label.pack(
            anchor="w",
            pady=(0, 15)
        )

        # ----------------------------------------------------
        # Drive
        # ----------------------------------------------------

        ttk.Label(
            main,
            text="Drive"
        ).pack(
            anchor="w"
        )

        drive_frame = ttk.Frame(
            main
        )

        drive_frame.pack(
            fill="x",
            pady=(5, 15)
        )

        self.drive_box = ttk.Combobox(
            drive_frame,
            textvariable=self.drive_var,
            state="readonly"
        )

        self.drive_box.pack(
            side="left",
            fill="x",
            expand=True
        )

        ttk.Button(
            drive_frame,
            text="Refresh",
            command=self.refresh_drives
        ).pack(
            side="left",
            padx=(8, 0)
        )

        # ----------------------------------------------------
        # Icon
        # ----------------------------------------------------

        ttk.Label(
            main,
            text="Icon file (.ico)"
        ).pack(
            anchor="w"
        )

        icon_frame = ttk.Frame(
            main
        )

        icon_frame.pack(
            fill="x",
            pady=(5, 15)
        )

        ttk.Entry(
            icon_frame,
            textvariable=self.icon_var
        ).pack(
            side="left",
            fill="x",
            expand=True
        )

        ttk.Button(
            icon_frame,
            text="Browse",
            command=self.select_icon
        ).pack(
            side="left",
            padx=(8, 0)
        )

        # ----------------------------------------------------
        # Options
        # ----------------------------------------------------

        options = ttk.LabelFrame(
            main,
            text="Icon methods",
            padding=12
        )

        options.pack(
            fill="x",
            pady=(0, 15)
        )

        ttk.Checkbutton(
            options,
            text="autorun.inf - ICON=icon.ico",
            variable=self.autorun_var
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=4
        )

        ttk.Checkbutton(
            options,
            text="desktop.ini - IconResource=icon.ico,0",
            variable=self.desktop_ini_var
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=4
        )

        ttk.Checkbutton(
            options,
            text="Hide configuration files (Hidden + System)",
            variable=self.hide_files_var
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=5,
            pady=4
        )

        ttk.Checkbutton(
            options,
            text="Restart Explorer automatically after Apply",
            variable=self.restart_after_apply_var
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=5,
            pady=4
        )

        # ----------------------------------------------------
        # Actions
        # ----------------------------------------------------

        actions = ttk.LabelFrame(
            main,
            text="Actions",
            padding=10
        )

        actions.pack(
            fill="x",
            pady=5
        )

        ttk.Button(
            actions,
            text="Apply Icon",
            command=self.apply
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="ew"
        )

        ttk.Button(
            actions,
            text="Restore Default",
            command=self.restore
        ).grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        ttk.Button(
            actions,
            text="Check Customization",
            command=self.check
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=5,
            sticky="ew"
        )

        ttk.Button(
            actions,
            text="Drive Information",
            command=self.drive_info
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="ew"
        )

        ttk.Button(
            actions,
            text="Open Drive",
            command=self.open_drive
        ).grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        ttk.Button(
            actions,
            text="Refresh Explorer",
            command=self.refresh
        ).grid(
            row=1,
            column=2,
            padx=5,
            pady=5,
            sticky="ew"
        )

        ttk.Button(
            actions,
            text="Restart Explorer",
            command=self.restart
        ).grid(
            row=2,
            column=0,
            columnspan=3,
            padx=5,
            pady=5,
            sticky="ew"
        )

        ttk.Button(
            actions,
            text="Reboot Windows",
            command=self.reboot
        ).grid(
            row=3,
            column=0,
            columnspan=3,
            padx=5,
            pady=(10, 5),
            sticky="ew"
        )

        for column in range(3):
            actions.columnconfigure(
                column,
                weight=1
            )

        # ----------------------------------------------------
        # Status
        # ----------------------------------------------------

        ttk.Label(
            main,
            text="Status"
        ).pack(
            anchor="w",
            pady=(15, 5)
        )

        self.status = tk.Text(
            main,
            height=8,
            state="disabled",
            font=(
                "Consolas",
                9
            )
        )

        self.status.pack(
            fill="both",
            expand=True
        )

        self.log(
            admin_text
        )

    # ========================================================
    # Logging
    # ========================================================

    def log(self, message):
        self.status.config(
            state="normal"
        )

        self.status.insert(
            "end",
            message + "\n"
        )

        self.status.see(
            "end"
        )

        self.status.config(
            state="disabled"
        )

    # ========================================================
    # Drives
    # ========================================================

    def refresh_drives(self):

        drives = get_drives()

        self.drive_box["values"] = drives

        if drives:
            self.drive_box.current(0)

        self.log(
            f"Detected {len(drives)} drive(s)."
        )

    def selected_drive(self):

        drive = self.drive_var.get()

        if not drive:
            messagebox.showwarning(
                "Disk Icon Maker",
                "Please select a drive."
            )

            return None

        return drive

    # ========================================================
    # Icon
    # ========================================================

    def select_icon(self):

        path = filedialog.askopenfilename(
            title="Select icon",
            filetypes=[
                (
                    "ICO files",
                    "*.ico"
                )
            ]
        )

        if path:

            self.icon_var.set(
                path
            )

            self.log(
                "Selected: "
                + os.path.basename(path)
            )

    # ========================================================
    # Apply
    # ========================================================

    def apply(self):

        drive = self.selected_drive()

        if not drive:
            return

        icon = self.icon_var.get()

        if not icon:
            messagebox.showwarning(
                "Disk Icon Maker",
                "Please select an icon."
            )

            return

        if not is_admin():
            messagebox.showerror(
                "Administrator required",
                "Disk Icon Maker must run as administrator.\n\n"
                "Please launch the application again "
                "with administrator privileges."
            )

            return

        if not self.autorun_var.get() and not self.desktop_ini_var.get():

            messagebox.showwarning(
                "No method selected",
                "Enable at least one icon method."
            )

            return

        # ----------------------------------------------------
        # Test write access
        # ----------------------------------------------------

        self.log(
            f"Testing write access to {drive}..."
        )

        if not is_drive_writable(drive):

            messagebox.showerror(
                "Permission denied",
                f"Windows does not allow writing to:\n\n"
                f"{drive}\n\n"
                f"The drive may be read-only, protected, "
                f"or inaccessible."
            )

            self.log(
                f"Write access denied: {drive}"
            )

            return

        # ----------------------------------------------------
        # Apply
        # ----------------------------------------------------

        try:

            apply_icon(
                drive=drive,
                source_icon=icon,
                use_autorun=self.autorun_var.get(),
                use_desktop_ini=self.desktop_ini_var.get(),
                hide_files=self.hide_files_var.get()
            )

            methods = []

            if self.autorun_var.get():
                methods.append(
                    "autorun.inf"
                )

            if self.desktop_ini_var.get():
                methods.append(
                    "desktop.ini"
                )

            self.log(
                "Applied using: "
                + ", ".join(methods)
            )

            self.log(
                f"Icon applied to {drive}"
            )

            # ------------------------------------------------
            # Optional Explorer restart
            # ------------------------------------------------

            if self.restart_after_apply_var.get():

                self.log(
                    "Restarting Explorer..."
                )

                restart_explorer()

            messagebox.showinfo(
                "Disk Icon Maker",
                "The drive icon configuration "
                "was applied successfully."
            )

        except Exception as error:

            self.log(
                f"Error: {type(error).__name__}: {error}"
            )

            messagebox.showerror(
                "Disk Icon Maker",
                str(error)
            )

    # ========================================================
    # Restore
    # ========================================================

    def restore(self):

        drive = self.selected_drive()

        if not drive:
            return

        if not is_admin():

            messagebox.showerror(
                "Administrator required",
                "Administrator privileges are required."
            )

            return

        answer = messagebox.askyesno(
            "Restore Default",
            f"Remove all custom icon files from {drive}?\n\n"
            "This will remove:\n"
            "- icon.ico\n"
            "- autorun.inf\n"
            "- desktop.ini"
        )

        if not answer:
            return

        try:

            restore_icon(
                drive
            )

            self.log(
                f"Default icon restored on {drive}"
            )

            messagebox.showinfo(
                "Disk Icon Maker",
                "Custom icon configuration removed."
            )

        except Exception as error:

            self.log(
                f"Error: {type(error).__name__}: {error}"
            )

            messagebox.showerror(
                "Disk Icon Maker",
                str(error)
            )

    # ========================================================
    # Check
    # ========================================================

    def check(self):

        drive = self.selected_drive()

        if not drive:
            return

        try:

            result = check_icon(
                drive
            )

            lines = [
                f"Drive: {drive}",
                "",
                f"icon.ico: "
                f"{'YES' if result['icon'] else 'NO'}",

                f"autorun.inf: "
                f"{'YES' if result['autorun'] else 'NO'}",

                f"autorun valid: "
                f"{'YES' if result['autorun_valid'] else 'NO'}",

                f"desktop.ini: "
                f"{'YES' if result['desktop_ini'] else 'NO'}",

                f"desktop.ini valid: "
                f"{'YES' if result['desktop_valid'] else 'NO'}",

                "",
                f"Customized: "
                f"{'YES' if result['customized'] else 'NO'}"
            ]

            text = "\n".join(
                lines
            )

            self.log(
                text
            )

            messagebox.showinfo(
                "Customization Status",
                text
            )

        except Exception as error:

            messagebox.showerror(
                "Disk Icon Maker",
                str(error)
            )

    # ========================================================
    # Drive information
    # ========================================================

    def drive_info(self):

        drive = self.selected_drive()

        if not drive:
            return

        try:

            total, used, free = get_drive_usage(
                drive
            )

            def gb(value):
                return value / (
                    1024 ** 3
                )

            drive_type = get_drive_type(
                drive
            )

            writable = is_drive_writable(
                drive
            )

            text = (
                f"Drive: {drive}\n\n"
                f"Type: {drive_type}\n"
                f"Writable: "
                f"{'Yes' if writable else 'No'}\n\n"
                f"Total: {gb(total):.2f} GB\n"
                f"Used: {gb(used):.2f} GB\n"
                f"Free: {gb(free):.2f} GB"
            )

            messagebox.showinfo(
                "Drive Information",
                text
            )

        except Exception as error:

            messagebox.showerror(
                "Disk Icon Maker",
                str(error)
            )

    # ========================================================
    # Open drive
    # ========================================================

    def open_drive(self):

        drive = self.selected_drive()

        if not drive:
            return

        try:
            os.startfile(
                drive
            )

        except Exception as error:

            messagebox.showerror(
                "Disk Icon Maker",
                str(error)
            )

    # ========================================================
    # Explorer
    # ========================================================

    def refresh(self):

        try:

            refresh_explorer()

            self.log(
                "Explorer refreshed."
            )

        except Exception as error:

            self.log(
                f"Error: {error}"
            )

    def restart(self):

        answer = messagebox.askyesno(
            "Restart Explorer",
            "Restart Windows Explorer now?"
        )

        if not answer:
            return

        try:

            self.log(
                "Restarting Explorer..."
            )

            restart_explorer()

            self.log(
                "Explorer restarted."
            )

        except Exception as error:

            messagebox.showerror(
                "Disk Icon Maker",
                str(error)
            )

    # ========================================================
    # Reboot
    # ========================================================

    def reboot(self):

        answer = messagebox.askyesno(
            "Reboot Windows",
            "Windows will restart in 5 seconds.\n\n"
            "Save your work before continuing.\n\n"
            "Do you want to restart Windows?"
        )

        if not answer:
            return

        try:

            self.log(
                "Windows will restart in 5 seconds..."
            )

            reboot_windows(
                delay=5
            )

            self.root.destroy()

        except Exception as error:

            messagebox.showerror(
                "Reboot Windows",
                str(error)
            )

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = DiskIconMaker()
    app.run()
