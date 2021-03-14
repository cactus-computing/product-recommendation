from google.cloud import storage
from google.oauth2 import service_account
import pandas as pd
import logging
from datetime import datetime
from django.utils import timezone
import os
from collections import defaultdict
from io import StringIO
# Instantiates a client
KEY_PATH = "cactusco/service_account_key.json"
BUCKET_NAME = "cactus_recommender"


credentials = service_account.Credentials.from_service_account_file(
    KEY_PATH, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

logger = logging.Logger(__name__)


def upload_blob_to_default_bucket(filename, destination_blob_name):
    """Uploads a file to the bucket.
    Parameters:
        - source_file: a file object containing the file which you need to upload.
        - destination_blob_name: the name the object will have once stored in google cloud platform"""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    client = storage.Client(credentials=credentials, project=credentials.project_id,)
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)
    with open(filename, 'rb') as f:
        blob.upload_from_file(f)

    gcs_path = f"gs://{BUCKET_NAME}/{blob.name}"
    logger.info(
        "Dataframe uploaded to GCS: {}.".format( destination_blob_name )
    )

    logger.info(gcs_path)
    return gcs_path, blob.public_url