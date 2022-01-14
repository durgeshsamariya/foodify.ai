import boto3
import uuid
import streamlit as st
from botocore.exceptions import ClientError
import tempfile
from pathlib import Path


def upload_image(source_file, destination_file_name):
    """
        Upload image file to AWS S3 Bucket.
    """
    print("Starting to upload file {0}...".format(source_file.name))

    """
    Connect to S3 AWS Service
    """
    client_s3 = boto3.client(
        's3',
        aws_access_key_id = st.secrets['ACCESS_KEY'],
        aws_secret_access_key = st.secrets['ACCESS_SECRET']
    )

    """
    Make temp file path from uploaded file
    see: https://shunyaueta.com/posts/2021-07-09/
    """
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        fp = Path(tmp_file.name)
        fp.write_bytes(source_file.getbuffer())
        """
        Uploading image to AWS S3 Bucket
        """
        try:
            client_s3.upload_file(
                tmp_file.name,
                st.secrets['BUCKET_NAME'],
                destination_file_name
            )
        except ClientError as e:
            print('Invalid Credentials.')
            print(e)
        except Exception as e:
            print(e)
    
    print("File {0} uploaded to {1}".format(source_file.name, destination_file_name))

def create_unique_filename() -> str:
    """
    Creates a unique filename for storing uploaded images.
    """
    return str(uuid.uuid4())

