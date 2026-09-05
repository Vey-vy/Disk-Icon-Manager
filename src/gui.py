import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .drive_manager import (
    get_drives,
    get_drive_usage
)

from .icon_manager import (
    apply_icon,
    restore_icon,
    check_icon
)

from .utils import (
    is_admin,
    refresh_explorer
)


class DiskIconMaker:

    def __init__(self):
        self.root = tk.Tk()

        self.root.title("Disk Icon Maker")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        self.drive_var = tk.StringVar()
        self.icon_var = tk.StringVar()

        self.create_ui()
        self.refresh_drives()

    def create_ui(self):

        main = ttk.Frame(
            self.root,
            padding=25
        )

        main.pack(
            fill="both",
            expand=True
        )

        ttk.Label(
            main,
            text="Disk Icon Maker",
            font=("Segoe UI", 22, "bold")
        ).pack(
            anchor="w"
        )

        ttk.Label(
            main,
            text="Customize your Windows drive icons."
        ).pack(
            anchor="w",
            pady=(0, 20)
        )

        # Drive

        ttk.Label(
            main,
            text="Drive"
        ).pack(anchor="w")

        drive_frame = ttk.Frame(main)

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

        # Icon

        ttk.Label(
            main,
            text="Icon file (.ico)"
        ).pack(anchor="w")

        icon_frame = ttk.Frame(main)

        icon_frame.pack(
            fill="x",
            pady=(5, 20)
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

        # Actions

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
            text="Refresh Explorer",
            command=refresh_explorer
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
            text="Check Customization",
            command=self.check
        ).grid(
            row=1,
            column=1,
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
            column=2,
            padx=5,
            pady=5,
            sticky="ew"
        )

        for column in range(3):
            actions.columnconfigure(
                column,
                weight=1
            )

        # Log

        ttk.Label(
            main,
            text="Status"
        ).pack(
            anchor="w",
            pady=(20, 5)
        )

        self.status = tk.Text(
            main,
            height=8,
            state="disabled",
            font=("Consolas", 9)
        )

        self.status.pack(
            fill="both",
            expand=True
        )

        admin_status = (
            "Administrator mode"
            if is_admin()
            else "Standard mode"
        )

        self.log(admin_status)

    def log(self, message):
        self.status.config(state="normal")
        self.status.insert("end", message + "\n")
        self.status.see("end")
        self.status.config(state="disabled")

    def refresh_drives(self):
        drives = get_drives()

        self.drive_box["values"] = drives

        if drives:
            self.drive_box.current(0)

        self.log(
            f"Detected {len(drives)} drive(s)."
        )

    def select_icon(self):
        path = filedialog.askopenfilename(
            title="Select icon",
            filetypes=[
                ("ICO files", "*.ico")
            ]
        )

        if path:
            self.icon_var.set(path)
            self.log(
                f"Selected: {os.path.basename(path)}"
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

        try:
            apply_icon(
                drive,
                icon
            )

            self.log(
                f"Icon applied to {drive}"
            )

            messagebox.showinfo(
                "Disk Icon Maker",
                "Icon applied successfully."
            )

        except Exception as error:
            self.log(
                f"Error: {error}"
            )

            messagebox.showerror(
                "Disk Icon Maker",
                str(error)
            )

    def restore(self):
        drive = self.selected_drive()

        if not drive:
            return

        try:
            restore_icon(drive)

            self.log(
                f"Default icon restored on {drive}"
            )

        except Exception as error:
            self.log(
                f"Error: {error}"
            )

            messagebox.showerror(
                "Disk Icon Maker",
                str(error)
            )

    def check(self):
        drive = self.selected_drive()

        if not drive:
            return

        result = check_icon(drive)

        if result["customized"]:
            text = "Customization is installed correctly."
        elif result["desktop_ini"]:
            text = "desktop.ini exists, but DriveIcon.ico is missing."
        elif result["drive_icon"]:
            text = "DriveIcon.ico exists, but desktop.ini is missing."
        else:
            text = "No customization found."

        self.log(text)

        messagebox.showinfo(
            "Customization Status",
            text
        )

    def drive_info(self):
        drive = self.selected_drive()

        if not drive:
            return

        try:
            total, used, free = get_drive_usage(
                drive
            )

            def gb(value):
                return value / (1024 ** 3)

            messagebox.showinfo(
                "Drive Information",
                f"Drive: {drive}\n\n"
                f"Total: {gb(total):.2f} GB\n"
                f"Used: {gb(used):.2f} GB\n"
                f"Free: {gb(free):.2f} GB"
            )

        except Exception as error:
            messagebox.showerror(
                "Disk Icon Maker",
                str(error)
            )

    def open_drive(self):
        drive = self.selected_drive()

        if not drive:
            return

        try:
            os.startfile(drive)
        except Exception as error:
            messagebox.showerror(
                "Disk Icon Maker",
                str(error)
            )

    def run(self):
        self.root.mainloop()
