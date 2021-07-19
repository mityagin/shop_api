from copy import deepcopy

from rest_framework.response import Response

from api.models import ProductType
from api.serializers import ProductSerializer


class UpdateProductManager:

    @staticmethod
    def make_bd_objects(request, product):
        if 'sku' in request.data:
            if product.sku != request.data['sku']:
                return Response(status=400, data=f'object with sku: {request.data["sku"]} — already exists')
            elif product.sku == request.data['sku']:
                request.data.pop('sku')
        is_type_uid = request.data.get('type')
        types = []
        existing_types = []
        request_data = deepcopy(request.data)
        if is_type_uid is not None:
            for ind, product_type in enumerate(request_data['type']):
                product_type_queryset = ProductType.objects.filter(type_uid=product_type['type_uid'])
                if product_type_queryset.exists():
                    existing_types.append(product_type)
                else:
                    types.append(product_type)
            request.data.pop('type')
            if types and not existing_types:
                serializer = ProductSerializer(data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    product = serializer.update(instance=product, validated_data=request.data)
                    for product_type in types:
                        product_type_instance = ProductType.objects.create(**product_type)
                        product.type.add(product_type_instance)
                    return Response(status=201, data=ProductSerializer(product).data)
            if types and existing_types:
                serializer = ProductSerializer(data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    product = serializer.update(instance=product, validated_data=request.data)
                    for existing_type in existing_types:
                        product_type_instance = ProductType.objects.get(**existing_type)
                        product.type.add(product_type_instance)
                    for product_type in types:
                        product_type_instance = ProductType.objects.create(**product_type)
                        product.type.add(product_type_instance)
                    return Response(status=201, data=ProductSerializer(product).data)
            if not types and existing_types:
                serializer = ProductSerializer(data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    product = serializer.update(instance=product, validated_data=request.data)
                    for existing_type in existing_types:
                        product_type_instance = ProductType.objects.get(**existing_type)
                        product.type.add(product_type_instance)
                    return Response(status=201, data=ProductSerializer(product).data)
        else:
            serializer = ProductSerializer(data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                product = serializer.update(instance=product, validated_data=request.data)
                return Response(status=200, data=ProductSerializer(product).data)
