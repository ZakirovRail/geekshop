from django.contrib.auth.models import AbstractUser
from django.db import models


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatar', blank=True, verbose_name='аватар')
    age = models.PositiveSmallIntegerField(verbose_name='возраст')
