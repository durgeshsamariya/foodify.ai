import os
from unicodedata import name
import uuid
from googleapiclient.http import MediaFileUpload
from utils.google import Create_Service
import streamlit as st

# secret file name
CLIENT_SECRET_FILE =  st.secrets["gcp_service_account"]
# Google Driv API name and Version
API_NAME = 'drive'
API_VERSION = 'v3'

# Scope of drive
SCOPES = ['https://www.googleapis.com/auth/drive']

def upload_image(source_file, destination_file_name):
    """
        Upload image file to Google Drive.
    """
    print("Starting to upload...")

    # Intializing Service
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    # Google Drive Folder ID, where images will be store
    folder_id = st.secrets['GOOGLE_DRIVE_FOLDER_ID']

        # Upload a file
    file_metadata = {
        'name': destination_file_name,
        'parents': [folder_id]
    }
    # with open(source_file_name, "wb") as f:
    
    media_content = MediaFileUpload(source_file)

    file = service.files().create(
        body=file_metadata,
        media_body=media_content
    ).execute()

    print(f"File {source_file} uploaded to {destination_file_name}")

def create_unique_filename() -> str:
    """
    Creates a unique filename for storing uploaded images.
    """
    return str(uuid.uuid4())

