from django.contrib import admin
from apps.models import Login
from apps.model.ArticleModel import Article


class LoginAdmin(admin.ModelAdmin):
    list_display = ['username', 'role', 'active']
    search_fields = ['username']

class UserAdmin(admin.ModelAdmin):
    list_display = [
        'title',
    ]
    search_fields = ['title',]

admin.site.register(Article, UserAdmin)
