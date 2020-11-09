"""Console script for ctimer."""
from ctimer import ctimer
import tkinter as tk
import ctimer.ctimer_db as db
import sys
import os
import argparse
from ctimer.visual import show_stats as ss
from tkinter import messagebox
import logging


def dir_path(rdir_path):
    root_path = os.path.dirname(ctimer.__file__).rsplit("/",1)[0]
    full_path = os.path.join(root_path, rdir_path)

    if os.path.exists(full_path):
        logging.info(f"Found existing db path {full_path}. Will re-use it.")
    else:
        logging.info(f"db path {full_path}/data not found. Create an new one.")
        os.makedirs(f"{full_path}")

    if os.path.isdir(full_path):
        return full_path
    else:
        raise NotADirectoryError(full_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="Shorten clock intervals for debugging purposes.",action="store_true")
    parser.add_argument("--stats", help="Show weekly stats of clock counts this week.", action="store_true")
    parser.add_argument("--overall", help="Show all clock counts across the years.", action="store_true")
    parser.add_argument("--hide", help="Display the timer always on top of other windows unless this statement is given"
                        , action="store_true")
    parser.add_argument("--silence", help="Silence Mode (visual hint instead of audio hint.", action="store_true")
    parser.add_argument("--db", type=dir_path, help="The relative or absolute folder path to store and/or read db",
                        default="./data")
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')

    args = parser.parse_args()

    # can also prompt user to enter a file path to store the database, but next time when the program launch
    #  it has to find it automatically. "from tkinter import filedialog"
    path = os.path.dirname(ctimer.__file__).rsplit("/", 1)[0]
    if os.path.exists(f"{path}/data"):
        pass
    else:
        os.makedirs(f"{path}/data/")
    logging.info(f"{args.db} is where the db stored in.")

    if args.debug:
        db_file = f"{args.db}/ctimer_debug.db"
        db.create_connection(db_file) # create if not exist
    else:
        db_file = f"{args.db}/ctimer.db"
        db.create_connection(db_file) # create if not exist
    if args.overall:
        events = db.get_yearly_stats(db_file)
        ss.plot_calmap(events=events)
    elif args.stats:
        ss.plot_timetable(path=db_file, outpath=f"{path}/data/")
    else:
        ctimer.maintk(db_file, hide=args.hide, debug=args.debug, silence=args.silence)


if __name__ == "__main__":
    sys.exit(main())
