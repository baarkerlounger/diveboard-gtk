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

from gi.repository import Gtk, GdkPixbuf, Gio

from .database_manager import DatabaseManager
from .api_manager import ApiManager
from .define import RES_PATH, API_KEY, API_URL
from .settings import Settings
from .spot import Spot

class Dive():

    def __init__(self, *args, **kwargs):
        self.id = kwargs["id"]
        self.trip_name = kwargs["trip_name"]
        self.maxdepth = kwargs["maxdepth"]
        self.maxdepth_unit = kwargs["maxdepth_unit"]
        self.time_in = kwargs["time_in"]
        self.duration = kwargs["duration"]
        self.date = kwargs["date"]
        self.thumbnail_image_url = kwargs["thumbnail_image_url"]
        self.spot_id = kwargs["spot_id"]
        self.spot = Spot.get_spot_by_id(self.spot_id)

    def dive_overview(self):
        return DiveOverview(self)

    @classmethod
    def insert_dive(cls, dive):
        sql = """INSERT OR IGNORE INTO dives(id,trip_name,maxdepth,maxdepth_unit,time_in,duration,date,thumbnail_image_url, spot_id) VALUES(?,?,?,?,?,?,?,?,?)"""
        values = (dive['id'], dive['trip_name'], dive['maxdepth'], dive['maxdepth_unit'], dive['time_in'], dive['duration'], dive['date'], dive['thumbnail_image_url'], dive['spot_id'])
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

        thumbnail = urllib.request.urlopen(dive.thumbnail_image_url)
        input_stream = Gio.MemoryInputStream.new_from_data(thumbnail.read(), None)
        pixbuf = GdkPixbuf.Pixbuf.new_from_stream(input_stream, None)
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
