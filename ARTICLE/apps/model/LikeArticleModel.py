from django.db import models
from apps.models import Login
from apps.model.ArticleModel import Article


class LikeArticle(models.Model):

    login        =   models.ForeignKey(Login, on_delete=models.CASCADE, unique=False)
    article      =   models.ForeignKey(Article, on_delete=models.CASCADE, unique=False)
    is_like      =   models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        db_table = "like_articles"
