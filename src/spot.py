import requests
import json
import multiprocessing.dummy as mp

from .database_manager import DatabaseManager
from .api_manager import ApiManager
from .define import RES_PATH, API_KEY, API_URL
from .settings import Settings

class Spot():

    def __init__(self, *args, **kwargs):
        self.id = id
        self.shaken_id = kwargs['shaken_id']
        self.country_name = kwargs['country_name']
        self.country_code = kwargs['country_code']
        self.country_flag_big = kwargs['country_flag_big']
        self.country_flag_small = kwargs['country_flag_small']
        self.within_country_bounds = kwargs['within_country_bounds']
        self.region_name = kwargs['region_name']
        self.location_name = kwargs['location_name']
        self.permalink = kwargs['permalink']
        self.fullpermalink = kwargs['fullpermalink']
        self.staticmap = kwargs['staticmap']
        self.name = kwargs['name']
        self.lat = kwargs['lat']
        self.lng = kwargs['lng']

    @classmethod
    def insert_spot(cls, spot):
        sql = """INSERT OR IGNORE INTO spots(id,shaken_id,country_name,country_code,country_flag_big,country_flag_small,within_country_bounds,region_name, location_name,
                             permalink, fullpermalink, staticmap, name, lat, lng)
                 VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        values = (spot['id'], spot['shaken_id'], spot['country_name'], spot['country_code'], spot['country_flag_big'], spot['country_flag_small'], spot['within_country_bounds'],
                  spot['region_name'], spot['location_name'], spot['permalink'], spot['fullpermalink'], spot['staticmap'], spot['name'], spot['lat'], spot['lng'])
        DatabaseManager().insert_row(sql, values)

    @classmethod
    def search_online(cls, **kwargs):
        return ApiManager.spot_search(**kwargs)

    @classmethod
    def create_from_online(cls):
        sql = """SELECT DISTINCT spot_id FROM dives"""
        id_objects = DatabaseManager().fetch(sql, None)
        ids = [x['spot_id'] for x in id_objects]
        online_spots = ApiManager.object_request('V2/spot', ids)
        if online_spots:
            thread_pool = mp.Pool(4)
            thread_pool.map(lambda s: Spot.insert_spot(s), online_spots)

    @classmethod
    def offline_spots(cls):
        res = []
        spots = DatabaseManager().fetch("""SELECT * FROM spots""", None)
        for spot in spots:
            res.append(Spot(**spot))
        return res

    @classmethod
    def get_spot_by_id(cls, spot_id):
        sql = """SELECT * FROM spots WHERE id in (?)"""
        saved_spot = DatabaseManager().fetch(sql, [str(spot_id)])
        if saved_spot:
            return Spot(**saved_spot[0])

    @classmethod
    def get_spots_in_boundary(cls, boundaries):
        res = []
        lngs = boundaries[0]
        lngs.sort()
        lats = boundaries[1]
        lats.sort()
        spots = DatabaseManager().fetch("""SELECT * FROM spots WHERE lng BETWEEN (?) AND(?) AND lat BETWEEN (?) AND (?)""", [lngs[0], lngs[1], lats[0], lats[1]])
        for spot in spots:
            res.append(Spot(**spot))
        return res

    @classmethod
    def download_mobile_spots_file(cls):
        response_bytes = ApiManager.download_mobile_spots_file()
        if response_bytes:
            memory_view = memoryview(response_bytes)
            sql = """INSERT OR IGNORE INTO spots(id,shaken_id,country_name,country_code,country_flag_big,country_flag_small,within_country_bounds,region_name, location_name,
                             permalink, fullpermalink, staticmap, name, lat, lng)
                 VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
            DatabaseManager().insert(sql, memory_view)
