from django.db import models
from django.utils import timezone
import os
from datetime import datetime
import logging
import pandas as pd

logger = logging.Logger(__name__)

class User(models.Model):
    '''
    User Model. The user of our application.
    '''
    name = models.CharField(max_length=250)
    company = models.CharField(max_length=250, default=None, blank=True, null=True)
    email = models.EmailField(max_length=250, unique=True)

    def __str__(self):
        return self.email
