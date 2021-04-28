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

    dive_count = Gtk.Template.Child()

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent

    def calculate(self):
        self.dive_count.set_text(str(self.get_dive_count()))

        divetrips = self.parent.logbook.divetrips
        max_depth = 0
        max_temp  = 0
        min_temp  = 0
        for divetrip in divetrips:
            for dive in divetrip.dives:
                depth = Utils.convert_depth_to_m(dive.maxdepth, dive.maxdepth_unit)
                temp  = Utils.convert_temp_to_c(dive.temp_bottom, dive.temp_bottom_unit)
                if depth and (depth > max_depth):
                    max_depth = depth
                if temp and temp > max_temp:
                    max_temp = temp
                if temp and temp < min_temp:
                    min_temp = temp


        print(f'Dive Sites: {self.get_spot_count()}')
        print(f'Total Time: {self.get_total_time()}')
        print(f'Most Dives in: {self.get_max_dive_country()}')
        print(f'Max Time: {self.get_max_duration()}')
        print(f'Max depth: {Utils.format_depth(max_depth, "m")}')
        print(f'Warmest Water: {Utils.format_temp(max_temp, "C")}')
        print(f'Coldest Water: {Utils.format_temp(min_temp, "C")}')

    def get_dive_count(self):
        sql = """SELECT COUNT(id) FROM dives"""
        return list(DatabaseManager().fetch(sql, None)[0].values())[0]

    def get_max_duration(self):
        sql = """SELECT MAX(duration) FROM dives"""
        mins = list(DatabaseManager().fetch(sql, None)[0].values())[0]
        return Utils.format_time(mins)

    def get_total_time(self):
        sql = """SELECT SUM(duration) FROM dives"""
        mins = list(DatabaseManager().fetch(sql, None)[0].values())[0]
        return Utils.format_time(mins)

    def get_spot_count(self):
        sql = """SELECT COUNT(DISTINCT id) FROM spots"""
        return list(DatabaseManager().fetch(sql, None)[0].values())[0]

    def get_max_dive_country(self):
        sql = """SELECT country_name, COUNT(country_name) AS cnt FROM spots GROUP BY country_name ORDER BY cnt DESC LIMIT 1;"""
        return list(DatabaseManager().fetch(sql, None)[0].values())[0]
