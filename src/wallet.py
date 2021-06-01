# wallet.py
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

from gi.repository import Gtk, GdkPixbuf

from .define import RES_PATH

@Gtk.Template(resource_path=f'{RES_PATH}/wallet.ui')
class Wallet(Gtk.Box):
    __gtype_name__ = 'Wallet'

    wallet_box   = Gtk.Template.Child()
    new_cert_btn = Gtk.Template.Child()

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent
        self.new_cert_btn.connect('clicked', self.file_chooser_dialog)

    def display_cert(self, file):
        image = Gtk.Picture()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=file.get_path(), width=250, height=150, preserve_aspect_ratio=False)
        image.set_pixbuf(pixbuf)
        self.wallet_box.append(image)

    def file_chooser_dialog(self, button):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", action=Gtk.FileChooserAction.OPEN
        )

        dialog.add_buttons(
            "_Cancel",
            Gtk.ResponseType.CANCEL,
            "_Open",
            Gtk.ResponseType.OK,
        )

        self.add_filters(dialog)
        dialog.set_transient_for(self.parent)
        dialog.connect("response", self.file_chooser_response)
        dialog.show()

    def file_chooser_response(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            self.display_cert(dialog.get_file())
        elif response == Gtk.ResponseType.CANCEL:
            pass
        dialog.destroy()

    def add_filters(self, dialog):
        filter_image = Gtk.FileFilter()
        filter_image.set_name("Image files")
        filter_image.add_mime_type("image/*")
        dialog.add_filter(filter_image)
