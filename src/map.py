# map.py
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

gi.require_version('Shumate', '0.0')
gi.require_version('Geoclue', '2.0')

from gi.repository import Gtk, Adw, Shumate, Geoclue

from .define import RES_PATH, MAPBOX_ACCESS_TOKEN
from .spot import Spot

@Gtk.Template(resource_path=f'{RES_PATH}/map.ui')
class MapWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MapWindow'

    map_container = Gtk.Template.Child()
    back_btn      = Gtk.Template.Child()
    spot_search   = Gtk.Template.Child()

    def __init__(self, spot=None, **kwargs):
        super().__init__(**kwargs)
        self.setup_actions()

        map_source_registry = Shumate.MapSourceRegistry.new_with_defaults()
        map_source = map_source_registry.get_by_id(Shumate.MAP_SOURCE_OSM_MAPNIK)
        self.view = Shumate.View()
        self.view.set_map_source(map_source)
        self.viewport = self.view.get_viewport()
        self.viewport.set_reference_map_source(map_source)

        tile_layer = Shumate.MapLayer.new(map_source, self.viewport)
        self.view.add_layer(tile_layer)

        self.marker_layer = Shumate.MarkerLayer.new(self.viewport)
        self.view.add_layer(self.marker_layer)

        self.map_container.append(self.view)
        lat, lng = self.user_location()

        if spot:
            self.center_on(spot.lat, spot.lng)
            self.set_marker(spot)
        else:
            self.center_on(lat, lng)

        self.set_zoom_level(9)
        self.viewport.set_min_zoom_level(2)

    def setup_actions(self):
        self.back_btn.connect('clicked', lambda clicked: self.destroy())
        self.spot_search.connect('search-changed', self.search)

    def search(self, event):
        search_text = self.spot_search.get_text()
        if len(search_text) > 2:
            matches = Spot.search_online(**{"name": search_text})
            spot_names = [ spot['name'] for spot in matches[0:3] ]
            print(spot_names)

    def user_location(self):
        try:
            clue = Geoclue.Simple.new_sync('diveboard',Geoclue.AccuracyLevel.NEIGHBORHOOD,None)
            location = clue.get_location()
            lat = location.get_property('latitude')
            lng = location.get_property('longitude')
        except GLib.Error as err:
            # If we don't have permission for geolocation let's just center on Greenwich
            lat = 51.4825766
            lng = -0.0076589
        return lat, lng

    def center_on(self, lat, lng):
        self.view.center_on(float(lat), float(lng))

    def set_zoom_level(self, level):
        self.viewport.set_zoom_level(level)

    def set_marker(self, spot):
        icon = Gtk.Image.new_from_resource(f'{RES_PATH}/images/map-marker-vector.png')
        marker = Shumate.Marker()
        marker.set_location(float(spot.lat), float(spot.lng))
        marker.set_child(icon)
        self.marker_layer.add_marker(marker)
        self.marker_layer.show_all_markers()
