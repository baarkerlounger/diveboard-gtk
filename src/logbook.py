from gi.repository import Gtk, Gio

from .define import RES_PATH
from .dive_trip import DiveTrip
from .dive import Dive
from .spot import Spot

@Gtk.Template(resource_path=f'{RES_PATH}/logbook.ui')
class Logbook(Gtk.Box):
    __gtype_name__ = 'Logbook'

    logbook_list   = Gtk.Template.Child()
    new_dive_btn   = Gtk.Template.Child()

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.new_dive_btn.connect('clicked', self.new_dive)
        self.window = parent
        self.dive_ids = []
        self.divetrips = Gio.ListStore.new(DiveTrip)
        selection_model = Gtk.NoSelection.new()
        selection_model.set_model(self.divetrips)
        self.logbook_list.bind_model(selection_model, lambda trip: trip.view())

    def populate(self):
        if not self.divetrips:
            trips = DiveTrip.offline_trips(self)
            if not trips:
                Dive.create_from_online(self.dive_ids)
                Spot.create_from_online()
                trips = DiveTrip.offline_trips(self)

            idx = 0
            for trip_name in trips:
                trip = DiveTrip(self, **{'name': trip_name, 'dives': trips[trip_name]})
                self.divetrips.append(trip)
                row = self.logbook_list.get_row_at_index(idx)
                row.set_activatable(False)
                idx += 1

    def refresh(self):
        self.divetrips.remove_all()
        self.populate()

    def new_dive(self, button):
        dive_no = len(Dive.offline_dives()) + 1
        divetrip = DiveTrip(self)
        window = Dive(divetrip).detail_view(dive_no)
        window.set_transient_for(self.window)
        window.show()
