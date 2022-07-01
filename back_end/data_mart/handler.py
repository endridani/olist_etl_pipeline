from datetime import datetime

from data_mart.api_manager import api_client
from data_mart.models import DimProduct, FactDeliveredOrders, DimCustomer, DimSeller
from data_mart.serializers import DimProductSerializer, FactDeliveredOrdersSerializer


class Handler:
    """
    A class for processing and transforming data to correlate with DWH format.
    Serializing, checking validity and updating/creating objects in DWH.
    """

    @staticmethod
    def process_customers_and_sellers(data_type=None, serializer=None, model=None, keys=None, sellers=False):
        api_data = api_client.get_data(data_type=data_type)
        record_data = [{key: data[key] for key in keys} for data in api_data]

        # Change field names for Seller model
        if sellers:
            for seller in record_data:
                seller['seller_city'] = seller.pop('city')
                seller['seller_state'] = seller.pop('state_name')

        record_data = serializer(data=record_data, many=True)
        record_data.is_valid(raise_exception=True)
        records = [model(**data) for data in record_data.validated_data]
        model.objects.bulk_create(records, batch_size=100)

    @staticmethod
    def process_products():
        keys = ['product_id', 'product_category_name', 'product_weight_g', 'product_length_cm', 'product_height_cm',
                'product_width_cm']
        api_data = api_client
        product_data = api_data.get_data(data_type='products')
        translations_data = api_data.get_data(data_type='product_translations')
        product_data = [{key: data[key] for key in keys} for data in product_data]

        # Transform fields to correlate with the DWH table
        for product in product_data:
            product['product_cat_name_pt'] = product.pop('product_category_name')

            product_translation = next((item for item in translations_data
                                        if item['product_category_name'] == product['product_cat_name_pt']), None)
            if product_translation:
                product['product_cat_name_en'] = product_translation['product_category_name_english']

        serializer = DimProductSerializer(data=product_data, many=True)
        serializer.is_valid(raise_exception=True)
        records = [DimProduct(**data) for data in serializer.validated_data]
        DimProduct.objects.bulk_create(records, batch_size=100)

    @staticmethod
    def process_delivered_orders():

        def get_number_of_orders(date, customer):
            filtered_orders = [data for data in orders
                               if data['order_delivered_customer_date'] == date
                               and data['customer_id'] == customer
                               and data['order_status'] == 'delivered']
            return len(filtered_orders)

        def get_order_item_fields(order):
            filtered_order_item = [data for data in order_items if data['order_id'] == order]
            if filtered_order_item:
                nr_of_products = len(filtered_order_item)
                product_sales_revenue = round(sum(float(item['price']) for item in filtered_order_item), 2)
                shipping_revenue = round(sum(float(item['freight_value']) for item in filtered_order_item), 2)
                order_item_fields = {key: filtered_order_item[0][key] for key in ['seller_id', 'product_id']}
                return {**order_item_fields,
                        'nr_of_products': nr_of_products,
                        'product_sales_revenue': product_sales_revenue,
                        'shipping_revenue': shipping_revenue}
            return {'seller_id': None,
                    'product_id': None,
                    'nr_of_products': None,
                    'product_sales_revenue': None,
                    'shipping_revenue': None
                    }

        def get_order_review_fields(order):
            filtered_order_item = [data for data in order_reviews if data['order_id'] == order]
            if filtered_order_item:
                nr_of_review_score = len(filtered_order_item)
                sum_review_score = sum(int(item['review_score']) for item in filtered_order_item)
                return {'nr_of_review_score': nr_of_review_score, 'sum_review_score': sum_review_score}
            return {'nr_of_review_score': None, 'sum_review_score': None}

        def get_date(order_item, default=None):
            try:
                return datetime.strptime(order_item.pop('order_delivered_customer_date'), '%Y-%m-%d %H:%M:%S').date()
            except (ValueError, TypeError):
                return default

        def get_object(model, lookup, object_id):
            try:
                return model.objects.get(**{lookup: object_id})
            except model.DoesNotExist:
                return None

        order_keys = ['order_id', 'customer_id', 'order_delivered_customer_date']

        # Get API data from needed tables
        api_data = api_client
        orders = api_data.get_data(data_type='orders')
        order_reviews = api_data.get_data(data_type='order_reviews')
        order_items = api_data.get_data(data_type='order_items')

        # Filter fields and get only delivered orders
        delivered_orders = [{key: order[key] for key in order_keys}
                            for order in orders if order['order_status'] == 'delivered']

        for order in delivered_orders:
            # Add field nr_of_orders
            delivery_day = order['order_delivered_customer_date']
            customer_id = order['customer_id']
            order['nr_of_orders'] = get_number_of_orders(delivery_day, customer_id)

            # Add fields from order items
            order.update(**get_order_item_fields(order['order_id']))

            # Add fields from order reviews
            order.update(**get_order_review_fields(order['order_id']))

            # Additional data processing
            order.pop('order_id')
            order['delivery_day_id'] = get_date(order)
            # order['customer_id'] = get_object(DimCustomer, 'customer_id', order.pop('customer_id'))

        serializer = FactDeliveredOrdersSerializer(data=delivered_orders, many=True)
        serializer.is_valid(raise_exception=True)
        records = [FactDeliveredOrders(**data) for data in serializer.validated_data]
        FactDeliveredOrders.objects.bulk_create(records, batch_size=100)
