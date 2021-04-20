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

from gi.repository import Gtk

from .database_manager import DatabaseManager
from .define import RES_PATH

class Dive():

    def __init__(self, *args, **kwargs):
        if kwargs:
            self.dive_id = kwargs["id"]
            self.trip_name = kwargs["trip_name"]
            self.max_depth = kwargs["maxdepth"]
            self.max_depth_unit = kwargs["maxdepth_unit"]
            self.duration = kwargs["duration"]
            self.date = kwargs["date"]
        else:
            self.dive_id = args[0]
            self.trip_name = args[1]
            self.max_depth = args[2]
            self.max_depth_unit = args[3]
            self.duration = args[4]
            self.date = args[5]

    def dive_overview(self):
        return DiveOverview(self)

    def insert_dive(self):
        sql = """INSERT INTO dives(id,trip_name,max_depth,max_depth_unit,duration,date)
              VALUES(?,?,?,?,?,?)"""
        values = (self.dive_id, self.trip_name, self.max_depth, self.max_depth_unit, self.duration, self.date)
        DatabaseManager().insert_row(sql, values)

@Gtk.Template(resource_path=f'{RES_PATH}/dive_overview.ui')
class DiveOverview(Gtk.Box):
    __gtype_name__ = 'DiveOverview'

    dive_site = Gtk.Template.Child()
    country   = Gtk.Template.Child()
    dive_date = Gtk.Template.Child()
    max_depth = Gtk.Template.Child()
    duration  = Gtk.Template.Child()

    def __init__(self, dive, **kwargs):
        super().__init__(**kwargs)

        self.dive_site.set_text(dive.trip_name)
        self.dive_date.set_text(dive.date)
        self.max_depth.set_text(f'{dive.max_depth}{dive.max_depth_unit}')
        self.duration.set_text(str(dive.duration) + ' mins')
