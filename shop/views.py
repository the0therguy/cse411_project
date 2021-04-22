from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import *


# Create your views here.

def home(request):
    products = Product.objects.all()
    "Hello najia"
    context = {'products': products}
    return render(request, 'shop/home.html', context)


def product_view(request, id):
    product = Product.objects.get(id=id)
    context = {'product': product}
    return render(request, 'shop/product_view.html', context=context)


def registration(request):
    if request.method == 'POST':
        f_name = request.POST['first_name']  # 'first_name' this name came from HTML tag name
        l_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        sex = request.POST['sex']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:  # checking if the confirmation password matches or not
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')  # passes this message (also edit in HTML)
                # print("User name taken")
                return redirect('registration')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')  # passes this message
                # print('email taken')
                return redirect('registration')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=f_name,
                                                last_name=l_name)
                user.save()
                customer = Customer.objects.create(
                    **{'id': user.id, 'user': user, 'name': f_name + " " + l_name, 'phone_number': phone_number,
                       'sex': sex})
                customer.save()
                messages.info(request, 'DONE')  # passes this message
                # print("DONE")
                return HttpResponse('Successfully created')
        else:
            messages.info(request, 'password not matching')
            return redirect('registration/')
        # return redirect('/')  # returns to homepage
    else:  # sending a get rqst
        return render(request, 'shop/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)  # auto matches the user name and password
        if user is not None:  # means username and password exist
            auth.login(request, user)
            return HttpResponse("Successfully logged in")
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'shop/login.html')


def logout(request):
    auth.logout(request)
    return HttpResponse('/')


class PasswordsChangeView(PasswordChangeView):
    # form_class = PasswordChangeForm
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')


def password_success(request):
    return render(request, 'shop/password_success.html')

