import unittest
import os
import json
import yaml
from .validator import validate_json # Use relative import

# Define paths relative to this test file or use absolute paths if necessary
# Assuming 'examples' directory is a sibling to this test file's parent directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXAMPLES_DIR = os.path.join(BASE_DIR, 'examples')
SCHEMA_FILE = os.path.join(EXAMPLES_DIR, 'schema.yaml')
VALID_PAYLOAD_FILE = os.path.join(EXAMPLES_DIR, 'payload.json')
INVALID_PAYLOAD_FILE = os.path.join(EXAMPLES_DIR, 'payload_invalid.json')

# Temporary files for testing malformed data
TEMP_BAD_SCHEMA_FILE = os.path.join(BASE_DIR, 'temp_bad_schema.yaml')
TEMP_BAD_PAYLOAD_FILE = os.path.join(BASE_DIR, 'temp_bad_payload.json')

class TestValidator(unittest.TestCase):

    def tearDown(self):
        # Clean up any temporary files created during tests
        if os.path.exists(TEMP_BAD_SCHEMA_FILE):
            os.remove(TEMP_BAD_SCHEMA_FILE)
        if os.path.exists(TEMP_BAD_PAYLOAD_FILE):
            os.remove(TEMP_BAD_PAYLOAD_FILE)

    def test_valid_payload(self):
        errors = validate_json(SCHEMA_FILE, VALID_PAYLOAD_FILE)
        self.assertEqual(len(errors), 0, f"Expected no errors for valid payload, got: {errors}")

    def test_invalid_payload(self):
        errors = validate_json(SCHEMA_FILE, INVALID_PAYLOAD_FILE)
        self.assertTrue(len(errors) > 0, "Expected errors for invalid payload, got none.")
        # Example: Check for specific error messages if they are consistent
        # For payload_invalid.json:
        # - age should be integer, but it's "twenty five"
        # - email format is invalid "jane.doe"
        self.assertTrue(any("'age'" in error and "instance is not of type 'integer'" in error.lower() for error in errors), "Missing age type error")
        self.assertTrue(any("'email'" in error and "is not a 'email'" in error.lower() for error in errors), "Missing email format error")


    def test_non_existent_schema_file(self):
        non_existent_schema = os.path.join(EXAMPLES_DIR, "non_existent_schema.yaml")
        errors = validate_json(non_existent_schema, VALID_PAYLOAD_FILE)
        self.assertEqual(len(errors), 1)
        self.assertIn(f"Schema file not found: {non_existent_schema}", errors[0])

    def test_non_existent_json_file(self):
        non_existent_payload = os.path.join(EXAMPLES_DIR, "non_existent_payload.json")
        errors = validate_json(SCHEMA_FILE, non_existent_payload)
        self.assertEqual(len(errors), 1)
        self.assertIn(f"JSON file not found: {non_existent_payload}", errors[0])

    def test_invalid_yaml_schema(self):
        # Create a malformed YAML file
        with open(TEMP_BAD_SCHEMA_FILE, 'w') as f:
            f.write("type: object\nproperties: name:\n  type: string\n  age: type: integer") # Malformed: bad indentation
        
        errors = validate_json(TEMP_BAD_SCHEMA_FILE, VALID_PAYLOAD_FILE)
        self.assertEqual(len(errors), 1)
        self.assertTrue("Error loading YAML schema" in errors[0], f"Unexpected error message: {errors[0]}")

    def test_invalid_json_payload(self):
        # Create a malformed JSON file
        with open(TEMP_BAD_PAYLOAD_FILE, 'w') as f:
            f.write('{"name": "Test", "age": 30, "email": "test@example.com"') # Malformed: missing closing brace
        
        errors = validate_json(SCHEMA_FILE, TEMP_BAD_PAYLOAD_FILE)
        self.assertEqual(len(errors), 1)
        self.assertTrue("Error loading JSON payload" in errors[0], f"Unexpected error message: {errors[0]}")

if __name__ == '__main__':
    unittest.main()
