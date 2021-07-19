from django.db import transaction
from rest_framework import serializers
from .models import Product, ProductType


class ProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductType
        exclude = ('id', 'created_at', 'updated_at',)


class ProductSerializer(serializers.ModelSerializer):

    type = ProductTypeSerializer(many=True)

    class Meta:
        model = Product
        exclude = ('id', 'created_at', 'updated_at',)

    @transaction.atomic
    def create(self, validated_data):
        product_instance = ''
        product_type_data = validated_data.pop('type')
        for entity in product_type_data:
            product_type_instance = ProductType.objects.create(**entity)
            product_instance = Product(**validated_data)
            product_instance.save()
            product_instance.type.add(product_type_instance)
        return product_instance
