from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='media_folder_product')
def media_folder_product(string):
    if not string:
        string = 'products_images/default.png'
    return f'{settings.MEDIA_URL}{string}'


def media_folder_users(string):
    if not string:
        string = 'users_avatars/default.jpg'
    return f'{settings.MEDIA_URL}{string}'


register.filter('media_folder_users', media_folder_users)


@register.filter(name='capitalize_name_user')
def capitalize_name_user(string):
    return string.capitalize()
