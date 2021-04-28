# logbook.py
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
from .dive_trip import DiveTrip
from .dive import Dive
from .spot import Spot

@Gtk.Template(resource_path=f'{RES_PATH}/logbook.ui')
class Logbook(Gtk.Box):
    __gtype_name__ = 'Logbook'

    logbook_list   = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.dive_ids = []
        self.divetrips = []

    def populate_divetrips(self):
        trips = DiveTrip.offline_trips()
        if not trips:
            Dive.create_from_online(self.dive_ids)
            Spot.create_from_online()
            trips = DiveTrip.offline_trips()

        for trip_name in trips:
            trip = DiveTrip(**{'name': trip_name, 'dives': trips[trip_name]})
            self.divetrips.append(trip)
            self.logbook_list.insert(trip.view, -1)
