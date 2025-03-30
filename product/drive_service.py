from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
import io
import json
import os
from django.conf import settings
from .functions import convert_decimal



#loading credentials from settings
credentials_path = settings.GOOGLE_SERVICE_ACCOUNT_JSON
    

SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = credentials_path

def get_drive_service():
    """Authenticate and return a Google Drive service instance."""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build("drive", "v3", credentials=creds)

def get_or_create_folder(service, folder_name):
    """Get the folder ID if it exists, otherwise create it."""
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    response = service.files().list(q=query, fields="files(id, name)").execute()
    files = response.get("files", [])

    if files:
        return files[0]["id"]  # Return existing folder ID

    # Create new folder
    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    folder = service.files().create(body=folder_metadata, fields="id").execute()
    return folder["id"]

def upload_json_to_drive(file_name, data, folder_name="django-app-api-data"):
    """Upload or update a JSON file in Google Drive."""
    service = get_drive_service()
    folder_id = get_or_create_folder(service, folder_name)


    # Convert data to JSON format, handling Decimal values
    file_stream = io.BytesIO(json.dumps(data, indent=4, default=convert_decimal).encode("utf-8"))


    # Check if the file exists in the folder
    query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
    response = service.files().list(q=query, fields="files(id)").execute()
    files = response.get("files", [])

    file_metadata = {
        "name": file_name,
        "mimeType": "application/json",
        "parents": [folder_id],
    }

    media = MediaIoBaseUpload(file_stream, mimetype="application/json")

    if files:
        # Update existing file
        file_id = files[0]["id"]
        service.files().update(fileId=file_id, media_body=media).execute()
    else:
        # Upload new file
        service.files().create(body=file_metadata, media_body=media).execute()
