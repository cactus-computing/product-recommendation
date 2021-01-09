from google.cloud import storage
from google.oauth2 import service_account

# Instantiates a client
KEY_PATH = "inventorymvp/service_account_key.json"
BUCKET_NAME = "cactus-stockapp"

credentials = service_account.Credentials.from_service_account_file(
    KEY_PATH, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

client = storage.Client(credentials=credentials, project=credentials.project_id,)

def upload_blob_to_default_bucket(source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_file(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )
    return blob.public_url