## FileFlow Project
A Python-based file organiser that validates, sorts, and manages files dropped into a shared folder. Automatically moves files into the correct directories, logs activity, and keeps storage clean and structured.

## Backlog Items (User Stories)
As a user, I want files placed in the input folder to be automatically sorted so I don’t have to organise them manually.

As a user, I want unsupported or suspicious files to be quarantined so the system stays safe.

As a user, I want logs created for every file action so I can track what happened.

As a user, I want a configuration file so I can change folder paths without editing the code.

As a user, I want the system to run repeatedly without crashing so it can be used reliably.

## Acceptance Criteria
### Feature: Sort valid files
Given a .txt file in the input folder

When the script runs

Then the file is moved to the processed folder

And a log entry is created

And the file is no longer in the input folder

### Feature: Quarantine invalid files
Given a file with an unsupported extension

When the script runs

Then the file is moved to the quarantine folder

And a log entry is created

### Feature: Use configuration file
Given a valid config.json

When the script runs

Then the script reads folder paths from the config

And uses those paths for sorting

### Possible File Classification Rules

| File Type | Action               |
|----------|-----------------------|
| .txt     | Move to processed     |
| .csv     | Move to processed     |
| .json    | Move to processed     |
| .exe     | Move to quarantine    |
| .zip     | Move to quarantine    |
| Unknown  | Move to quarantine    |


### Starter Project Structure

fileflow/
│── fileflow.py
│── config.json
│
│── archive/
│── input/
│── logs/
│── processed/
│── quarantine/
│── reports/





