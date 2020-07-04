"""Console script for concentratetimer."""
from concentratetimer import concentratetimer
import tkinter as tk
import concentratetimer.ctimer_db as db

import sys


def main():
    db_file = './data/ctimer.db'
    db.create_connection(db_file) # create if not exist
    root = tk.Tk()
    app = concentratetimer.ConcentrateTimer(master=root, db_file=db_file)
    app.mainloop()


    return 0


if __name__ == "__main__":
    sys.exit(main())
