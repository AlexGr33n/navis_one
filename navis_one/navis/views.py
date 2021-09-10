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
    products = Product.objects.all()
    category = get_object_or_404(Category, url=category_slug)
    products = products.filter(category=category)
    context = {'category': category, 'categories': categories, 'products': products}
    return render(request, 'navis_one/product/product_list.html', context)


def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug)
    category = get_object_or_404(Category, url=category_slug)
    context = {'category': category, 'product': product}
    return render(request, 'navis_one/product/product_detail.html', context)


class Search(ListView):
    paginate_by = 15

    def get_queryset(self):
        return Product.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context

