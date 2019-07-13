"""
Model for url to hash mapping
"""
from django.db import models

class Url(models.Model):
    # User input url
    url = models.TextField()
    # Url hash
    hash = models.CharField(max_length=7, null=True)
