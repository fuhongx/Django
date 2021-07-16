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