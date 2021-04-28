# dive.py
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
import os
import re

from gi.repository import Gtk, GdkPixbuf, Gio

from .database_manager import DatabaseManager
from .api_manager import ApiManager
from .define import RES_PATH, DATA_PATH, API_KEY, API_URL
from .settings import Settings
from .spot import Spot

class Dive():

    def __init__(self, *args, **kwargs):
        self.id                     = kwargs['id']
        self.shaken_id              = kwargs['shaken_id']
        self.time_in                = kwargs['time_in']
        self.duration               = kwargs['duration']
        self.surface_interval       = kwargs['surface_interval']
        self.maxdepth               = kwargs['maxdepth']
        self.maxdepth_value         = kwargs['maxdepth_value']
        self.maxdepth_unit          = kwargs['maxdepth_unit']
        self.user_id                = kwargs['user_id']
        self.spot_id                = kwargs['spot_id']
        self.temp_surface           = kwargs['temp_surface']
        self.temp_surface_value     = kwargs['temp_surface_value']
        self.temp_surface_unit      = kwargs['temp_surface_unit']
        self.temp_bottom            = kwargs['temp_bottom']
        self.temp_bottom_unit       = kwargs['temp_bottom_unit']
        self.temp_bottom_value      = kwargs['temp_bottom_value']
        self.privacy                = kwargs['privacy']
        self.weights                = kwargs['weights']
        self.weights_value          = kwargs['weights_value']
        self.weights_unit           = kwargs['weights_unit']
        self.safetystops            = kwargs['safetystops']
        self.safetystops_unit_value = kwargs['safetystops_unit_value']
        self.divetype               = json.loads(kwargs['divetype'])
        self.favorite               = kwargs['favorite']
        self.visibility             = kwargs['visibility']
        self.trip_name              = kwargs['trip_name']
        self.water                  = kwargs['water']
        self.altitude               = kwargs['altitude']
        self.fullpermalink          = kwargs['fullpermalink']
        self.permalink              = kwargs['permalink']
        self.complete               = kwargs['complete']
        self.thumbnail_image_url    = kwargs['thumbnail_image_url']
        self.thumbnail_profile_url  = kwargs['thumbnail_profile_url']
        self.guide                  = kwargs['guide']
        self.shop_id                = kwargs['shop_id']
        self.notes                  = kwargs['notes']
        self.public_notes           = kwargs['public_notes']
        self.diveshop               = json.loads(kwargs['diveshop'])
        self.current                = kwargs['current']
        self.species                = json.loads(kwargs['species'])
        self.gears                  = json.loads(kwargs['gears'])
        self.user_gears             = json.loads(kwargs['user_gears'])
        self.dive_gears             = json.loads(kwargs['dive_gears'])
        self.legacy_buddies_hash    = json.loads(kwargs['legacy_buddies_hash'])
        self.lat                    = kwargs['lat']
        self.lng                    = kwargs['lng']
        self.date                   = kwargs['date']
        self.time                   = kwargs['time']
        self.buddies                = json.loads(kwargs['buddies'])
        self.shop                   = json.loads(kwargs['shop'])
        self.dive_reviews           = json.loads(kwargs['dive_reviews'])

        self.spot = Spot.get_spot_by_id(self.spot_id)

        self.cache_thumbnail_path = self.cache_thumbnail()
        self.overview = DiveOverview(self)

    def cache_thumbnail(self):
        # Match everything after last backslash
        thumbnail_id = re.search('([^\/]+$)', self.thumbnail_image_url)[0]
        thumbnail_path = f'{DATA_PATH}/{thumbnail_id}'
        if not os.path.isfile(thumbnail_path):
            file = open(thumbnail_path, 'wb')
            thumbnail = urllib.request.urlopen(self.thumbnail_image_url)
            file.write(thumbnail.read())
            file.close()
        return thumbnail_path

    @classmethod
    def insert_dive(cls, dive):
        sql = """INSERT OR IGNORE INTO dives(
                    id, shaken_id, time_in, duration, surface_interval, maxdepth, maxdepth_value, maxdepth_unit, user_id, spot_id,
                    temp_surface, temp_surface_value, temp_surface_unit, temp_bottom, temp_bottom_unit, temp_bottom_value,
                    privacy, weights, weights_value, weights_unit, safetystops, safetystops_unit_value, divetype, favorite,
                    visibility, trip_name, water, altitude, fullpermalink, permalink, complete, thumbnail_image_url, thumbnail_profile_url,
                    guide, shop_id, notes, public_notes, diveshop, current, species, gears, user_gears, dive_gears, legacy_buddies_hash,
                    lat, lng, date, time, buddies, shop, dive_reviews)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""

        values = (dive['id'], dive['shaken_id'], dive['time_in'], dive['duration'], dive['surface_interval'], dive['maxdepth'],
                  dive['maxdepth_value'], dive['maxdepth_unit'], dive['user_id'], dive['spot_id'], dive['temp_surface'],
                  dive['temp_surface_value'], dive['temp_surface_unit'], dive['temp_bottom'], dive['temp_bottom_unit'],
                  dive['temp_bottom_value'], dive['privacy'], dive['weights'], dive['weights_value'], dive['weights_unit'],
                  dive['safetystops'], dive['safetystops_unit_value'], json.dumps(dive['divetype']), dive['favorite'], dive['visibility'],
                  dive['trip_name'], dive['water'], dive['altitude'], dive['fullpermalink'], dive['permalink'], dive['complete'],
                  dive['thumbnail_image_url'], dive['thumbnail_profile_url'], dive['guide'], dive['shop_id'], dive['notes'],
                  dive['public_notes'], json.dumps(dive['diveshop']), dive['current'], json.dumps(dive['species']),
                  json.dumps(dive['gears']), json.dumps(dive['user_gears']), json.dumps(dive['dive_gears']),
                  json.dumps(dive['legacy_buddies_hash']), dive['lat'], dive['lng'], dive['date'], dive['time'],
                  json.dumps(dive['buddies']), json.dumps(dive['shop']), json.dumps(dive['dive_reviews']))
        print(values)
        DatabaseManager().insert_row(sql, values)

    @classmethod
    def offline_dives(cls):
        dives_sql = """SELECT * FROM dives ORDER BY DATETIME(dives.time_in) DESC"""
        return DatabaseManager().fetch(dives_sql, None)

    @classmethod
    def create_from_online(cls, dive_ids):
        online_dives = ApiManager.object_request('V2/dive', dive_ids)
        if online_dives:
            for d in online_dives:
                Dive.insert_dive(d)

@Gtk.Template(resource_path=f'{RES_PATH}/dive_overview.ui')
class DiveOverview(Gtk.Box):
    __gtype_name__ = 'DiveOverview'

    dive_site     = Gtk.Template.Child()
    country       = Gtk.Template.Child()
    dive_date     = Gtk.Template.Child()
    maxdepth      = Gtk.Template.Child()
    duration      = Gtk.Template.Child()
    duration_icon = Gtk.Template.Child()
    depth_icon    = Gtk.Template.Child()
    thumbnail     = Gtk.Template.Child()

    def __init__(self, dive, **kwargs):
        super().__init__(**kwargs)

        self.dive_site.set_text(dive.trip_name)
        self.dive_date.set_text(dive.date)
        self.maxdepth.set_text(self.format_depth(dive.maxdepth, dive.maxdepth_unit))
        self.duration.set_text(str(round(dive.duration)) + ' min')
        self.duration_icon.set_from_pixbuf(GdkPixbuf.Pixbuf.new_from_resource(f'{RES_PATH}/images/duration.svg'))
        self.depth_icon.set_from_pixbuf(GdkPixbuf.Pixbuf.new_from_resource(f'{RES_PATH}/images/depth.svg'))

        pixbuf = GdkPixbuf.Pixbuf.new_from_file(dive.cache_thumbnail_path)
        self.thumbnail.set_from_pixbuf(pixbuf)

        self.dive_site.set_text(dive.spot.name)
        self.country.set_text(dive.spot.country_name)

    def format_depth(self, depth, depth_unit):
        units = Settings.get().get_units()
        # Metric
        if (units == 0):
            value = depth
            unit = depth_unit
        #Imperial
        elif (units == 1):
            value = depth / 0.3048
            unit = "ft"
        return f'{round(value)}{unit}'
