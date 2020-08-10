import sqlite3
import arrow

def round_epoch_to_day(epoch_time):
    timestamp = arrow.get(epoch_time)
    rounded_timestamp_to_day = timestamp.floor('day')
    rounded_timestamp_to_day.format('X')
    return rounded_timestamp_to_day

def get_clock_count_per_day(db_file):
    # count date column (not good for more information (if we want to include the half finished clocks as well)
    # add a column boolean for "finished clocks", select "True" + Date


# connect to the SQlite databases
connection = sqlite3.connect("../../data/ctimer.db")
cursor = connection.cursor()
# select all the dates and clock count from the database
cursor.execute("SELECT clock_count FROM clock_details;")
tables = cursor.fetchall()
# for each of the bables , select all the records from the table
for table_name in tables:
    # table_name = table_name[0]
    print(table_name['clock_count'])

    conn = sqlite3.connect("../../data/ctimer.db")
    conn.row_factory = dict_factory

    cur1 = conn.cursor()

    cur1.execute("SELECT * FROM " + table_name['clock_count'])

    # fetch all or one we'll go for all.

    results = cur1.fetchall()

    print(results)

    # generate and save JSON files with the table name for each of the database tables
    with open(table_name['clock_count'] + '.json', 'a') as the_file:
        the_file.write(format(results).replace(" u'", "'").replace("'", "\""))

connection.close()
