from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:id>/', views.product_view, name='product'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # path('change_password/', auth_views.PasswordChangeView.as_view(template_name='shop/change_password.html'), name='change_password')
    path('change_password/', views.PasswordsChangeView.as_view(template_name='shop/change_password.html')),
    path('password_success/', views.password_success, name='password_success'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='shop/password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='shop/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='shop/password_reset_complete.html'),
         name='password_reset_complete'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
]
