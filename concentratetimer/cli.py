"""Console script for concentratetimer."""
from concentratetimer import concentratetimer
import tkinter as tk
import concentratetimer.ctimer_db as db
import sys
from subprocess import Popen, PIPE
import os
import argparse
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="Shorten clock intervals for debugging purposes.",action="store_true")
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
    root = tk.Tk()
    app = concentratetimer.ConcentrateTimer(master=root, db_file=db_file, debug=args.debug)
    #app.protocol("WM_DELETE_WINDOW", safe_closing)
    app.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
