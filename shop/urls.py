from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product_view/<int:id>/', views.product_view, name='product_view'),

]
