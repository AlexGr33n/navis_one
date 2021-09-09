from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from modeltranslation.admin import TranslationAdmin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe

from .models import *

admin.site.site_title = 'Navis.one'
admin.site.site_header = 'Navis.one'


class ContentAdminForm(forms.ModelForm):
    full_text_ru = forms.CharField(widget=CKEditorUploadingWidget())
    full_text_uk = forms.CharField(widget=CKEditorUploadingWidget())
    full_text_en = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Content
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ('name',)


@admin.register(ContentCategory)
class ContentCategoryAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ('name',)


@admin.register(Content)
class ContentAdmin(TranslationAdmin):
    list_display = ('id', 'title', 'alias', 'category_id', 'main_image', 'published')
    list_filter = ('category_id',)
    list_display_links = ('title',)
    readonly_fields = ('get_main_image',)
    save_on_top = True
    form = ContentAdminForm

    def get_main_image(self, obj):
        return mark_safe(f'<img src={obj.main_image.url} widht="50" height="60"')

    get_main_image.short_description = 'image'


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'article', 'specification', 'category', 'slug', 'is_active')
    list_display_links = ('name', 'article',)
    search_fields = ('name', 'article',)


@admin.register(Filter)
class FilterAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ('name',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image_url')
    list_display_links = ('product',)
