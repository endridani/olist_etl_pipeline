import django
import pandas as pd
import json
import decimal
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_end.settings')
django.setup()
from source_olist_data.models import Geolocations
from source_olist_data.serializers import GeolocationsSerializer


class Extractor:

    @staticmethod
    def synchronize_sources():
        column_names = ['zip_code_prefix', 'latitude', 'longitude', 'city', 'state_name']
        df_geolocation = pd.read_csv('back_end/source_olist_data/olist_csv_files/olist_geolocation_dataset.txt',
                                     dtype={'geolocation_zip_code_prefix': str,
                                            'geolocation_city': 'string',
                                            'geolocation_state': 'string'},
                                     converters={'geolocation_lat': decimal.Decimal,
                                                 'geolocation_lng': decimal.Decimal},
                                     names=column_names,  # Rename columns
                                     header=0)

        df_geolocation.drop_duplicates(subset=['zip_code_prefix'], keep='first', inplace=True)
        df_geolocation = df_geolocation.to_json(orient='records')
        location = json.loads(df_geolocation)[0]
        serializer = GeolocationsSerializer(data=location)
        serializer.is_valid(raise_exception=True)
        geolocation = Geolocations(**serializer.validated_data)
        geolocation.save()
        print(geolocation)



