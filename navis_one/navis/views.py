from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View

from .models import *

def index(request):
    return render(request, 'navis_one/index.html')
