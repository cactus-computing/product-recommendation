from google.cloud import storage
from google.oauth2 import service_account
import pandas as pd
import logging
# Instantiates a client
KEY_PATH = "cactusco/service_account_key.json"
BUCKET_NAME = "cactus_recommender"

credentials = service_account.Credentials.from_service_account_file(
    KEY_PATH, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

logger = logging.Logger(__name__)


def upload_blob_to_default_bucket(df, destination_blob_name):
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

    blob.upload_from_string(df.to_csv(index=False), 'text/csv')
    
    
    gcs_path = f"gs://{BUCKET_NAME}/{blob.name}"

    logger.info(
        "Dataframe uploaded to GCS: {}.".format( destination_blob_name )
    )

    logger.info(gcs_path)
    return gcs_path, blob.public_url

def dataframe_to_gcs(df, name_to_update):
    '''
    This function takes a dataframe and creates a renamed version of the original dataframe
    Parameters: 
        - df: dataframe 
        - name_to_update: a dataframe already existing in gcs
    Returns:
        - None    
    '''
    name_to_update = name_to_update.split(BUCKET_NAME)[-1][1:]
    splitted_name = name_to_update.split('/')
    new_name = splitted_name[0] + '/' + 'renamed' + '/' + splitted_name[1]

    client = storage.Client(credentials=credentials, project=credentials.project_id)
    client.bucket(BUCKET_NAME).blob(f"{new_name}").upload_from_string(df.to_csv(), 'text/csv')