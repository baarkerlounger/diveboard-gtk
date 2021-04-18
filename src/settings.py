# settings.py
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

from gi.repository import Gio, GLib

from .define import APP_ID

class Settings(Gio.Settings):

    instance = None

    def __init__(self):
        Gio.Settings.__init__(self)

    @staticmethod
    def new():
        """Create a new instance of Settings."""
        g_settings = Gio.Settings.new(APP_ID)
        g_settings.__class__ = Settings
        return g_settings

    @staticmethod
    def get():
        """Return an active instance of Settings."""
        if Settings.instance is None:
            Settings.instance = Settings.new()

        return Settings.instance

    def get_window_size(self):
        value = self.get_value('window-size')
        return (value[0], value[1])

    def set_window_size(self, size):
        width, height = size
        self.set_value('window-size', GLib.Variant('ai', [width, height]))

    def get_user_id(self):
        return self.get_string('user-id')

    def set_user_id(self, user_id):
        self.set_value('user-id', GLib.Variant('s', user_id))

    def get_auth_token(self):
        return self.get_string('auth-token')

    def set_auth_token(self, token):
        self.set_value('auth-token', GLib.Variant('s', token))

    def get_units(self):
        return self.get_int('units')

    def set_units(self, index):
        self.set_value('units', GLib.Variant('i', index))
