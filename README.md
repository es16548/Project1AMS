## FileFlow — Automated File Processing & Archiving Tool
FileFlow is a lightweight, configurable file‑processing tool designed to keep folders organised automatically.
It scans an input directory, validates files, sorts them into categories, quarantines invalid files, archives older files, generates reports, and logs all actions.
It can run locally or inside a Docker (Linux) container.

## Features
Process incoming files based on extension rules

Sort valid files into category folders (e.g., text, data)

Quarantine invalid files

Archive old processed files after a configurable number of days

Generate summary reports

Readable logging for all actions

Config‑driven behaviour via config.json

Interactive menu for easy use

Runs on Windows or Linux (via Docker)

## Folder structure
project/
│
├── input/              # New files to be processed
├── processed/          # Valid files sorted into categories
│     ├── text/
│     └── data/
│
├── quarantine/         # Invalid or unapproved files
├── archive/            # Old processed files (e.g., >30 days)
│
├── reports/            # Summary reports
├── logs/               # Log file (log.txt)
│
├── fileflow.py         # Main script
├── config.json         # Configuration file
├── Dockerfile          # Docker container definition
└── README.md           # Project documentation

## Configuration
### Valid Extensions 
"valid_extensions": {
    ".txt": "text",
    ".csv": "data",
    ".json": "data"
}

### Folder Paths
"folders": {
    "input": "input",
    "processed": "processed",
    "quarantine": "quarantine",
    "archive": "archive",
    "reports": "reports",
    "logs": "logs"
}

### Archived Settings 
"archive_days": 30


## How to run locally 
Install Python
run script - python fileflow.py
use interactive menu
=== FileFlow Menu ===
1. Process files
2. Generate report
3. View logs
4. Exit

## How to run using Docker
Make sure linux is installed 
Build image - docker build -t fileflow .
Run container- docker run fileflow

## Testing 
Add valid files in input folder, examples: notes.txt, data.csv, info.json
Add invalid files, examples: test.exe, image.jpg, random.xyz
Create old valid files by addig them to prcessed folders and then changing the date in poweshell e.g (Get-Item "old1.txt").LastWriteTime = (Get-Date).AddDays(-40)

### Expected behaviour
Valid files → processed/category
Invalid files → quarantine
Old files → archive
Logs updated
Report generated

### Example log 
[2026-04-17 10:32:11] INFO Processed file: notes.txt
[2026-04-17 10:32:11] INFO Archived file: old1.txt
[2026-04-17 10:32:11] WARNING Quarantined file: virus.exe


### Example report
=== FileFlow Report ===
Processed: 12 files
Quarantined: 3 files
Archived: 4 files







