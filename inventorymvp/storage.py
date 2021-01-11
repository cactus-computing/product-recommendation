from google.cloud import storage
from google.oauth2 import service_account
import pandas as pd

# Instantiates a client
KEY_PATH = "inventorymvp/service_account_key.json"
BUCKET_NAME = "cactus-stockapp"

credentials = service_account.Credentials.from_service_account_file(
    KEY_PATH, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)



def upload_blob_to_default_bucket(source_file, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    client = storage.Client(credentials=credentials, project=credentials.project_id,)
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_file(source_file)
    
    
    gcs_path = f"gs://{BUCKET_NAME}/{blob.name}"

    print(
        "File {} uploaded to GCS: {}.".format(
            source_file, destination_blob_name
        )
    )

    print(gcs_path)
    return gcs_path, blob.public_url

def dataframe_to_gcs(df, name_to_update):

    name_to_update = name_to_update.split(BUCKET_NAME)[-1][1:]
    splitted_name = name_to_update.split('/')
    new_name = splitted_name[0] + '/' + 'renamed' + '/' + splitted_name[1]

    client = storage.Client(credentials=credentials, project=credentials.project_id)
    client.bucket(BUCKET_NAME).blob(f"{new_name}").upload_from_string(df.to_csv(), 'text/csv')

    return True