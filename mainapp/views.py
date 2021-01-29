import random
import datetime
import os
import json

from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from django.core.cache import cache
from django.conf import settings
from django.views.decorators.cache import cache_page, never_cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from mainapp.models import ProductCategory, Product

JSON_PATH = 'mainapp/json'


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


@never_cache
def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
    if products is None:
        products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
        cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', errors='ignore') as infile:
        return json.load(infile)


def get_hot_product():
    product_list = Product.objects.all()
    # product_list = Product.objects.filter(is_active=True, category__is_active=True)  # если много категорий, то
    # при открытии раздела Продукты появляется ошибк аraise ValueError("Sample larger than population or is negative")
    # ValueError: Sample larger than population or is negative
    return random.sample(list(product_list), 1)[0]


def get_same_products(hot_product):
    return Product.objects.filter(category__pk=hot_product.category.pk).exclude(pk=hot_product.pk)[:3]


def main(request):
    title = 'главная'
    products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')[:3]
    content = {
        'title': title,
        'products': products}
    return render(request, 'mainapp/index.html', content)


# @cache_page(3600)  # uncomment in case I need to cache the products page
def products(request, pk=None, page=1):
    title = 'продукты'
    links_menu = get_links_menu()

    if pk is not None:
        if pk == 0:
            category = {'name': 'все', 'pk': 0}
            products = Product.objects.all().order_by('price')

        else:
            category = get_category(pk)
            products = Product.objects.filter(Q(category__pk=1) | Q(category__pk=2))

        paginator = Paginator(products, 2)  # отображение количества товаров на странице
        try:
            product_paginator = paginator.page(page)
        except PageNotAnInteger:
            product_paginator = paginator.page(1)  # Если польз ввел некоректный номер страницы, вывод первой стр
        except EmptyPage:
            product_paginator = paginator.page(paginator.num_pages)  # return last page to a user

        content = {
            'title': title,
            'links_menu': links_menu,
            'products': product_paginator,
            'category': category,
            # 'basket': basket
        }

        return render(request, 'mainapp/products_list.html', content)
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
        # 'basket': get_basket(request.user),
        'hot_product': hot_product,
    }
    return render(request, 'mainapp/products.html', content)


def product(request, pk):
    title = 'продукты'
    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk)
    }
    return render(request, 'mainapp/product.html', content)


def contacts(request):
    title = 'о нас'
    visit_date = datetime.datetime.now()
    locations = []
    file_path = os.path.join(settings.BASE_DIR, 'contacts.json')
    with open(file_path) as file_contacts:
        locations = json.load(file_contacts)
    content = {
        'title': title,
        'visit_date': visit_date,
        'locations': locations,
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
        'title': 'Все продукты',
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
        'title': 'Дом',
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
        'title': 'Офис',
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
        'title': 'Модерн',
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
        'title': 'Класика',
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', content)
