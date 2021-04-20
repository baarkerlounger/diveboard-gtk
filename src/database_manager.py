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
	                                id integer PRIMARY KEY,
	                                trip_name text NOT NULL,
	                                max_depth integer,
                                    max_depth_unit text,
                                    duration interger,
	                                date text
                                );"""

    def setup_database(self):
        conn = self.create_connection()
        self.create_tables(conn, self.CREATE_DIVES_TABLE_SQL)

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

    def fetch(self, sql):
        conn = self.create_connection()
        curr = conn.cursor()
        ex = curr.execute(sql)
        return ex.fetchall()




