import requests
import json
import urllib

from .define import API_KEY, API_URL, SERVER_URL
from .settings import Settings

class ApiManager:

    @classmethod
    def object_request(cls, endpoint, ids):
        objects = []
        if (len(ids) > 0):
            for id in ids:
                objects.append({"id": id})
        else:
            return []

        url = API_URL + endpoint
        payload = {
            "arg": json.dumps(objects),
            "flavour": "mobile",
            "auth_token": Settings.get().get_auth_token(),
            "apikey": API_KEY
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            json_response = response.json()
            return json_response['result']
        elif response.status_code == 404:
            print('Not Found.')

    @classmethod
    def spot_search(cls, **kwargs):
        url = API_URL + 'search/spot'
        name = kwargs.get('name')
        if name:
            if len(name) < 3:
                return None
            payload = {
                "q": kwargs['name'],
                "auth_token": Settings.get().get_auth_token(),
                "apikey": API_KEY,
                "flavour": "mobile"
            }
        elif kwargs.get('lat'):
            payload = {
                "lat": kwargs['lat'],
                "lng": kwargs['lng'],
                "auth_token": Settings.get().get_auth_token(),
                "apikey": API_KEY,
                "flavour": "mobile"
            }

        response = requests.post(url, data=payload)
        if response.status_code == 200:
            json_response = response.json()
            return json_response['data']
        elif response.status_code == 404:
            print('Not Found.')

    @classmethod
    def download_mobile_spots_file(cls):
        url = SERVER_URL + 'assets/mobilespots.db.gz'
        payload = {
            "auth_token": Settings.get().get_auth_token(),
            "apikey": API_KEY
        }
        response = requests.get(url, data=payload, stream=True)
        if response.status_code == 200:
            with open('/home/dan/Downloads/test.sqlite3.gz', 'wb') as f:
                for chunk in response.raw.stream(1024, decode_content=False):
                    if chunk:
                        f.write(chunk)
            return response.content
