# ==============================================================================
# FileOrganizer Script
# Description: An interactive menu-driven script to organize files in a 
#              directory into subfolders based on their file type.
# ==============================================================================

import os
import sys
import shutil
import logging
import json
from datetime import datetime

# Configure logging
def setup_logging():
    """Set up logging configuration for file operations."""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Create a unique log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"logs/organizer_{timestamp}.log"
    
    # Configure logging format
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("FileOrganizer session started")
    logger.info(f"Log file: {log_filename}")
    return logger

def load_categories():
    """Load file categories from the configuration file."""
    config_file = "categories.json"
    default_categories = {
        "Images": [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw", ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps"],
        "Videos": [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mp4", ".m4p", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"],
        "Audio": [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"],
        "Documents": [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ods", ".ppt", ".pptx", ".odp", ".txt", ".rtf", ".md"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".iso", ".dmg"],
        "Scripts": [".py", ".js", ".ts", ".html", ".htm", ".css", ".scss", ".java", ".c", ".cpp", ".h", ".cs", ".sh", ".bat", ".php", ".go", ".swift", ".sql", ".json", ".xml", ".yml", ".yaml"],
        "Executables": [".exe", ".msi", ".app", ".deb", ".rpm"],
        "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
        "Data": [".csv", ".dat", ".db", ".log", ".mdb", ".sav", ".sqlite", ".dbf"],
        "Presentations": [".ppt", ".pptx", ".odp", ".key"],
        "Spreadsheets": [".xls", ".xlsx", ".ods", ".csv"]
    }
    
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                categories = json.load(f)
            logger = logging.getLogger(__name__)
            logger.info(f"Loaded categories from {config_file}")
            return categories
        else:
            # Create the config file with default categories if it doesn't exist
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_categories, f, indent=2)
            logger = logging.getLogger(__name__)
            logger.info(f"Created default {config_file}")
            return default_categories
    except (json.JSONDecodeError, IOError) as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error loading {config_file}: {e}. Using default categories.")
        return default_categories

# This dictionary acts as the "rulebook" for the organization.
# - The "keys" (e.g., "Images") are the names of the folders that will be created.
# - The "values" are lists of file extensions (in lowercase) that belong to that category.
# - You can easily customize this list by editing the categories.json file.

def get_files_to_organize(target_dir):
    """Scans a directory and returns a list of files to be organized."""
    try:
        # Get a list of all items (files and folders) in the target directory.
        all_items = os.listdir(target_dir)
    except FileNotFoundError:
        # If the directory doesn't exist, return None to indicate an error.
        return None

    files = []
    # Loop through every item found in the directory.
    for item in all_items:
        # Create the full path for the item.
        item_path = os.path.join(target_dir, item)
        
        # Check if the item is a file.
        # CRITICAL CHECK: Also check that the file is not this script itself.
        # We compare the absolute paths to ensure it works correctly everywhere.
        if os.path.isfile(item_path) and os.path.abspath(item_path) != os.path.abspath(__file__):
            files.append(item)
    return files

def list_available_files(target_dir):
    """Handles Menu Options 4, 5, 6: Lists all organizable files."""
    print(f"\n--- Listing files in: {os.path.abspath(target_dir)} ---")
    files = get_files_to_organize(target_dir)
    
    # Handle case where the directory was not found.
    if files is None:
        print(f"Error: Directory not found.")
        return
    
    # Handle case where there are no files to list.
    if not files:
        print("No files to list in this directory.")
    else:
        for filename in files:
            print(f"  - {filename}")
    print("-----------------------------------------------------\n")

def perform_organization(target_dir, is_dry_run, categories):
    """Handles Menu Options 1, 2, 3, 7, 8, 9: Performs the dry run or the actual organization."""
    logger = logging.getLogger(__name__)
    
    # Set the header message based on whether it's a dry run or a real one.
    header = f"--- Dry Run: Planning organization in: {os.path.abspath(target_dir)} ---"
    if not is_dry_run:
        header = f"--- Organizing files in: {os.path.abspath(target_dir)} ---"
    print(f"\n{header}")
    
    # Log the operation start
    operation_type = "DRY RUN" if is_dry_run else "ORGANIZATION"
    logger.info(f"{operation_type} started in directory: {os.path.abspath(target_dir)}")

    files_to_organize = get_files_to_organize(target_dir)
    if files_to_organize is None:
        error_msg = f"Error: Directory not found."
        print(error_msg)
        logger.error(f"Directory not found: {os.path.abspath(target_dir)}")
        return

    if not files_to_organize:
        info_msg = "No files to organize in this directory."
        print(info_msg)
        logger.info(f"No files found to organize in: {os.path.abspath(target_dir)}")
        return

    logger.info(f"Found {len(files_to_organize)} files to process")

    # Process each file one by one.
    for filename in files_to_organize:
        # Extract the file extension (e.g., '.jpg') and convert to lowercase.
        file_ext = os.path.splitext(filename)[1].lower()
        
        # Skip files that have no extension.
        if not file_ext:
            skip_msg = f"  - Skipping '{filename}' (no file extension)."
            print(skip_msg)
            logger.info(f"Skipped file without extension: {filename}")
            continue

        # Search for the extension in our categories dictionary.
        found_category = False
        for category, extensions in categories.items():
            if file_ext in extensions:
                # If a match is found, prepare the source and destination paths.
                dest_folder_path = os.path.join(target_dir, category)
                source_file_path = os.path.join(target_dir, filename)

                # This is the main logic branch: either plan or execute the move.
                if is_dry_run:
                    # DRY RUN: Just print the plan.
                    plan_msg = f"  - Plan: Move '{filename}' to '{category}' folder."
                    print(plan_msg)
                    logger.info(f"DRY RUN: Would move '{filename}' to '{category}' folder")
                else:
                    # EXECUTION: Try to move the file, with error handling.
                    try:
                        os.makedirs(dest_folder_path, exist_ok=True)
                        shutil.move(source_file_path, dest_folder_path)
                        success_msg = f"  - Moved '{filename}' to '{category}' folder."
                        print(success_msg)
                        logger.info(f"Successfully moved '{filename}' to '{category}' folder at {dest_folder_path}")
                    except PermissionError:
                        error_msg = f"  - ERROR moving '{filename}': Permission denied. Suggestion: Check if the file is in use or if you have write permissions."
                        print(error_msg)
                        logger.error(f"Permission denied when moving '{filename}' to '{category}' folder")
                    except FileNotFoundError:
                        error_msg = f"  - ERROR moving '{filename}': File not found. Suggestion: It may have been moved or deleted by another process."
                        print(error_msg)
                        logger.error(f"File not found when attempting to move '{filename}'")
                    except OSError as e:
                        if "already exists" in str(e):
                            skip_msg = f"  - SKIPPED: '{filename}' already exists in the '{category}' folder."
                            print(skip_msg)
                            logger.warning(f"File '{filename}' already exists in '{category}' folder - skipped")
                        else:
                            error_msg = f"  - ERROR moving '{filename}': An unexpected OS error occurred."
                            print(error_msg)
                            print(f"    |--> OS Message: {e}")
                            print(f"    |--> Instructions:")
                            print(f"    |    1. Read the 'OS Message' above for specific details.")
                            print(f"    |    2. Check if the destination drive is full.")
                            print(f"    |    3. Check if the file path is becoming too long (a common issue on Windows).")
                            print(f"    |    4. Ensure the filename does not contain characters that are illegal in the destination path.")
                            logger.error(f"OS error when moving '{filename}': {e}")
                
                found_category = True
                break # Stop searching for categories once one is found.
        
        # If the file extension was not found in any category, skip the file.
        if not found_category:
            skip_msg = f"  - Skipping '{filename}' (unknown file type '{file_ext}')."
            print(skip_msg)
            logger.info(f"Skipped unknown file type: {filename} ({file_ext})")

    # Print a final status message.
    if is_dry_run:
        final_msg = "--- Dry Run Complete. No files were moved. ---"
        print(final_msg)
        logger.info("DRY RUN completed successfully")
    else:
        final_msg = "--- File Organization Complete. ---"
        print(final_msg)
        logger.info("File organization completed successfully")

def get_target_dir_from_user():
    """Handles Menu Options 3, 6, 9: Prompts user for a specific directory and validates it."""
    path = input("Enter the full path to the specific folder: ").strip()
    if not os.path.isdir(path):
        print(f"\nError: The directory '{path}' does not exist. Returning to main menu.\n")
        return None
    return path

def main():
    """The main function that runs the interactive menu loop."""
    # Set up logging
    logger = setup_logging()
    
    # Load categories from config file
    categories = load_categories()
    
    # The main loop runs forever until the user chooses to exit.
    while True:
        # Step 1: Display the menu of options.
        print("============================================")
        print("           File Organizer Menu            ")
        print("============================================")
        print("ORGANIZE (MOVE FILES):")
        print("  1. In the CURRENT folder")
        print("  2. In the PARENT folder")
        print("  3. In a SPECIFIC folder")
        print("\nLIST FILES:")
        print("  4. In the CURRENT folder")
        print("  5. In the PARENT folder")
        print("  6. In a SPECIFIC folder")
        print("\nPLAN ORGANIZATION (DRY RUN):")
        print("  7. In the CURRENT folder")
        print("  8. In the PARENT folder")
        print("  9. In a SPECIFIC folder")
        print("\n--------------------------------------------")
        print("  10. Exit")
        print("============================================")
        
        # Step 2: Get the user's choice.
        choice = input("Enter your choice (1-10): ").strip()

        # Step 3: Determine the target directory based on the user's choice.
        target_dir = None
        if choice in ['1', '4', '7']:
            target_dir = "."  # Current directory
        elif choice in ['2', '5', '8']:
            target_dir = ".." # Parent directory
        elif choice in ['3', '6', '9']:
            target_dir = get_target_dir_from_user()
        elif choice == '10':
            print("Exiting.")
            break # Exit the while loop.
        else:
            print("\nInvalid choice. Please enter a number between 1 and 10.\n")
            continue # Skip the rest of the loop and show the menu again.

        # If the user chose a specific folder but entered an invalid path, loop again.
        if target_dir is None:
            continue

        # Step 4: Call the appropriate function based on the user's choice.
        if choice in ['1', '2', '3']:
            # These are the "Organize" options.
            perform_organization(target_dir, is_dry_run=False, categories=categories)
        elif choice in ['4', '5', '6']:
            # These are the "List" options.
            list_available_files(target_dir)
        elif choice in ['7', '8', '9']:
            # These are the "Dry Run" options.
            perform_organization(target_dir, is_dry_run=True, categories=categories)

# This is a standard Python convention. 
# It ensures that the main() function is called only when the script is executed directly.
if __name__ == "__main__":
    main()
