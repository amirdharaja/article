from django.db import models
from datetime import datetime

class Contact(models.Model):

    email       =   models.CharField(max_length=255, blank=True)
    details     =   models.CharField(max_length=255, blank=True)
    response    =   models.CharField(max_length=1024, blank=True)
    created_at  =   models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        db_table = "contact"