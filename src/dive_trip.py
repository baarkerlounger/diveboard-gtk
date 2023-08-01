from gi.repository import Gtk, Gio, GObject
import multiprocessing.dummy as mp

from .database_manager import DatabaseManager
from .dive import Dive, DiveOverview
from .define import RES_PATH

class DiveTrip(GObject.Object):

    def __init__(self, logbook, **kwargs):
        super().__init__()
        self.name    = kwargs.get('name')
        self.dives   = kwargs.get('dives', [])
        self.logbook = logbook
        self.dive_liststore = Gio.ListStore.new(Dive)
        for dive in self.dives:
            self.dive_liststore.append(dive)
            dive.divetrip = self

    def view(self):
        return DiveTripView(self)

    @classmethod
    def offline_trips(cls, logbook):
        all_trips = {}
        thread_pool = mp.Pool(4)
        dives = thread_pool.map(lambda d: Dive(**d), Dive.offline_dives())

        for dive in dives:
            logbook.dive_ids.append(dive.id)
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
        selection_model = Gtk.SingleSelection.new()
        selection_model.set_model(self.divetrip.dive_liststore)
        self.dive_list.bind_model(selection_model, lambda dive: dive.overview())

    def on_row_activated(self, dive_list, row):
        clicked_dive = row.get_child().dive
        dives = Dive.offline_dives()
        dives.reverse()
        sorted_dive_ids = [ sub['id'] for sub in dives ]
        dive_number = sorted_dive_ids.index(clicked_dive.id) + 1
        window = clicked_dive.detail_view(dive_number)
        window.set_transient_for(self.divetrip.logbook.window)
        self.unselect_dives(row)
        window.show()

    def unselect_dives(self, selected_dive):
        divetrips = self.divetrip.logbook.divetrips
        for divetrip in divetrips:
            for dive in divetrip.view().dive_list.get_selected_rows():
                if not selected_dive == dive:
                    divetrip.view.dive_list.unselect_row(dive)
