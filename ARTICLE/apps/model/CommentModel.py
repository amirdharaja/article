from django.db import models
from apps.models import Login
from apps.model.ArticleModel import Article


class Comments(models.Model):

    login        =   models.ForeignKey(Login, on_delete=models.CASCADE, unique=False)
    article      =   models.ForeignKey(Article, on_delete=models.CASCADE, unique=False)
    comment      =   models.CharField(max_length=512, blank=False)

    objects = models.Manager()

    class Meta:
        db_table = "comments"
