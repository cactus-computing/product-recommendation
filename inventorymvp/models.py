from django.db import models
from django.utils import timezone
import os
from datetime import datetime
import logging
from django.forms import ValidationError
from .storage import upload_blob_to_default_bucket

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
        filename = upload_blob_to_default_bucket(f, blob_name)
    
    return filename

class User(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    #password = None
    email = models.EmailField(max_length=180, unique=True)
    company = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    recieve_info_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def create_user(self):
        pass

    def search(self, email_string):
        try:
            uid = self.objects.get(email=email_string)
        except User.DoesNotExist:
            return None
        return uid

class CompanyData(models.Model):
    document_location = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)