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


def handle_uploaded_file(f, company, local=True):
    '''
    Parameters:
        - f: a file object
        - company: company name as inputed in the form
        - local: boolean parameter to set the file storage to local (True) or cloud (GCS) (False).
    Returns:
        - filename: the filename as a gs:// pattern or a local path
        - gc_url: if local is True, it returns the url of the object
    '''
    
    if ('xlsx' in f.name) or ('xls' in f.name):
        is_excel = True
        df = pd.read_excel(f.read(), sheet_name=0)
        f.name = f.name.replace('xlsx', 'csv')
        f.name = f.name.replace('xls', 'csv')
    elif 'csv' in f.name:
        is_excel = False
        df = pd.read_csv(f)

    filename = path_and_rename('documents')
    filename = filename(f, f.name, company)
    
    if local:
        df.to_csv(filename, index=False)
        gc_url = None
    else:
        blob_name = 'company_data/' + filename.split('/')[-1]
        filename, gc_url = upload_blob_to_default_bucket(df, blob_name)
    
    return filename, gc_url

def get_available_fields(file_path):
    '''
    Reads a file specified by `file_path` and outputs the columns.
    Parameters:
        - file_path: path to the file. Allowed GCS path syntax
    '''
    if '.csv' in file_path:
        df = pd.read_csv(file_path, chunksize=1, index_col=0).get_chunk(1)
        return list(df.columns)

def rename_dataset(file_path, new_columns):
    '''
    Renames the columns of a dataset using the invers of `new_columns`
    as the rename mapper and stores it with the same name but under 
    the folder `renamed/`
    Parameters 
        - file_path: path to file
        - new_columns: dictionary similar to { 'new_column': 'current_cloumn' }
    Returns 
        - None
    '''
    new_columns = { v: k for k, v in new_columns.items() }
    df = pd.read_csv(file_path)
    df = df.rename(columns=new_columns)
    dataframe_to_gcs(df, file_path)

