import datetime
from pathlib import Path
import os
import sys

# --- Configuration ---
# Folder to store the daily text files
LOGS_DIR = "daily_logs"
# ---------------------

def run_daily_counter():
    """
    Automated process to create a daily log file, calculating the current day 
    count based on existing logs.
    
    Returns 0 on successful file creation, 1 on skip or error.
    """
    
    logs_path = Path(LOGS_DIR)
    current_date = datetime.date.today()
    date_str = current_date.strftime('%Y-%m-%d')
    
    # 1. Directory creation and error handling
    try:
        # Create the logs directory if it doesn't exist. 'exist_ok=True' prevents an error 
        # if the directory is already there.
        logs_path.mkdir(parents=True, exist_ok=True)
        print(f"Directory '{LOGS_DIR}/' checked/created successfully.")
    except OSError as e:
        print(f"FATAL ERROR: Could not create directory '{LOGS_DIR}/': {e}")
        return 1

    # 2. Calculate the current day count
    try:
        # We strictly count files that end in .txt and are not directories.
        # This determines the sequential day number.
        existing_files = [p for p in logs_path.iterdir() if p.is_file() and p.suffix == '.txt']
        current_day_count = len(existing_files) + 1
    except Exception as e:
        print(f"ERROR: Failed to read files in '{LOGS_DIR}/' to determine count: {e}")
        return 1
    
    # 3. Format filename and path
    day_prefix = f"Day-{current_day_count}" 
    filename = f"{day_prefix}_{date_str}.txt"
    log_file_path = logs_path / filename
    
    # 4. Critical check: Prevent duplicate run (idempotence)
    if log_file_path.exists():
        print(f"Skipping update (Exit Code 1): Log file for today ({filename}) already exists.")
        # If the file exists, we consider this a successful execution of the check,
        # but return 1 to prevent the GitHub Action from committing unnecessary changes.
        return 1 
    
    # 5. Prepare content and write the new file
    file_content = f"--- Daily Log: {day_prefix} ---\n"
    file_content += f"Date: {date_str}\n"
    file_content += "Status: Log created automatically.\n"
    
    try:
        # Use 'w' (write) mode since the file existence was checked above.
        with log_file_path.open('w', encoding='utf-8') as f:
            f.write(file_content)
            
        print(f"SUCCESS (Exit Code 0): Created new log file: {log_file_path}")
        return 0 

    except IOError as e:
        # Catch specific I/O errors (permission denied, disk full, etc.)
        print(f"CRITICAL WRITE ERROR: Could not write file {log_file_path}: {e}")
        return 1
        
if __name__ == "__main__":
    exit_code = run_daily_counter()
    
    # Logic for signaling the GitHub Action based on the exit code
    if os.environ.get('GITHUB_ACTIONS'):
        # This is the standard way to communicate status to subsequent steps in the workflow
        output_value = 'true' if exit_code == 0 else 'false'
        print(f"::set-output name=has_changed::{output_value}")
        # Note: Using GITHUB_OUTPUT environment variable is the modern standard,
        # but the ::set-output command is often used for maximum compatibility.
        # The previous version used GITHUB_OUTPUT correctly, but for clarity/debugging 
        # we'll use the print method here as it's often easier to see in logs.
            
    sys.exit(exit_code)
