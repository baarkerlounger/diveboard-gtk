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

class DiveTrip():

    def __init__(self):
        pass

    @classmethod
    def all(cls):
        all_trips = {}
        dives = Dive.offline_dives()

        for d in dives:
            dive = Dive(**d)
            if dive.trip_name in all_trips.keys():
                all_trips.get(dive.trip_name).append(dive)
            else:
                all_trips[dive.trip_name] = [dive]

        return all_trips

    @classmethod
    def dive_trip_view(cls, trip_name, dives):
        return DiveTripView(trip_name, dives)

@Gtk.Template(resource_path=f'{RES_PATH}/dive_trip.ui')
class DiveTripView(Gtk.Box):
    __gtype_name__ = 'DiveTrip'

    # Takes a Trip Name and an Array of Dive objects and creates
    # the GtkBox to be added to the list view

    trip_name = Gtk.Template.Child()
    dive      = Gtk.Template.Child()

    def __init__(self, name, dives, **kwargs):
        super().__init__(**kwargs)

        self.trip_name.set_text(name)
        for dive in dives:
            self.dive.insert(dive.dive_overview(), -1)
