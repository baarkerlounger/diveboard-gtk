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

@Gtk.Template(resource_path=f'{RES_PATH}/statistics.ui')
class Statistics(Gtk.Box):
    __gtype_name__ = 'Statistics'

    dive_count = Gtk.Template.Child()

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent

    def calculate(self):
        self.dive_count.set_text(str(self.get_dive_count()))
        print(self.get_max_depth())
        print(round(self.get_total_time() / 60.0))

    def get_dive_count(self):
        divetrips = self.parent.logbook.divetrips
        dive_count = 0
        for divetrip in divetrips:
            for dive in divetrip.dives:
                dive_count += 1
        return dive_count

    def get_max_depth(self):
        sql = """SELECT MAX(maxdepth) FROM dives"""
        return list(DatabaseManager().fetch(sql, None)[0].values())[0]

    def get_max_time(self):
        sql = """SELECT MAX(duration) FROM dives"""
        return list(DatabaseManager().fetch(sql, None)[0].values())[0]

    def get_total_time(self):
        sql = """SELECT SUM(duration) FROM dives"""
        return list(DatabaseManager().fetch(sql, None)[0].values())[0]
