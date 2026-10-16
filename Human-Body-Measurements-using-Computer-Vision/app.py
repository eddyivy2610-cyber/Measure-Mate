# from flask import Flask, request, jsonify
# import subprocess
# import os
# import re

# app = Flask(__name__)
# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# @app.route('/')
# def index():
#     return 'Welcome to the Flask app!'

# import sys
# print(f"Using Python executable: {sys.executable}")
# print(f"Python version: {sys.version}")

# @app.route('/process', methods=['POST'])
# def process_file():
#     if 'image' not in request.files or not request.form.get('height'):
#         return jsonify({'error': 'Missing image or height input.'}), 400

#     # Save uploaded file
#     file = request.files['image']
#     height = request.form['height']
#     input_path = os.path.join(UPLOAD_FOLDER, file.filename)
#     file.save(input_path)

#     # Run your command and capture output
#     command = [
#         'python', 'inference.py',
#         '-i', input_path,
#         '-ht', height
#     ]
#     process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#     stdout, stderr = process.communicate()

#     # Extract results from stdout
#     output_pattern = r"(height|waist|belly|chest|wrist|neck|arm length|thigh|shoulder width|hips|ankle):\s([\d.]+)"
#     results = re.findall(output_pattern, stdout)
#     results_dict = {key: value for key, value in results}

#     if results_dict:
#         return jsonify({'results': results_dict})
#     else:
#         return jsonify({'error': f'Processing completed, but no measurements were found. Errors: {stderr}'}), 500

# if __name__ == '__main__':
#     app.run( host='0.0.0.0',port=5000, debug=True)
#------------------------------------------------------------------------------------------------------------------------------------------
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import subprocess
# import os
# import re

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route('/')
# def index():
#     return 'Welcome to the Flask app!'

# import sys
# print(f"Using Python executable: {sys.executable}")
# print(f"Python version: {sys.version}")

# @app.route('/process', methods=['POST'])
# def process_file():
#     if 'image' not in request.files or not request.form.get('height'):
#         return jsonify({'error': 'Missing image or height input.'}), 400

#     # Save uploaded file
#     file = request.files['image']
#     height = request.form['height']
#     input_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, file.filename))
#     file.save(input_path)

#     # Run your command and capture output
#     command = [
#         'python', 'inference.py',
#         '-i', input_path,
#         '-ht', height
#     ]
#     process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#     stdout, stderr = process.communicate()

#     if process.returncode != 0:
#         return jsonify({'error': f'Error running command: {stderr}'}), 500

#     # Extract results from stdout
#     output_pattern = r"(height|waist|belly|chest|wrist|neck|arm length|thigh|shoulder width|hips|ankle):\s([\d.]+)"
#     results = re.findall(output_pattern, stdout)
#     results_dict = {key: value for key, value in results}

#     if results_dict:
#         return jsonify({'results': results_dict})
#     else:
#         return jsonify({'error': f'Processing completed, but no measurements were found. Errors: {stderr}'}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)##
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os
import re
import sys

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['TEMPLATES_AUTO_RELOAD'] = True
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

print(f"Using Python executable: {sys.executable}")
print(f"Python version: {sys.version}")


# ── Pages ──────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')

@app.route('/samples')
@app.route('/measurements')
def samples():
    return render_template('run.html')

@app.route('/model.obj')
def get_model_obj():
    obj_path = os.path.join(BASE_DIR, 'test.obj')
    if os.path.exists(obj_path):
        return send_from_directory(BASE_DIR, 'test.obj', mimetype='text/plain')
    return jsonify({'error': 'No 3D model found'}), 404

@app.route('/configure')
def configure():
    return render_template('index.html')

@app.route('/api')
def api_docs():
    return render_template('api.html')


# ── API ─────────────────────────────────────────────────────────────────────

@app.route('/process', methods=['GET', 'POST'])
def process_file():
    if request.method == 'GET':
        return jsonify({
            'message': 'Use POST to submit an image and height for measurement processing.',
            'accepted_methods': ['POST']
        })

    if 'image' not in request.files or not request.form.get('height'):
        return jsonify({'error': 'Missing image or height input.'}), 400

    file = request.files['image']
    height = request.form['height']
    # inference.py expects an integer height in inches
    try:
        height_int = str(round(float(height)))
    except ValueError:
        return jsonify({'error': 'Invalid height value.'}), 400
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    command = [
        sys.executable, os.path.join(BASE_DIR, 'inference.py'),
        '-i', input_path,
        '-ht', height_int
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        return jsonify({'error': f'Command execution failed: {stderr.strip()}'}), 500

    output_pattern = r"(height|waist|belly|chest|wrist|neck|arm length|thigh|shoulder width|hips|ankle):\s([\d.]+)"
    results = re.findall(output_pattern, stdout)
    results_dict = {key: value for key, value in results}

    import time
    if results_dict:
        return jsonify({
            'results': results_dict,
            'model_url': f'/model.obj?v={int(time.time())}'
        })
    else:
        return jsonify({'error': f'No measurements found. Output: {stdout.strip()}'}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
