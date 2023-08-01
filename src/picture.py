from .database_manager import DatabaseManager
from .settings import Settings

class Picture():

    def __init__(self, *args, **kwargs):
        self.shaken_id          = kwargs['id']
        self.thumbnail          = kwargs['thumbnail']
        self.medium             = kwargs['medium']
        self.large              = kwargs['large']
        self.small              = kwargs['small']
        self.notes              = kwargs['notes']
        self.media              = kwargs['media']
        self.player             = kwargs['player']
        self.full_redirect_link = kwargs['full_redirect_link']
        self.fullpermalink      = kwargs['fullpermalink']
        self.permalink          = kwargs['permalink']
        self.created_at         = kwargs['created_at']

    @classmethod
    def insert_pictures(cls, pictures):
        for picture in pictures:
            sql = """INSERT OR IGNORE INTO pictures(id, thumbnail, medium, large, small, notes, media, player, full_redirect_link, fullpermalink, permalink, created_at)
                     VALUES(?,?,?,?,?,?,?,?,?,?,?,?)"""
            values = (picture['id'], picture['thumbnail'], picture['medium'], picture['large'], picture['small'], picture['notes'],
                      picture['media'], picture['player'], picture['full_redirect_link'], picture['fullpermalink'], picture['permalink'], picture['created_at'])
            DatabaseManager().insert_row(sql, values)

    @classmethod
    def get_picture_by_id(cls, id):
        sql = """SELECT * FROM pictures WHERE id in (?)"""
        picture = DatabaseManager().fetch(sql, [str(id)])
        if picture:
            return Picture(**picture[0])

