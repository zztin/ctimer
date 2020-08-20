import sqlite3
from sqlite3 import Error
from datetime import date
from datetime import datetime
from collections import namedtuple
from dataclasses import dataclass
from dataclasses import astuple
import pandas as pd

@dataclass(init=True, repr=True)
class Clock_details:
    date: str = ""
    clock_count: int = 0
    start_clock: float = 0
    end_clock: float = 0
    end_break: float = 0
    task_title: str = "Task title TO BE IMPLEMENT"
    task_description: str = "Task description to be set"
    reached_bool: bool = False
    reason: str = "N.A."


def get_yearly_stats(db_file):
    conn = create_connection(db_file)
    df = pd.read_sql_query("SELECT * FROM clock_details", conn)

    # new feature while including all clocks (also halted clocks)
    # df[df['clock_done'] == True]['clock_start']
    start_series_raw = df['start_clock']
    start_series = [datetime.fromtimestamp(int(float(x))) for x in start_series_raw]
    events = pd.DataFrame(index=start_series, columns=["count"])
    events['count'] = 1
    events = events['count']
    return events

def get_clock_count(db_file):
    # create a database connection
    conn = create_connection(db_file)
    c = conn.cursor()
    # Create table
    try:
        last_row = c.execute('''SELECT * FROM clock_details ORDER BY id DESC LIMIT 1;''').fetchall()[-1]
        if last_row[1] == f"{date.today()}":
            clock_count = last_row[2]
        else:
            clock_count = 0
    except Exception as e:
        # if the db is empty: error --list index out of range
        #print("Exception ctimer_db.py:49", e, ". Clock_count set to 0. Exception handled, keep running.")
        clock_count = 0
    return clock_count


def db_add_clock_details(db_file, clock_instance):
    # create a database connection
    conn = create_connection(db_file)
    with conn:
        clock_id = create_clock_details(conn, astuple(clock_instance))
    conn.close()
    return clock_id


def create_table(db_file):
    """ create a table from nothing
    """
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        # Create table
        c.execute('''CREATE TABLE IF NOT EXISTS clock_details
                     (id integer PRIMARY KEY,
                     date text,
                     clock_count integer,
                     start_clock text,
                     end_clock text,
                     end_break text,
                     task_title text,
                     task_description text,
                     reached_bool text,
                     reason text )''')
        conn.commit()
        conn.close()
    except Error as e:
        print(e)



def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        create_table(db_file)
    except Error as e:
        print(e)

    return conn


def create_clock_details(conn, entry):
    """
    Create a new clock detail entry into the clock_details table
    :param conn: connection
    :param entry:
    :return: clock id
    """
    # Insert a row of data
    sql = '''INSERT INTO clock_details(date, clock_count, start_clock, end_clock, end_break, task_title, 
    task_description, reached_bool, reason) VALUES (?,?,?,?,?,?,?,?,?)'''
    #TODO: add pause interval
    cur = conn.cursor()
    cur.execute(sql, entry)
    return cur.lastrowid


def create_connection_new(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


