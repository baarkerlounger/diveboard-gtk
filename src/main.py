import sys
import gi
import os
from concurrent import futures
from pathlib import Path

gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gdk, Gtk, Gio, GdkPixbuf, Adw

from .window import DiveboardWindow
from .preferences import DiveboardPreferencesWindow
from .settings import Settings
from .define import APP_ID, RES_PATH, VERSION, DIVE_THUMBNAIL_PATH
from .database_manager import DatabaseManager
from .dive import Dive
from .spot import Spot


class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id=APP_ID, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.window = None

    def do_activate(self):
        window = self.props.active_window
        if not window:
            window = DiveboardWindow(application=self)
        window.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)
        Adw.init()
        DatabaseManager().setup_database()
        if not os.path.isdir(DIVE_THUMBNAIL_PATH):
            os.mkdir(DIVE_THUMBNAIL_PATH)
        self.setup_actions()
        self.load_css()
        self.load_data()

    def load_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource(f'{RES_PATH}/css/style.css')
        display = Gdk.Display.get_default()
        Gtk.StyleContext.add_provider_for_display(display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def setup_actions(self):
        preferences_action = Gio.SimpleAction.new('preferences', None)
        preferences_action.connect('activate', self.on_preferences)
        self.add_action(preferences_action)

        about_action = Gio.SimpleAction.new('about', None)
        about_action.connect('activate', self.on_about)
        self.add_action(about_action)

    def load_data(self):
        executor = futures.ProcessPoolExecutor(max_workers=1)
        future = executor.submit(Spot.download_mobile_spots_file)
        future.add_done_callback(self.on_data_load_complete)

    def on_data_load_complete(self, future):
        print(future.result())

    def on_preferences(self, _action, _param):
        """ Show preferences window """
        window = DiveboardPreferencesWindow()
        window.set_transient_for(self.window)
        window.show()

    def on_about(self, _action, _param):
        """ Show about dialog """
        builder = Gtk.Builder.new_from_resource(f'{RES_PATH}/about.ui')
        about = builder.get_object('about')
        about.set_transient_for(self.window)
        about.set_logo_icon_name(APP_ID)
        about.set_version(VERSION)
        about.show()

def main(version):
    app = Application()
    return app.run(sys.argv)
