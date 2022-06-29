import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_end.settings')
django.setup()

from django.db import models


class DimCustomer(models.Model):
    customer_id = models.CharField(primary_key=True, max_length=32)
    customer_city = models.CharField(max_length=100, null=True)
    customer_state = models.CharField(max_length=100, null=True)

    COLUMN_NAMES = ['customer_id', 'customer_city', 'customer_state']

    class Meta:
        db_table = 'DIM_CUSTOMER'


class DimSeller(models.Model):
    seller_id = models.CharField(primary_key=True, max_length=32)
    seller_city = models.CharField(max_length=100, null=True)
    seller_state = models.CharField(max_length=100, null=True)

    COLUMN_NAMES = ['seller_id', 'seller_city', 'seller_state']

    class Meta:
        db_table = 'DIM_SELLER'


class DimProduct(models.Model):
    product_id = models.CharField(primary_key=True, max_length=32)
    product_cat_name_pt = models.CharField(max_length=100, null=True, blank=True)
    product_cat_name_en = models.CharField(max_length=100, null=True, blank=True)
    product_weight_g = models.DecimalField(max_digits=12, decimal_places=6, null=True)
    product_length_cm = models.DecimalField(max_digits=12, decimal_places=6, null=True)
    product_height_cm = models.DecimalField(max_digits=12, decimal_places=6, null=True)
    product_width_cm = models.DecimalField(max_digits=12, decimal_places=6, null=True)

    COLUMN_NAMES = ['product_id', 'product_cat_name_pt', 'product_cat_name_en', 'product_weight_g', 'product_length_cm',
                    'product_height_cm', 'product_width_cm']

    class Meta:
        db_table = 'DIM_PRODUCT'


class FactDeliveredOrders(models.Model):
    unique_id = models.BigAutoField(primary_key=True)
    customer_id = models.ForeignKey('DimCustomer', null=True, on_delete=models.SET_NULL)
    seller_id = models.ForeignKey('DimSeller', null=True, on_delete=models.SET_NULL)
    product_id = models.ForeignKey('DimProduct', null=True, on_delete=models.SET_NULL)
    delivery_day_id = models.DateField(null=True)
    nr_of_orders = models.IntegerField(null=True)
    nr_of_products = models.IntegerField(null=True)
    product_sales_revenue = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    shipping_revenue = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    nr_of_review_score = models.IntegerField(null=True)
    sum_review_score = models.IntegerField(null=True)

    class Meta:
        db_table = 'FACT_DELIVERED_ORDERS'
