from django.db import models


# Create your models here.
class UserRegister(models.Model):
    user_name = models.CharField(max_length=100, null=True, blank=True)
    user_email = models.EmailField(max_length=100, null=True, blank=True)
    user_password = models.CharField(max_length=100, null=True, blank=True)


class Cart(models.Model):
    ct_user = models.CharField(max_length=100, null=True, blank=True)
    ct_product_name = models.CharField(max_length=100, null=True, blank=True)
    ct_quantity = models.IntegerField(null=True, blank=True)
    ct_total_price = models.IntegerField(null=True, blank=True)
    ct_image = models.ImageField(upload_to="Cart Images", null=True, blank=True)


class Order(models.Model):
    customer_name = models.CharField(max_length=100, null=True, blank=True)
    customer_state = models.CharField(max_length=100, null=True, blank=True)
    customer_address = models.CharField(max_length=100, null=True, blank=True)
    customer_city = models.CharField(max_length=100, null=True, blank=True)
    order_price = models.IntegerField(null=True, blank=True)
    customer_email = models.EmailField(max_length=100, null=True, blank=True)


class Contact(models.Model):
    fd_back_name = models.CharField(max_length=100, null=True, blank=True)
    fd_back_mobile = models.BigIntegerField(null=True, blank=True)
    fd_back_email = models.EmailField(max_length=100, null=True, blank=True)
    fd_back_subject = models.CharField(max_length=100, null=True, blank=True)
    fd_back_message = models.CharField(max_length=100, null=True, blank=True)