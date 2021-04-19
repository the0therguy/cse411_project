from django.shortcuts import render

from .forms import *


# Create your views here.

def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/home.html', context)


def product_view(request, id):
    product = Product.objects.get(id=id)
    context = {'product': product}
    return render(request, 'shop/product_view.html', context=context)
