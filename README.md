# Simple Backup Utility

A Python script to create timestamped, compressed backups (e.g., ZIP archives) of specified source directories to a designated backup location. Configuration is managed via an external JSON file, and operations are logged for auditing.

## Features

*   **Configurable Backups:** Define multiple source directories and a single destination directory in a JSON configuration file.
*   **Timestamped Archives:** Each backup archive is named with the source directory's name and a timestamp (YYYYMMDD_HHMMSS) for easy identification and versioning.
*   **Archive Format Options:** Supports different archive formats like 'zip' (default) or 'tar' (configurable in the JSON file).
*   **Command-Line Interface:** Specify the configuration file path using a command-line argument.
*   **Logging:** All operations, successes, warnings (e.g., missing source directories), and errors are logged to both the console and a `backup.log` file.
*   **Directory Creation:** Automatically creates the main backup destination directory if it doesn't exist.
*   **Error Handling:** Gracefully handles missing source directories and configuration file issues.

## Requirements

*   Python 3.6+
*   Standard Python libraries: `os`, `shutil`, `datetime`, `json`, `argparse`, `logging`.
*   (For `.tar`, `.gztar`, `.bztar` formats, your system may need corresponding command-line utilities installed if Python's `shutil` relies on them).

## Setup

1.  **Save the Script:**
    Save the main Python script as `backup_tool.py`.

2.  **Create a Configuration File:**
    Create a JSON configuration file (e.g., `backup_config.json`) in the same directory as the script, or specify its path when running the script. This file defines what to back up and where.

    **Example `backup_config.json`:**
    ```json
    {
      "sources": [
        "./project_alpha",
        "/Users/yourname/Documents/important_files",
        "D:/work/project_beta"
      ],
      "destination": "./my_backups/archives",
      "archive_format": "zip"
    }
    ```
    *   **`sources`**: A list of strings, where each string is a path to a directory you want to back up. Paths can be relative (to where the script is run) or absolute.
    *   **`destination`**: A string representing the path to the directory where backup archives will be stored.
    *   **`archive_format`**: (Optional) The format for the archive. Common values: `"zip"` (default), `"tar"`, `"gztar"` (gzipped tar), `"bztar"` (bzipped tar).

3.  **Source Directories:**
    Ensure the directories listed in the `"sources"` array of your configuration file actually exist.

## How to Use

Open your terminal or command prompt, navigate to the directory containing `backup_tool.py` (or ensure it's in your PATH), and run the script.

**Basic Usage (using default `backup_config.json`):**
```bash
python backup_tool.py


Specifying a Configuration File:
python backup_tool.py -c /path/to/your/custom_config.json
or
python backup_tool.py --config my_other_backup_plan.json


Command-Line Arguments:

-h, --help: Show the help message and exit.
-c CONFIG_PATH, --config CONFIG_PATH: Path to the JSON configuration file. (Default: backup_config.json in the script's directory).

Output
Console: The script will print log messages to the console indicating its progress, successes, warnings, and any errors.
Backup Archives: Timestamped archive files (e.g., project_alpha_20231027_153000.zip) will be created in the destination directory specified in your configuration file.
Log File: A backup.log file will be created (or appended to) in the same directory where backup_tool.py is run. This file contains a detailed history of all backup operations.

How It Works

Logging Setup: Initializes logging to output to both console and backup.log.
Argument Parsing: Uses argparse to determine the path to the configuration file.
Configuration Loading: Reads and parses the specified JSON configuration file. Validates essential fields.

Main Backup Process:

Iterates through each source directory defined in the configuration.
Checks if the source directory exists. If not, logs a warning and skips it.
For each valid source, it constructs a unique, timestamped archive name.
Uses shutil.make_archive() to create a compressed archive (e.g., ZIP) of the source directory's contents.
Logs the success or failure of each backup operation.

Summary: After processing all sources, prints and logs a summary of successful and failed backups.

Future Improvements (TODO)
More sophisticated exclusion rules for files/folders within sources.
Basic backup retention policies (e.g., keep only the last N backups for each source).
Encryption for backup archives.
Support for cloud storage destinations.
Email notifications for backup completion or failure.

---
