
# PowerPoint Text Extractor and GPT Explainer

## Overview

This project is designed to upload a PowerPoint file, extract the text from each slide, and generate explanations for the extracted text using OpenAI's GPT-3.5 model. The system is composed of several components:
- A Flask web server to handle file uploads and status checks.
- An explainer module to process the PowerPoint file and generate explanations.
- A client module to interact with the web server.
- Test scripts to ensure the system works as expected.
- Logging to keep track of operations and issues.

## Components

### 1. Flask Web Server (`server.py`)
Handles file uploads, triggers the explainer to process the file, and provides status updates.

### 2. Explainer Module (`explainer.py`)
Processes the uploaded PowerPoint file, extracts text, and generates explanations using GPT-3.5.

### 3. PowerPoint Reader (`read_pptx.py`)
Extracts text from each slide in the PowerPoint file.

### 4. Client Module (`client.py`)
Provides a convenient interface for Python developers to interact with the web server.

### 5. System Tests (`test_system.py`)
End-to-end tests to ensure the system functions correctly.

### 6. Logging
Both the Flask server and the explainer module generate logs that are saved in separate files for each day, retaining logs from the last 5 days.

## Usage

### Running the Server

1. Start the Flask server:
    ```bash
    python server/server.py
    ```

### Using the Client

You can use the client module to interact with the server. Here is an example of how to upload a file and check its status:

```python
from client import Client

client = Client("http://127.0.0.1:5000")

# Upload a PowerPoint file
uid = client.upload("path_to_your_pptx_file.pptx")
print(f"File uploaded successfully. UID: {uid}")

# Check the status of the file
status = client.status(uid)
print(f"Status: {status.status}")
print(f"Filename: {status.filename}")
print(f"Timestamp: {status.timestamp}")
print(f"Explanation: {status.explanation}")

if status.is_done():
    print("The file has been processed.")
else:
    print("The file is still being processed.")
```

### Running Tests

You can run the tests to ensure the system is functioning correctly:

```bash
pytest tests/test_system.py
```

## Logging

Logs are saved in the `logs` directory with separate subfolders for the server and explainer. Each log file is rotated daily, and logs from the last 5 days are retained.

- Server logs: `logs/server/server.log`
- Explainer logs: `logs/explainer/explainer.log`

## Directory Structure

```
<repository_name>/
├── client/
│   ├── client.py
├── explainer/
│   ├── explainer.py
│   ├── read_pptx.py
├── server/
│   ├── server.py
├── tests/
│   ├── test_system.py
├── logs/
│   ├── server/
│   ├── explainer/
├── .env
├── requirements.txt
└── README.md
```
