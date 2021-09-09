from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *


def index(request):
    return render(request, 'navis_one/index.html')


def about(request):
    return render(request, 'navis_one/about.html')


def contact(request):
    return render(request, 'navis_one/contact.html')


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, url=category_slug)
        products = products.filter(category=category)
    context = {'category': category, 'categories': categories, 'products': products}
    return render(request, 'navis_one/product/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {'product': product}
    return render(request, 'navis_one/product/product_detail.html', context)
