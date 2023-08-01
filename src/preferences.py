import gi

from gi.repository import Gtk, Adw, Gio

from .settings import Settings
from .define import RES_PATH


@Gtk.Template(resource_path=f'{RES_PATH}/preferences.ui')
class DiveboardPreferencesWindow(Adw.PreferencesWindow):
    __gtype_name__ = 'DiveboardPreferencesWindow'

    parent = NotImplemented

    units = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Called in init() so set_transient for hasn't run yet
        self.parent = self.get_group().list_windows()[-1]
        self.setup()

    def setup(self):
        self.setup_units_preferences()

    def setup_units_preferences(self):
        units_list = Gtk.StringList.new(["Metric","Imperial"])

        self.units.set_model(units_list)
        self.units.set_selected(Settings.get().get_units())
        self.units.connect('notify::selected', self._switch_units)

    def _switch_units(self, _row, _value):
        selected_index = self.units.get_selected()
        Settings.get().set_units(selected_index)
        self.parent.logbook.refresh()


