
# Sync Project

## Overview
This program performs one-way synchronization between two folders, ensuring that the **replica folder** matches the contents of the **source folder**. 
Synchronization runs periodically, and all changes (updates, additions, and removals) are displayed in the console and logged to a file.

---

## Key Features
- Copies new or updated files from the source to the replica.
- Removes files or folders in the replica that no longer exist in the source.
- Logs all synchronization actions with timestamps.
- Runs at regular intervals specified by the user.

---

## Requirements
- Python 3.x .

---

## How to Run

Run the script with the following command:

```bash
python sync.py [--source SOURCE] [--replica REPLICA] [--log-file LOG_FILE] [--time-interval TIME_INTERVAL]
```

### Arguments:
- `--source`: Path to the source folder (default: `"source"`).
- `--replica`: Path to the replica folder (default: `"replica"`).
- `--log-file`: Path to the log file (default: `"sync.log"`).
- `--time-interval`: Time interval for synchronization in seconds (default: `60`).

### Example
To sync `source` with `replica` every minute and log actions to `sync.log`:

```bash
python sync.py --source source --replica replica --log-file sync.log --time-interval 60
```

---

## Notes
- Uses **MD5 hashing** to detect changes in files.
- Automatically creates the replica folder if it doesn’t exist.
- If the source folder is missing, the program will exit with an error.
- Press `CTRL+C` to stop the program.

---