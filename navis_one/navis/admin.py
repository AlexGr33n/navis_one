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


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ContentCategory)
admin.site.register(Content)


