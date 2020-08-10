"""Console script for concentratetimer."""
from concentratetimer import concentratetimer
import tkinter as tk
import concentratetimer.ctimer_db as db
import sys
import os
import argparse
from concentratetimer.visual import clock_count_cal as ccc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="Shorten clock intervals for debugging purposes.",action="store_true")
    parser.add_argument("--overall", help="Show all clock counts across the years.",action="store_true")
    args = parser.parse_args()
    # can also prompt user to enter a file path to store the database, but next time when the program launch
    #  it has to find it automatically. "from tkinter import filedialog"
    path = os.path.dirname(concentratetimer.__file__).rsplit("/",1)[0]
    if os.path.exists(f"{path}/data"):
        pass
    else:
        os.makedirs(f"{path}/data/")
    db_file = f"{path}/data/ctimer.db"
    db.create_connection(db_file) # create if not exist
    if args.overall:
        events = db.get_yearly_stats(db_file)
        ccc.plot_calmap(events=events)
    else:
        root = tk.Tk()
        app = concentratetimer.ConcentrateTimer(master=root, db_file=db_file, debug=args.debug)
        app.mainloop()
        return 0


if __name__ == "__main__":
    sys.exit(main())
