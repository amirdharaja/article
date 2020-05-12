from django.db import models

from apps.models import Login
from apps.model.CaregoryModel import Category



class Article(models.Model):

    login       =   models.ForeignKey(Login, on_delete=models.CASCADE, unique=False)
    category    =   models.ForeignKey(Category, on_delete=models.CASCADE, unique=False, null=True)
    title       =   models.CharField(max_length=128, blank=False)
    image       =   models.FileField(upload_to='images/', null=True)
    content     =   models.TextField(null=True)
    created_at  =   models.DateTimeField(auto_now_add=True)
    updated_at  =   models.DateTimeField(null=True)

    objects = models.Manager()


    class Meta:
        db_table = "articles"