📌 Features 🧮 Calculates SHA-256 hash for every file

🔄 Detects:

✅ No changes

⚠️ Modified files

➕ Newly added files

❌ Deleted files

🖥️ Simple GUI with Tkinter

📂 Folder selection dialog

🔁 Supports one-time or auto monitoring (every 10 seconds)

💾 Stores hash data in file_hashes.json

📁 Project Structure bash Copy Edit 📁 FileIntegrityMonitor/ ├── file_hashes.json # Auto-generated file storing hash records ├── file_integrity_monitor.py # Main Python script 🚀 How It Works (Step by Step) User selects a folder through the GUI.

The tool scans all files inside the selected folder.

It calculates a SHA-256 hash for each file.

It compares current hashes with saved hashes in file_hashes.json.

It shows in the GUI:

Which files are added, modified, or deleted

Or no changes

It updates file_hashes.json with the latest hashes after each scan.

You can choose:

📌 Run Once (manual check)

🔁 Auto Monitor (checks every 10 seconds)

🛠️ Requirements Python 3.6+

Tkinter (comes pre-installed with Python)

✅ How to Run ⬇️ Copy the given code ⬇️ copy this for GUI ➡️👉 (python file_integrity_monitor_gui.py) ....IN LAST ⬇️ create a folder in Visual studio code and save the code with .py and paste ⬇️ RUN
