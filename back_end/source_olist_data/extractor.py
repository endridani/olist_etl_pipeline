import django
import pandas as pd
import json
import decimal
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_end.settings')
django.setup()
from source_olist_data.models import Geolocations, Sellers, Customers, Orders, OrderReviews, Products, OrderItems, \
    OrderPayments, ProductCategoryNameTranslation
from source_olist_data.serializers import GeolocationsSerializer, SellersSerializer, CustomersSerializer, \
    OrdersSerializer, OrderReviewsSerializer, ProductsSerializer, OrderItemsSerializer, OrderPaymentsSerializer, \
    ProductCategoryNameTranslationSerializer


class Extractor:

    @staticmethod
    def synchronize_sources():
        def extract_geolocations():
            df_geolocation = pd.read_csv('source_olist_data/olist_csv_files/olist_geolocation_dataset.txt',
                                         names=Geolocations.COLUMN_NAMES,
                                         header=0,
                                         dtype={'city': 'string',
                                                'state_name': 'string'},
                                         converters={'zip_code_prefix': lambda x: str(x),
                                                     'latitude': decimal.Decimal,
                                                     'longitude': decimal.Decimal})
            df_geolocation.drop_duplicates(subset=['zip_code_prefix'], keep='first', inplace=True)
            df_geolocation = df_geolocation.where(pd.notnull(df_geolocation), None)
            df_geolocation = df_geolocation.to_json(orient='records')
            df_geolocation = json.loads(df_geolocation)
            serializer = GeolocationsSerializer(data=df_geolocation, many=True)
            serializer.is_valid(raise_exception=True)
            print(len([data for data in serializer.validated_data]), 'Geolocation records to be inserted...')
            print('Inserting records...')
            records = [Geolocations(**data) for data in serializer.validated_data]
            Geolocations.objects.bulk_create(records)
            print(len(Geolocations.objects.all()), 'Geolocation records inserted!')

        def extract_sellers():
            df_sellers = pd.read_csv('source_olist_data/olist_csv_files/olist_sellers_dataset.txt',
                                     names=Sellers.COLUMN_NAMES,
                                     header=0,
                                     dtype={'city': 'string',
                                            'state_name': 'string'},
                                     converters={'seller_id': lambda x: str(x),
                                                 'seller_zip_code_prefix': lambda x: str(x)})
            df_sellers.drop_duplicates(subset=['seller_id'], keep='first', inplace=True)
            df_sellers = df_sellers.where(pd.notnull(df_sellers), None)
            df_sellers = df_sellers[df_sellers["seller_zip_code_prefix"].isin(
                [geolocation.zip_code_prefix for geolocation in Geolocations.objects.all()]) == True]
            df_sellers = df_sellers.to_json(orient='records')
            df_sellers = json.loads(df_sellers)
            serializer = SellersSerializer(data=df_sellers, many=True)
            serializer.is_valid(raise_exception=True)
            print(len([data for data in serializer.validated_data]), 'Seller records to be inserted...')
            print('Inserting records...')
            records = [Sellers(**data) for data in serializer.validated_data]
            Sellers.objects.bulk_create(records)
            print(len(Sellers.objects.all()), 'Seller records inserted!')

        def extract_customers():
            df_customers = pd.read_csv('source_olist_data/olist_csv_files/olist_customers_dataset.txt',
                                       names=Customers.COLUMN_NAMES,
                                       header=0,
                                       dtype={'customer_city': 'string',
                                              'customer_state': 'string'},
                                       converters={'customer_id': lambda x: str(x),
                                                   'customer_unique_id': lambda x: str(x),
                                                   'customer_zip_code_prefix': lambda x: str(x)})
            df_customers.drop_duplicates(subset=['customer_id'], keep='first', inplace=True)
            df_customers = df_customers.where(pd.notnull(df_customers), None)
            df_customers = df_customers[df_customers["customer_zip_code_prefix"].isin(
                [geolocation.zip_code_prefix for geolocation in Geolocations.objects.all()]) == True]
            df_customers = df_customers.to_json(orient='records')
            df_customers = json.loads(df_customers)
            serializer = CustomersSerializer(data=df_customers, many=True)
            serializer.is_valid(raise_exception=True)
            print(len([data for data in serializer.validated_data]), 'Customer records to be inserted...')
            print('Inserting records...')
            records = [Customers(**data) for data in serializer.validated_data]
            Customers.objects.bulk_create(records)
            print(len(Customers.objects.all()), 'Customer records inserted!')

        def extract_orders():
            df_orders = pd.read_csv('source_olist_data/olist_csv_files/olist_orders_dataset.txt',
                                    names=Orders.COLUMN_NAMES,
                                    header=0,
                                    dtype={'order_status': 'string'},
                                    converters={'order_id': lambda x: str(x),
                                                'customer_id': lambda x: str(x)},
                                    parse_dates=['order_purchase_timestamp',
                                                 'order_approved_at',
                                                 'order_delivered_carrier_date',
                                                 'order_delivered_customer_date',
                                                 'order_estimated_delivery_date'],
                                    date_parser=lambda col: pd.to_datetime(col, format='%Y-%m-%d %H:%M:%S'))
            df_orders.drop_duplicates(subset=['order_id'], keep='first', inplace=True)
            df_orders = df_orders.where(pd.notnull(df_orders), None)
            df_orders = df_orders[df_orders["customer_id"].isin(
                [customer.customer_id for customer in Customers.objects.all()]) == True]
            df_orders = df_orders.to_json(orient='records')
            df_orders = json.loads(df_orders)
            serializer = OrdersSerializer(data=df_orders, many=True)
            serializer.is_valid(raise_exception=True)
            print(len([data for data in serializer.validated_data]), 'Order records to be inserted...')
            print('Inserting records...')
            records = [Orders(**data) for data in serializer.validated_data]
            Orders.objects.bulk_create(records)
            print(len(Orders.objects.all()), 'Order records inserted!')

        def extract_order_reviews():
            df_order_reviews = pd.read_csv('source_olist_data/olist_csv_files/olist_order_reviews_dataset.txt',
                                           names=OrderReviews.COLUMN_NAMES,
                                           header=0,
                                           dtype={'review_score': 'int32',
                                                  'review_comment_title': 'string',
                                                  'review_comment_message': 'string'},
                                           converters={'review_id': lambda x: str(x),
                                                       'order_id': lambda x: str(x)},
                                           parse_dates=['review_creation_date',
                                                        'review_answer_timestamp'],
                                           date_parser=lambda col: pd.to_datetime(col, format='%Y-%m-%d %H:%M:%S'),
                                           na_filter=False)
            df_order_reviews.drop_duplicates(subset=['review_id'], keep='first', inplace=True)
            df_order_reviews = df_order_reviews.where(pd.notnull(df_order_reviews), None)
            df_order_reviews = df_order_reviews[df_order_reviews["order_id"].isin(
                [order.order_id for order in Orders.objects.all()]) == True]
            df_order_reviews = df_order_reviews.to_json(orient='records')
            df_order_reviews = json.loads(df_order_reviews)
            serializer = OrderReviewsSerializer(data=df_order_reviews, many=True)
            serializer.is_valid(raise_exception=True)
            print(len([data for data in serializer.validated_data]), 'Order review records to be inserted...')
            print('Inserting records...')
            records = [OrderReviews(**data) for data in serializer.validated_data]
            OrderReviews.objects.bulk_create(records)
            print(len(OrderReviews.objects.all()), 'Order review records inserted!')

        def extract_products():
            df_products = pd.read_csv('source_olist_data/olist_csv_files/olist_products_dataset.txt',
                                      names=Products.COLUMN_NAMES,
                                      header=0,
                                      dtype={'product_category_name': 'string'},
                                      converters={'product_id': lambda x: str(x),
                                                  'product_name_length': decimal.Decimal,
                                                  'product_description_length': decimal.Decimal,
                                                  'product_photos_qty': decimal.Decimal,
                                                  'product_weight_g': decimal.Decimal,
                                                  'product_length_cm': decimal.Decimal,
                                                  'product_height_cm': decimal.Decimal,
                                                  'product_width_cm': decimal.Decimal})
            df_products.drop_duplicates(subset=['product_id'], keep='first', inplace=True)
            df_products = df_products.where(pd.notnull(df_products), None)
            # df_products.replace({np.inf: np.nan, -np.inf: np.nan}, inplace=True)
            # df_products = df_products.fillna(0)
            df_products = df_products.to_json(orient='records')
            df_products = json.loads(df_products)
            serializer = ProductsSerializer(data=df_products, many=True)
            serializer.is_valid(raise_exception=True)
            print(len([data for data in serializer.validated_data]), 'Product records to be inserted...')
            print('Inserting records...')
            records = [Products(**data) for data in serializer.validated_data]
            Products.objects.bulk_create(records)
            print(len(Products.objects.all()), 'Product records inserted!')

        def extract_order_items():
            df_order_items = pd.read_csv('source_olist_data/olist_csv_files/olist_order_items_dataset.txt',
                                         names=OrderItems.COLUMN_NAMES,
                                         header=0,
                                         dtype={'order_item_id': 'string'},
                                         converters={'order_id': lambda x: str(x),
                                                     'product_id': lambda x: str(x),
                                                     'seller_id': lambda x: str(x),
                                                     'price': decimal.Decimal,
                                                     'freight_value': decimal.Decimal},
                                         parse_dates=['shipping_limit_date'],
                                         date_parser=lambda col: pd.to_datetime(col, format='%Y-%m-%d %H:%M:%S'))
            df_order_items = df_order_items[df_order_items["order_id"].isin(
                [order.order_id for order in Orders.objects.all()]) == True]
            df_order_items = df_order_items[df_order_items["product_id"].isin(
                [product.product_id for product in Products.objects.all()]) == True]
            df_order_items = df_order_items[df_order_items["seller_id"].isin(
                [seller.seller_id for seller in Sellers.objects.all()]) == True]
            # df_order_items.replace({np.inf: np.nan, -np.inf: np.nan}, inplace=True)

            df_order_items = df_order_items.to_json(orient='records')
            df_order_items = json.loads(df_order_items)
            serializer = OrderItemsSerializer(data=df_order_items, many=True)
            serializer.is_valid(raise_exception=True)
            print(len([data for data in serializer.validated_data]), 'Order item records to be inserted...')
            print('Inserting records...')
            records = [OrderItems(**data) for data in serializer.validated_data]
            OrderItems.objects.bulk_create(records)
            print(len(OrderItems.objects.all()), 'Order item records inserted!')

        def extract_order_payments():
            df_order_payments = pd.read_csv('source_olist_data/olist_csv_files/olist_order_payments_dataset.txt',
                                            names=OrderPayments.COLUMN_NAMES,
                                            header=0,
                                            dtype={'payment_sequential': 'int32',
                                                   'payment_type': 'string',
                                                   'payment_installments': 'int32'},
                                            converters={'order_id': lambda x: str(x),
                                                        'payment_value': decimal.Decimal})
            df_order_payments = df_order_payments[df_order_payments["order_id"].isin(
                [order.order_id for order in Orders.objects.all()]) == True]
            # df_order_payments.replace({np.inf: np.nan, -np.inf: np.nan}, inplace=True)
            df_order_payments = df_order_payments.to_json(orient='records')
            df_order_payments = json.loads(df_order_payments)
            serializer = OrderPaymentsSerializer(data=df_order_payments, many=True)
            serializer.is_valid(raise_exception=True)
            print(len([data for data in serializer.validated_data]), 'Order payment records to be inserted...')
            print('Inserting records...')
            records = [OrderPayments(**data) for data in serializer.validated_data]
            OrderPayments.objects.bulk_create(records)
            print(len(OrderPayments.objects.all()), 'Order payment records inserted!')

        def extract_product_category_name_translation():
            df_category_names = pd.read_csv('source_olist_data/olist_csv_files/product_category_name_translation.txt',
                                            names=ProductCategoryNameTranslation.COLUMN_NAMES,
                                            header=0,
                                            dtype={'product_category_name': 'string',
                                                   'product_category_name_english': 'string'})
            df_category_names = df_category_names.to_json(orient='records')
            df_category_names = json.loads(df_category_names)
            serializer = ProductCategoryNameTranslationSerializer(data=df_category_names, many=True)
            serializer.is_valid(raise_exception=True)
            print(len([data for data in serializer.validated_data]), 'Category name records to be inserted...')
            print('Inserting records...')
            records = [ProductCategoryNameTranslation(**data) for data in serializer.validated_data]
            ProductCategoryNameTranslation.objects.bulk_create(records)
            print(len(ProductCategoryNameTranslation.objects.all()), 'Category name records inserted!')

        # extract_geolocations()
        # extract_sellers()
        # extract_customers()
        extract_orders()
        extract_order_reviews()
        extract_products()
        extract_order_items()
        extract_order_payments()
        extract_product_category_name_translation()
