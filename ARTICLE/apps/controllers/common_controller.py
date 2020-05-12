from django.contrib.auth.models import auth
from django.shortcuts import render, redirect
from django.contrib import messages

from datetime import datetime

from apps.models import Login
from apps.model.LoginHistoryModel import LoginHistory
from apps.model.ArticleModel import Article
from apps.model.CaregoryModel import Category
from apps.model.CommentModel import Comments
from apps.model.LikeArticleModel import LikeArticle

from apps.helpers import make_hash, pagination
from apps.email.email import send_email

from random import randint
from pluck import pluck


def home(request):
    if request.user.is_authenticated:
        intrests = Login.objects.filter(id=request.user.id).first()
        intrests = intrests.intrests.replace('[', '')
        intrests = intrests.replace(']', '')
        intrests = intrests.replace("'", '')
        print(intrests)
        intrests = intrests.split(',')
        intrests_id = []
        for d in intrests:
            intrests_id.append(int(d))
        articles = Article.objects.filter(category_id__in=intrests_id).order_by('-created_at')

    else:
        if 'category' in request.GET:
            articles = Article.objects.filter(category_id=request.GET['category']).order_by('-created_at')
        elif 'all' in request.GET:
            articles = Article.objects.filter().order_by('-created_at')
        else:
            articles = Article.objects.filter().order_by('-created_at')

    categories = Category.objects.filter()
    total = len(articles)
    articles = pagination(articles, request.GET.get('page'))
    login_ids = pluck(articles, 'login_id')
    user_details = Login.objects.filter(id__in=login_ids)
    categories = Category.objects.filter()
    all_articles = []
    for article in articles:
        for user_detail in user_details:
            if article.login_id == user_detail.id:
                data = {
                    'id':article.id,
                    'author':user_detail.first_name + ' ' + user_detail.last_name,
                    'title':article.title,
                    'image':article.image,
                    'content':article.content,
                    'created_at':article.created_at if not article.updated_at else article.updated_at,
                    'login_id':article.login_id,
                    'category_id':article.category_id,
                }
                all_articles.append(data)
    for d in all_articles:
        for category in categories:
            if category.id == d['category_id']:
                d.update({'category_name':category.name})
    return render(request, 'home.html', {'articles': articles, 'all_articles':all_articles, 'total':total, 'categories':categories})

def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    elif request.method == 'POST':
        check = Login.objects.filter(username=request.POST['username']).first()
        if not check:
            messages.error(request, 'Username or Email id not found')
            return render(request, 'login.html', {'username': request.POST['username']})

        if not check.active:
            messages.error(request, 'Your account has been blocked')
            return render(request, 'login.html', {'username': request.POST['username']})

        login = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if not login:
            messages.error(request, 'Sorry, Given password is wrong')
            return render(request, 'login.html', {'username':request.POST['username']})

        auth.login(request, login)

        new_login = LoginHistory(
            login_id=login.id,
            login_at=datetime.now(),
        )
        new_login.save()
        messages.success(request, 'Welcome {}'.format(login.first_name))
        return redirect('home')

    return render(request, 'login.html')

def register(request):
    if request.user.is_authenticated:
            messages.info(request, 'You already registred')
            return redirect('home')

    if request.method == 'POST':

        data = {
            'first_name': request.POST['first_name'].title(),
            'last_name': request.POST['last_name'].title(),
            'gender': request.POST['gender'].title(),
            'email': request.POST['email'],
            'password': request.POST['password'],
            'confirm_password': request.POST['confirm_password'],
            'mobile': request.POST['mobile'],
        }

        if not data['first_name']:
            messages.error(request, 'FIRSTNAME_IS_REQUIRED')
            return render(request, 'register.html', {'form':data})

        if not data['gender']:
            messages.error(request, 'GENDER_IS_REQUIRED')
            return render(request, 'register.html', {'form':data})

        if not data['email']:
            messages.error(request, 'EMAIL_REQUIRED')
            return render(request, 'register.html', {'form':data})

        if not data['mobile']:
            messages.error(request, 'PHONE_NUMBER_IS_REQUIRED')
            return render(request, 'register.html', {'form':data})

        check_phone = Login.objects.filter(mobile=data['mobile'])
        if check_phone:
            messages.error(request, 'MOBILE_NUMBER_ALREADY_EXISTS')
            return render(request, 'register.html', {'form': data})

        check_email = Login.objects.filter(username=data['email'])
        if check_email:
            messages.error(request, 'EMAIL_ALREADY_EXISTS')
            return render(request, 'register.html', {'form':data})

        if data['password'] != data['confirm_password']:
            messages.error(request, 'PASSWORD_MISMATCH, TRY_AGAIN')
            return render(request, 'register.html', {'form':data})

        Login(
            username = data['email'],
            password = make_hash(data['password']),
            first_name = data['first_name'],
            last_name = data['last_name'],
            gender = data['gender'],
            mobile = data['mobile'],
            intrests = request.POST.getlist('intrests', []),
            active=False
        ).save()

        messages.success(request, 'Mr/Mrs/Miss {}, YOUR_ACCOUNT_HAS_BEEN_CREATED_AND_OTP_SUCCESSFULLY_SEND_TO_YOUR_MAIL'.format(data['first_name']))
        return generate_otp(data['first_name'], data['last_name'], data['email'])

    category = Category.objects.filter()
    return render(request, 'register.html', {'category':category})

def generate_otp(first_name, last_name, email):
    randam_number = randint(1000, 9999)
    otp = str(randam_number) + ',' + email
    subject = 'OTP - SARAH Articles'
    content = '''Dear, {} {}\n
                Account successfully created.\n
                Enthe the following OTP to activate your account
                Your OTP : {}'''.format(first_name, last_name, randam_number)
    send_email(email, subject, content)
    response = redirect('otp')
    response.set_cookie('otp', otp)
    return response

def validate_otp(request):
    if request.method == 'POST':
        if 'otp' in request.COOKIES:
            otp = request.COOKIES['otp'].split(',')
            if request.POST['otp'] == otp[0]:
                login = Login.objects.filter(username=otp[1]).first()
                login.active = True
                login.save()
                messages.success(request, 'OTP VERIFIED, NOW YOU CAN LOGIN')
                response = redirect('login')
                response.delete_cookie('otp')
                return response

            messages.error(request, 'Invalid OTP')
            return redirect('otp')

        messages.success(request, 'OTP Not found')
        return redirect('register')

    return render(request, 'otp.html')

def resend_otp(request):
    if request.method == 'POST':
        login = Login.objects.filter(username=request.POST['email']).first()
        if not login:
            messages.error(request, 'Email not found')
            return redirect('login')

        otp = request.COOKIES['otp'].split(',')
        subject = 'OTP - SARAH Articles'
        content = '''Dear, {} {}\n
                    Your OTP : {}'''.format(login.first_name, login.last_name, otp[0])
        send_email(login.username, subject, content)
        return redirect('otp')

    return render(request, 'resend_otp.html')

def logout(request):
    auth.logout(request)
    response = redirect('home')
    # response.delete_cookie('kpr_ticket')
    return response

def get_comments(request):
    comments = Comments.objects.filter(article_id=request.GET['id']).order_by('-id')
    comments = pagination(comments, request.GET.get('page'))
    login_ids = pluck(comments, 'login_id')
    user_details = Login.objects.filter(id__in=login_ids)
    all_comments = []
    for comment, user_detail in zip(comments, user_details):
        if comment.login_id == user_detail.id:
            data = {
                'name' : user_detail.first_name + ' ' + user_detail.last_name,
                'comment': comment.comment
            }
            all_comments.append(data)
    return render(request, 'comments.html', {'comments':comments, 'all_comments':all_comments, 'id':request.GET['id']})

def make_like(request):
    if 'like' in request.GET:
        LikeArticle.objects.update_or_create(login_id=request.user.id, article_id=request.GET['like'], defaults={'is_like': True})
        messages.success(request, 'Thank You')
        return redirect('home')

    elif 'not_like' in request.GET:
        LikeArticle.objects.update_or_create(login_id=request.user.id, article_id=request.GET['not_like'], defaults={'is_like': False})
        messages.success(request, 'Thank You')
        return redirect('home')

def get_my_articles(request):
    articles = Article.objects.filter(login_id=request.user.id).order_by('-created_at')
    articles = pagination(articles, request.GET.get('page'))
    category = Category.objects.filter()
    return render(request, 'my_articles.html', {'articles':articles, 'category':category})

def delete_my_articles(request):
    Article.objects.filter(id=request.GET['id']).delete()
    Comments.objects.filter(article_id=request.GET['id']).delete()
    LikeArticle.objects.filter(article_id=request.GET['id']).delete()
    messages.success(request, 'Article deleted')
    return redirect('get_my_articles')

def update_article(request):
    article = Article.objects.filter(id=request.GET['id']).first()
    if 'title' in request.POST:
        article.title = request.POST['title'] if 'title' in request.POST else article.title
        article.content = request.POST['content'] if 'content' in request.POST else article.content
        article.category_id = request.POST['category_id'] if 'category_id' in request.POST else article.category_id
        article.updated_at = datetime.now()
        article.save()
        messages.success(request, 'Successfully updated')
        return redirect('get_my_articles')

    category = Category.objects.filter()
    return render(request, 'update_article.html', {'article':article, 'category':category})

def my_account(request):
    my = Login.objects.filter(id=request.user.id).first()
    article = Article.objects.filter(login_id=request.user.id)
    return render(request, 'account.html', {'my':my, 'total':len(article)})

def update_account(request):
    my = Login.objects.filter(id=request.user.id).first()
    my.first_name = request.POST['first_name'] if request.POST['first_name'] else my.first_name
    my.last_name = request.POST['last_name'] if request.POST['last_name'] else my.last_name
    my.mobile = request.POST['mobile'] if request.POST['mobile'] else my.mobile
    my.save()
    messages.success(request, 'Account updated')
    return redirect('my_account')

def update_password(request):
    my = Login.objects.filter(id=request.user.id).first()
    my.password = make_hash(request.POST['new_password'])
    my.save()
    messages.success(request, 'Password updated')
    return redirect('my_account')

def create_article(request):
    image = request.FILES['image']
    Article(
        title=request.POST['title'],
        image=image if image else None,
        content=request.POST['content'],
        category_id=request.POST['category_id'],
        login_id=request.user.id,
    ).save()
    messages.success(request, 'New article created')
    return redirect('get_my_articles')

def add_comment(request):
    Comments(
        comment = request.POST['comment'],
        article_id = request.POST['article_id'],
        login_id = request.user.id
    ).save()
    messages.success(request, 'Comment added')
    return redirect('/comments/?id={}'.format(request.POST['article_id']))