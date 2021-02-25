from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
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


class CompanyData(models.Model):
    '''
    Company Data Model. Stores the document location and is related to the User Model.
    '''
    document_location = models.CharField(max_length=500)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)