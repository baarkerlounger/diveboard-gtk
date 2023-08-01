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
