from django.db import models
from django.utils import timezone
import os
from datetime import datetime

def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        name = filename.split('.')[0]
        # get filename
        filename = f'{name}_{datetime.timestamp(timezone.now())}.{ext}'
        # return the whole path to the file
        return os.path.join(path, filename)
    return wrapper


class Snippet(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    company = models.CharField(max_length=100)
    document = models.FileField(upload_to=path_and_rename('files'))
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name