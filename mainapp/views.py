from django.shortcuts import render, get_object_or_404
from django.conf import settings

from basketapp.models import Basket
from mainapp.models import ProductCategory, Product

import json
import datetime
import os


def main(request):
    title = 'главная'
    # products = Product.objects.all()[:4]
    products = Product.objects.all()
    content = {'title': title, 'products': products}
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    print(pk)
    title = 'продукты'
    links_menu = ProductCategory.objects.all()

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)  #!!!!!!!!

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category = {'name': 'все', 'pk': 0}
        else:
            # category = ProductCategory.objects.get(pk=pk)
            category = get_object_or_404(ProductCategory,
                                         pk=pk)  # return 404 error in case required category is not found
            products_list = Product.objects.filter(category__pk=pk)

        content = {
            'title': title,
            'links_menu': links_menu,
            'products': products_list,
            'category': category,
            'basket': basket
        }

        return render(request, 'mainapp/products_list.html', content)

    same_products = Product.objects.all()
    # same_products = [
    #     {
    #         'name': 'Отличный стул',
    #         'desc': 'Не оторваться',
    #         'image_src': 'product-11.jpg',
    #         'alt': 'продукт 11'
    #     },
    #     {
    #         'name': 'Стул повышенного качества',
    #         'desc': 'комфортно',
    #         'image_src': 'product-21.jpg',
    #         'alt': 'продукт 21'
    #     },
    #     {
    #         'name': 'Стул премиального качества',
    #         'desc': 'росто попробуйте ',
    #         'image_src': 'product-31.jpg',
    #         'alt': 'продукт 31'
    #     },
    # ]

    content = {'title': title, 'links_menu': links_menu, 'same_products': same_products}
    return render(request, 'mainapp/products.html', content)


def contacts(request):
    title = 'о нас'
    visit_date = datetime.datetime.now()
    # locations = []
    file_path = os.path.join(settings.BASE_DIR, 'contacts.json')
    with open(file_path) as file_contacts:
        locations = json.load(file_contacts)
    content = {'title': title, 'visit_date': visit_date, 'locations': locations}
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
