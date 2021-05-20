# main.py
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

import sys
import gi
import os
from pathlib import Path

gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')

from gi.repository import Gdk, Gtk, Gio, GdkPixbuf, Adw

from .window import DiveboardWindow
from .preferences import DiveboardPreferencesWindow
from .settings import Settings
from .define import APP_ID, RES_PATH, VERSION, DIVE_THUMBNAIL_PATH
from .database_manager import DatabaseManager
from .dive import Dive


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

    def load_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource(f'{RES_PATH}/css/style.css')
        display = Gdk.Display.get_default()
        style_context = Gtk.StyleContext()
        #   style_context.add_provider_for_display(display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def setup_actions(self):
        preferences_action = Gio.SimpleAction.new('preferences', None)
        preferences_action.connect('activate', self.on_preferences)
        self.add_action(preferences_action)

        about_action = Gio.SimpleAction.new('about', None)
        about_action.connect('activate', self.on_about)
        self.add_action(about_action)

    def on_preferences(self, _action, _param):
        """ Show preferences window """
        window = DiveboardPreferencesWindow(self)
        window.set_transient_for(self.window)

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
