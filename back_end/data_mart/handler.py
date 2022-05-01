from data_mart.api_manager import api_client


class Handler:

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
