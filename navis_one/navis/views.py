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


def product_list(request, category_slug):
    categories = Category.objects.all()
    category = get_object_or_404(Category, url=category_slug)
    products = Product.objects.filter(category_id=category)
    paginator = Paginator(products, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj, 'category': category, 'categories': categories, 'products': products
    }
    return render(request, 'navis_one/product/product_list.html', context)


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    context = {'product': product}
    return render(request, 'navis_one/product/product_detail.html', context)
