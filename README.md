# LUIS Model JSON Converter

## Overview

This tool addresses the issue of migrating Azure LUIS model JSON files to a format compatible with Azure CLU (Conversational Language Understanding). The main challenges include:
- CLU does not support structured entities.
- Many entity names in Quallie LUIS models contain redundancy, and concatenated names often exceed the 50-character limit imposed by CLU.

This converter processes the LUIS model JSON files to remove redundant parent names from child entity names and handles specific renaming cases.

## Features

- Removes concatenated parent names from child entity names.
- Handles special renaming cases as specified in the `special_cases` dictionary.
- Fixes character encoding issues.
- Command-line interface for easy usage.

## Usage

### Prerequisites

- Python 3.10 or later
- Poetry for dependency management

### Running the Converter

To convert a LUIS model JSON file:

```sh
python luis_json_converter a_given_luis_model.json
```
or

```sh
python luis_json_converter a_given_luis_model.json -o /path/to/output_folder
```

This command will generate a JSON compatible with CLU in the output folder with the same file name plus the  `_clu` suffix.

### Poetry 

**Install dependencies using Poetry:**

  ```sh
  poetry install
  ```

**Running the Converter**

  ```sh
  poetry run luis_json_converter a_given_luis_model.json
  ```


### Command-Line Arguments

- `input_file` (required): Path to the input LUIS JSON file.
- `-o, --output_dir` (optional): Directory to save the processed JSON file (default: `output`).

### Example

```sh
luis_json_converter path/to/your/luis_model.json -o path/to/output
```

## Developer Notes

### Project Structure

```
luis_json_converter/
├── luis_json_converter/
│   ├── __main__.py
│   ├── migrator.py
├── pyproject.toml
├── poetry.lock
├── Dockerfile
```

### Scripts

- `converter.py`: Contains the core logic for processing LUIS model JSON files.
  - `process_entity`: Recursively processes entities to remove concatenated parent names from child entity names.
  - `process_luis_model`: Handles special cases, fixes character encoding issues, and processes the LUIS model JSON file.
- `__main__.py`: Handles command-line interface and integrates with `migrator.py`.

### Special Cases

A dictionary of special cases is used to handle specific entity renaming:

```python
special_cases = {
    'WhereOperatorSubstractionExact': 'SubstractionExact',
    'WhereOperatorSubstractionRange': 'SubstractionRange',
    'WhereOperatorSumExact': 'SumExact',
    'WhereOperatorSumRange': 'SumRange',
    'WhereOperatorNumber': 'Number'
}
```
