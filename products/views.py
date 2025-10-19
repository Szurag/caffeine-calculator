import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from .forms import AddProductForm
from .models import Product
from media.models import Media


@login_required(login_url='login')
def index(request):
    products = Product.objects.filter(created_by=request.user, is_global=False)
    return render(request, "products/index.html", {"products": products})


@login_required(login_url='login')
def add(request):
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.is_global = False

            photo_file = form.cleaned_data.get('photo')
            if photo_file:
                media = Media()
                media.file = photo_file
                media.uploaded_by = request.user
                media.save()
                product.photo = media

            product.save()
            messages.success(request, f'Produkt "{product.name}" został dodany pomyślnie!')
            return redirect('product_index')
    else:
        form = AddProductForm()

    return render(request, "products/add.html", {"form": form})


@login_required(login_url='login')
def product_detail(request, product_id):
    return render(request, "products/detail.html", {"product_id": product_id})

@login_required(login_url='login')
def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id, created_by=request.user, is_global=False)
        product_name = product.name

        if product.photo:
            product.photo.delete()

        product.delete()
        messages.success(request, f'Produkt "{product_name}" został usunięty.')
    except Product.DoesNotExist:
        messages.error(request, 'Nie znaleziono produktu lub nie masz do niego dostępu.')
    except Exception as e:
        messages.error(request, f'Błąd podczas usuwania produktu: {str(e)}')

    return redirect('product_index')