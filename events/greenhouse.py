# coding=utf-8

import sqlite3
from sqlite3 import Error

def add_temperature(temperature):
    try:
        conn = sqlite3.connect("../greenhouse.db")
        sql = """ INSERT INTO greenhouse(time, temperature) values(?, ?) """
        cur = conn.cursor()
        cur.execute(sql, temperature)
        conn.commit()
    except sqlite3.Error as error:
        print("Error while talking to sqlite...", error)

    finally:
        if(conn):
            conn.close()
