from django.conf import settings
from django.contrib import auth
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm
from authapp.models import ShopUser


# def send_verify_mail(user):
#     verify_link = reverse(
#         'auth:verify',
#         args=[user.email, user.activation_key])
#
#     title = f'Подтверждение учетной записи'
#     message = f'Для подтверждения учетной записи {user.username}\
#               на портале {settings.DOMAIN_NAME} перейдите по ссылке \
#               \n{settings.DOMAIN_NAME}{verify_link}'
#
#     print(f'from: {settings.EMAIL_HOST_USER}, to {user.email}')
#     return send_mail(
#         title,
#         message,
#     )

def send_verify_email(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    subject = 'Подтверждение учетной записи'
    message = f'{settings.DOMAIN_NAME}{verify_link}'  # ПРОВЕРКА сообщения на соответствие требованиям

    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def login(request):
    title_login = 'Авторизация пользователя'
    login_form = ShopUserLoginForm(data=request.POST)
    next_url = request.GET.get('next', '')

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            return HttpResponseRedirect(reverse('main'))
    content = {'title': title_login, 'login_form': login_form, 'next': next_url}
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    title_register = 'Регистрация нового пользователя'
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            if send_verify_email(user):
                print('Success confirmation registration ')
            else:
                print('Error confirmation registration')
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    content = {'title': title_register, 'register_form': register_form}
    return render(request, 'authapp/register.html', content)


def edit(request):
    title_edit = 'Изменение данных'
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_edit_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('authapp:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_edit_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)

    content = {'title': title_edit, 'edit_form': edit_form, 'profile_form': profile_edit_form}
    return render(request, 'authapp/edit.html', content)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            print(user.activation_key)
            user.activation_key = ''  # если закоментировать эту строку, то пользователь повторно может перейти
            # на страницу подтверждения по ссылке
            user.is_active = True
            user.save()
            auth.login(request, user)
        return render(request, 'authapp/verification.html')
    except Exeption as e:
        print('error')