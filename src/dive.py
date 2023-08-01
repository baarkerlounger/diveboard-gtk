import requests
import json
import urllib
import os
import re
from datetime import datetime
import multiprocessing.dummy as mp

from gi.repository import Gtk, Gdk, GdkPixbuf, Gio, Adw, GObject

from .database_manager import DatabaseManager
from .api_manager import ApiManager
from .define import RES_PATH, DATA_PATH, API_KEY, API_URL, DIVE_THUMBNAIL_PATH
from .settings import Settings
from .spot import Spot
from .utils import Utils
from .map import MapWindow
from .picture import Picture

class Dive(GObject.Object):

    def __init__(self, divetrip=None, *args, **kwargs):
        super().__init__()
        self.id                     = kwargs.get('id', None)
        self.shaken_id              = kwargs.get('shaken_id')
        self.time_in                = kwargs.get('time_in')
        self.duration               = kwargs.get('duration')
        self.surface_interval       = kwargs.get('surface_interval')
        self.maxdepth               = kwargs.get('maxdepth')
        self.maxdepth_value         = kwargs.get('maxdepth_value')
        self.maxdepth_unit          = kwargs.get('maxdepth_unit')
        self.user_id                = kwargs.get('user_id')
        self.spot_id                = kwargs.get('spot_id')
        self.temp_surface           = kwargs.get('temp_surface')
        self.temp_surface_value     = kwargs.get('temp_surface_value')
        self.temp_surface_unit      = kwargs.get('temp_surface_unit')
        self.temp_bottom            = kwargs.get('temp_bottom')
        self.temp_bottom_unit       = kwargs.get('temp_bottom_unit')
        self.temp_bottom_value      = kwargs.get('temp_bottom_value')
        self.privacy                = kwargs.get('privacy')
        self.weights                = kwargs.get('weights')
        self.weights_value          = kwargs.get('weights_value')
        self.weights_unit           = kwargs.get('weights_unit')
        self.safetystops            = kwargs.get('safetystops')
        self.safetystops_unit_value = kwargs.get('safetystops_unit_value')
        self.divetype               = self.from_json_or_none('divetype', **kwargs)
        self.favorite               = kwargs.get('favorite')
        self.visibility             = kwargs.get('visibility')
        self.trip_name              = kwargs.get('trip_name')
        self.water                  = kwargs.get('water')
        self.altitude               = kwargs.get('altitude')
        self.fullpermalink          = kwargs.get('fullpermalink')
        self.permalink              = kwargs.get('permalink')
        self.complete               = kwargs.get('complete')
        self.thumbnail_image_url    = kwargs.get('thumbnail_image_url')
        self.thumbnail_profile_url  = kwargs.get('thumbnail_profile_url')
        self.guide                  = kwargs.get('guide')
        self.shop_id                = kwargs.get('shop_id')
        self.notes                  = kwargs.get('notes')
        self.public_notes           = kwargs.get('public_notes')
        self.diveshop               = self.from_json_or_none('diveshop', **kwargs)
        self.current                = kwargs.get('current')
        self.species                = self.from_json_or_none('species', **kwargs)
        self.gears                  = self.from_json_or_none('gears', **kwargs)
        self.used_gears             = self.from_json_or_none('used_gears', **kwargs)
        self.dive_gears             = self.from_json_or_none('dive_gears', **kwargs)
        self.legacy_buddies_hash    = self.from_json_or_none('legacy_buddies_hash', **kwargs)
        self.lat                    = kwargs.get('lat')
        self.lng                    = kwargs.get('lng')
        self.date                   = kwargs.get('date')
        self.time                   = kwargs.get('time')
        self.buddies                = self.from_json_or_none('buddies', **kwargs)
        self.shop                   = self.from_json_or_none('shop', **kwargs)
        self.dive_reviews           = self.from_json_or_none('dive_reviews', **kwargs)
        self.pictures               = self.from_json_or_none('pictures', **kwargs)

        self.spot = Spot.get_spot_by_id(self.spot_id)

        self.cache_thumbnail_path = self.cache_thumbnail()

        self.divetrip = divetrip

    def cache_thumbnail(self):
        if self.thumbnail_image_url is None:
            return None

        # Match everything after last backslash
        thumbnail_id = re.search('([^\/]+$)', self.thumbnail_image_url)[0]
        thumbnail_path = f'{DIVE_THUMBNAIL_PATH}/{thumbnail_id}'
        if not os.path.isfile(thumbnail_path):
            file = open(thumbnail_path, 'wb')
            thumbnail = urllib.request.urlopen(self.thumbnail_image_url)
            file.write(thumbnail.read())
            file.close()
        return thumbnail_path

    def overview(self):
        return DiveOverview(self)

    def detail_view(self, dive_no):
        return DiveDetailView(self, dive_no)

    def from_json_or_none(self, val, **kwargs):
        jsn = kwargs.get(val)
        if jsn:
            return json.loads(jsn)
        else:
            return None

    @classmethod
    def insert_dive(cls, dive):
        sql = """INSERT OR IGNORE INTO dives(
                    id, shaken_id, time_in, duration, surface_interval, maxdepth, maxdepth_value, maxdepth_unit, user_id, spot_id,
                    temp_surface, temp_surface_value, temp_surface_unit, temp_bottom, temp_bottom_unit, temp_bottom_value,
                    privacy, weights, weights_value, weights_unit, safetystops, safetystops_unit_value, divetype, favorite,
                    visibility, trip_name, water, altitude, fullpermalink, permalink, complete, thumbnail_image_url, thumbnail_profile_url,
                    guide, shop_id, notes, public_notes, diveshop, current, species, gears, user_gears, dive_gears, legacy_buddies_hash,
                    lat, lng, date, time, buddies, shop, dive_reviews, pictures)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""

        values = (dive['id'], dive['shaken_id'], dive['time_in'], dive['duration'], dive['surface_interval'], dive['maxdepth'],
                  dive['maxdepth_value'], dive['maxdepth_unit'], dive['user_id'], dive['spot_id'], dive['temp_surface'],
                  dive['temp_surface_value'], dive['temp_surface_unit'], dive['temp_bottom'], dive['temp_bottom_unit'],
                  dive['temp_bottom_value'], dive['privacy'], dive['weights'], dive['weights_value'], dive['weights_unit'],
                  dive['safetystops'], dive['safetystops_unit_value'], json.dumps(dive['divetype']), dive['favorite'], dive['visibility'],
                  dive['trip_name'], dive['water'], dive['altitude'], dive['fullpermalink'], dive['permalink'], dive['complete'],
                  dive['thumbnail_image_url'], dive['thumbnail_profile_url'], dive['guide'], dive['shop_id'], dive['notes'],
                  dive['public_notes'], json.dumps(dive['diveshop']), dive['current'], json.dumps(dive['species']),
                  json.dumps(dive['gears']), json.dumps(dive['user_gears']), json.dumps(dive['dive_gears']),
                  json.dumps(dive['legacy_buddies_hash']), dive['lat'], dive['lng'], dive['date'], dive['time'],
                  json.dumps(dive['buddies']), json.dumps(dive['shop']), json.dumps(dive['dive_reviews']), json.dumps([x['id'] for x in dive['pictures']]))
        DatabaseManager().insert_row(sql, values)

        Picture.insert_pictures(dive['pictures'])

    @classmethod
    def offline_dives(cls):
        dives_sql = """SELECT * FROM dives ORDER BY DATETIME(dives.time_in) DESC"""
        return DatabaseManager().fetch(dives_sql, None)

    @classmethod
    def create_from_online(cls, dive_ids):
        online_dives = ApiManager.object_request('V2/dive', dive_ids)
        if online_dives:
            thread_pool = mp.Pool(4)
            thread_pool.map(lambda d: Dive.insert_dive(d), online_dives)

@Gtk.Template(resource_path=f'{RES_PATH}/dive_overview.ui')
class DiveOverview(Gtk.Box):
    __gtype_name__ = 'DiveOverview'

    dive_site     = Gtk.Template.Child()
    country       = Gtk.Template.Child()
    dive_date     = Gtk.Template.Child()
    maxdepth      = Gtk.Template.Child()
    duration      = Gtk.Template.Child()
    duration_icon = Gtk.Template.Child()
    depth_icon    = Gtk.Template.Child()
    thumbnail     = Gtk.Template.Child()

    def __init__(self, dive, **kwargs):
        super().__init__(**kwargs)
        self.dive = dive

        if dive.id:
            self.dive_site.set_text(dive.trip_name)
            self.dive_date.set_text(dive.date)
            self.maxdepth.set_text(Utils.format_depth(dive.maxdepth, dive.maxdepth_unit))
            self.duration.set_text(str(round(dive.duration)) + ' min')
            self.duration_icon.set_from_pixbuf(GdkPixbuf.Pixbuf.new_from_resource(f'{RES_PATH}/images/duration.svg'))
            self.depth_icon.set_from_pixbuf(GdkPixbuf.Pixbuf.new_from_resource(f'{RES_PATH}/images/depth.svg'))

            pixbuf = GdkPixbuf.Pixbuf.new_from_file(dive.cache_thumbnail_path)
            self.thumbnail.set_pixbuf(pixbuf)

            self.dive_site.set_text(dive.spot.name)
            self.country.set_text(dive.spot.country_name)


@Gtk.Template(resource_path=f'{RES_PATH}/dive_detail.ui')
class DiveDetailView(Adw.ApplicationWindow):
    __gtype_name__ = 'DiveDetailView'

    window_title = Gtk.Template.Child()
    back_btn     = Gtk.Template.Child()
    header_bar   = Gtk.Template.Child()
    save_btn     = Gtk.Template.Child()

    #General Page
    dive_no          = Gtk.Template.Child()
    trip_name_label  = Gtk.Template.Child()
    trip_name        = Gtk.Template.Child()
    spot_label       = Gtk.Template.Child()
    spot             = Gtk.Template.Child()
    date             = Gtk.Template.Child()
    time             = Gtk.Template.Child()
    max_depth        = Gtk.Template.Child()
    duration         = Gtk.Template.Child()
    safety_stops     = Gtk.Template.Child()
    weights_label    = Gtk.Template.Child()
    weights          = Gtk.Template.Child()
    tanks_label      = Gtk.Template.Child()
    tanks            = Gtk.Template.Child()
    dive_type_label  = Gtk.Template.Child()
    dive_type        = Gtk.Template.Child()
    air_temp_label   = Gtk.Template.Child()
    air_temp         = Gtk.Template.Child()
    water_temp_label = Gtk.Template.Child()
    water_temp       = Gtk.Template.Child()
    water_type_label = Gtk.Template.Child()
    salt_water       = Gtk.Template.Child()
    fresh_water      = Gtk.Template.Child()
    visibility_label = Gtk.Template.Child()
    visibility       = Gtk.Template.Child()
    current_label    = Gtk.Template.Child()
    current          = Gtk.Template.Child()
    altitude_label   = Gtk.Template.Child()
    altitude         = Gtk.Template.Child()

    # Notes Page
    notes    = Gtk.Template.Child()

    # Photo Page
    photo_grid = Gtk.Template.Child()

    # People Page
    dive_center = Gtk.Template.Child()
    dive_buddy  = Gtk.Template.Child()
    guide       = Gtk.Template.Child()

    time_popover = Gtk.Template.Child()
    hour         = Gtk.Template.Child()
    minute       = Gtk.Template.Child()
    time_set     = Gtk.Template.Child()
    time_cancel  = Gtk.Template.Child()



    def __init__(self, dive, dive_no, **kwargs):
        super().__init__(**kwargs)
        self.dive = dive
        self.dive_number = dive_no
        self.popup_labels = {
            self.trip_name:  self.trip_name_label,
            self.spot:       self.spot_label,
            self.weights:    self.weights_label,
            self.tanks:      self.tanks_label,
            self.dive_type:  self.dive_type_label,
            self.air_temp:   self.air_temp_label,
            self.water_temp: self.water_temp_label,
            self.altitude:   self.altitude_label
        }
        self.setup_actions()
        logo_texture = Gdk.Texture.new_from_resource(f'{RES_PATH}/images/logo.svg')
        self.dive_buddy.set_icon_from_paintable(0, logo_texture)
        self.dive_center.set_icon_from_paintable(0, logo_texture)
        location_texture = Gdk.Texture.new_from_resource(f'{RES_PATH}/images/map-marker-symbolic.svg')
        self.spot.set_icon_from_paintable(1, location_texture)
        self.dive_no.set_text(str(self.dive_number))
        if dive.id:
            self.fill_props()
        else:
            self.window_title.set_title("New Dive")
            self.fill_defaults()
        self.set_label_visibilities()

    def setup_actions(self):
        self.back_btn.connect('clicked', lambda clicked: self.destroy())
        self.save_btn.connect('clicked', self.save_dive)
        self.time_set.connect('clicked', self.update_time)
        self.minute.connect('output', self.show_leading_zeros)
        self.time_cancel.connect('clicked', lambda clicked: self.time_popover.hide())
        for entry in self.popup_labels:
            controller = Gtk.EventControllerFocus()
            controller.connect('enter', self.entry_widget_focus, True)
            controller.connect('leave', self.entry_widget_focus, False)
            entry.add_controller(controller)

    @Gtk.Template.Callback()
    def _open_map(self, _event):
        window = MapWindow(self.dive.spot)
        window.set_transient_for(self.dive.divetrip.logbook.window)
        window.show()

    def fill_props(self):
        self.fill_details_props()
        self.fill_people_props()
        self.fill_notes_props()
        self.fill_photos_props()

    def fill_details_props(self):
        self.date.set_text(self.dive.date)
        self.set_time_label_and_adjustment(datetime.strptime(self.dive.time, '%H:%M'))
        self.trip_name.set_text(self.dive.trip_name)
        self.spot.set_text(', '.join([self.dive.spot.name, self.dive.spot.country_name]))
        self.max_depth.set_text(Utils.format_depth(self.dive.maxdepth_value, self.dive.maxdepth_unit))
        self.duration.set_text(Utils.format_time(self.dive.duration))
        self.altitude.set_text(Utils.format_depth(self.dive.altitude, self.dive.maxdepth_unit))
        self.weights.set_text(Utils.format_weight(self.dive.weights, self.dive.weights_unit))
        self.visibility.set_active_id(self.dive.visibility)
        self.current.set_active_id(self.dive.current)
        if self.dive.water == 'salt' or self.dive.water is None:
            self.salt_water.set_active(True)
            self.fresh_water.set_active(False)
        else:
            self.fresh_water.set_active(True)
            self.salt_water.set_active(False)

    def fill_people_props(self):
        guide = self.dive.guide
        if guide is not None:
            self.guide.set_text(self.dive.guide)
        buddies = ', '.join(self.dive.buddies)
        if buddies:
            self.dive_buddy.set_text(buddies)
        dive_center_name = self.dive.diveshop.get("name")
        if dive_center_name is not None:
            self.dive_center.set_text(dive_center_name)

    def fill_notes_props(self):
        notes_buffer = self.notes.get_buffer()
        notes_buffer.set_text(str(self.dive.notes))

    def fill_photos_props(self):
        self.populate_photo_grid()

    def fill_defaults(self):
        self.set_time_label_and_adjustment(datetime.now())
        self.max_depth.set_text('0.0')
        self.duration.set_text('0')
        self.safety_stops.set_text('5 m - 3 m')

    def entry_widget_focus(self, event_controller, focused):
        self.set_label_visibilities({'widget': event_controller.get_widget(), 'focused': focused})

    def set_label_visibilities(self, event_object=None):
        for entry in self.popup_labels:
            label = self.popup_labels[entry]
            self.set_label_visibility(entry , label, event_object)

    def set_label_visibility(self, entry, entry_label, event_object):
        focused_entry = None
        if event_object:
            if event_object.get('focused'):
                focused_entry = event_object.get('widget')
        if entry == focused_entry:
            entry_label.set_visible(True)
            entry_label.get_style_context().add_class('yellow_text')
            entry.set_placeholder_text("")
        elif entry.get_text():
            entry_label.set_visible(True)
            entry_label.get_style_context().remove_class('yellow_text')
        else:
            entry_label.set_visible(False)
            entry_label.get_style_context().remove_class('yellow_text')
            entry.set_placeholder_text(entry_label.get_text())

    def set_time_label_and_adjustment(self, time):
        self.date.set_text(time.strftime("%d/%m/%Y"))
        self.time.set_label(time.strftime("%H:%M"))
        self.hour.set_value(time.hour)
        self.minute.set_value(time.minute)

    def show_leading_zeros(self, spin_button):
        adjustment = spin_button.get_adjustment()
        self.minute.set_text('{:02d}'.format(int(adjustment.get_value())))
        return True

    def update_time(self, _event):
        hours = self.hour.get_value()
        mins = self.minute.get_value()
        self.time.set_label(f'{hours}:{mins}')

    def populate_photo_grid(self):
        row = 0
        col = 0
        for pic_id in self.dive.pictures:
            picture = Picture.get_picture_by_id(pic_id)
            # Match everything after last backslash
            pic_id = re.search('([^\/]+$)', picture.small)[0]
            pic_path = f'{DIVE_THUMBNAIL_PATH}/{pic_id}'
            if not os.path.isfile(pic_path):
                file = open(pic_path, 'wb')
                pic = urllib.request.urlopen(picture.small)
                file.write(pic.read())
                file.close()
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(pic_path, 110, 110, False)
            image = Gtk.Picture.new_for_pixbuf(pixbuf)
            image.set_can_shrink(False)
            self.photo_grid.attach(image, col, row, 1, 1)
            if col < 2:
                col = col + 1
            else:
                col = 0
                row = row + 1

    def save_dive(self, _btn):
        print('Implement Saving here')
        #kwargs = {"tripname": self.trip_name.get_text()}
        #self.dive.__dict__.update(kwargs)

