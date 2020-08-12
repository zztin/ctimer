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
    parser.add_argument("--overall", help="Show all clock counts across the years.", action="store_true")
    parser.add_argument("--hide", help="Display the timer always on top of other windows unless this statement is given"
                        , action="store_true")
    parser.add_argument("--silence", help="Silence Mode (visual hint instead of audio hint.", action="store_true")
    args = parser.parse_args()
    # can also prompt user to enter a file path to store the database, but next time when the program launch
    #  it has to find it automatically. "from tkinter import filedialog"
    path = os.path.dirname(concentratetimer.__file__).rsplit("/",1)[0]
    if os.path.exists(f"{path}/data"):
        pass
    else:
        os.makedirs(f"{path}/data/")
    if args.debug:
        db_file = f"{path}/data/ctimer_debug.db"
        db.create_connection(db_file) # create if not exist
    else:
        db_file = f"{path}/data/ctimer.db"
        db.create_connection(db_file) # create if not exist
    if args.overall:
        events = db.get_yearly_stats(db_file)
        ccc.plot_calmap(events=events)
    else:
        root = tk.Tk()
        if args.hide is False:
            root.attributes("-topmost", True)
        app = concentratetimer.ConcentrateTimer(master=root,
                                                db_file=db_file,
                                                debug=args.debug,
                                                hide=args.hide,
                                                silence=args.silence)
        app.mainloop()
        return 0


if __name__ == "__main__":
    sys.exit(main())
