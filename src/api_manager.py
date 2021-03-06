# api_manager.py
#
# Copyright 2021 baarkerlounger
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name(s) of the above copyright
# holders shall not be used in advertising or otherwise to promote the sale,
# use or other dealings in this Software without prior written
# authorization.

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
