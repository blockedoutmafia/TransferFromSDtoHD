import shutil
from pathlib import Path
from datetime import datetime, timedelta
from PIL import Image
import tkinter as tk
from tkinter import ttk, messagebox

# Source and destination directories
src_dir = Path(r"I:/DCIM")
dest_dir = Path(r"G:/2025")
dest_dir.mkdir(parents=True, exist_ok=True)
log_path = dest_dir / "copy_log.txt"

# Supported image extensions
image_exts = ('.jpg', '.jpeg', '.png', '.heic', '.arw')
raw_exts = ('.arw',)

# Gather all image files
files = [p for p in src_dir.rglob("*") if p.is_file() and p.suffix.lower() in image_exts]
total_files = len(files)

# Setup GUI: compact size, side-by-side elapsed and remaining

def setup_gui():
    root = tk.Tk()
    root.title("Photo Copy Progress")
    root.geometry("380x180")  # smaller window
    folder_label = ttk.Label(root, text="Folder: ")
    folder_label.pack(fill='x', padx=8, pady=(8, 4))
    file_label = ttk.Label(root, text="File: ")
    file_label.pack(fill='x', padx=8, pady=(0, 8))
    progress = ttk.Progressbar(root, length=360, maximum=total_files, mode='determinate')
    progress.pack(fill='x', padx=8, pady=(0, 8))
    time_frame = ttk.Frame(root)
    time_frame.pack(fill='x', padx=8, pady=(0, 8))
    elapsed_label = ttk.Label(time_frame, text="Elapsed: 00:00:00")
    elapsed_label.pack(side='left')
    remaining_label = ttk.Label(time_frame, text="Remaining: 00:00:00")
    remaining_label.pack(side='right')
    root.update()
    return root, folder_label, file_label, progress, elapsed_label, remaining_label

root, folder_label, file_label, progress, elapsed_label, remaining_label = setup_gui()

# Flags for overwrite decisions
overwrite_all = False
skip_all = False

def ask_overwrite(filepath):
    dialog = tk.Toplevel(root)
    dialog.title("File Exists")
    ttk.Label(dialog, text=f"File exists: {filepath.name}").pack(padx=20, pady=10)
    choice = {'value': None}
    def set_choice(val):
        choice['value'] = val
        dialog.destroy()
    btn_frame = ttk.Frame(dialog)
    btn_frame.pack(pady=10)
    ttk.Button(btn_frame, text="Overwrite",    command=lambda: set_choice('yes')).grid(row=0, column=0, padx=5)
    ttk.Button(btn_frame, text="Overwrite All",command=lambda: set_choice('yes_all')).grid(row=0, column=1, padx=5)
    ttk.Button(btn_frame, text="Skip",         command=lambda: set_choice('no')).grid(row=0, column=2, padx=5)
    ttk.Button(btn_frame, text="Skip All",    command=lambda: set_choice('no_all')).grid(row=0, column=3, padx=5)
    dialog.transient(root)
    dialog.grab_set()
    while choice['value'] is None:
        root.update()
    return choice['value']

# Main copy loop with logging
with open(log_path, "a", encoding="utf-8") as log:
    start_time = datetime.now()
    log.write(f"{start_time.isoformat()} - Starting copy from {src_dir} to {dest_dir}\n")
    copied = 0
    skipped = 0

    for idx, filepath in enumerate(files, 1):
        root.update()
        folder_label.config(text=f"Folder: {filepath.parent.name}")
        file_label.config(text=f"File: {filepath.name}")
        progress['value'] = idx

        # Calculate elapsed time
        elapsed = datetime.now() - start_time
        total_elapsed_sec = int(elapsed.total_seconds())
        eh, rem = divmod(total_elapsed_sec, 3600)
        em, es = divmod(rem, 60)
        elapsed_label.config(text=f"Elapsed: {eh:02d}:{em:02d}:{es:02d}")

        # Calculate remaining time
        avg_sec = elapsed.total_seconds() / idx
        remaining_sec = int(avg_sec * (total_files - idx))
        rh, rem2 = divmod(remaining_sec, 3600)
        rm, rs = divmod(rem2, 60)
        remaining_label.config(text=f"Remaining: {rh:02d}:{rm:02d}:{rs:02d}")
        root.update()

        # Determine date taken
        ext = filepath.suffix.lower()
        if ext in raw_exts:
            dt = datetime.fromtimestamp(filepath.stat().st_mtime)
        else:
            try:
                with Image.open(filepath) as img:
                    exif = img._getexif()
                    if exif and 36867 in exif:
                        dt = datetime.strptime(exif[36867], "%Y:%m:%d %H:%M:%S")
                    else:
                        dt = datetime.fromtimestamp(filepath.stat().st_mtime)
            except Exception:
                dt = datetime.fromtimestamp(filepath.stat().st_mtime)

        # Prepare destination path
        folder_name = dt.strftime("%m-%d-%Y")
        target_folder = dest_dir / folder_name
        target_folder.mkdir(parents=True, exist_ok=True)
        target_file = target_folder / filepath.name

        # Handle existing files
        if target_file.exists():
            if skip_all:
                skipped += 1
                continue
            if not overwrite_all:
                resp = ask_overwrite(filepath)
                if resp == 'yes':
                    pass
                elif resp == 'yes_all':
                    overwrite_all = True
                elif resp == 'no':
                    skipped += 1
                    continue
                elif resp == 'no_all':
                    skip_all = True
                    skipped += 1
                    continue

        # Copy file
        try:
            shutil.copy2(filepath, target_file)
            copied += 1
        except Exception as e:
            log.write(f"{datetime.now().isoformat()} - Error copying {filepath}: {e}\n")

    end_time = datetime.now()
    log.write(f"{end_time.isoformat()} - Completed. Files: {total_files}, copied: {copied}, skipped: {skipped}, Duration: {end_time - start_time}\n")

# Final summary dialog
message = f"Copied {copied} of {total_files} files" + (f", skipped {skipped}" if skipped else "") + f" in {str(end_time - start_time).split('.')[0]}"
messagebox.showinfo("Done", message)
root.destroy()
