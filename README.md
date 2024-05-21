
# TEXTEN - TEXT Extraction Node

## TEXTEN is a robust and efficient application designed to automate the process of extracting text from various file formats, detecting Personally Identifiable Information (PII), and managing the results effectively. This tool is particularly useful for organizations that handle large volumes of documents and need to ensure compliance with data privacy regulations.

Key Features
- Text Extraction: Supports multiple file formats including DOCX, PDF, XLSX, PPTX, and others.
- PII Detection: Uses configurable regex patterns to identify and flag sensitive information such as SSNs and credit card numbers.
- File Hashing: Implements file hashing to detect changes and avoid reprocessing files unnecessarily.
- Exclusion Patterns: Allows configuration of file and directory exclusion patterns.
- Logging and Reporting: Maintains comprehensive logs of processing activities.
- Configurable Output: Saves processed text and PII-flagged content to designated output directories.

## Git Repositories
- https://github.com/msuliot/texten.git
- https://github.com/msuliot/webtexten.git
- https://github.com/msuliot/chunken.git
- https://github.com/msuliot/datamyn.git

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## Prerequisites

Before you begin, ensure you have met the following requirements:
- You have installed Python 3.7 or later.
- You have a working internet connection.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/msuliot/texten.git
    cd texten
    ```

2. **Set up a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the TEXTEN application, use the following command:

```bash
python app.py
```

### Configuration

The configuration is managed through a `config.json` file. Create a configuration file with the following structure:

```json
{
  "input_directories": ["path/to/input/directory"],
  "text_output_directory": "path/to/text/output/directory",
  "pii_output_directory": "path/to/pii/output/directory",
  "hash_file_path": "file_hashes.json",
  "patterns": {
    "SSN": "\\b\\d{3}-\\d{2}-\\d{4}\\b",
    "CreditCard": "\\b\\d{4}-\\d{4}-\\d{4}-\\d{4}\\b"
  },
  "pii_ok": ["path/to/pii_ok_file.json"],
  "exclusions": ["*.tmp", "*.log"]
}
```