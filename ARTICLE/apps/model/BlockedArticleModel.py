from django.db import models
from apps.models import Login
from apps.model.ArticleModel import Article


class BlockedArticle(models.Model):

    login        =   models.ForeignKey(Login, on_delete=models.CASCADE, unique=False)
    article      =   models.ForeignKey(Article, on_delete=models.CASCADE, unique=False)

    objects = models.Manager()

    class Meta:
        db_table = "blocked_articles"
