# database_manager.py
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

import sqlite3
from sqlite3 import Error

from .define import DATABASE_FILE

class DatabaseManager:


    CREATE_DIVES_TABLE_SQL = """CREATE TABLE IF NOT EXISTS dives (
	                                id integer,
	                                shaken_id text PRIMARY KEY,
	                                time_in text,
	                                duration integer,
	                                surface_interval text,
	                                maxdepth integer,
	                                maxdepth_value integer,
	                                maxdepth_unit text,
	                                user_id integer,
	                                spot_id integer,
	                                temp_surface integer,
	                                temp_surface_value integer,
	                                temp_surface_unit text,
	                                temp_bottom integer,
	                                temp_bottom_unit text,
	                                temp_bottom_value integer,
	                                privacy integer,
	                                weights integer,
	                                weights_value integer,
	                                weights_unit text,
	                                safetystops text,
	                                safetystops_unit_value text,
	                                divetype text,
	                                favorite text,
	                                visibility text,
	                                trip_name text NOT NULL,
	                                water text,
	                                altitude text,
	                                fullpermalink text,
	                                permalink text,
	                                complete text,
	                                thumbnail_image_url text,
	                                thumbnail_profile_url text,
	                                guide text,
	                                shop_id integer,
	                                notes text,
	                                public_notes text,
	                                diveshop text,
	                                current text,
	                                species text,
	                                gears text,
	                                user_gears text,
	                                dive_gears text,
	                                legacy_buddies_hash text,
	                                lat text,
	                                lng text,
	                                date text,
	                                time text,
	                                buddies text,
	                                shop text,
	                                dive_reviews text,
	                                pictures text,
	                            UNIQUE(shaken_id)
                                );"""

    CREATE_SPOTS_TABLE_SQL = """CREATE TABLE IF NOT EXISTS spots (
	                                id integer PRIMARY KEY,
	                                shaken_id integer,
	                                country_name text,
	                                country_code text,
                                    country_flag_big text,
                                    country_flag_small text,
                                    within_country_bounds boolean,
                                    region_name text,
	                                location_name text,
	                                permalink text,
	                                fullpermalink text,
	                                staticmap text,
	                                name text,
	                                lat text,
	                                lng text,
	                            UNIQUE(id)
                                );"""

    CREATE_PICTURES_TABLE_SQL = """CREATE TABLE IF NOT EXISTS pictures (
	                                id integer PRIMARY KEY,
	                                thumbnail text,
	                                medium text,
                                    large text,
                                    small text,
                                    notes text,
                                    media text,
	                                player text,
	                                full_redirect_link text,
	                                fullpermalink text,
	                                permalink text,
	                                staticmap text,
	                                created_at text,
	                            UNIQUE(id)
                                );"""

    def setup_database(self):
        conn = self.create_connection()
        self.create_tables(conn, self.CREATE_DIVES_TABLE_SQL)
        self.create_tables(conn, self.CREATE_SPOTS_TABLE_SQL)
        self.create_tables(conn, self.CREATE_PICTURES_TABLE_SQL)

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(DATABASE_FILE)
            return conn
        except Error as e:
            print(e)

    def create_tables(self, conn, sql):
        try:
            c = conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)

    def insert_row(self, sql, values):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()

        return cur.lastrowid

    def fetch(self, sql, args):
        conn = self.create_connection()
        conn.row_factory = sqlite3.Row
        curr = conn.cursor()
        if args:
            ex = curr.execute(sql, args)
        else:
            ex = curr.execute(sql)
        rows = ex.fetchall()
        return [dict(row) for row in rows]






