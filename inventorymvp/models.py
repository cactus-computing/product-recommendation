from django.db import models
from django.utils import timezone
import os
from datetime import datetime
import logging
from django.forms import ValidationError
from .storage import upload_blob_to_default_bucket, dataframe_to_gcs
import pandas as pd

logger = logging.Logger(__name__)


def path_and_rename(path):
    '''
    Given a directory `path` it creates a standrized file name.
    '''
    def wrapper(instance, filename, company):
        ext = filename.split('.')[-1]
        name = filename.split('.')[0]
        company = company.lower().replace(' ', '_')
        # get filename
        filename = f'{company}_{datetime.timestamp(timezone.now())}.{ext}'
        # return the whole path to the file
        return os.path.join(path, filename)
    return wrapper
    
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

    filename = path_and_rename('documents')
    filename = filename(f, f.name, company)
    
    if local:
        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        gc_url = None
    else:
        blob_name = 'company_data/' + filename.split('/')[-1]
        filename, gc_url = upload_blob_to_default_bucket(f, blob_name)
    
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

    if ('.xlsx' in file_path) or ('.xls' in file_path):
        df = pd.read_excel(file_path, chunksize=1, index_col=0).get_chunk(1)
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
    

    
    
class User(models.Model):
    '''
    User Model. The user of our application.
    '''
    name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    #password = None
    email = models.EmailField(max_length=250, unique=True)
    company = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    recieve_info_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class CompanyData(models.Model):
    '''
    Company Data Model. Stores the document location and is related to the User Model.
    '''
    document_location = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)