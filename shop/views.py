from datetime import date

from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth.views import PasswordChangeView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View

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
                return redirect('login/')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')  # passes this message
                # print('email taken')
                return redirect('registration/')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=f_name,
                                                last_name=l_name)
                user.save()
                customer = Customer.objects.create(
                    **{'id': user.id, 'user': user, 'name': f_name + " " + l_name,
                       'sex': sex})
                customer.save()
                messages.info(request, 'You are successfully registered. Now login.')  # passes this message
                # print("DONE")
                return redirect('login')
                # return HttpResponse('Successfully created')

        else:
            messages.info(request, 'password not matching')
            return redirect('registration')
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
            # return HttpResponse("Successfully logged in")
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'shop/login.html')


def logout(request):
    auth.logout(request)
    # return HttpResponse('/')
    return redirect('home')


class PasswordsChangeView(PasswordChangeView):
    # form_class = PasswordChangeForm
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')


def password_success(request):
    return render(request, 'shop/password_success.html')


def add_to_cart(request, id):
    current_user = request.user
    product = get_object_or_404(Product, id=id)
    customer = Customer.objects.get(id=current_user.id)
    order_item, created = OrderItem.objects.get_or_create(product=product,
                                                          customer=customer,
                                                          ordered=False)
    order_qs = Order.objects.filter(**{'customer': customer, 'ordered': False}).first()
    if order_qs is None:
        order = Order.objects.create(
            **{'customer': customer, 'date_ordered': str(date.today())})
        order.products.add(order_item)
        order.save()
        messages.info(request, "This item was added to your cart.")
        return redirect("order_summary")
    else:
        if order_qs.products.filter(product__id=product.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
            return redirect("order_summary")
        else:
            order_qs.products.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("order_summary")


def remove_from_cart(request, id):
    current_user = request.user
    product = get_object_or_404(Product, id=id)
    customer = Customer.objects.get(id=current_user.id)
    order_item, created = OrderItem.objects.get_or_create(product=product,
                                                          customer=customer,
                                                          ordered=False)
    order_qs = Order.objects.filter(**{'customer': customer, 'ordered': False}).first()
    if order_qs is None:
        messages.info(request, "you do not have an active order")
        return redirect("/")
    else:
        if order_qs.products.filter(product__id=product.id).exists():
            order_item = OrderItem.objects.filter(product=product,
                                                  customer=customer,
                                                  ordered=False)[0]

            order_item.quantity -= 1
            if order_item.quantity == 0:
                order_qs.products.remove(order_item)
                order_item.delete()
                order_qs.save()
            else:
                order_item.save()
            messages.info(request, "This item is updated")
        else:
            messages.info(request, "This is not in your cart")
            return redirect("order_summary")

    return redirect("order_summary")


def remove_full_product_from_cart(request, id):
    product = get_object_or_404(Product, id=id)
    customer = Customer.objects.get(id=1)
    order_item, created = OrderItem.objects.get_or_create(product=product,
                                                          customer=customer,
                                                          ordered=False)
    order_qs = Order.objects.filter(**{'customer': customer, 'ordered': False}).first()
    if order_qs is None:
        messages.info(request, "you do not have an active order")
        return redirect("/")
    else:
        if order_qs.products.filter(product__id=product.id).exists():
            order_item = OrderItem.objects.filter(product=product,
                                                  customer=customer,
                                                  ordered=False)[0]

            order_qs.products.remove(order_item)
            order_item.delete()
            messages.info(request, "This item is removed from your cart")
        else:
            messages.info(request, "This is not in your cart")
            return redirect("order_summary")

    return redirect("order_summary")


def order_summary(request):
    current_user = request.user
    customer = Customer.objects.get(id=current_user.id)
    order = Order.objects.get(customer=customer, ordered=False)
    context = {'order': order}
    return render(request, 'shop/order_summary.html', context=context)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form,
        }
        return render(self.request, 'shop/checkout.html', context=context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(customer=Customer.objects.get(id=1), ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                phone_number = form.cleaned_data.get('phone_number')
                area = form.cleaned_data.get('area')
                district = form.cleaned_data.get('district')
                payment_options = form.cleaned_data.get('payment_options')
                shipping_address = Address.objects.create(**
                                                          {'customer': Customer.objects.get(id=1),
                                                           'phone_number': phone_number,
                                                           'street': street_address,
                                                           'apartment': apartment_address,
                                                           'area': area,
                                                           'district': district, }
                                                          )
                shipping_address.save()
                order.shipping_address = shipping_address
                order.save()
                # if payment_options == 'C':
                #     order.update(**{'ordered': True})
                #     order.save()
                #     return render(self.request, 'shop/order_confirmation.html')
                return redirect("checkout")
            messages.warning(self.request, "Failed checkout")
            return redirect("checkout")
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("checkout")


def profile(request):
    
    current_user = request.user
    customer = Customer.objects.get(id=current_user.id)
    user = User.objects.get(id=current_user.id)
    name = customer.__dict__.get('name')
    sex = customer.__dict__.get('sex')
    first_name = user.__dict__.get('first_name')
    last_name = user.__dict__.get('last_name')
    email = user.__dict__.get('email')
    username = user.__dict__.get('username')
    order = Order.objects.filter(**{'customer': customer, 'ordered': True})
    context = {'name': name, 'sex': sex, 'first_name': first_name, 'last_name': last_name, 'email': email,
               'username': username,
               'order': order}
    return render(request, 'shop/profile.html', context=context)
