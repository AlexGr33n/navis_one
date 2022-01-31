from modeltranslation.translator import register, TranslationOptions
from .models import Product, ContentCategory, Category, Content, Filter


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'comment')


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'advanced_description', 'comment')


@register(ContentCategory)
class CatalogCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'comment')


@register(Content)
class ContentTypeMethodTranslationOptions(TranslationOptions):
    fields = ('title', 'full_text')


@register(Filter)
class FilterTranslationOptions(TranslationOptions):
    fields = ('name', 'comment')

