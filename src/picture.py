# picture.py
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
    def insert_picture(cls, pictures):
        for picture in pictures:
            sql = """INSERT OR IGNORE INTO pictures(id, thumbnail, medium, large, small, notes, media, player, full_redirect_link, fullpermalink, permalink, created_at)
                     VALUES(?,?,?,?,?,?,?,?,?,?,?,?)"""
            values = (picture['id'], picture['thumbnail'], picture['medium'], picture['large'], picture['small'], picture['notes'],
                      picture['media'], picture['player'], picture['full_redirect_link'], picture['fullpermalink'], picture['permalink'], picture['created_at'])
            DatabaseManager().insert_row(sql, values)


