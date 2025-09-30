![GitHub repo size](https://img.shields.io/github/repo-size/4uffin/daily-count)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-brightgreen)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

# **📅 Automated Daily Log Tracker**

This repository contains a simple, self-managing system to automatically track a daily streak or continuous counter. It runs once per day using **GitHub Actions**, executes a Python script to calculate the current day count, and commits a new, timestamped log file back to the repository.

The resulting files are named with the format: ```Day-X_YYYY-MM-DD.txt```.

## **📂 Project Structure**

```
├── .github/  
│   └── workflows/  
│       └── daily_run.yml    # GitHub Action configuration  
├── daily_logs/              # Automated output folder  
│   └── Day-1_2025-09-29.txt  
│   └── Day-2_2025-09-30.txt  
└── daily_counter.py         # The core Python logic
```

## **🚀 Setup and Installation**

Follow these steps to deploy the tracker in your own GitHub repository.

### **1. Repository Preparation**

1. **Create Repository:** Start a new GitHub repository.  
2. **Add Files:** Add the ```daily_counter.py``` script and the ```.github/workflows/daily_run.yml``` file to the root of your repository.  
3. **(Optional but Recommended):** Create the empty directory ```daily_logs``` locally and add a placeholder file (e.g., ```.gitkeep```) to ensure the directory is tracked by Git, though the Python script will create it if needed.

### **2. GitHub Action Configuration**

The GitHub Action is configured to run automatically, but you must ensure it has the necessary permissions to commit the files.

**No additional secrets are needed.** The action uses the built-in ```GITHUB_TOKEN``` which already has the permissions required by the workflow file ```(permissions: contents: write)```.

### **3. Execution Schedule**

The workflow is currently scheduled to run every day at **midnight UTC** ```(0 0 * * *)```.

If you want to manually trigger the first run or test the process:

1. Go to the **Actions** tab in your repository.  
2. Select the **Daily Log Creator** workflow.  
3. Click the **Run workflow** dropdown and select the ```main``` branch.

## **⚙️ How It Works**

The system ensures **idempotence** (it won't create duplicate files if run multiple times in one day).

1. **Daily Trigger:** GitHub runs the ```daily_run.yml``` job at the scheduled time.  
2. **Count Calculation:** ```daily_counter.py``` looks inside the ```daily_logs/``` folder and counts all existing ```.txt``` files. This count is used to determine the sequential **Day-X** number.  
3. **Duplicate Check:** The script generates the expected filename (e.g., ```Day-15_2026-03-05.txt```) and checks if it already exists.  
   * **If file exists:** The script exits with a ```non-zero exit code (1)```, and the commit step is skipped.  
   * **If file is new:** The script creates the file and exits with a ```zero exit code (0)```.  
4. **Commit:** The GitHub Action sees the ```success status (0)```, stages the new file ```(git add daily_logs/*.txt)```, commits it, and pushes the change to the ```main``` branch.

## **🐍 Python Dependencies**

The core logic relies solely on the Python Standard Library.

| Module | Purpose |
| :---- | :---- |
| ```datetime``` | Used to get the current date ```(YYYY-MM-DD)```. |
| ```pathlib``` | Used for reliable, cross-platform file and directory manipulation. |
| ```os```, ```sys``` | Used for interacting with the system exit codes (crucial for GitHub Actions). |
