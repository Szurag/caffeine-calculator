from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.utils import timezone

from intake.models import Intake
from products.models import Product


def landing(request):
    products_all = Product.objects.filter(is_global=True)
    products_with_high_caffeine = Product.objects.filter(caffeine_mg__gte=160)

    searched_products = None
    searchQuery = request.GET.get('search')
    if searchQuery:
        searched_products = Product.objects.filter(name__icontains=searchQuery)

    return render(request, "users/landing.html", {
        "products_all": products_all,
        "products_with_high_caffeine": products_with_high_caffeine,
        "searched_products": searched_products
    })


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


@login_required(login_url='login')
def dashboard(request):
    products_all = Product.objects.filter(is_global=True)
    user_products = Product.objects.filter(created_by=request.user)

    today = timezone.now().date()

    total_caffeine = (
        Intake.objects.filter(
            user=request.user,
            timestamp__date=today
        )
        .aggregate(total=Sum('product__caffeine_mg', distinct=False))
    )

    drink_count = Intake.objects.filter(
        user=request.user,
        timestamp__date=today
    ).count()

    your_intakes = Intake.objects.filter(
        user=request.user,
        timestamp__date=today
    )

    return render(request, "users/dashboard.html", {
        "products_all": products_all,
        "user_products": user_products,
        "total_caffeine": total_caffeine["total"] or 0,
        "drink_count": drink_count,
        "intakes": your_intakes
    })
