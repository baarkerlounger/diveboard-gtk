# window.py
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

gi.require_version('Handy', '1')

from gi.repository import Gtk, Gio, GLib, Handy

from .settings import Settings
from .define import RES_PATH
from .dive import Dive
from .dive_trip import DiveTrip
from .spot import Spot
from .logbook import Logbook
from .login import Login
from .statistics import Statistics
from .wallet import Wallet

@Gtk.Template(resource_path=f'{RES_PATH}/window.ui')
class DiveboardWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'DiveboardWindow'

    main_stack     = Gtk.Template.Child()

    screen_stack    = Gtk.Template.Child()

    login_screen   = Gtk.Template.Child()
    main_screen    = Gtk.Template.Child()

    all_dive_ids = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login = Login(self)
        self.login_screen.add(self.login)
        self.logbook = Logbook()
        self.screen_stack.add(self.logbook)
        self.statistics = Statistics()
        self.screen_stack.add(self.statistics)
        self.wallet = Wallet()
        self.screen_stack.add(self.wallet)
        self.set_main_screen()
        self.setup_actions()

    def setup_actions(self):
        screen_state_action = Gio.SimpleAction.new_stateful('screen_state', GLib.VariantType.new('s'), GLib.Variant.new_string("logbook"))
        screen_state_action.connect('activate', self.on_screen_state_change)
        self.add_action(screen_state_action)

    def on_screen_state_change(self, action, param):
        action.set_state(param)
        screen = param.get_string()
        if screen == "statistics":
            self.display_statistics()
        elif screen == "wallet":
            self.display_wallet()
        else:
            self.display_logbook()

    def set_main_screen(self):
        auth_token = Settings.get().get_auth_token()
        if auth_token:
            self.display_logbook()
        else:
            self.display_login()

    def display_logbook(self):
        self.main_stack.set_visible_child(self.main_screen)
        self.screen_stack.set_visible_child(self.logbook)
        trips = DiveTrip.all()
        if not trips:
            Dive.create_from_online(self.all_dive_ids)
            Spot.create_from_online()
            trips = DiveTrip.all()

        for trip_name in trips:
            trip_view = DiveTrip.dive_trip_view(trip_name, trips[trip_name])
            self.logbook.logbook_list.insert(trip_view, -1)

    def display_login(self):
        self.main_stack.set_visible_child(self.login_screen)

    def display_statistics(self):
        self.screen_stack.set_visible_child(self.statistics)

    def display_wallet(self):
        self.screen_stack.set_visible_child(self.wallet)



        
