from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=100, null=True, blank=True)
    category_description = models.CharField(max_length=100, null=True, blank=True)
    category_image = models.ImageField(upload_to="Category Image", null=True, blank=True)


class Product(models.Model):
    pd_category = models.CharField(max_length=100, null=True, blank=True)
    product_name = models.CharField(max_length=100, null=True, blank=True)
    product_price = models.IntegerField(null=True, blank=True)
    product_description = models.CharField(max_length=100, null=True, blank=True)
    product_image = models.ImageField(upload_to="Product Images", null=True,blank=True)
