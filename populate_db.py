import sqlite3
from sqlite3 import Error
import csv
import json

def main():
    conn = sqlite3.connect("greenhouse.db")
    create_table(conn)

    with open('greenhouse_log.txt', 'r') as the_file:
        for line in the_file:
            it = iter(map(lambda s: s.strip(), line.split(";")))
            t_data = dict(zip(it, it))
            t_data['temperature'] = float(t_data['temperature'])
            t_data['humidity'] = int(t_data['humidity'])
            values = (t_data['date'], t_data['temperature'])
            insert_value(conn, values)

    print_no_of_rows(conn)

def print_no_of_rows(conn):
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM greenhouse")
    print("No of lines: {}".format(cur.fetchone()))

def insert_value(conn, temperature):
    sql = """ INSERT INTO greenhouse(time, temperature) values(?, ?) """
    cur = conn.cursor()
    cur.execute(sql, temperature)

def wef():
    temp_values = []
    with open('./green.log', 'r') as the_file:
        for line in the_file:
            it = iter(map(lambda s: s.strip(), line.split(";")))
            temperature_data = dict(zip(it, it))
            temperature_data['temp'] = float(temperature_data['temp'])
            temperature_data['humidity'] = int(temperature_data['humidity'])
            temp_values.append(temperature_data)
        json_str = json.dumps(temp_values)


def create_table(conn):
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS greenhouse (
              time text NOT NULL,
              temperature real
        );"""
    )
            

if __name__ == '__main__':
    main()
