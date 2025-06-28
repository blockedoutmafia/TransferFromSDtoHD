# Copy Photos By Date

A Python script with a simple Tkinter GUI to copy photos from an SD card (or any folder) into a target directory, automatically organizing them into folders by date taken. Features include:

* **Recursive scanning** of a source directory for image files (`.jpg`, `.jpeg`, `.png`, `.heic`, `.arw`).
* **Metadata extraction** using `Pillow` to read EXIF `DateTimeOriginal` when available, falling back to file modification time for RAW files.
* **Folder structure** in `MM-DD-YYYY` format created automatically in the destination directory.
* **GUI feedback** showing current folder, file, progress bar, elapsed time, and remaining time.
* **Overwrite handling** with per-file dialogs: Overwrite, Overwrite All, Skip, Skip All.
* **Logging** of operations and errors to `copy_log.txt` in the destination directory.

## Requirements

* Python 3.7+
* [Pillow](https://pypi.org/project/Pillow/)

```bash
pip install pillow
```

Tkinter is included with most Python installations.

## Installation

1. Clone or download this repository.
2. Ensure you have Python and dependencies installed:

   ```bash
   python -m pip install pillow
   ```
3. Edit the script to set your source (`src_dir`) and destination (`dest_dir`) paths.

## Usage

Run the script directly (double-click or via command line):

```bash
python copy_photos.py
```

1. A GUI window will appear showing:

   * Current **Folder** and **File** being processed.
   * A **Progress Bar** tracking the number of files processed.
   * **Elapsed** time since start.
   * **Remaining** time estimated based on average speed.
2. If a destination file already exists, choose:

   * **Overwrite** / **Overwrite All** / **Skip** / **Skip All**.
3. Upon completion, a summary dialog shows total copied/skipped and duration.

## Logging

All operations and errors are appended to `copy_log.txt` in your destination directory for audit and troubleshooting.

## Customization

* **Extensions**: Modify the `image_exts` and `raw_exts` tuples for additional formats.
* **GUI size**: Adjust `root.geometry("380x180")` for a different window size.
* **Folder naming**: Change `folder_name = dt.strftime("%m-%d-%Y")` to use different date formats.

## Packaging as an Executable

To distribute without requiring Python:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed copy_photos.py
```

This creates a standalone executable in `dist/`.

## License

MIT License — feel free to modify and share.
