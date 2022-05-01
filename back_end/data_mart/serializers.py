from rest_framework import serializers
from data_mart.models import DimSeller, DimProduct, DimCustomer, FactDeliveredOrders


class DimSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimSeller
        fields = ['seller_id', 'seller_city', 'seller_state']


class DimCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimCustomer
        fields = ['customer_id', 'customer_city', 'customer_state']


class DimProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimProduct
        fields = ['product_id', 'product_cat_name_pt', 'product_cat_name_en', 'product_weight_g', 'product_length_cm',
                  'product_height_cm', 'product_width_cm']


class FactDeliveredOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactDeliveredOrders
        fields = ['unique_id', 'customer_id', 'seller_id', 'product_id', 'delivery_day_id', 'nr_of_orders',
                  'nr_of_products', 'product_sales_revenue', 'shipping_revenue', 'nr_of_review_score',
                  'sum_review_score']
