#print ("Hello World")

#imports
import os
import shutil
import json
import uuid
from datetime import datetime

# reading the config.json so it knows where to move the files
with open("config.json", "r") as f:
    config = json.load(f)

#Error handling for config file
required_sections = ["folders", "valid_extensions", "log_file"]

for section in required_sections:
    if section not in config:
        print(f"Config error: Missing '{section}' in config.json")
        exit(1)

# Validate folders section
required_folders = ["input", "processed", "quarantine", "archive", "reports", "logs"]
for folder in required_folders:
    if folder not in config["folders"]:
        print(f"Config error: Missing folder path for '{folder}' in config.json")
        exit(1)

# Validate archive_days
if not isinstance(config.get("archive_days", 30), int):
    print("Config warning: 'archive_days' is invalid. Using default of 30.")
    config["archive_days"] = 30



#constant variables 
INPUT_FOLDER = config["folders"]["input"]
PROCESSED_FOLDER = config["folders"]["processed"]
QUARANTINE_FOLDER = config["folders"]["quarantine"]
ARCHIVE_FOLDER = config["folders"]["archive"]
LOG_FILE = config["log_file"]

VALID_EXTENSIONS = list(config["valid_extensions"].keys())

#create missing folders if they don't exist
for folder in config["folders"].values():
    os.makedirs(folder, exist_ok=True)

# function to write logs to the log file
def write_log(message, level ="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"[{timestamp}] - {level} {message}\n")



#sorting to subfolders
def get_destination_folder(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext in config["valid_extensions"]:
        category = config["valid_extensions"][ext]  
        return os.path.join(PROCESSED_FOLDER, category)
    else:
        return QUARANTINE_FOLDER
    
for category in set(config["valid_extensions"].values()):
    os.makedirs(os.path.join(PROCESSED_FOLDER, category), exist_ok=True)

#protection for duplicate files
def safe_move(src, dest):
    base, ext = os.path.splitext(dest)
    while os.path.exists(dest):
        dest = f"{base}_{uuid.uuid4().hex[:6]}{ext}"
    shutil.move(src, dest)
 
#archive function
def archive_old_files(archived_files_list):
    days_old=config.get("archive_days", 30)
    now = datetime.now().timestamp()
    cutoff = now - (days_old * 86400)  #86400seconds in a day

    for root, dirs, files in os.walk(PROCESSED_FOLDER):
        for filename in files:
            file_path = os.path.join(root, filename)
            modified_time = os.path.getmtime(file_path)

            if modified_time < cutoff:
                archive_path = os.path.join(ARCHIVE_FOLDER, filename)
                safe_move(file_path, archive_path)
                write_log(f"Archived: {filename}", "ARCHIVE")
                archived_files_list.append(filename)

#report function
def generate_report(processed_files, quarantined_files, archived_files):
    timestamp =datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_name = f"report_{timestamp}.txt"
    report_path = os.path.join(config["folders"]["reports"], report_name)

    with open(report_path, "w") as report:
        report.write(f"FileFlow Report - {timestamp}\n")
        report.write("=" * 40 + "\n\n")

        report.write(f"Processed files: {len(processed_files)}\n")
        report.write(f"Quarantined files: {len(quarantined_files)}\n")
        report.write(f"Archived files: {len(archived_files)}\n\n")

        report.write("Processed Files:\n")
        for f in processed_files:
            report.write(f"- {f}\n")

        report.write("\nQuarantined Files:\n")
        for f in quarantined_files:
            report.write(f"- {f}\n")

        report.write("\nArchived Files:\n")
        for f in archived_files:
            report.write(f"- {f}\n")
    write_log(f"Generated report: {report_name}", "INFO")  

#main function to process files
def process_files():
    files = os.listdir(INPUT_FOLDER) #make a list of input files
    #counters for the summary log
    processed_count = 0
    quarantined_count = 0 

    processed_files_list = []
    quarantined_files_list = []
    archived_files_list = []  


    #loop through all files in the input folder
    for filename in files:
        file_path = os.path.join(INPUT_FOLDER, filename)
        #skip processed files
        if os.path.isdir(file_path):
            continue

        #check for valid file extensions
        dest_folder=get_destination_folder(filename)
        os.makedirs(dest_folder, exist_ok=True)
        dest_path = os.path.join(dest_folder, filename)

        _, ext = os.path.splitext(filename)

        if ext.lower() in VALID_EXTENSIONS:
            safe_move(file_path, dest_path)
            write_log(f"processed file: {filename}", "INFO")
            processed_count += 1
            processed_files_list.append(filename)

        else:
            safe_move(file_path, dest_path)
            write_log(f"Quarantined: {filename}", "WARNING")
            quarantined_count += 1
            quarantined_files_list.append(filename)


    #summary log
    print(" Summary:")
    print(f"Processed files: {processed_count}")
    print(f"Quarantined files: {quarantined_count}")

    archive_old_files(archived_files_list)
    generate_report(processed_files_list, quarantined_files_list, archived_files_list)




#running script 
if __name__ == "__main__":
    process_files()

       
          
    