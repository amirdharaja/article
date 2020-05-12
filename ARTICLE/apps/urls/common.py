from django.urls import path

from apps.controllers.common_controller import (
    login,
    home,
    register,
    validate_otp,
    resend_otp,
    logout,
    get_comments,
    make_like,
    get_my_articles,
    delete_my_articles,
    update_article,
    my_account,
    update_account,
    update_password,
    create_article,
    add_comment
)


urlpatterns = [
    path('', home, name='home'),
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('validate-otp/', validate_otp, name='otp'),
    path('resend-otp/', resend_otp, name='resend_otp'),
    path('logout/', logout, name='logout'),
    path('comments/', get_comments, name='get_comments'),
    path('like/', make_like, name='make_like'),
    path('my-articles/', get_my_articles, name='get_my_articles'),
    path('delete/', delete_my_articles, name='delete_my_articles'),
    path('update/', update_article, name='update_article'),
    path('account/', my_account, name='my_account'),
    path('update-account', update_account, name='update_account'),
    path('update-password', update_password, name='update_password'),
    path('add-comment', add_comment, name='add_comment'),
    path('new-article', create_article, name='create_article'),


]
