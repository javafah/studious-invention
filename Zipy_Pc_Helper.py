
import os
import shutil
import string
import threading
import queue
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

APP_NAME = "NEXOS Space Helper"

BG = "#080B12"
PANEL = "#111722"
CARD = "#161F2D"
BLUE = "#2878FF"
WHITE = "#F4F7FC"
MUTED = "#8996AA"
BORDER = "#263348"


class NexosApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("1000x680")
        self.root.minsize(780, 550)
        self.root.configure(bg=BG)

        self.results = queue.Queue()
        self.scanning = False

        self.setup_theme()
        self.build_ui()
        self.root.after(100, self.check_queue)

    def setup_theme(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TProgressbar",
            troughcolor=PANEL,
            background=BLUE,
            bordercolor=PANEL,
            lightcolor=BLUE,
            darkcolor=BLUE
        )

        style.configure(
            "Treeview",
            background=PANEL,
            foreground=WHITE,
            fieldbackground=PANEL,
            rowheight=30,
            borderwidth=0,
            font=("Segoe UI", 9)
        )

        style.configure(
            "Treeview.Heading",
            background=CARD,
            foreground=WHITE,
            font=("Segoe UI", 10, "bold"),
            relief="flat"
        )

        style.map(
            "Treeview",
            background=[("selected", BLUE)],
            foreground=[("selected", WHITE)]
        )

    def label(self, parent, text, size=10, color=WHITE, bold=False):
        return tk.Label(
            parent,
            text=text,
            bg=parent["bg"],
            fg=color,
            font=("Segoe UI", size, "bold" if bold else "normal")
        )

    def button(self, parent, text, command, primary=False):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=BLUE if primary else CARD,
            fg=WHITE,
            activebackground="#195BCB" if primary else "#263348",
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            padx=17,
            pady=10,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2"
        )

    def build_ui(self):
        self.sidebar = tk.Frame(self.root, bg="#0D121C", width=215)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="NEXOS",
            bg="#0D121C",
            fg=WHITE,
            font=("Segoe UI", 27, "bold")
        ).pack(anchor="w", padx=23, pady=(30, 0))

        tk.Label(
            self.sidebar,
            text="SPACE HELPER",
            bg="#0D121C",
            fg=BLUE,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=26, pady=(0, 40))

        self.nav_button("Dashboard", self.show_dashboard)
        self.nav_button("Folder Analyzer", self.choose_folder)
        self.nav_button("Large Files", self.scan_large_files)

        tk.Label(
            self.sidebar,
            text="VERSION 1.0",
            bg="#0D121C",
            fg=MUTED,
            font=("Segoe UI", 8)
        ).pack(side="bottom", anchor="w", padx=23, pady=22)

        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

        header = tk.Frame(self.main, bg=BG)
        header.pack(fill="x", padx=30, pady=(28, 15))

        self.label(
            header, "Storage Manager", 23, WHITE, True
        ).pack(side="left")

        self.button(
            header, "↻ Refresh", self.refresh_drives, True
        ).pack(side="right")

        self.content = tk.Frame(self.main, bg=BG)
        self.content.pack(
            fill="both", expand=True, padx=30, pady=12
        )

        self.show_dashboard()

    def nav_button(self, text, command):
        tk.Button(
            self.sidebar,
            text="   " + text,
            command=command,
            bg="#0D121C",
            fg=WHITE,
            activebackground=CARD,
            activeforeground=BLUE,
            relief="flat",
            bd=0,
            anchor="w",
            padx=15,
            pady=14,
            font=("Segoe UI", 11),
            cursor="hand2"
        ).pack(fill="x", padx=10, pady=3)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def format_size(self, size):
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024 or unit == "TB":
                return f"{size:.2f} {unit}"
            size /= 1024

    def card(self, parent, title, value, subtitle):
        frame = tk.Frame(
            parent, bg=CARD, padx=17, pady=18
        )
        frame.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(
            frame, text=title, bg=CARD,
            fg=MUTED, font=("Segoe UI", 10)
        ).pack(anchor="w")

        tk.Label(
            frame, text=value, bg=CARD,
            fg=WHITE, font=("Segoe UI", 21, "bold")
        ).pack(anchor="w", pady=9)

        tk.Label(
            frame, text=subtitle, bg=CARD,
            fg=MUTED, font=("Segoe UI", 9)
        ).pack(anchor="w")

    def show_dashboard(self):
        self.clear_content()

        self.label(
            self.content, "Your PC Storage", 16, WHITE, True
        ).pack(anchor="w", pady=(0, 18))

        self.drive_frame = tk.Frame(self.content, bg=BG)
        self.drive_frame.pack(fill="x")

        self.drive_list = tk.Frame(self.content, bg=BG)
        self.drive_list.pack(fill="both", expand=True, pady=25)

        self.refresh_drives()

    def refresh_drives(self):
        if not hasattr(self, "drive_list"):
            return

        for widget in self.drive_frame.winfo_children():
            widget.destroy()

        for widget in self.drive_list.winfo_children():
            widget.destroy()

        drives = []

        for letter in string.ascii_uppercase:
            path = letter + ":\\"
            if os.path.exists(path):
                try:
                    drives.append((path, shutil.disk_usage(path)))
                except OSError:
                    pass

        total = sum(d.total for _, d in drives)
        used = sum(d.used for _, d in drives)
        free = sum(d.free for _, d in drives)

        self.card(
            self.drive_frame, "Total Storage",
            self.format_size(total), "All detected drives"
        )
        self.card(
            self.drive_frame, "Used Storage",
            self.format_size(used), "Occupied space"
        )
        self.card(
            self.drive_frame, "Free Storage",
            self.format_size(free), "Available space"
        )

        self.label(
            self.drive_list, "Detected Drives", 14, WHITE, True
        ).pack(anchor="w", pady=(0, 12))

        for path, usage in drives:
            row = tk.Frame(
                self.drive_list, bg=CARD, padx=17, pady=14
            )
            row.pack(fill="x", pady=5)

            percent = usage.used / usage.total * 100

            top = tk.Frame(row, bg=CARD)
            top.pack(fill="x")

            tk.Label(
                top, text="Drive " + path,
                bg=CARD, fg=WHITE,
                font=("Segoe UI", 11, "bold")
            ).pack(side="left")

            tk.Label(
                top,
                text=f"{percent:.1f}% used  |  "
                     f"{self.format_size(usage.free)} free",
                bg=CARD, fg=MUTED,
                font=("Segoe UI", 9)
            ).pack(side="right")

            ttk.Progressbar(
                row, maximum=100, value=percent
            ).pack(fill="x", pady=(13, 0))

    def choose_folder(self):
        folder = filedialog.askdirectory(
            title="Choose folder to analyze"
        )
        if folder:
            self.start_scan(folder, "folder")

    def scan_large_files(self):
        folder = filedialog.askdirectory(
            title="Choose folder to find large files"
        )
        if folder:
            self.start_scan(folder, "large")

    def start_scan(self, folder, mode):
        if self.scanning:
            messagebox.showinfo(
                "Scanner busy", "Wait for the current scan."
            )
            return

        self.scanning = True
        self.clear_content()

        self.label(
            self.content, "Scanning...", 20, WHITE, True
        ).pack(anchor="w", pady=12)

        tk.Label(
            self.content, text=folder,
            bg=BG, fg=MUTED, wraplength=650
        ).pack(anchor="w")

        progress = ttk.Progressbar(
            self.content, mode="indeterminate"
        )
        progress.pack(fill="x", pady=20)
        progress.start(10)

        self.progress = progress

        self.label(
            self.content, "Please wait...",
            10, MUTED
        ).pack(anchor="w")

        threading.Thread(
            target=self.scan_folder,
            args=(folder, mode),
            daemon=True
        ).start()

    def scan_folder(self, folder, mode):
        files = []
        total_size = 0
        errors = 0

        for current, dirs, filenames in os.walk(folder):
            for filename in filenames:
                path = os.path.join(current, filename)
                try:
                    size = os.path.getsize(path)
                    total_size += size
                    files.append((size, path))
                except OSError:
                    errors += 1

        files.sort(reverse=True)

        self.results.put((
            mode, folder, total_size,
            files[:20], len(files), errors
        ))

    def check_queue(self):
        try:
            while True:
                result = self.results.get_nowait()
                self.display_results(*result)
        except queue.Empty:
            pass

        self.root.after(100, self.check_queue)

    def display_results(
        self, mode, folder, total_size,
        files, file_count, errors
    ):
        self.scanning = False
        self.clear_content()

        self.label(
            self.content, "Scan Complete!", 20, WHITE, True
        ).pack(anchor="w", pady=10)

        info = (
            f"Folder: {folder}\n"
            f"Files scanned: {file_count}\n"
            f"Total size: {self.format_size(total_size)}\n"
            f"Files skipped: {errors}"
        )

        tk.Label(
            self.content, text=info,
            bg=BG, fg=MUTED, justify="left"
        ).pack(anchor="w", pady=12)

        self.label(
            self.content, "Largest Files", 14, WHITE, True
        ).pack(anchor="w", pady=10)

        table_frame = tk.Frame(self.content, bg=PANEL)
        table_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(
            table_frame,
            columns=("size", "file"),
            show="headings",
            height=12
        )

        tree.heading("size", text="File Size")
        tree.heading("file", text="File Location")
        tree.column("size", width=120)
        tree.column("file", width=500)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical",
            command=tree.yview
        )
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for size, path in files:
            tree.insert(
                "", "end",
                values=(self.format_size(size), path)
            )

        tk.Label(
            self.content,
            text="Report only. No files have been deleted.",
            bg=BG, fg=BLUE,
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=12)

        self.button(
            self.content, "← Dashboard",
            self.show_dashboard, True
        ).pack(anchor="w", pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = NexosApp(root)
    root.mainloop()
