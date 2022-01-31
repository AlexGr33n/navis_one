from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=300)
    comment = models.CharField(max_length=300, null=True, blank=True)
    url = models.SlugField(max_length=300, unique=True)

    def __str__(self):
        return str(self.url)

    def get_absolute_url(self):
        return reverse('navis:product_list', args=[self.url])

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Filter(models.Model):
    name = models.CharField(max_length=300)
    comment = models.CharField(max_length=300, null=True, blank=True)
    url = models.SlugField(max_length=300, unique=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Filter"
        verbose_name_plural = "Filters"


class Commercial(models.Model):
    name = models.CharField(max_length=300)
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL, related_name="commercial_category", null=True, blank=True)
    comment = models.CharField(max_length=300, null=True, blank=True)
    url = models.SlugField(max_length=300, unique=True)
    image = models.ImageField(upload_to="commercial_image/", null=True, blank=True)
    source_commercial = models.CharField(max_length=300, null=True, blank=True)
    source_category = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name = "Commercial"
        verbose_name_plural = "Commercials"


class Product(models.Model):
    source_id = models.CharField(max_length=300, null=True, blank=True)
    article = models.CharField(max_length=300, null=True, blank=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL, related_name="product_category", null=True, blank=True)
    specification = models.CharField(max_length=300, null=True, blank=True)
    advanced_description = models.TextField("Advanced description", null=True, blank=True)
    is_active = models.BooleanField(default=1, null=True)
    comment = models.CharField(max_length=300, null=True, blank=True)
    filter = models.ManyToManyField(Filter, related_name="product_filter", blank=True)
    slug = models.SlugField(max_length=300, unique=True)
    commercial = models.ForeignKey(Commercial,
                                   on_delete=models.SET_NULL, related_name="product_commercial", null=True, blank=True)
    source_commercial = models.CharField(max_length=300, null=True, blank=True)
    source_category = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.article)

    def get_absolute_url(self):
        return reverse('navis:product_detail', args=[self.category.url, self.slug])

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    source_product = models.CharField(max_length=300, null=True, blank=True)
    image_url = models.URLField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "ProductImage"
        verbose_name_plural = "ProductImages"


class ContentCategory(models.Model):
    name = models.CharField(max_length=300)
    comment = models.CharField(max_length=300, null=True, blank=True)
    url = models.SlugField(max_length=300, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ContentCategory"
        verbose_name_plural = "ContentCategories"


class Content(models.Model):
    alias = models.SlugField(max_length=300, unique=True)
    published = models.BooleanField(default=0)
    main_image = models.ImageField(upload_to="content/main_image/", blank=True, null=True)
    category = models.ForeignKey(
        ContentCategory, on_delete=models.SET_NULL, related_name="content_category", null=True, blank=True)
    title = models.CharField(max_length=300, null=True)
    full_text = models.TextField(null=True)

    def __str__(self):
        return self.alias

    class Meta:
        verbose_name = "Content"
        verbose_name_plural = "Contents"
