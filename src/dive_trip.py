# dive_trip.py
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
from .dive import Dive
from .define import RES_PATH
from .dive_detail import DiveDetailWindow

class DiveTrip():

    def __init__(self, logbook, **kwargs):
        self.name    = kwargs['name']
        self.dives   = kwargs['dives']
        self.view    = DiveTripView(self)
        self.logbook = logbook

    @classmethod
    def offline_trips(cls):
        all_trips = {}
        dives = Dive.offline_dives()

        for d in dives:
            dive = Dive(**d)
            if dive.trip_name in all_trips.keys():
                all_trips.get(dive.trip_name).append(dive)
            else:
                all_trips[dive.trip_name] = [dive]

        return all_trips

@Gtk.Template(resource_path=f'{RES_PATH}/dive_trip.ui')
class DiveTripView(Gtk.Box):
    __gtype_name__ = 'DiveTrip'

    trip_name  = Gtk.Template.Child()
    dive_count = Gtk.Template.Child()
    dive_list  = Gtk.Template.Child()

    def __init__(self, divetrip, **kwargs):
        super().__init__(**kwargs)
        self.divetrip = divetrip
        self.dive_list.connect("row-activated", self.on_row_activated)
        dive_count = len(divetrip.dives)

        self.trip_name.set_text(divetrip.name)
        self.dive_count.set_text(f'({dive_count} dives)')
        for dive in divetrip.dives:
            self.dive_list.insert(dive.overview, -1)

    def on_row_activated(self, dive_list, row):
        clicked_dive = row.get_child().dive
        window = DiveDetailWindow(self, clicked_dive)
        window.set_transient_for(self.divetrip.logbook.window)
        self.unselect_dives(row)


    def unselect_dives(self, selected_dive):
        divetrips = self.divetrip.logbook.divetrips
        for divetrip in divetrips:
            for dive in divetrip.view.dive_list.get_selected_rows():
                if not selected_dive == dive:
                    divetrip.view.dive_list.unselect_row(dive)
