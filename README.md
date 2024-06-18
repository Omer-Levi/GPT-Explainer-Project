# GPT-Explainer Project

## Introduction

Learning Software Development can be challenging, especially when the lecture presentations are unclear. This project aims to implement a Python script that explains PowerPoint presentations using the GPT-3.5 AI model. The script takes a presentation file as input, extracts text from each slide, sends the text to GPT for explanation, and saves the results in an output JSON file.

## Requirements

- Python 3.7+
- `openai` library
- `python-pptx` library
- `aiofiles` library
- `pytest` for testing

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/Omer-Levi/GPT-Explainer-Project.git
    cd gpt-explainer
    ```

2. **Set your OpenAI API key:**
    ```sh
    export OPENAI_API_KEY='your-api-key'  # On Windows use `set OPENAI_API_KEY=your-api-key`
    ```

## Usage

To run the script and generate explanations for the slides in a PowerPoint presentation:

```sh
python main.py ./test.pptx
```

This will generate a JSON file named `test.json` with explanations for each slide.

## File Structure

- `main.py`: The main script that runs the process.
- `read_pptx.py`: A module to read and extract text from PowerPoint files.
- `test.pptx`: A sample PowerPoint presentation for testing.
- `test_system.py`: Pytest test file to run system tests.

## Running Tests

To run the system test that checks if the script processes the presentation and generates the JSON file:

```sh
python -m pytest -v test_system.py
```

## Code Overview

### `main.py`
This script handles the main flow of the program:

- Loads the OpenAI API key.
- Extracts text from the PowerPoint file.
- Sends the extracted text to the GPT-3.5 model for explanation.
- Saves the explanations to a JSON file.

### `read_pptx.py`
This module contains the ReadPptx class, which handles:

- Reading the PowerPoint file.
- Extracting text from text boxes and placeholders on each slide.

### `test_system.py`
This file contains a single system test to ensure that the script works as expected:

- It runs the main script with a sample PowerPoint file.
- Checks if the output JSON file is created.
- Verifies the content of the JSON file.
