# API Schema Validator

This project provides a simple web-based utility to validate JSON payloads against a YAML-defined schema. It uses `jsonschema` for validation logic and `Flask` for the web interface.

## Features

- Validates JSON payloads against a provided YAML schema.
- Web UI for easy uploading of schema and JSON files.
- Displays detailed validation errors if the payload does not conform to the schema.
- Returns a success message for valid payloads.
- Includes example schema and payload files.

## Project Structure

```
api_validator/
├── app.py                # Flask application: handles web requests, file uploads, and UI.
├── validator.py          # Core validation logic: `validate_json` function.
├── requirements.txt      # Python dependencies for the project.
├── templates/
│   └── index.html        # HTML template for the web UI.
├── examples/
│   ├── schema.yaml       # Example YAML schema.
│   ├── payload.json      # Example valid JSON payload.
│   └── payload_invalid.json # Example invalid JSON payload.
└── README.md             # This file.
```

## Setup

1.  **Clone the repository** (or download the files into a directory named `api_validator`).
    ```bash
    # If it's a git repository (example command)
    # git clone <repository_url>
    # cd <repository_name>/api_validator 
    # If you only have the api_validator folder, navigate into it:
    # cd api_validator
    ```

2.  **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    ```
    Activate it:
    -   Windows: `venv\Scripts\activate`
    -   macOS/Linux: `source venv/bin/activate`

3.  **Install dependencies**:
    Ensure you are in the `api_validator` directory where `requirements.txt` is located.
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the Flask application**:
    Navigate to the `api_validator` directory in your terminal and run:
    ```bash
    python app.py
    ```
    You should see output indicating the server is running, typically on `http://127.0.0.1:5000/` or `http://0.0.0.0:5000/`.

2.  **Use the Web UI**:
    -   Open your web browser and go to `http://127.0.0.1:5000/`.
    -   Click "Choose File" under "YAML Schema File" and select your schema file (e.g., `examples/schema.yaml`).
    -   Click "Choose File" under "JSON Payload File" and select your JSON payload file (e.g., `examples/payload.json` or `examples/payload_invalid.json`).
    -   Click "Validate".
    -   The page will refresh and display either a success message or a list of validation errors.

3.  **Example Files**:
    The `examples/` directory contains:
    -   `schema.yaml`: A sample schema.
    -   `payload.json`: A JSON payload that is valid against `schema.yaml`.
    -   `payload_invalid.json`: A JSON payload that is invalid against `schema.yaml`.
    Use these to test the validator.

## Dependencies

The main Python dependencies are:

-   **Flask**: For the web framework.
-   **jsonschema**: For performing the JSON schema validation.
-   **PyYAML**: For loading the YAML schema files.

These are listed in `requirements.txt`.
