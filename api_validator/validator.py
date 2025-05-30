import json
import yaml
from jsonschema import validate
from jsonschema.exceptions import ValidationError

def validate_json(schema_path: str, json_path: str) -> list[str]:
    """
    Validates a JSON payload against a YAML schema.

    Args:
        schema_path: Path to the YAML file containing the API schema.
        json_path: Path to the JSON file containing the payload to validate.

    Returns:
        A list of error messages if validation fails, otherwise an empty list.
    """
    errors = []
    try:
        with open(schema_path, 'r') as schema_file:
            schema = yaml.safe_load(schema_file)
    except FileNotFoundError:
        errors.append(f"Schema file not found: {schema_path}")
        return errors
    except yaml.YAMLError as e:
        errors.append(f"Error loading YAML schema: {e}")
        return errors

    try:
        with open(json_path, 'r') as json_file:
            payload = json.load(json_file)
    except FileNotFoundError:
        errors.append(f"JSON file not found: {json_path}")
        return errors
    except json.JSONDecodeError as e:
        errors.append(f"Error loading JSON payload: {e}")
        return errors

    try:
        validate(instance=payload, schema=schema)
    except ValidationError as e:
        errors.append(e.message)
    
    return errors

if __name__ == '__main__':
    # This part is for basic testing and can be expanded later
    # Create dummy schema and json files for testing
    with open('dummy_schema.yaml', 'w') as f:
        yaml.dump({'type': 'object', 'properties': {'name': {'type': 'string'}}, 'required': ['name']}, f)
    
    with open('dummy_payload_valid.json', 'w') as f:
        json.dump({'name': 'Test'}, f)

    with open('dummy_payload_invalid.json', 'w') as f:
        json.dump({'age': 30}, f)

    print("Validating dummy_payload_valid.json...")
    validation_errors = validate_json('dummy_schema.yaml', 'dummy_payload_valid.json')
    if not validation_errors:
        print("Validation successful!")
    else:
        print("Validation failed:")
        for error in validation_errors:
            print(f"- {error}")

    print("\nValidating dummy_payload_invalid.json...")
    validation_errors_invalid = validate_json('dummy_schema.yaml', 'dummy_payload_invalid.json')
    if not validation_errors_invalid:
        print("Validation successful!") # This should not happen for invalid payload
    else:
        print("Validation failed:")
        for error in validation_errors_invalid:
            print(f"- {error}")
    
    # Clean up dummy files
    import os
    os.remove('dummy_schema.yaml')
    os.remove('dummy_payload_valid.json')
    os.remove('dummy_payload_invalid.json')
