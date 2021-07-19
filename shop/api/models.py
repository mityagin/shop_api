import uuid
from django.db import models


class Product(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    sku = models.CharField(max_length=50, blank=False, null=False, unique=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    type = models.ManyToManyField('ProductType', related_name='product')
    cost = models.DecimalField(max_digits=10, blank=True, null=True, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductType(models.Model):
    type_uid = models.IntegerField(blank=False, null=False, unique=True)
    type_name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

