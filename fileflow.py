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
#constant variables 
INPUT_FOLDER = config["folders"]["input"]
PROCESSED_FOLDER = config["folders"]["processed"]
QUARANTINE_FOLDER = config["folders"]["quarantine"]
LOG_FILE = config["log_file"]

VALID_EXTENSIONS = list(config["valid_extensions"].keys())

#create missing folders if they don't exist
for folder in config["folders"].values():
    os.makedirs(folder, exist_ok=True)

# function to write logs to the log file
def write_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{timestamp} - {message}\n")



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
    if os.path.exists(dest):
        dest = f"{base}_{uuid.uuid4().hex[:6]}{ext}"
    shutil.move(src, dest)
 

#main function to process files
def process_files():
    files = os.listdir(INPUT_FOLDER) #make a list of input files
    #counters for the summary log
    processed_count = 0
    quarantined_count = 0 
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
            write_log(f"processed: {filename}")
            processed_count += 1

        else:
            safe_move(file_path, dest_path)
            write_log(f"Quarantined: {filename}")
            quarantined_count += 1

            #summary log
    print(" Summary:")
    print(f"Processed files: {processed_count}")
    print(f"Quarantined files: {quarantined_count}")

#running script 
if __name__ == "__main__":
    process_files()

       
          
    