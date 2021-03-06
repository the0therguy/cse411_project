from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Customer(models.Model):
    CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True)
    sex = models.CharField(max_length=20, choices=CHOICES)
    nid_no = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=14, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/product/{self.id}/"

    def get_add_to_cart_url(self):
        return f"add-to-cart/{self.id}/"

    def get_remove_from_cart_url(self):
        return f"remove-from-cart/{self.id}/"

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class OrderItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1, null=True, blank=True)

    def get_total(self):
        self.total = self.product.price * self.quantity
        return self.total

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=12)
    street = models.CharField(max_length=100)
    apartment = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    district = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.customer.name


class PaymentTable(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    payment_option = models.CharField(max_length=10)
    transaction_id = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    date_ordered = models.DateField()
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    payment = models.ForeignKey(PaymentTable, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_boy = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name="delivery_boy")
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def get_order_total(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_total()
        return total
