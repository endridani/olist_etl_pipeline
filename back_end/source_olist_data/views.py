from rest_framework import mixins
from rest_framework import generics

from source_olist_data.models import Products, Customers, Sellers
from source_olist_data.serializers import ProductsSerializer, CustomersSerializer, SellersSerializer


class ProductsList(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer


class CustomersList(generics.ListCreateAPIView):
    queryset = Customers.objects.all()
    serializer_class = CustomersSerializer


class SellersList(generics.ListCreateAPIView):
    queryset = Sellers.objects.all()
    serializer_class = SellersSerializer
