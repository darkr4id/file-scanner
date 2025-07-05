import os
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox


def format_size(bytes_size):
    """Convert a size in bytes to a human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} EB"


def compute_folder_sizes(root_path):
    """
    Traverse directories under root_path and calculate total size for each folder.
    Returns a dict {folder_path: size_in_bytes}.
    """
    sizes = {}
    # Calculate file sizes
    for dirpath, _, filenames in os.walk(root_path):
        total = 0
        for fname in filenames:
            try:
                full = os.path.join(dirpath, fname)
                total += os.path.getsize(full)
            except OSError:
                continue
        sizes[dirpath] = total
    # Aggregate subfolder sizes into parents
    for path in sorted(sizes, key=lambda p: p.count(os.sep), reverse=True):
        parent = os.path.dirname(path)
        if parent in sizes:
            sizes[parent] += sizes[path]
    return sizes


class FolderScannerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Drive/Folder Size Scanner")
        self.geometry("800x600")
        self.resizable(True, True)

        # Variables
        self.path_var = tk.StringVar()
        self.sort_order = tk.StringVar(value="Descending")

        # Build UI
        self._build_header()
        self._build_treeview()

    def _build_header(self):
        frame = ttk.Frame(self)
        frame.pack(fill='x', pady=5, padx=5)

        ttk.Label(frame, text="Select Drive or Folder:").pack(side='left')
        ttk.Entry(frame, textvariable=self.path_var).pack(side='left', fill='x', expand=True, padx=5)
        ttk.Button(frame, text="Browse", command=self._browse).pack(side='left')

        ttk.Label(frame, text="Sort Order:").pack(side='left', padx=(20, 0))
        ttk.Combobox(
            frame, textvariable=self.sort_order,
            values=["Descending", "Ascending"], width=12,
            state='readonly'
        ).pack(side='left', padx=5)

        ttk.Button(frame, text="Scan", command=self._start_scan).pack(side='left', padx=10)

    def _build_treeview(self):
        columns = ('Path', 'Size')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.heading('Path', text='Folder Path')
        self.tree.heading('Size', text='Size')
        self.tree.column('Path', anchor='w', width=600)
        self.tree.column('Size', anchor='e', width=150)
        self.tree.pack(fill='both', expand=True, padx=5, pady=5)

        # Add vertical scrollbar
        vsb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        vsb.pack(side='right', fill='y')

    def _browse(self):
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)

    def _start_scan(self):
        path = self.path_var.get().strip()
        if not path or not os.path.isdir(path):
            messagebox.showerror("Invalid Path", "Please select a valid folder or drive.")
            return
        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Disable UI
        self._set_controls_state('disabled')
        # Launch scan thread
        threading.Thread(target=self._scan_and_display, args=(path,), daemon=True).start()

    def _scan_and_display(self, path):
        try:
            sizes = compute_folder_sizes(path)
            # Sort
            reverse = self.sort_order.get() == 'Descending'
            sorted_list = sorted(sizes.items(), key=lambda x: x[1], reverse=reverse)
            # Populate treeview
            for folder, size in sorted_list:
                self.tree.insert('', 'end', values=(folder, format_size(size)))
        except Exception as e:
            messagebox.showerror("Error", f"Scan failed: {e}")
        finally:
            self._set_controls_state('normal')

    def _set_controls_state(self, state):
        # Enable/disable buttons and entries
        for widget in self.winfo_children():
            try:
                widget_state = getattr(widget, 'state', None)
                if callable(widget_state):
                    widget.state([state])
            except Exception:
                pass


if __name__ == '__main__':
    app = FolderScannerApp()
    app.mainloop()
