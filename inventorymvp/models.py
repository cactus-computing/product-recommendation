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
    filename = path_and_rename('documents')
    filename = filename(f, f.name, company)
    
    if local:
        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    else:
        blob_name = 'company_data/' + filename.split('/')[-1]
        filename, gc_url = upload_blob_to_default_bucket(f, blob_name)
    
    return filename, gc_url

def get_available_fields(file_path):
    if '.csv' in file_path:
        df = pd.read_csv(file_path, chunksize=1, index_col=0).get_chunk(1)
        return list(df.columns)

def rename_dataset(file_path, new_columns):
    
    new_columns = { v: k for k, v in new_columns.items() }
    df = pd.read_csv(file_path)
    df = df.rename(columns=new_columns)
    dataframe_to_gcs(df, file_path)
    

    
    
class User(models.Model):
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
    document_location = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)