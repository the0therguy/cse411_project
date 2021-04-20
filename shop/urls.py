from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product_view/<int:id>/', views.product_view, name='product_view'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # path('change_password/', auth_views.PasswordChangeView.as_view(template_name='shop/change_password.html'), name='change_password')
    path('change_password/', views.PasswordsChangeView.as_view(template_name='shop/change_password.html')),
    path('password_success/', views.password_success, name='password_success'),
]
