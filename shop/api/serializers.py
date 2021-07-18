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


    @transaction.atomic
    def update(self, instance, validated_data, uid):
        product_instance = Product.objects.get(uid=uid)
        sku_data = validated_data.pop('sku')

    @transaction.atomic
    def partial_update(self, validated_data, uid):
        product_instance = Product.objects.partial_update(uid=uid)
        return product_instance
        # sku_data = validated_data.pop('sku')
        # cost_data = sku_data.pop('cost')
        # product_type_data = validated_data.pop('product_type')
        # product_sku_instance = ProductSKU.objects.filter(sku=sku_data['sku'])
        # if product_sku_instance.exists():
        #     product_cost_instance = ProductCost.objects.get(sku=product_sku_instance)
        #     if cost_data['cost'] != product_cost_instance.cost:
        #         product_cost_instance.partial_update(cost=cost_data['cost'])
        #     if cost_data['vat'] != product_cost_instance.vat:
        #         product_cost_instance.partial_update(vat=cost_data['vat'])
        #
        # product_instance = Product.objects.partial_update(**validated_data)


