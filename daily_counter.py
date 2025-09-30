import datetime
from pathlib import Path
import os
import sys

# --- Configuration ---
# Folder to store the daily text files
LOGS_DIR = "daily_logs"
# ---------------------

def run_daily_counter():
    """Creates a new log file for the current day in the daily_logs directory,
    using the dynamic day count (Day-X) and the date in the filename."""
    
    # 1. Define paths and get date
    logs_path = Path(LOGS_DIR)
    current_date = datetime.date.today()
    date_str = current_date.strftime('%Y-%m-%d')
    
    # 2. Ensure the logs directory exists
    logs_path.mkdir(parents=True, exist_ok=True)
    print(f"Ensured directory '{LOGS_DIR}/' exists.")
    
    # 3. Get the current day count
    # Count the number of .txt files already in the directory.
    existing_files = [p for p in logs_path.iterdir() if p.is_file() and p.suffix == '.txt']
    current_day_count = len(existing_files) + 1
    
    # 4. Format the new filename: Day-X_YYYY-MM-DD.txt
    day_prefix = f"Day-{current_day_count}" 
    filename = f"{day_prefix}_{date_str}.txt"
    log_file_path = logs_path / filename
    
    # 5. Check for duplicate run (file already exists)
    if log_file_path.exists():
        print(f"Skipping update: Log file for today ({filename}) already exists.")
        return 1 # Exit with non-zero code for 'no changes'
    
    # 6. Write the content for the new file
    file_content = f"--- Daily Log: {day_prefix} ---\n"
    file_content += f"Date: {date_str}\n"
    file_content += "Status: Log created automatically.\n"
    
    try:
        with log_file_path.open('w', encoding='utf-8') as f:
            f.write(file_content)
            
        print(f"Successfully created new log file: {log_file_path}")
        return 0 # Exit with zero code for 'success/changes made'

    except Exception as e:
        print(f"An error occurred while writing the file: {e}")
        return 1
        
if __name__ == "__main__":
    exit_code = run_daily_counter()
    
    # Set the output for GitHub Actions to determine if the commit step should run
    if os.environ.get('GITHUB_ACTIONS'):
        # Use the recommended GITHUB_OUTPUT environment file
        with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
            f.write(f"has_changed={'true' if exit_code == 0 else 'false'}\n")
            
    sys.exit(exit_code)
