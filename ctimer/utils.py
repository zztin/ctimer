from ctimer import ctimer
import ctimer.ctimer as ct
import tkinter as tk
import ctimer.ctimer_db as db
import sys
import os
import argparse
from ctimer.visual import show_stats as ss
from tkinter import messagebox
import logging
from pathlib import Path


def yesno(question):
    """
    Commandline prompt ask yes/no question recursively.
    """
    prompt = f"{question}? (y/n)"
    ans = input(prompt).strip().lower()
    if ans not in ["y", "n"]:
        print("please type y or n.")
        return yesno(question)
    if ans == "y":
        return True
    return False

def ask_customized():
    set_time = input(f"Desired length of clock? (min, default=25): ")
    break_time = input(f"Desired length of normal breaks? (min, default=5): ")
    long_break_time = input(f"Desired length of long break? (min, default=15): ")
    long_break_clock_count = input(
        f"Every N break you want to have a long break? (N, default=4): "
    )
    aim_clock_count = input("How many clocks are you aiming today? (N, default=8): ")
    return ct.Meta(
        set_time=int(set_time) * 60,
        break_time=int(break_time) * 60,
        long_break_time=int(long_break_time) * 60,
        long_break_clock_count=int(long_break_clock_count),
        aim_clock_count=int(aim_clock_count),
    )

def create_cache_folder():
    # store database path information in users' home folder.
    home = str(Path.home())
    cache_path = os.path.join(home, ".ctimer/")
    if os.path.isdir(cache_path):
        pass
    else:
        os.makedirs(cache_path)
    return cache_path

def get_cache_filepath(arg_db, debug=False, mock_test=False):
    cache_path = create_cache_folder()
    if debug:
        filename = "db_debug_path.txt"
    elif mocktest:
        filename = "db_mock_path.txt"
    else:
        filename = "db_path.txt"
    # read cache
    try:
        with open(cache_path + filename, "r") as db_path_file:
            stored_path = db_path_file.readline().strip()
        # Continue if file exists.
        if arg_db == None:
            return stored_path
        else:
            # Not first time user. But provided new db path.
            given_path = str(os.path.join(root_path, arg_db))
            if given_path != stored_path:
                if yesno(
                    f"You have a previously created database stored at {stored_path}. Are you sure you want to create a new database? \
                          If not, type 'n', previously saved db will be used. If you want to create new database, type 'y', a new database will be \
                          created and default database path will be changed."
                ):
                    cwd = os.getcwd()
                    new_path = str(os.path.join(cwd, arg_db))
                    with open(cache_path + filename, "w") as db_path_file:
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
            new_path = str(os.path.join(root_path, arg_db))
            # create default path at HOME/.ctimer
        with open(cache_path + filename, "w") as db_path_file:
            db_path_file.write(new_path)
        return new_path

def dir_path(rdir_path):
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

def time_print(time):
    mins, secs = divmod(time, 60)
    print_time = "{:02d}:{:02d}".format(mins, secs)
    return print_time

