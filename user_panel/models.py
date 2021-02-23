from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone
import os
from datetime import datetime
import logging
from .storage import upload_blob_to_default_bucket, dataframe_to_gcs
import pandas as pd


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Company = models.CharField(max_length=100)


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

class CompanyData(models.Model):
    '''
    Company Data Model. Stores the document location and is related to the User Model.
    '''
    document_location = models.CharField(max_length=500)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)