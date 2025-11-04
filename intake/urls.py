from django.urls import path

from intake import views

urlpatterns = [
    path('add/', views.add_intake, name='add_intake'),
    path('delete/<int:intake_id>/', views.delete_intake, name='delete_intake')
]

