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
gi.require_version('Champlain', '0.12')
gi.require_version('GtkChamplain', '0.12')
gi.require_version('GtkClutter', '1.0')
gi.require_version('Geoclue', '2.0')
from gi.repository import GtkClutter
from gi.repository import Gtk, Champlain, GtkChamplain, Handy
from gi.repository import Geoclue

from .define import RES_PATH, MAPBOX_ACCESS_TOKEN
from .spot import Spot

@Gtk.Template(resource_path=f'{RES_PATH}/map.ui')
class MapWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'MapWindow'

    CACHE_SIZE = 100000000  # size of cache stored on disk
    MEMORY_CACHE_SIZE = 100 # in-memory cache size (tiles stored in memory)
    MIN_ZOOM = 2
    MAX_ZOOM = 15
    TILE_SIZE = 256
    LICENSE_TEXT = ""
    LICENSE_URI = "https://www.mapbox.com/tos/"

    map_container = Gtk.Template.Child()
    back_btn      = Gtk.Template.Child()
    spot_search   = Gtk.Template.Child()

    def __init__(self, parent, **kwargs):
        GtkClutter.init([])
        super().__init__(**kwargs)
        self.setup_actions()

        self.map_widget = GtkChamplain.Embed()
        self.view = self.map_widget.get_view()
        #self.view.set_map_source(self.create_cached_source())
        self.view.connect('touch-event', self.test)

        self.map_container.add(self.map_widget)
        lat, lng = self.user_location()
        self.center_on(lat, lng)
        self.set_zoom_level(9)
        self.show_all()

    def test(self):
        print('Touched')

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
        self.view.set_zoom_level(level)

    def create_cached_source(self):
        factory = Champlain.MapSourceFactory.dup_default()

        tile_source = Champlain.NetworkTileSource.new_full(
            "mapbox",
            "mapbox",
            self.LICENSE_TEXT,
            self.LICENSE_URI,
            self.MIN_ZOOM,
            self.MAX_ZOOM,
            self.TILE_SIZE,
            Champlain.MapProjection.MERCATOR,
            "https://api.mapbox.com/v4/mapbox.satellite/#Z#/#X#/#Y#.png?access_token=" + MAPBOX_ACCESS_TOKEN,
            Champlain.ImageRenderer())

        tile_size = tile_source.get_tile_size()

        error_source = factory.create_error_source(tile_size)
        file_cache = Champlain.FileCache.new_full(self.CACHE_SIZE, None, Champlain.ImageRenderer())
        memory_cache = Champlain.MemoryCache.new_full(self.MEMORY_CACHE_SIZE, Champlain.ImageRenderer())

        source_chain = Champlain.MapSourceChain()
        # tile is retrieved in this order:
        # memory_cache -> file_cache -> tile_source -> error_source
        # the first source that contains the tile returns it
        source_chain.push(error_source)
        source_chain.push(tile_source)
        source_chain.push(file_cache)
        source_chain.push(memory_cache)

        return source_chain








  
