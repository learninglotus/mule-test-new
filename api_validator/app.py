import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from .validator import validate_json

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the templates directory is correctly identified by Flask if it's not in the default location
# However, by placing 'templates' inside 'api_validator' and Flask app in 'api_validator',
# Flask should find it automatically.

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    result_message = None
    if request.method == 'POST':
        if 'schema_file' not in request.files or 'json_file' not in request.files:
            errors.append("Both schema and JSON files are required.")
            return render_template('index.html', errors=errors)

        schema_file = request.files['schema_file']
        json_file = request.files['json_file']

        if schema_file.filename == '' or json_file.filename == '':
            errors.append("No selected file. Both schema and JSON files are required.")
            return render_template('index.html', errors=errors)

        if not (schema_file.filename.endswith('.yaml') or schema_file.filename.endswith('.yml')):
            errors.append("Schema file must be a YAML file (.yaml or .yml).")
        
        if not json_file.filename.endswith('.json'):
            errors.append("Payload file must be a JSON file (.json).")

        if errors: # If there are file type errors, return early
            return render_template('index.html', errors=errors)

        # Create uploads directory if it doesn't exist
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        schema_filename = secure_filename(schema_file.filename)
        json_filename = secure_filename(json_file.filename)

        schema_path = os.path.join(app.config['UPLOAD_FOLDER'], schema_filename)
        json_path = os.path.join(app.config['UPLOAD_FOLDER'], json_filename)

        try:
            schema_file.save(schema_path)
            json_file.save(json_path)

            errors = validate_json(schema_path, json_path)
            if not errors:
                result_message = "Validation successful!"
        except Exception as e:
            errors.append(f"An unexpected error occurred: {str(e)}")
        finally:
            # Clean up uploaded files
            if os.path.exists(schema_path):
                os.remove(schema_path)
            if os.path.exists(json_path):
                os.remove(json_path)
        
        return render_template('index.html', errors=errors, result_message=result_message)

    return render_template('index.html', errors=None, result_message=None)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
