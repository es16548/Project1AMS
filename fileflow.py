#print ("Hello World")

#imports
import os
import shutil
import json
from datetime import datetime

# reading the config.json so it knows where to move the files
with open("config.json", "r") as f:
    config = json.load(f)
#constant variables 
INPUT_FOLDER = config["input_folder"]
PROCESSED_FOLDER = config["processed_folder"]
QUARANTINE_FOLDER = config["quarantine_folder"]
LOG_FILE = config["log_file"]

VALID_EXTENSIONS = [".txt", ".csv", ".json"]

# function to write logs to the log file
def write_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{timestamp} - {message}\n")

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
        _, ext = os.path.splitext(filename)
        if ext.lower() in VALID_EXTENSIONS:
            dest = os.path.join(PROCESSED_FOLDER, filename)
            shutil.move(file_path, dest)
            write_log(f"processed: {filename}")
            processed_count += 1

        else:
            dest = os.path.join(QUARANTINE_FOLDER, filename)
            shutil.move(file_path, dest)
            write_log(f"Quarantined: {filename}")
            quarantined_count += 1

            #summary log
    print(" Summary:")
    print(f"Processed files: {processed_count}")
    print(f"Quarantined files: {quarantined_count}")

#running script 
if __name__ == "__main__":
    process_files()

       
          
    