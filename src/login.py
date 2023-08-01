import requests
import json

from gi.repository import Gtk

from .define import RES_PATH, API_KEY, API_URL
from .settings import Settings

@Gtk.Template(resource_path=f'{RES_PATH}/login.ui')
class Login(Gtk.Box):
    __gtype_name__ = 'Login'

    login_btn      = Gtk.Template.Child()
    username_entry = Gtk.Template.Child()
    password_entry = Gtk.Template.Child()

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent
        self.login_btn.connect('clicked', self.on_login_clicked)

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
                    self.parent.logbook.dive_ids = json_response['user']['all_dive_ids']
                    self.parent.set_main_screen('logbook')
                else:
                    print('Credentials not accepted')
            elif response.status_code == 404:
                print('Not Found.')
        elif not username:
            self.username_entry.grab_focus()
        else:
            self.password_entry.grab_focus()

    def on_logout(self, _action, _param):
        window = self.parent
        self.username_entry.set_text("")
        self.password_entry.set_text("")
        Settings.get().set_auth_token("")
        Settings.get().set_user_id("")
        window.set_main_screen(None)
