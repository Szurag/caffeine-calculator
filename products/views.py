from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product
from media.models import Media


@login_required(login_url='login')
def index(request):
    products = Product.objects.filter(created_by=request.user, is_global=False)
    return render(request, "products/index.html", {"products": products})


def add(request):
    return None


def product_detail(request):
    return None