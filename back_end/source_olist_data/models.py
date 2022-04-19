import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_end.settings')
django.setup()
from django.db import models

ddl = ['geolocation_ddl',
       'sellers_ddl',
       'customers_ddl',
       'orders_ddl',
       'order_reviews_ddl',
       'products_ddl',
       'order_items_ddl',
       'order_payments_ddl',
       'prod_cat_name_ddl']


class Geolocations(models.Model):
    zip_code_prefix = models.CharField(primary_key=True, max_length=5)
    latitude = models.DecimalField(max_digits=17, decimal_places=15)
    longitude = models.DecimalField(max_digits=18, decimal_places=15)
    city = models.CharField(max_length=100)
    state_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'geolocations'

    @classmethod
    def create(cls, kwargs):
        geolocation = cls.create(**kwargs)
        # do something with the geolocation
        return geolocation


class Sellers(models.Model):
    seller_id = models.CharField(primary_key=True, max_length=32)
    seller_zip_code_prefix = models.ForeignKey('Geolocations', null=True, on_delete=models.SET_NULL)
    city = models.CharField(max_length=100)
    state_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'sellers'


class Customers(models.Model):
    customer_id = models.CharField(primary_key=True, max_length=32)
    customer_unique_id = models.CharField(max_length=32)
    customer_zip_code_prefix = models.ForeignKey('Geolocations', null=True, on_delete=models.SET_NULL)
    customer_city = models.CharField(max_length=100)
    customer_state = models.CharField(max_length=100)

    class Meta:
        db_table = 'customers'


class Orders(models.Model):
    order_id = models.CharField(primary_key=True, max_length=32)
    customer_id = models.ForeignKey('Customers', null=True, on_delete=models.SET_NULL)
    order_status = models.CharField(max_length=30)
    order_purchase_timestamp = models.DateTimeField()
    order_approved_at = models.DateTimeField()
    order_delivered_carrier_date = models.DateTimeField()
    order_delivered_customer_date = models.DateTimeField()
    order_estimated_delivery_date = models.DateTimeField()

    class Meta:
        db_table = 'orders'


class OrderReviews(models.Model):
    review_id = models.CharField(primary_key=True, max_length=32)
    order_id = models.ForeignKey('Orders', null=True, on_delete=models.SET_NULL)
    review_score = models.IntegerField()
    review_comment_title = models.CharField(max_length=200)
    review_comment_message = models.CharField(max_length=300)
    review_creation_date = models.DateTimeField()
    review_answer_timestamp = models.DateTimeField()

    class Meta:
        db_table = 'order_reviews'


class Products(models.Model):
    product_id = models.CharField(primary_key=True, max_length=32)
    product_category_name = models.CharField(max_length=100)
    product_name_length = models.DecimalField(max_digits=12, decimal_places=6)
    product_description_length = models.DecimalField(max_digits=12, decimal_places=6)
    product_photos_qty = models.DecimalField(max_digits=12, decimal_places=6)
    product_weight_g = models.DecimalField(max_digits=12, decimal_places=6)
    product_length_cm = models.DecimalField(max_digits=12, decimal_places=6)
    product_height_cm = models.DecimalField(max_digits=12, decimal_places=6)
    product_width_cm = models.DecimalField(max_digits=12, decimal_places=6)

    class Meta:
        db_table = 'products'


class OrderItems(models.Model):
    order_id = models.ForeignKey('Orders', null=True, on_delete=models.SET_NULL)
    order_item_id = models.CharField(max_length=32)
    product_id = models.ForeignKey('Products', null=True, on_delete=models.SET_NULL)
    seller_id = models.ForeignKey('Sellers', null=True, on_delete=models.SET_NULL)
    shipping_limit_date = models.DateTimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    freight_value = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        db_table = 'order_items'


class OrderPayments(models.Model):
    order_id = models.ForeignKey('Orders', null=True, on_delete=models.SET_NULL)
    payment_sequential = models.IntegerField()
    payment_type = models.CharField(max_length=100)
    payment_installments = models.IntegerField()
    payment_value = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        db_table = 'order_payments'


class ProductCategoryNameTranslation(models.Model):
    product_category_name = models.CharField(max_length=200)
    product_category_name_english = models.CharField(max_length=200)

    class Meta:
        db_table = 'product_category_name_translation'
