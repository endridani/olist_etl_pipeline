from rest_framework import generics

from source_olist_data.models import Products, Customers, Sellers
from source_olist_data.serializers import ProductsSerializer, CustomersSerializer, SellersSerializer, \
    ProductCategoryNameTranslation, ProductCategoryNameTranslationSerializer


class CustomersList(generics.ListCreateAPIView):
    queryset = Customers.objects.all()
    serializer_class = CustomersSerializer


class SellersList(generics.ListCreateAPIView):
    queryset = Sellers.objects.all()
    serializer_class = SellersSerializer


class ProductsList(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer


class ProductCategoryNameTranslationList(generics.ListCreateAPIView):
    queryset = ProductCategoryNameTranslation.objects.all()
    serializer_class = ProductCategoryNameTranslationSerializer
