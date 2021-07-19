from django.urls import path
from api.views import CreateProductView, ProductView, ProductPartialView, UpdateUIDProductView, UpdateSKUProductView, DeleteUIDProductView, DeleteSKUProductView, ProductSingleUIDView, ProductSingleSKUView

urlpatterns = [
    path('products/', ProductView.as_view(), name='get'),
    path('products/<int:begin>-<int:end>', ProductPartialView.as_view(), name='get'),
    path('product/delete/uid/<uid>', DeleteUIDProductView.as_view(), name='delete'),
    path('product/delete/sku/<sku>', DeleteSKUProductView.as_view(), name='delete'),
    path('product/', CreateProductView.as_view(), name='post'),
    path('product/update/uid/<uid>', UpdateUIDProductView.as_view(), name='patch'),
    path('product/update/sku/<sku>', UpdateSKUProductView.as_view(), name='patch'),
    path('product/uid/<uid>', ProductSingleUIDView.as_view(), name='get'),
    path('product/sku/<sku>', ProductSingleSKUView.as_view(), name='get'),
]