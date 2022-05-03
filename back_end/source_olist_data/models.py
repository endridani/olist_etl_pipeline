import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_end.settings')
django.setup()
from django.db import models


class Geolocations(models.Model):
    zip_code_prefix = models.CharField(primary_key=True, max_length=5)
    latitude = models.DecimalField(max_digits=17, decimal_places=15)
    longitude = models.DecimalField(max_digits=18, decimal_places=15)
    city = models.CharField(max_length=100)
    state_name = models.CharField(max_length=100)

    COLUMN_NAMES = ['zip_code_prefix', 'latitude', 'longitude', 'city', 'state_name']

    class Meta:
        db_table = 'geolocations'


class Sellers(models.Model):
    seller_id = models.CharField(primary_key=True, max_length=32)
    seller_zip_code_prefix = models.ForeignKey('Geolocations', null=True, on_delete=models.SET_NULL)
    city = models.CharField(max_length=100)
    state_name = models.CharField(max_length=100)

    COLUMN_NAMES = ['seller_id', 'seller_zip_code_prefix', 'city', 'state_name']

    class Meta:
        db_table = 'sellers'


class Customers(models.Model):
    customer_id = models.CharField(primary_key=True, max_length=32)
    customer_unique_id = models.CharField(max_length=32)
    customer_zip_code_prefix = models.ForeignKey('Geolocations', null=True, on_delete=models.SET_NULL)
    customer_city = models.CharField(max_length=100)
    customer_state = models.CharField(max_length=100)

    COLUMN_NAMES = ['customer_id', 'customer_unique_id', 'customer_zip_code_prefix', 'customer_city', 'customer_state']

    class Meta:
        db_table = 'customers'


class Orders(models.Model):
    order_id = models.CharField(primary_key=True, max_length=32)
    customer_id = models.ForeignKey('Customers', null=True, on_delete=models.SET_NULL)
    order_status = models.CharField(max_length=30)
    order_purchase_timestamp = models.DateTimeField(blank=True, null=True)
    order_approved_at = models.DateTimeField(blank=True, null=True)
    order_delivered_carrier_date = models.DateTimeField(blank=True, null=True)
    order_delivered_customer_date = models.DateTimeField(blank=True, null=True)
    order_estimated_delivery_date = models.DateTimeField(blank=True, null=True)

    COLUMN_NAMES = ['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp', 'order_approved_at',
                    'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']

    class Meta:
        db_table = 'orders'


class OrderReviews(models.Model):
    review_id = models.CharField(primary_key=True, max_length=32)
    order_id = models.ForeignKey('Orders', null=True, on_delete=models.SET_NULL)
    review_score = models.IntegerField()
    review_comment_title = models.CharField(max_length=200, blank=True, null=True)
    review_comment_message = models.CharField(max_length=300, blank=True, null=True)
    review_creation_date = models.DateTimeField(blank=True, null=True)
    review_answer_timestamp = models.DateTimeField(blank=True, null=True)

    COLUMN_NAMES = ['review_id', 'order_id', 'review_score', 'review_comment_title', 'review_comment_message',
                    'review_creation_date', 'review_answer_timestamp']

    class Meta:
        db_table = 'order_reviews'


class Products(models.Model):
    product_id = models.CharField(primary_key=True, max_length=32)
    product_category_name = models.CharField(max_length=100, blank=True)
    product_name_length = models.DecimalField(max_digits=12, decimal_places=6)
    product_description_length = models.DecimalField(max_digits=12, decimal_places=6, blank=True)
    product_photos_qty = models.DecimalField(max_digits=12, decimal_places=6)
    product_weight_g = models.DecimalField(max_digits=12, decimal_places=6)
    product_length_cm = models.DecimalField(max_digits=12, decimal_places=6)
    product_height_cm = models.DecimalField(max_digits=12, decimal_places=6)
    product_width_cm = models.DecimalField(max_digits=12, decimal_places=6)

    COLUMN_NAMES = ['product_id', 'product_category_name', 'product_name_length', 'product_description_length',
                    'product_photos_qty', 'product_weight_g', 'product_length_cm', 'product_height_cm',
                    'product_width_cm']

    class Meta:
        db_table = 'products'


class OrderItems(models.Model):
    order_id = models.ForeignKey('Orders', null=True, on_delete=models.SET_NULL)
    order_item_id = models.CharField(max_length=32)
    product_id = models.ForeignKey('Products', null=True, on_delete=models.SET_NULL)
    seller_id = models.ForeignKey('Sellers', null=True, on_delete=models.SET_NULL)
    shipping_limit_date = models.DateTimeField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    freight_value = models.DecimalField(max_digits=6, decimal_places=2)

    COLUMN_NAMES = ['order_id', 'order_item_id', 'product_id', 'seller_id', 'shipping_limit_date', 'price',
                    'freight_value']

    class Meta:
        db_table = 'order_items'


class OrderPayments(models.Model):
    order_id = models.ForeignKey('Orders', null=True, on_delete=models.SET_NULL)
    payment_sequential = models.IntegerField()
    payment_type = models.CharField(max_length=100)
    payment_installments = models.IntegerField()
    payment_value = models.DecimalField(max_digits=8, decimal_places=2)

    COLUMN_NAMES = ['order_id', 'payment_sequential', 'payment_type', 'payment_installments', 'payment_value']

    class Meta:
        db_table = 'order_payments'


class ProductCategoryNameTranslation(models.Model):
    product_category_name = models.CharField(max_length=200, blank=True)
    product_category_name_english = models.CharField(max_length=200, blank=True)

    COLUMN_NAMES = ['product_category_name', 'product_category_name_english']
