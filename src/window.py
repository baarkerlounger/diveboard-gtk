import gi

from gi.repository import Gtk, Gio, GLib, Adw

from .settings import Settings
from .define import RES_PATH
from .logbook import Logbook
from .login import Login
from .statistics import Statistics
from .wallet import Wallet

@Gtk.Template(resource_path=f'{RES_PATH}/window.ui')
class DiveboardWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'DiveboardWindow'

    main_stack     = Gtk.Template.Child()

    screen_stack   = Gtk.Template.Child()

    login_screen   = Gtk.Template.Child()
    main_screen    = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login = Login(self)
        self.login_screen.set_child(self.login)
        self.logbook = Logbook(self)
        self.screen_stack.add_child(self.logbook)
        self.statistics = Statistics(self)
        self.screen_stack.add_child(self.statistics)
        self.wallet = Wallet(self)
        self.screen_stack.add_child(self.wallet)
        self.set_main_screen(None)
        self.setup_actions()

    def setup_actions(self):
        screen_state_action = Gio.SimpleAction.new_stateful('screen_state', GLib.VariantType.new('s'), GLib.Variant.new_string("logbook"))
        screen_state_action.connect('activate', self.on_screen_state_change)
        self.add_action(screen_state_action)

        logout_action = Gio.SimpleAction.new('logout', None)
        logout_action.connect('activate', self.login.on_logout)
        self.add_action(logout_action)

    def on_screen_state_change(self, action, param):
        action.set_state(param)
        screen = param.get_string()
        self.set_main_screen(screen)

    def set_main_screen(self, screen_state):
        auth_token = Settings.get().get_auth_token()
        if auth_token:
            if screen_state == "statistics":
                self.display_statistics()
            elif screen_state == "wallet":
                self.display_wallet()
            else:
                self.display_logbook()
        else:
            self.display_login()

    def display_logbook(self):
        self.main_stack.set_visible_child(self.main_screen)
        self.screen_stack.set_visible_child(self.logbook)
        self.logbook.populate()

    def display_login(self):
        self.main_stack.set_visible_child(self.login_screen)

    def display_statistics(self):
        self.screen_stack.set_visible_child(self.statistics)
        self.statistics.calculate()

    def display_wallet(self):
        self.screen_stack.set_visible_child(self.wallet)
