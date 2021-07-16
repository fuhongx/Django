import random

from django.http import HttpResponse
from django.shortcuts import render, redirect
from . import models
from . import forms
from .serializers import tian1Serializer
# Create your views here.
from numpy.random.mtrand import randint

from .models import tian1

# 创建api接口
from rest_framework import viewsets
class tian1ViewSet(viewsets.ModelViewSet):
    queryset = tian1.objects.all()
    serializer_class = tian1Serializer

# 使密码不可视化
import hashlib

def hash_code(s, salt='lf'):  # 加点盐,salt变量很重要，要牢记
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

# 验证邮箱验证码
import datetime

def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.username, now)
    models.ConfirmString.objects.create(code=code, user=user,)
    return code


# send_email
from django.conf import settings

def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '来自www.liufengblog.com的注册确认邮件'

    text_content = '''感谢注册www.liufengblog.com，这里是流风的博客和教程站点，专注于Python、Django和机器学习技术的分享！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.liufengblog.com</a>，\
                    这里是流风的博客和教程站点，专注于Python、Django和机器学习技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# def index(request):
#     # first = ['刘','李','张','王','郑','蒋']
#     # last_name = ['三','四','五','六','七']
#     # sex1 = ['female','male']
#     # tian1s = []
#     # for id in range(10):
#     #     username = first[randint(0,5)]+last_name[randint(0,4)]+str(randint(1,1000))
#     #     tian1s.append(tian1(username=username,password=str(randint(10000,99999)),sex=random.choice(sex1),phone=str(randint(10000000,999999999))))
#     # tian1.objects.bulk_create(tian1s)
#
#     return HttpResponse('ok')


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request,'login/index.html')


def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == "POST":
        login_form = forms.Tian1Form(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            try:
                user = models.tian1.objects.get(username=username)
            except:
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())

            if not user.has_confirmed:
                message = '该用户还未经过邮件确认！'
                return render(request, 'login/login.html', locals())

            if user.password == hash_code(password):  # 注意hash_code
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())

    login_form = forms.Tian1Form()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            phone = register_form.cleaned_data.get('phone')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.tian1.objects.filter(username=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())
                same_phone_user = models.tian1.objects.filter(phone=phone)
                if same_phone_user:
                    message = '该手机号码已经被注册了！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.tian1.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request,'login/register.html',locals())

                new_user = models.tian1()
                new_user.username = username
                new_user.password = hash_code(password1)
                new_user.phone = phone
                new_user.email = email
                new_user.sex = sex
                new_user.save()


                code = make_confirm_string(new_user)
                send_email(email, code)

                message = '请前往邮箱进行确认！'
                return render(request, 'login/confirm.html', locals())
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")


def shouye(request):
    data = tian1.objects.all()
    print(data)
    # data.delete()
    return HttpResponse('ok')


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())