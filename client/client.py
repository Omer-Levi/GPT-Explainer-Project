import requests
from dataclasses import dataclass
from datetime import datetime

class APIError(Exception):
    pass

@dataclass
class Status:
    status: str
    filename: str
    timestamp: datetime
    explanation: str

    @staticmethod
    def from_json(json_data):
        """
        Create a Status object from a JSON dictionary.

        Args:
            json_data (dict): The JSON data to parse.

        Returns:
            Status: A Status object.
        """
        return Status(
            status=json_data['status'],
            filename=json_data['filename'],
            timestamp=datetime.strptime(json_data['timestamp'], '%d-%m-%Y-%H-%M'),
            explanation=json_data.get('explanation')
        )

    def is_done(self):
        """
        Check if the status is 'done'.

        Returns:
            bool: True if status is 'done', False otherwise.
        """
        return self.status == 'done'

class Client:
    def __init__(self, base_url):
        self.base_url = base_url

    def upload(self, file_path):
        """
        Upload a file to the web service.

        Args:
            file_path (str): The path to the file to upload.

        Returns:
            str: The UID of the uploaded file.

        Raises:
            APIError: If there is an error uploading the file.
        """
        url = f"{self.base_url}/upload"
        with open(file_path, 'rb') as file:
            response = requests.post(url, files={'file': file})
        
        if response.status_code == 200:
            return response.json()['uid']
        else:
            raise APIError(f"Error uploading file: {response.content.decode()}")

    def status(self, uid):
        """
        Get the status of an uploaded file.

        Args:
            uid (str): The UID of the uploaded file.

        Returns:
            Status: The status of the uploaded file.

        Raises:
            APIError: If there is an error fetching the status.
        """
        url = f"{self.base_url}/status/{uid}"
        response = requests.get(url)
        
        if response.status_code == 200:
            return Status.from_json(response.json())
        else:
            raise APIError(f"Error fetching status: {response.content.decode()}")