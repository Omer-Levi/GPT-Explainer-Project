import sys
import os
import logging
from logging.handlers import TimedRotatingFileHandler
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import uuid
import asyncio
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from explainer.explainer import process_file

app = Flask(__name__)
UPLOAD_FOLDER = 'server/uploads'
RESULTS_FOLDER = 'server/results'
ERROR = 'error'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(RESULTS_FOLDER):
    os.makedirs(RESULTS_FOLDER)

# Set up logging
log_dir = 'logs/server'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_handler = TimedRotatingFileHandler(f"{log_dir}/server.log", when="midnight", interval=1, backupCount=5)
log_handler.suffix = "%Y%m%d"
logging.basicConfig(level=logging.INFO, handlers=[log_handler])
logger = logging.getLogger("server")
app.logger.addHandler(log_handler)

executor = ThreadPoolExecutor(2)

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload and trigger processing.
    """
    logger.info("Received file upload request")
    if 'file' not in request.files:
        return jsonify({ERROR: 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({ERROR: 'No selected file'}), 400
    if file:
        original_filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime('%d-%m-%Y-%H-%M')
        new_filename = f"{unique_id}_{timestamp}_{original_filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(filepath)
        logger.info(f"File saved to: {filepath}")

        # Trigger file processing in the background
        executor.submit(asyncio.run, process_file(filepath))
        logger.info(f"Processing triggered for: {filepath}")
        
        return jsonify({'uid': unique_id}), 200

@app.route('/status/<uid>', methods=['GET'])
def get_status(uid):
    """
    Check the processing status of a file.

    Args:
        uid (str): The unique identifier of the uploaded file.

    Returns:
        json: JSON response with status, filename, timestamp, and explanation.
    """
    logger.info(f"Checking status for UID: {uid}")
    # Find the corresponding upload file
    upload_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.startswith(uid)]
    if not upload_files:
        return jsonify({'status': 'not found', 'filename': None, 'timestamp': None, 'explanation': None}), 404
    
    upload_file = upload_files[0]
    _, timestamp, original_filename = upload_file.split('_', 2)
    # Check if the result file exists
    result_files = [f for f in os.listdir(RESULTS_FOLDER) if f.startswith(uid)]
    if result_files:
        with open(os.path.join(RESULTS_FOLDER, result_files[0]), 'r') as result_file:
            explanation = result_file.read()
        logger.info(f"Found result for UID: {uid}")
        return jsonify({'status': 'done', 'filename': original_filename, 'timestamp': timestamp, 'explanation': explanation}), 200
    else:
        logger.info(f"No result found for UID: {uid}, returning pending")
        return jsonify({'status': 'pending', 'filename': original_filename, 'timestamp': timestamp, 'explanation': None}), 200

@app.route('/result/<uid>', methods=['GET'])
def get_result(uid):
    """
    Fetch the processing result of a file.

    Args:
        uid (str): The unique identifier of the uploaded file.

    Returns:
        json: JSON response with the result or an error message if not found.
    """
    logger.info(f"Fetching result for UID: {uid}")
    # Fetch the result file
    result_files = [f for f in os.listdir(RESULTS_FOLDER) if f.startswith(uid)]
    if result_files:
        result_file_path = os.path.join(RESULTS_FOLDER, result_files[0])
        with open(result_file_path, 'r') as result_file:
            result = result_file.read()
        logger.info(f"Returning result for UID: {uid}")
        return jsonify({'result': result}), 200
    else:
        logger.info(f"Result not found for UID: {uid}")
        return jsonify({ERROR: 'Result not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
