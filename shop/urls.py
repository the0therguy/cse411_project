from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product_view/<int:id>/', views.product_view, name='product_view'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
