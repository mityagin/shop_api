from copy import deepcopy

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer
from .models import Product, ProductType
from .managers import UpdateProductManager


class CreateProductView(APIView):

    def post(self, request):
        sku_queryset = Product.objects.filter(sku=request.data['sku'])
        if sku_queryset.exists():
            return Response(status=400, data=f'object with sku: {request.data["sku"]} — already exists')
        product = ''
        is_type_uid = request.data.get('type')
        types = []
        existing_types = []
        request_data = deepcopy(request.data)
        if is_type_uid is not None:
            for ind, product_type in enumerate(request_data['type']):
                product_type_queryset = ProductType.objects.filter(type_uid=product_type['type_uid'])
                if product_type_queryset.exists():
                    existing_types.append(request.data['type'].pop(ind))
                else:
                    types.append(product_type)
            if types and not existing_types:
                serializer = ProductSerializer(data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    product = serializer.create(serializer.data)
                    return Response(status=201, data=product.uid)
            if types and existing_types:
                serializer = ProductSerializer(data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    product = serializer.create(serializer.data)
                for existing_type in existing_types:
                    product_type_instance = ProductType.objects.get(**existing_type)
                    product.save()
                    product.type.add(product_type_instance)
                return Response(status=201, data=product.uid)
            if not types and existing_types:
                request.data.pop('type')
                for existing_type in existing_types:
                    product_type_instance = ProductType.objects.get(**existing_type)
                    product = Product(**request.data)
                    product.save()
                    product.type.add(product_type_instance)
                return Response(status=201, data=product.uid)
        return Response(status=400)


class DeleteUIDProductView(APIView):

    def delete(self, request, uid):
        try:
            product = get_object_or_404(Product, uid=uid)
            product.delete()
        except ValidationError as err:
            return Response(status=400, data=err)
        return Response(status=200, data=f'{uid} deleted')


class DeleteSKUProductView(APIView):

    def delete(self, request, sku):
        try:
            product = get_object_or_404(Product, sku=sku)
            product.delete()
        except ValidationError as err:
            return Response(status=400, data=err)
        return Response(status=200, data=f'{sku} deleted')


class UpdateUIDProductView(APIView):

    def patch(self, request, uid):
        try:
            product = get_object_or_404(Product, uid=uid)
            response = UpdateProductManager.make_bd_objects(request, product)
            if response:
                return response
        except ValidationError as err:
            return Response(status=400, data=err)
        return Response(status=400)


class UpdateSKUProductView(APIView):

    def patch(self, request, sku):

        product = get_object_or_404(Product, sku=sku)
        if 'uid' in request.data:
            request.data.pop('uid')
        response = UpdateProductManager.make_bd_objects(request, product)
        if response:
            return response
        return Response(status=400)


class ProductView(APIView):

    def get(self, request):
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(status=200, data=serializer.data)


class ProductPartialView(APIView):

    def get(self, request, begin, end):
        product = Product.objects.all()[begin-1 if begin != 0 else 0:end]
        serializer = ProductSerializer(product, many=True)
        return Response(status=200, data=serializer.data)


class ProductSingleUIDView(APIView):

    def get(self, request, uid):
        try:
            product = get_object_or_404(Product, uid=uid)
        except ValidationError as err:
            return Response(status=400, data=err)
        serializer = ProductSerializer(product, many=False)
        return Response(status=200, data=serializer.data)


class ProductSingleSKUView(APIView):

    def get(self, request, sku):
        try:
            product = get_object_or_404(Product, sku=sku)
        except ValidationError as err:
            return Response(status=400, data=err)
        serializer = ProductSerializer(product, many=False)
        return Response(status=200, data=serializer.data)



