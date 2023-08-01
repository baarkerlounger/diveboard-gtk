import gi

gi.require_version('Shumate', '1.0')
gi.require_version('Geoclue', '2.0')

from gi.repository import Gtk, Adw, Shumate, Geoclue, GLib, Gio, GObject

from .define import RES_PATH
from .spot import Spot

@Gtk.Template(resource_path=f'{RES_PATH}/map.ui')
class MapWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MapWindow'

    map_container = Gtk.Template.Child()
    back_btn      = Gtk.Template.Child()
    spot_search   = Gtk.Template.Child()

    def __init__(self, spot=None, **kwargs):
        super().__init__(**kwargs)
        # Called in init() so set_transient for hasn't run yet
        self.parent = self.get_group().list_windows()[-1]
        self.setup_actions()
        self.setup_search_model()

        map_source_registry = Shumate.MapSourceRegistry.new_with_defaults()
        map_source = map_source_registry.get_by_id(Shumate.MAP_SOURCE_OSM_MAPNIK)
        self.map = Shumate.SimpleMap.new()
        self.map.set_map_source(map_source)
        self.viewport = self.map.get_viewport()
        self.viewport.set_reference_map_source(map_source)
        self.map.add_overlay_layer(Shumate.MapLayer.new(map_source, self.viewport))
        self.marker_layer = Shumate.MarkerLayer.new(self.viewport)
        self.map.add_overlay_layer(self.marker_layer)
        self.map_container.append(self.map)
        self.set_zoom_level(9)
        self.viewport.set_min_zoom_level(2)
        self.setup_location(spot)
        self.mark_all_spots_in_view(self.viewport, self.viewport.get_zoom_level())
        self.viewport.connect('notify::zoom-level', self.mark_all_spots_in_view)


    def setup_actions(self):
        self.back_btn.connect('clicked', lambda clicked: self.destroy())
        #self.spot_search.connect('search-changed', self.search)

    def setup_search_model(self):
        entry_completion = Gtk.EntryCompletion()
        entry_completion.set_minimum_key_length(3)
        entry_completion.set_popup_completion(True)
        entry_completion.set_text_column(0)
        entry_completion.set_match_func(self.search_match)
        spot_candidates = Spot.offline_spots()
        self.spot_list_store = Gtk.TreeStore(GObject.TYPE_STRING)
        for spot in spot_candidates:
            self.spot_list_store.append(None, [f'{spot.name}, {spot.location_name}'])
        self.spot_search.set_completion(entry_completion)
        entry_completion.set_model(self.spot_list_store)

    def search_match(self, entry_completion, text, tree_iter):
        row_spot_name = self.spot_list_store[tree_iter][0]
        return str.lower(text) in str.lower(row_spot_name)

    # def online_search(self, event):
    #     search_text = self.spot_search.get_text()
    #     if len(search_text) > 2:
    #         matches = Spot.search_online(**{"name": search_text})
    #         spot_candidates = [ f'{spot["name"][0:30]}...' for spot in matches ]
    #         self.spot_list_store.splice(0, 0, spot_candidates, len(spot_candidates))

    def setup_location(self, spot=None):
        if spot:
            self.center_on(spot.lat, spot.lng)
        else:
            self.center_on(*self.user_location())

    def user_location(self):
        try:
            clue = Geoclue.Simple.new_sync('diveboard',Geoclue.AccuracyLevel.NEIGHBORHOOD,None)
            location = clue.get_location()
            lat = location.get_property('latitude')
            lng = location.get_property('longitude')
        except GLib.GError as err:
            # If we don't have permission for geolocation let's just center on Greenwich
            lat = 51.4825766
            lng = -0.00
        return lat, lng

    def center_on(self, lat, lng):
        self.viewport.set_location(float(lat), float(lng))

    def set_zoom_level(self, level):
        self.viewport.set_zoom_level(level)

    def set_marker(self, spot):
        icon = Gtk.Image.new_from_resource(f'{RES_PATH}/images/map-marker-vector.png')
        marker = Shumate.Marker()
        marker.set_location(float(spot.lat), float(spot.lng))
        marker.set_child(icon)
        self.marker_layer.add_marker(marker)

    def mark_all_spots_in_view(self, _viewport, _zoom):
        lng1, lng2, lat1, lat2 = self.calculate_map_boundaries()
        for spot in Spot.get_spots_in_boundary([[lng1, lng2], [lat1, lat2]]):
            self.set_marker(spot)

    def calculate_map_boundaries(self):
        top_left = self.viewport.widget_coords_to_location(self.parent, 0, 0)
        bottom_right = self.viewport.widget_coords_to_location(self.parent, 360, 720)
        lng1 = top_left.longitude
        lng2 = bottom_right.longitude
        lat1 = top_left.latitude
        lat2 = bottom_right.latitude
        return lng1, lng2, lat1, lat2
