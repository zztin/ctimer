"""Console script for concentratetimer."""
from concentratetimer import concentratetimer
import tkinter as tk
import sys


def main():
    root = tk.Tk()
    app = concentratetimer.ConcentrateTimer(master=root)
    app.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
