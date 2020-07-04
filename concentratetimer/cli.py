"""Console script for concentratetimer."""
from concentratetimer import concentratetimer
import tkinter as tk
import concentratetimer.ctimer_db as db
import sys
from subprocess import Popen, PIPE
import os

def main():
    # can also prompt user to enter a file path to store the database, but next time when the program launch
    #  it has to find it automatically. "from tkinter import filedialog"
    path = os.path.dirname(concentratetimer.__file__).rsplit("/",1)[0]
    db_file = f"{path}/data/ctimer.db"
    db.create_connection(db_file) # create if not exist
    root = tk.Tk()
    app = concentratetimer.ConcentrateTimer(master=root, db_file=db_file)
    app.mainloop()


    return 0


if __name__ == "__main__":
    sys.exit(main())
