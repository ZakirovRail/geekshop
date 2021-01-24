import random, datetime, os, json

from django.shortcuts import render, get_object_or_404
from mainapp.models import ProductCategory, Product
from django.core.cache import cache
from django.conf import settings
from django.views.decorators.cache import cache_page, never_cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from basketapp.models import Basket

JSON_PATH = 'mainapp/json'


# def get_basket(user):
#     if user.is_authenticated:
#         return Basket.objects.filter(user=user)
#     else:
#         return []


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
        # return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


@never_cache  # exclude from caching, when the whole site is cached
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


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', errors='ignore') as infile:
        return json.load(infile)


def get_hot_product():
    product_list = Product.objects.all()
    # product_list = Product.objects.filter(is_active=True, category__is_active=True)  # добавить в требование, будет дефект
    return random.sample(list(product_list), 1)[0]


def get_same_products(hot_product):
    return Product.objects.filter(category__pk=hot_product.category.pk).exclude(pk=hot_product.pk)[:3]


def main(request):
    title = 'главная'
    # products = Product.objects.all()[:4]
    # products = Product.objects.all()
    # products = Product.objects.filter(is_active=True, category__is_active=True)
    #    uncomment to improve performance - reduce number of requests to DB
    products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')[:3]
    content = {
        'title': title,
        'products': products}
    return render(request, 'mainapp/index.html', content)


@cache_page(3600)
def products(request, pk=None, page=1):
    # print(pk)
    title = 'продукты'
    links_menu = get_links_menu()
    # basket = get_basket(request.user)

    if pk is not None:
        if pk == 0:
            category = {'name': 'все', 'pk': 0}
            products = Product.objects.all().order_by('price')

        else:
            # category = ProductCategory.objects.get(pk=pk)
            category = get_category(pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        paginator = Paginator(products, 5)  # отображение количества товаров на странице - поиграть со значениями+requir
        try:
            product_paginator = paginator.page(page)
        except PageNotAnInteger:
            product_paginator = paginator.page(1)
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
        # 'basket': get_basket(request.user),
        'product': get_object_or_404(Product, pk=pk)
    }
    return render(request, 'mainapp/product.html', content)


def contacts(request):
    title = 'о нас'
    visit_date = datetime.datetime.now()
    # locations = []
    file_path = os.path.join(settings.BASE_DIR, 'contacts.json')
    with open(file_path) as file_contacts:
        locations = json.load(file_contacts)
    content = {
        'title': title,
        'visit_date': visit_date,
        'locations': locations,
        # 'basket': get_basket(request.user)
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
