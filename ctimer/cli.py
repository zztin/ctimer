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
from pathlib import Path

        
def create_cache_folder():
    # store database path information in users' home folder.
    home = str(Path.home())
    cache_path = os.path.join(home, ".ctimer/")
    if os.path.isdir(cache_path):
        pass
    else:
        os.makedirs(cache_path)

def yesno(question):
    prompt = f"{question}? (y/n)"
    ans = input(prompt).strip().lower()
    if ans not in ["y","n"]:
        print("please type y or n.")
        return yestno(question)
    if ans == "y":
        return True
    return False


def get_cache_filepath(arg_db):
    # read cache
    try:
        with open(cache_path+"db_path.txt", "r") as db_path_file: 
            stored_path = db_path_file.readline().strip()
        # Continue if file exists.
        if arg_db == None:
            return stored_path
        else:
            # Not first time user. But provided new db path.
            given_path = str(os.path.join(root_path, arg_db)))
            if given_path != stored_path:
                if yesno(f"You have a previously created database stored at {stored_path}. Are you sure you want to create a new database? \
                          If not, type 'n', previously saved db will be used. If you want to create new database, type 'y', a new database will be \
                          created and default database path will be changed."):
                    cwd = os.getcwd()
                    new_path = str(os.path.join(cwd, arg_db)) 
                    with open(cache_path+"db_path.txt", "w") as db_path_file:
                        db_path_file.write(new_path)
                    return new_path
                else:
                     # used original path. Ignore --db path.
                    return stored_path
    except Exception as e:
        # File does not exist. First time user. Create db_path.txt file
        if arg_db == None:
            new_path = cache_path
        else:
            new_path = str(os.path.join(root_path, arg_db)))
            # create default path at HOME/.ctimer
            with open(cache_path+"db_path.txt", "w") as db_path_file:
                db_path_file.write(new_path)
        return new_path


def  dir_path(rdir_path):
    root_path = str(Path.home())
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
                        default=None)
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')

    args = parser.parse_args()
    # cache
    create_cache_folder()
    get_cache_filepath(args.db)
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
        ss.plot_timetable(path=db_file, outpath=f"./")
    else:
        ctimer.maintk(db_file, hide=args.hide, debug=args.debug, silence=args.silence)


if __name__ == "__main__":
    sys.exit(main())
