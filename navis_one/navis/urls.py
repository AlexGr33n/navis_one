from django.urls import path
from . import views
app_name = 'navis'

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('<slug:category_slug>/', views.product_list, name='product_list'),
    # path('<slug:category_slug>/<slug:slug>/', views.product_detail, name='product_detail'),

]
