import sqlite3
from sqlite3 import Error
from collections import namedtuple
from dataclasses import dataclass
from dataclasses import astuple


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


