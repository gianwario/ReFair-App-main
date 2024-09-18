import tkinter as tk
from tkinter import ttk, messagebox
import json

class CustomMessageBox:
    def __init__(self, parent, title, results):
        self.window = tk.Toplevel(parent)
        self.window.title(title)

        if not results or all(len(features) == 0 for features in results.values()):
            messagebox.showinfo(title=title, message="No sensitive features have been found")
            self.window.destroy()
            return

        label = ttk.Label(self.window, text="Sensitive Features Found", font=("Arial", 14))
        label.pack(pady=10)

        self.tree = ttk.Treeview(self.window, columns=("task", "sensitive_features"), show='headings', height=10)
        self.tree.heading("task", text="Task")
        self.tree.heading("sensitive_features", text="Sensitive Features")
        self.tree.column("task", anchor=tk.CENTER, width=150)
        self.tree.column("sensitive_features", anchor=tk.CENTER, width=300)

        for task, features in results.items():
            # Le features vengono concatenate in una singola stringa separata da virgole
            features_str = ", ".join(features)
            self.tree.insert("", tk.END, values=(task, features_str))

        self.tree.pack(pady=10)

        # Bottone di chiusura
        close_button = ttk.Button(self.window, text="Close", command=self.window.destroy)
        close_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Bottone di download
        download_button = ttk.Button(self.window, text="Download", command=lambda: self.download_results(results))
        download_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

        self.window.grab_set()

    def download_results(self, results):
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".json",
                                                    filetypes=[("JSON files", "*.json"),
                                                               ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as json_file:
                json.dump(results, json_file, indent=4)
            messagebox.showinfo("Success", "Results have been downloaded successfully!")
