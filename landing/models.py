from django.db import models
from django.utils import timezone
import os
from datetime import datetime
import logging
import pandas as pd

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
