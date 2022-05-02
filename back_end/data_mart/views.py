from rest_framework.response import Response
from rest_framework import mixins, viewsets
from rest_framework.decorators import action

from data_mart.handler import Handler
from data_mart.models import DimCustomer, DimSeller, DimProduct, FactDeliveredOrders
from data_mart.serializers import DimCustomerSerializer, DimSellerSerializer, DimProductSerializer, \
    FactDeliveredOrdersSerializer


class CustomersViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """A ViewSet for viewing and updating Customers information"""

    queryset = DimCustomer.objects.all()
    serializer_class = DimCustomerSerializer

    @action(detail=False, methods=['post'])
    def add_customers(self, request):
        columns = DimCustomer.COLUMN_NAMES
        Handler.process_customers_and_sellers(data_type='customers', serializer=DimCustomerSerializer,
                                              model=DimCustomer, keys=columns)
        return Response({"success": True})


class SellersViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """A ViewSet for viewing and updating Sellers information"""

    queryset = DimSeller.objects.all()
    serializer_class = DimSellerSerializer

    @action(detail=False, methods=['post'])
    def add_sellers(self, request):
        columns = ['seller_id', 'city', 'state_name']
        Handler.process_customers_and_sellers(data_type='sellers', serializer=DimSellerSerializer,
                                              model=DimSeller, keys=columns, sellers=True)
        return Response({"success": True})


class ProductsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """A ViewSet for viewing and updating Products information"""

    queryset = DimProduct.objects.all()
    serializer_class = DimProductSerializer

    @action(detail=False, methods=['post'])
    def add_products(self, request):
        Handler.process_products()
        return Response({'success': True})


class DeliveredOrdersViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """A ViewSet for viewing and updating Delivered Orders information"""

    queryset = FactDeliveredOrders.objects.all()
    serializer_class = FactDeliveredOrdersSerializer
