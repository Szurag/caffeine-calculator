from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='product_index'),
    path('add/', views.add, name='product_add'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
]

