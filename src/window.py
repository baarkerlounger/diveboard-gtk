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
import requests
import json

gi.require_version('Handy', '1')

from gi.repository import Gtk, Handy

from .settings import Settings
from .define import RES_PATH, API_KEY, API_URL
from .dive import Dive
from .dive_trip import DiveTrip

@Gtk.Template(resource_path=f'{RES_PATH}/window.ui')
class DiveboardWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'DiveboardWindow'

    main_stack     = Gtk.Template.Child()

    login_screen   = Gtk.Template.Child()
    logbook_screen = Gtk.Template.Child()

    menu_btn       = Gtk.Template.Child()

    login_btn      = Gtk.Template.Child()
    username_entry = Gtk.Template.Child()
    password_entry = Gtk.Template.Child()

    logbook_list   = Gtk.Template.Child()

    all_dive_ids = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login_btn.connect('clicked', self.on_login_clicked)
        self.set_main_screen()

    def set_main_screen(self):
        auth_token = Settings.get().get_auth_token()
        if auth_token:
            self.display_logbook()
        else:
            self.display_login()

    def on_login_clicked(self, widget):
        username = self.username_entry.get_text()
        password = self.password_entry.get_text()
        if (username and password):
            url = API_URL + "login_email"
            payload = {"email": username, "password": password, "apikey": API_KEY}
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                json_response = response.json()
                if (json_response['success'] == True):
                    Settings.get().set_auth_token(json_response['token'])
                    Settings.get().set_user_id(json_response['token'])
                    self.all_dive_ids = json_response['user']['all_dive_ids']
                    self.set_main_screen()
                else:
                    print('Credentials not accepted')
            elif response.status_code == 404:
                print('Not Found.')
        elif not username:
            self.username_entry.grab_focus()
        else:
            self.password_entry.grab_focus()

    def display_logbook(self):
        self.main_stack.set_visible_child(self.logbook_screen)
        trips = DiveTrip.all()
        if not trips:
            Dive.get_online_dives(self.all_dive_ids)
            trips = DiveTrip.all()

        for trip_name in trips:
            trip_view = DiveTrip.dive_trip_view(trip_name, trips[trip_name])
            self.logbook_list.insert(trip_view, -1)



    def display_login(self):
        self.main_stack.set_visible_child(self.login_screen)



        
