# FileTypeOrganizer - AI Coding Agent Instructions

## Project Overview

FileTypeOrganizer is a Python-based file management utility that organizes files into category-based subfolders. The project follows a clean architecture with external configuration, comprehensive logging, and test coverage.

## Core Architecture

### Main Components
- **`organizer.py`**: Main interactive script with menu-driven interface
- **`categories.json`**: External configuration file defining file type categorizations
- **`test_organizer.py`**: Unit test suite for core functionality
- **`logs/`**: Directory for operation logs (auto-created)

### Key Design Patterns
- **Configuration-driven**: File categories loaded from `categories.json`, not hardcoded
- **Logging-first**: All operations logged to timestamped files in `logs/` directory
- **Error-resilient**: Comprehensive exception handling for file operations
- **Self-excluding**: Script never organizes itself (uses `__file__` comparison)

## Critical Development Guidelines

### File Operations
- Always use `shutil.move()` for file operations, never `os.rename()`
- Create destination directories with `os.makedirs(dest_folder_path, exist_ok=True)`
- Handle common exceptions: `PermissionError`, `FileNotFoundError`, `OSError`
- Log all file operations (success, failure, skips) with detailed context

### Configuration Management
- Categories loaded via `load_categories()` function
- Falls back to default categories if `categories.json` is missing/corrupted
- Config file auto-created with defaults on first run
- Extensions stored in lowercase format (e.g., `".jpg"`)

### Testing Approach
- Tests use temporary directories (`tempfile.mkdtemp()`)
- Mock logging and print functions to avoid output during tests
- Test both success and error conditions
- Validate file categorization logic separately from file operations

## Common Workflows

### Adding New File Types
1. Edit `categories.json` directly, or
2. Modify `default_categories` in `load_categories()` function
3. Extensions must include the dot (e.g., `".newext"`)
4. Add corresponding test cases in `test_organizer.py`

### Running Tests
```bash
python test_organizer.py
```

### Debugging File Operations
- Check `logs/organizer_YYYYMMDD_HHMMSS.log` for detailed operation history
- Use dry run mode (menu options 7-9) to preview operations
- Verify file paths with `os.path.abspath()` for debugging

## Integration Points

### Logging System
- Configured in `setup_logging()` - creates timestamped log files
- Logger instance retrieved with `logging.getLogger(__name__)`
- Log levels: INFO (operations), ERROR (failures), WARNING (skips)

### Menu System
- Options 1-3: Actual file organization
- Options 4-6: File listing (read-only)
- Options 7-9: Dry run (plan without execution)
- Each function receives `categories` parameter from loaded config

### Error Handling Patterns
```python
try:
    # File operation
    operation_result = perform_file_operation()
    logger.info(f"Success: {operation_result}")
except SpecificError as e:
    logger.error(f"Specific error: {e}")
    # User-friendly error message
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    # Fallback handling
```

## File Structure Conventions
- Main script: `organizer.py`
- Config: `categories.json` (JSON format)
- Tests: `test_organizer.py` (unittest framework)
- Logs: `logs/organizer_*.log` (auto-generated)
- Executable: `organizer.exe` (Windows standalone)

## Windows-Specific Considerations
- Uses PowerShell as default shell (`pwsh.exe`)
- Handles long path limitations in error messages
- File permission errors common with locked files
- Path separators handled by `os.path.join()`