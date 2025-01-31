# Computer Information Application

## Overview
This Python application retrieves and displays system information such as:
- Computer name
- Total physical memory
- Number of processors and cores
- Number of hard disks
- Top 5 CPU-consuming processes

Additionally, the application supports logging system information to a file.

## Features
- Displays system details in the console
- Logs information to a file (when `-logInfo` is used)
- Supports command-line arguments
- Supported platforms: Windows and Linux

## Prerequisites
Clone the source code repository:
```sh
git clone https://github.com/aniketpawar7048/Nice.git
cd Nice
```
## Install Dependencies
Ensure you have Python 3 installed. Required Python modules:
```bash
pip install -r requirements.txt
```
## Usage
Run the script using Python:

1. Display Help Message:
```bash
python NiceTestApp.py -help
```

2. Display Information on Console:
```bash
python NiceTestApp.py
```

3. Display Information on Console and Log to File:
```bash
python NiceTestApp.py -logInfo
```
## Logging
If the `-logInfo` flag is specified.

- logs are stored in the `Application_Logs` directory inside the project folder.
- Log filenames follow the format: `MM_DD_YYYY_HH_MM_SS.log`

## Output
Console Output:

```bash
Computer Name: DESKTOP-5B8OJC1.bbrouter
Total Physical Memory: 7.88 GB
Total Number of Physical Processors: 2
Total Number of Cores: 4
Total Number of Hard Disks: 1
Top 5 processes in terms of CPU: {'Process1': 'System Idle Process: 0.0%', 'Process2': 'System: 0.0%', 'Process3': 'Registry: 0.0%', 'Process4': 'Code.exe: 0.0%', 'Process5': 'smss.exe: 0.0%'}
```

### Author
Aniket Pawar
