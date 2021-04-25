from django.db import models
from django.utils import timezone
import os
from datetime import datetime
import logging

logger = logging.Logger(__name__)

class Suscription(models.Model):
    '''
    User Model. The user of our application.
    '''
    #name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    #company = models.CharField(max_length=250, default=None, blank=True, null=True)

    def __str__(self):
        return self.email

class Contact(models.Model):
    '''
    Model contact. Allows the user to send his personal data.
    '''
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    phone = models.CharField(max_length=9)
    website = models.CharField(max_length=2000, default=None)
    created_at = models.DateTimeField(auto_now=True)
    