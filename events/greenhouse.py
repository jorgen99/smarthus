# coding=utf-8

import sqlite3
from sqlite3 import Error

def add_temperature(temperature, db="greenhouse.db"):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        create_table_if_not_exist(cursor)
        sql = """ INSERT INTO greenhouse(time, temperature) values(?, ?) """
        cursor.execute(sql, temperature)
        conn.commit()
    except sqlite3.Error as error:
        print("Error while talking to sqlite...", error)

    finally:
        if conn:
            conn.close()

def create_table_if_not_exist(cursor):
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS greenhouse (
              time text NOT NULL,
              temperature real
        );"""
    )

def apa(bepa):
    return "Hej {}".format(bepa)
