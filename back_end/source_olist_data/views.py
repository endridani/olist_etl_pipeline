from rest_framework import generics

from source_olist_data.models import Products, Customers, Sellers, Orders, OrderReviews, OrderItems, OrderPayments
from source_olist_data.serializers import ProductsSerializer, CustomersSerializer, SellersSerializer, \
    ProductCategoryNameTranslation, ProductCategoryNameTranslationSerializer, OrdersSerializer, \
    OrderReviewsSerializer, OrderItemsSerializer, OrderPaymentsSerializer


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


class OrdersList(generics.ListCreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer


class OrderReviewsList(generics.ListCreateAPIView):
    queryset = OrderReviews.objects.all()
    serializer_class = OrderReviewsSerializer


class OrderItemsList(generics.ListCreateAPIView):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer


class OrderPaymentsList(generics.ListCreateAPIView):
    queryset = OrderPayments.objects.all()
    serializer_class = OrderPaymentsSerializer
