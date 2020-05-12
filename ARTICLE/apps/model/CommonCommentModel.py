from django.db import models
from apps.models import Login


class CommonComments(models.Model):

    login        =   models.ForeignKey(Login, on_delete=models.CASCADE, unique=False)
    comment      =   models.CharField(max_length=512, blank=False)

    objects = models.Manager()

    class Meta:
        db_table = "common_comments"
