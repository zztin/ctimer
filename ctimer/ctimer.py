import tkinter as tk
from tkinter import messagebox as mbox
import ctimer.ctimer_db as db
import ctimer.controller as cc


def maintk(db_file, hide=False, debug=False, silence=False, meta=None):
    root = tk.Tk()

    def on_closing():
        if mbox.askokcancel("Quit", "Do you want to quit?"):
            db.safe_closing_data_entry(db_file, current_clock_details)
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    if hide is False:
        root.attributes("-topmost", True)
    current_clock_details = db.Clock_details()
    ccc = cc.CtimerClockController(db_file,
                                   current_clock_details,
                                   hide,
                                   debug,
                                   silence,
                                   meta,
                                   root)

    ccc.countdown()

    root.mainloop()
    return 0






