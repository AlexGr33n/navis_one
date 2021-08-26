from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import datetime


class Category(models.Model):
    name = models.CharField(max_length=500)
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return str(self.url)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.url})

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=500)
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'int': self.id})

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductImage(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    source_url = models.CharField(max_length=300, null=True, blank=True)
    image_url = models.URLField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "ProductImage"
        verbose_name_plural = "ProductImages"


