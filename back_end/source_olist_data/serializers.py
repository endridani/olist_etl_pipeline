from rest_framework import serializers
from source_olist_data.models import Geolocations, Products, Sellers, Customers, Orders, OrderReviews, \
    OrderItems, OrderPayments, ProductCategoryNameTranslation


class GeolocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geolocations
        fields = ['zip_code_prefix', 'latitude', 'longitude', 'city', 'state_name']


class SellersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sellers
        fields = ['seller_id', 'seller_zip_code_prefix', 'city', 'state_name']


class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ['customer_id', 'customer_unique_id', 'customer_zip_code_prefix', 'customer_city', 'customer_state']


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp', 'order_approved_at',
                  'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']


class OrderReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderReviews
        fields = ['review_id', 'order_id', 'review_score', 'review_comment_title', 'review_comment_message',
                  'review_creation_date', 'review_answer_timestamp']


class ProductsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['product_id', 'product_category_name', 'product_name_length', 'product_description_length',
                  'product_photos_qty', 'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['order_id', 'order_item_id', 'product_id', 'seller_id', 'shipping_limit_date', 'price',
                  'freight_value']


class OrderPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPayments
        fields = ['order_id', 'payment_sequential', 'payment_type', 'payment_installments', 'payment_value']


class ProductCategoryNameTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategoryNameTranslation
        fields = ['product_category_name', 'product_category_name_english']
