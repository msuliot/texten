
# TEXTEN - TEXT Extraction Node

TEXTEN is a text extraction node designed to process files, detect and manage Personally Identifiable Information (PII), and save the processed files in a specified format.

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
- [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, ensure you have met the following requirements:
- You have installed Python 3.7 or later.
- You have a working internet connection.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/texten.git
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