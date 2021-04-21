# spot.py
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

from .database_manager import DatabaseManager
from .api_manager import ApiManager
from .define import RES_PATH, API_KEY, API_URL
from .settings import Settings

class Spot():

    def __init__(self, id):
        self.id = id
        self.get_online_values()
        self.insert_spot()

    def set_values(self, **kwargs):
        self.shaken_id = kwargs['shaken_id']
        self.country_name = kwargs['country_name']
        self.country_code = kwargs['country_code']
        self.country_flag_big = kwargs['country_flag_big']
        self.country_flag_small = kwargs['country_flag_small']
        self.within_country_bounds = kwargs['within_country_bounds']
        self.region_name = kwargs['region_name']
        self.location_name = kwargs['location_name']
        self.permalink = kwargs['permalink']
        self.fullpermalink = kwargs['fullpermalink']
        self.staticmap = kwargs['staticmap']
        self.name = kwargs['name']
        self.lat = kwargs['lat']
        self.lng = kwargs['lng']

    def insert_spot(self):
        sql = """INSERT OR IGNORE INTO spots(id,shaken_id,country_name,country_code,country_flag_big,country_flag_small,within_country_bounds,region_name, location_name,
                             permalink, fullpermalink, staticmap, name, lat, lng)
                 VALUES(?,?,?,?,?,?,?,?, ?, ?, ?, ?, ?, ?, ?)"""
        values = (self.id, self.shaken_id, self.country_name, self.country_code, self.country_flag_big, self.country_flag_small, self.within_country_bounds,
                  self.region_name, self.location_name, self.permalink, self.fullpermalink, self.staticmap, self.name, self.lat, self.lng)
        DatabaseManager().insert_row(sql, values)

    def get_online_values(self):
        arg = json.dumps({"id": str(self.id)})
        response = ApiManager.object_request('V2/spot', arg)
        if response:
            self.set_values(**response)

    @classmethod
    def get_online_spots(cls, spot_ids):
        spots = []
        if (len(spots) > 0):
            for spot_id in spot_ids:
                if response:
                    spot = Spot(spot_id)
                    spot.get_online_values()
                    spot.insert_spot()
        return spots

        
