import os
import hashlib
import json
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading
import time

HASH_RECORD_FILE = "file_hashes.json"

def calculate_hash(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None

def load_hashes():
    if Path(HASH_RECORD_FILE).exists():
        with open(HASH_RECORD_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_hashes(hashes):
    with open(HASH_RECORD_FILE, 'w') as f:
        json.dump(hashes, f, indent=4)

def scan_directory(directory):
    current_hashes = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_hash = calculate_hash(file_path)
            if file_hash:
                current_hashes[file_path] = file_hash
    return current_hashes

def monitor_changes_gui(directory, output, auto=False, interval=10):
    def run_monitor():
        while True:
            old_hashes = load_hashes()
            new_hashes = scan_directory(directory)

            modified, added, deleted = [], [], []

            for path, old_hash in old_hashes.items():
                new_hash = new_hashes.get(path)
                if new_hash is None:
                    deleted.append(path)
                elif new_hash != old_hash:
                    modified.append(path)

            for path in new_hashes:
                if path not in old_hashes:
                    added.append(path)

            output.insert(tk.END, f"\nScanning {directory}...\n")
            if modified:
                output.insert(tk.END, "⚠️ Modified:\n" + "\n".join(modified) + "\n")
            if added:
                output.insert(tk.END, "➕ Added:\n" + "\n".join(added) + "\n")
            if deleted:
                output.insert(tk.END, "❌ Deleted:\n" + "\n".join(deleted) + "\n")
            if not (modified or added or deleted):
                output.insert(tk.END, "✅ No changes.\n")

            output.see(tk.END)
            save_hashes(new_hashes)

            if not auto:
                break
            time.sleep(interval)

    threading.Thread(target=run_monitor, daemon=True).start()

# === GUI SETUP ===
def launch_gui():
    root = tk.Tk()
    root.title("File Integrity Monitor")

    folder_path = tk.StringVar()

    def browse_folder():
        folder = filedialog.askdirectory()
        if folder:
            folder_path.set(folder)

    def start_monitoring(auto=False):
        directory = folder_path.get()
        if not os.path.isdir(directory):
            messagebox.showerror("Error", "Invalid directory selected.")
            return
        monitor_changes_gui(directory, log_output, auto=auto)

    tk.Label(root, text="Select folder to monitor:").pack(pady=5)
    tk.Entry(root, textvariable=folder_path, width=50).pack()
    tk.Button(root, text="Browse", command=browse_folder).pack(pady=5)
    tk.Button(root, text="Run Once", command=lambda: start_monitoring(False)).pack(pady=5)
    tk.Button(root, text="Auto Monitor (10s interval)", command=lambda: start_monitoring(True)).pack(pady=5)

    log_output = scrolledtext.ScrolledText(root, width=80, height=20)
    log_output.pack(padx=10, pady=10)

    root.mainloop()

# === MAIN ===
if __name__ == "__main__":
    launch_gui()
