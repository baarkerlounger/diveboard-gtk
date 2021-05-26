# preferences.py
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

import gi

from gi.repository import Gtk, Adw, Gio

from .settings import Settings
from .define import RES_PATH


@Gtk.Template(resource_path=f'{RES_PATH}/preferences.ui')
class DiveboardPreferencesWindow(Adw.PreferencesWindow):
    __gtype_name__ = 'DiveboardPreferencesWindow'

    parent = NotImplemented

    units = Gtk.Template.Child()

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent
        self.setup()

    def setup(self):
        self.setup_units_preferences()

    def setup_units_preferences(self):
        units_list = Gio.ListStore.new(Adw.ValueObject)
        units_list.insert(0, Adw.ValueObject.new("Metric"))
        units_list.insert(1, Adw.ValueObject.new("Imperial"))
        self.units.set_expression(Adw.ValueObject.dup_string)
        self.units.set_model(units_list)
        self.units.set_selected_index(Settings.get().get_units())
        self.units.connect('notify::selected-index', self._switch_units)

    def _switch_units(self, _row, _value):
        selected_index = self.units.get_selected_index()
        Settings.get().set_units(selected_index)
        self.parent.props.active_window.logbook.refresh()


