from data_mart.api_manager import api_client
from data_mart.models import DimProduct
from data_mart.serializers import DimProductSerializer


class Handler:
    """
    A class for processing and transforming data to correlate with DWH format.
    Serializing, checking validity and updating/creating objects.
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
        pass
