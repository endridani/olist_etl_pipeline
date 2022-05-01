import requests


class ApiClient:
    """Stores communication data for source tables"""

    def __init__(self):
        self.url = "http://127.0.0.1:8000"

    def get_data(self, data_id=None, data_type=None):
        if data_id:
            api_url = f"{self.url}/{data_type}/{data_id}"
        else:
            api_url = f"{self.url}/{data_type}/"

        req = requests.get(api_url)
        return req.json()


api_client = ApiClient()
