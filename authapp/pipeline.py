import datetime
import os
import urllib.request
from collections import OrderedDict
from urllib.parse import urlencode, urlunparse

import requests
from django.conf import settings
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return
    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_400_orig')),
                                                access_token=response['access_token'],
                                                v='5.92')),
                          None
                          ))
    resp = requests.get(api_url)
    if resp.status_code !=200:
        return
    else:
        print('error during receiving error from VK API')

    data = resp.json()['response'][0]

    if data['sex']:  # потестировать если скрыта инфа о поле (ЕСЛИ ОНА ВООБЩЕ СКРЫВАЕТСЯ!!!), то будет ли вытягиваться?
        if data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE
        elif data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
    if data['about']:  # потестировать если скрыта инфа о себе, то будет ли вытягиваться?
        user.shopuserprofile.about_me = data['about']
    if data['bdate']:  # потестировать если скрыта инфа о дате рождения, то будет ли вытягиваться?
        bdate = datetime.datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        # проверка если пользователю есть 18 лет
        age = timezone.now().date().year - bdate.year  # потенциально может быть ошибка - можно потестить
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        if data['photo_400_orig']:
            urllib.request.urlretrieve(
                data['photo_400_orig'],
                os.path.join(settings.MEDIA_ROOT, 'users_avatars', f'{user.pk}.jpg'))
        user.avatar = os.path.join('users_avatars', f'{user.pk}.jpg')
    user.save()





