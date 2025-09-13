# FileTypeOrganizer

A user-friendly, interactive Python script to organize files in a directory into clean, category-based subfolders.

## Features

- **Interactive Menu:** An easy-to-use menu to choose actions and target directories (current, parent, or specific path).
- **Multiple Actions:** Organize files, list files, or perform a safe "dry run" to see a plan.
- **Comprehensive Categorization:** Sorts files into folders like `Images`, `Documents`, `Videos`, `Archives`, and more, based on their extension.
- **Customizable Configuration:** Easily add new file types or change categories by editing the `categories.json` configuration file.
- **Comprehensive Logging:** All operations are logged to timestamped files in the `logs/` directory for full traceability.
- **Robust Error Handling:** Gracefully handles common issues like file-already-exists, permissions errors, and locked files without crashing.
- **Professional Testing:** Includes a complete unit test suite (`test_organizer.py`) for reliable functionality.
- **Self-Contained:** No external libraries needed. Runs with a standard Python installation.

## Download the Executable

For Windows users, you can download the standalone `organizer.exe` directly from the [Releases page](https://github.com/rohitkusharma/FileTypeOrganizer/releases/tag/v1.0.0).

## Requirements

- Python 3.x

## How to Use (Source Code)

If you prefer to run the Python source code directly:

1.  Open a terminal or command prompt.
2.  Navigate to the directory where the script is located:
    ```sh
    cd path\to\FileTypeOrganizer
    ```
3.  Run the script:
    ```sh
    python organizer.py
    ```
4.  The script will present a menu of options. Enter the number corresponding to the action you want to perform and press Enter.

    - **Organize Options (1-3):** Will move files into category folders.
    - **List Options (4-6):** Will show you which files are available to be organized.
    - **Dry Run Options (7-9):** Will show you a plan of which files will be moved where, without actually moving anything.

## Customization

You can customize file categories by editing the `categories.json` file. This file is automatically created with default categories when you first run the script.

For example, to add a category for CAD files, you could add a new entry to `categories.json`:

```json
{
  "CAD": [".dwg", ".dxf"],
  "Images": [".jpg", ".jpeg", ".png", "..."],
  "...": "..."
}
```

## Project Structure

- `organizer.py` - Main script with interactive menu
- `categories.json` - Configuration file for file type categories
- `test_organizer.py` - Unit test suite
- `logs/` - Directory containing operation logs (auto-created)
- `requirements.txt` - Python dependencies (none required)

## Development

### Running Tests
```sh
python test_organizer.py
```

### Viewing Logs
All file operations are logged to timestamped files in the `logs/` directory. Check these logs for detailed information about what files were moved, skipped, or encountered errors.

