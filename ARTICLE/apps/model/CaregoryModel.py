from django.db import models

from apps.models import Login



class Category(models.Model):

    name       =   models.CharField(max_length=128, blank=False)
    created_at  =   models.DateTimeField(auto_now_add=True)
    updated_at  =   models.DateTimeField(null=True)

    objects = models.Manager()


    class Meta:
        db_table = "categories"