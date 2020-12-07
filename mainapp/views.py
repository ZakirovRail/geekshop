from django.shortcuts import render
from django.conf import settings

import json
import datetime
import os

# Create your views here.
from mainapp.models import Product


def main(request):
    # content = {
    #     'users': ['Oleg', 'Django', 'Geekbrains']
    # }

    # content = {
    #     'user': {
    #         'first_name': 'oleg',
    #         'last_name': 'maslov',
    #     }
    # }
    # content = {
    #     'title': 'Главная',
    # }

    title = 'главная'
    products = Product.objects.all()[:4]
    content = {'title': title, 'products': products}
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    print(pk)
    title = 'продукты'
    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]

    same_products = [
        {
            'name': 'Отличный стул',
            'desc': 'Не оторваться',
            'image_src': 'product-11.jpg',
            'alt': 'продукт 11'
        },
        {
            'name': 'Стул повышенного качества',
            'desc': 'комфортно',
            'image_src': 'product-21.jpg',
            'alt': 'продукт 21'
        },
        {
            'name': 'Стул премиального качества',
            'desc': 'росто попробуйте ',
            'image_src': 'product-31.jpg',
            'alt': 'продукт 31'
        },
    ]

    content = {
        'title': title,
        # 'links_menu': links_menu,
        'same_products': same_products
    }
    return render(request, 'mainapp/products.html', content)


def contacts(request):
    title = ''
    visit_date = datetime.datetime.now()
    locations = []
    file_path = os.path.join(settings.BASE_DIR, 'contacts.json')
    with open(file_path) as file_contacts:
        locations = json.load(file_contacts)
    content = {
        'title': title, 'visit_date': visit_date, 'locations': locations
    }
    return render(request, 'mainapp/contacts.html', content)


def products_all(request):
    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', content)


def products_home(request):
    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', content)


def products_office(request):
    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', content)


def products_modern(request):
    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', content)


def products_classic(request):
    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', content)
