from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


SALT = settings.SALT
HASHER = settings.HASHER

def make_hash(user_password):
    hash_password = make_password(user_password, salt=SALT, hasher=HASHER)
    return hash_password

def pagination(data, page):
    paginator = Paginator(data, 10)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    return data