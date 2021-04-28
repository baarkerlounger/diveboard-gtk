# statistics.py
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

from gi.repository import Gtk

from .define import RES_PATH
from .database_manager import DatabaseManager
from .utils import Utils

@Gtk.Template(resource_path=f'{RES_PATH}/statistics.ui')
class Statistics(Gtk.Box):
    __gtype_name__ = 'Statistics'

    dive_count           = Gtk.Template.Child()
    country_count        = Gtk.Template.Child()
    spot_count           = Gtk.Template.Child()
    total_duration       = Gtk.Template.Child()
    most_dives_country   = Gtk.Template.Child()
    max_time             = Gtk.Template.Child()
    max_time_location_1  = Gtk.Template.Child()
    max_time_location_2  = Gtk.Template.Child()
    max_depth            = Gtk.Template.Child()
    max_depth_location_1 = Gtk.Template.Child()
    max_depth_location_2 = Gtk.Template.Child()
    max_temp             = Gtk.Template.Child()
    max_temp_location_1  = Gtk.Template.Child()
    max_temp_location_2  = Gtk.Template.Child()
    min_temp             = Gtk.Template.Child()
    min_temp_location_1  = Gtk.Template.Child()
    min_temp_location_2  = Gtk.Template.Child()

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent

    def calculate(self):
        divetrips = self.parent.logbook.divetrips
        dive_count = 0
        total_time = 0
        max_time = 0
        max_depth = 0
        max_temp  = 0
        min_temp  = 1000
        max_time_location = None
        max_depth_location = None
        max_temp_location = None
        min_temp_location = None
        for divetrip in divetrips:
            for dive in divetrip.dives:
                dive_count += 1
                total_time += dive.duration
                depth = Utils.convert_depth_to_m(dive.maxdepth, dive.maxdepth_unit)
                temp  = Utils.convert_temp_to_c(dive.temp_bottom, dive.temp_bottom_unit)
                if dive.duration > max_time:
                    max_time = dive.duration
                    max_time_location = dive.spot
                if depth and (depth > max_depth):
                    max_depth = depth
                    max_depth_location = dive.spot
                if temp and temp > max_temp:
                    max_temp = temp
                    max_temp_location = dive.spot
                if temp and temp < min_temp:
                    min_temp = temp
                    min_temp_location = dive.spot

        self.dive_count.set_text(str(dive_count))

        self.spot_count.set_text(str(self.get_spot_count()))

        self.country_count.set_text(str(self.get_country_count()))

        self.total_duration.set_text(Utils.format_time(total_time))

        self.most_dives_country.set_text(self.get_max_dive_country())

        self.max_time.set_text(Utils.format_time(max_time))
        if max_time_location:
            self.max_time_location_1.set_text(f'in {max_time_location.location_name},')
            self.max_time_location_2.set_text(f'{max_time_location.country_name}')

        self.max_depth.set_text(Utils.format_depth(max_depth, "m"))
        if max_depth_location:
            self.max_depth_location_1.set_text(f'in {max_depth_location.location_name},')
            self.max_depth_location_2.set_text(f'{max_depth_location.country_name}')

        self.max_temp.set_text(Utils.format_temp(max_temp, "C"))
        if max_temp_location:
            self.max_temp_location_1.set_text(f'in {max_temp_location.location_name},')
            self.max_temp_location_2.set_text(f'{max_temp_location.country_name}')

        self.min_temp.set_text(Utils.format_temp(min_temp, "C"))
        if min_temp_location:
            self.min_temp_location_1.set_text(f'in {min_temp_location.location_name},')
            self.min_temp_location_2.set_text(f'{min_temp_location.country_name}')

    def get_spot_count(self):
        sql = """SELECT COUNT(DISTINCT id) FROM spots"""
        return list(DatabaseManager().fetch(sql, None)[0].values())[0]

    def get_country_count(self):
        sql = """SELECT COUNT(DISTINCT country_name) FROM spots"""
        return list(DatabaseManager().fetch(sql, None)[0].values())[0]

    def get_max_dive_country(self):
        sql = """SELECT country_name, COUNT(country_name) AS cnt FROM spots GROUP BY country_name ORDER BY cnt DESC LIMIT 1;"""
        return list(DatabaseManager().fetch(sql, None)[0].values())[0]
