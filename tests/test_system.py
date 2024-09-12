import pytest
import subprocess
import time
import os
from client.client import Client, APIError

UPLOAD_FOLDER = 'server/uploads'
RESULTS_FOLDER = 'server/results'
PATH = "test.pptx"

@pytest.fixture(scope="module")
def start_server():
    # Start the Flask server
    server = subprocess.Popen(["python", "./server/server.py"])
    time.sleep(5) 
    yield
    server.terminate()

@pytest.fixture(scope="module")
def start_explainer():
    # Start the Explainer
    explainer = subprocess.Popen(["python", "./explainer/explainer.py"])
    time.sleep(5)  
    yield
    explainer.terminate()

@pytest.fixture
def client():
    return Client("http://127.0.0.1:5000")

def test_upload_returns_uid(client):
    """
    Test if the upload returns a UID.
    """
    uid = client.upload(PATH)
    assert uid is not None
    assert isinstance(uid, str)

def test_file_created_in_uploads(client):
    """
    Test if the file is created in the uploads folder.
    """
    uid = client.upload(PATH)
    time.sleep(1) 
    files = os.listdir(UPLOAD_FOLDER)
    uploaded_file = next((f for f in files if uid in f), None)
    assert uploaded_file is not None
    assert uid in uploaded_file

def test_explainer_processes_new_files(client):
    """
    Test if the explainer processes new files.
    """
    uid = client.upload(PATH)
    time.sleep(1)  
    files = os.listdir(UPLOAD_FOLDER)
    processed_file = next((f for f in files if uid in f), None)
    assert processed_file is not None

def test_client_raises_error_for_invalid_uid(client):
    """
    Test if the client raises an error for an invalid UID.
    """
    with pytest.raises(APIError):
        client.status("invalid_uid")

def test_status_returns_pending_immediately_after_upload(client):
    """
    Test if the status returns 'pending' immediately after upload.
    """
    uid = client.upload(PATH)
    status = client.status(uid)
    assert status.status == 'pending'

def test_status_returns_done_after_processing(client):
    """
    Test if the status returns 'done' after processing.
    """
    uid = client.upload(PATH)
    time.sleep(60)  
    status = client.status(uid)
    assert status.status == 'done'
    assert status.explanation is not None

if __name__ == "__main__":
    pytest.main()