from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

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


@login_required
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


def checkout(request):
    if request.method == 'POST':
        street_address = request.POST.get('street')
        apartment_address = request.POST.get('apartment')
        phone_number = request.POST.get('phone_number')
        area = request.POST.get('area')
        district = request.POST.get('district')
        payment_option = request.POST.get('payment-option')
        if payment_option == 'cash':
            shipping_address = Address.objects.create(**{
                'customer': Customer.objects.get(id=1),
                'phone_number': phone_number,
                'street': street_address,
                'apartment': apartment_address,
                'area': area,
                'district': district
            })
            shipping_address.save()
            order_item = Order.objects.filter(**{'customer': Customer.objects.get(id=1), 'ordered': False})
            payment = PaymentTable.objects.create(**{
                'customer': Customer.objects.get(id=1),
                'payment_option': payment_option,
                'transaction_id': '',
            })
            payment.save()
            order_item.update(**{'shipping_address': shipping_address, 'payment': payment, 'ordered': True})
            context = {'order': order_item}
            return render(request, 'shop/cash_payment.html', context=context)
        else:
            messages.info(request, "Those options are not available at this moment")
            return redirect("checkout")

    else:
        context = {}
        return render(request, 'shop/checkout.html', context=context)


@login_required
def order_accepting(request):
    user = request.user
    if user.is_staff:
        if request.method == "POST":
            return HttpResponse("shei")
        order = Order.objects.filter(**{'being_delivered': False})
        # print(order.values())
        context = {'order': order}
        return render(request, 'shop/order_accept.html', context=context)
    return HttpResponse("Permission denied")


@login_required
def delivery_boy(request):
    user = request.user
    if user.is_staff:
        return HttpResponse("You already regisered")
    if request.method == "POST":
        nid_no = request.POST.get("nid_no")
        phone_number = request.POST.get("phone_number")
        customer = Customer.objects.filter(**{'user': user})
        customer.update(**{'nid_no': nid_no, 'phone_number': phone_number})
        user.is_staff = True
        user.save()
        return redirect('/')

    return render(request, "shop/delivery_boy_registration.html")
