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

        def extract_geolocation():
            """
            TODO: Add abstract class with custom manager for bulk_create method
            """
            df_geolocation = pd.read_csv('back_end/source_olist_data/olist_csv_files/olist_geolocation_dataset.txt',
                                         names=Geolocations.column_names,
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
            geolocation = Geolocations.object.bulk_create([Geolocations(**data) for data in serializer.validated_data])
            geolocation.save()

        extract_geolocation()
