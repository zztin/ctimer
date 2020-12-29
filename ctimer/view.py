import tkinter as tk
import shlex
import subprocess
import time
from tkinter import simpledialog
from tkinter import messagebox as mbox
import ctimer.ctimer_db as db


class CtimerClockView(tk.Frame):
    def __init__(self, timer_model, master):
        super().__init__(master)

        labels = [
            tk.Label(self, text="", height=2),
            tk.Label(self, height=1, width=15, textvariable=""),
            tk.Label(self, height=1, width=10, textvariable=""),
            tk.Label(self, height=1, width=10, textvariable=""),
            tk.Label(self, height=3, width=10, font=("Arial", 30), textvariable="")
        ]

        buttons = [
            tk.Button(self,
                      text="Start",
                      fg="Green",
                      width=8,
                      height=4,
                      command=self.start_pause),
            tk.Button(self,
                      fg="Dark Red",
                      activebackground="Dark Red",
                      text="Stop",
                      width=8,
                      height=4,
                      command=self.terminate)
        ]

        self.master = master
        self.tm = timer_model
        master.title(self.tm.title)
        if self.tm.debug:
            self.voice_message("Welcome_debug")
        else:
            self.voice_message("Welcome")
        self.data = self.tm.data

        self._start_pause_button = buttons[0]
        self._stop_button = buttons[1]

        self.goal_show_label = labels[0]
        self.total_clock_counts = labels[1]
        self.total_clock_aim = labels[2]
        self.date = labels[3]
        self._display = labels[4]

        self.create_widgets()
        self.total_clock_counts.config(text=f"Done: {self.tm.clock_details.clock_count}")

    def bring_to_front(self):
        self.master.attributes('-topmost', 1)

    def not_bring_to_front(self):
        self.master.attributes('-topmost', 0)

    def create_widgets(self):
        self._display.config(text="Click start!")
        # self._display.config(text=self.set_time_print)
        self.date.config(text=self.tm.clock_details.date)
        self.total_clock_aim.config(text=f"Aim: {self.data.aim_clock_count}")
        self.total_clock_counts.config(text=f"Done: ...Loading...")
        self.date.grid(row=0, column=0, columnspan=2)
        self.total_clock_aim.grid(row=1, column=0, columnspan=2)
        self.total_clock_counts.grid(row=2, column=0, columnspan=2)
        self._display.grid(row=3, column=0, columnspan=2)
        self._start_pause_button.grid(row=5, column=0)
        self._stop_button.grid(row=5, column=1)
        self.goal_show_label.grid(row=6, column=0, columnspan=2)

        self.pack()

    def show_time(self, time_text, total_clock_counts):
        self._display.config(text=time_print(time_text))
        self.total_clock_counts.config(text=f"Total clocks: {total_clock_counts}")

    def show_pause_button(self):
        self._start_pause_button['text'] = "Pause"
        self._start_pause_button['fg'] = "Red"

    def show_start_button(self):
        self._start_pause_button['text'] = "Start"
        self._start_pause_button['fg'] = "Green"
        self._display['fg'] = "Black"

    def configure_display(self, text, is_break):
        """
        configure the count down timer display
        """
        self._display.config(text=text)
        if is_break:
            self._display['fg'] = "Green"
        else:
            self._display['fg'] = "Black"

    def get_goal(self):
        # TODO: get all goals for all clocks for the day
        self.tm.clock_details.task_description = simpledialog.askstring(title="Set your goals",
                                                                        prompt="What's your goal for this clock:")
        self.goal_show_label["text"] = f"Goal: {self.tm.clock_details.task_description}"

    def ask_reached_goal_reason(self):
        reason = "N.A."
        reached_bool = mbox.askyesno("Goal reached?",
                                     "Did you reach your goal?",
                                     parent=self)

        if reached_bool is False:
            reason = simpledialog.askstring("Goal reached description",
                                            "What happened? "
                                            "What was a suprise? \n"
                                            "What needs to modify to "
                                            "have a realistic goal? ",
                                            parent=self)
        return reached_bool, reason

    def voice_message(self, message_type):
        message = ""
        if not self.tm.silence:
            if message_type == "done":
                if self.tm.clock_details.clock_count == 1:
                    message = f"Beebeebeebee beebee. Done. You have achieved 1 clock today. " \
                              f"Did you reach your goal?"
                elif self.tm.clock_details.clock_count % self.data.long_break_clock_count == 0:
                    message = f"Beebeebeebee. Hooray. You achieved {self.tm.clock_details.clock_count} clocks " \
                              f"already. " \
                              f"Did you finish your goal?."
                else:
                    message = f"Beebeebeebee beebee. Done. You have achieved {self.tm.clock_details.clock_count} " \
                              f"clocks today. Did you reach your goal?"
            elif message_type == "start":
                # TODO: if starting a new clock, new message: ready? set your goal
                message = "ready? Start."
            elif message_type == "pause":
                message = "Pause"
            elif message_type == "stop":
                message = "Stop and recharge"
            elif message_type == "break_over":
                message = "Times up. Click start to start a new clock!"
            elif message_type == "enjoy":
                message = "Thanks! Enjoy your break!"
            elif message_type == "enjoy_long":
                message = "Thanks! Enjoy your long break!"
            elif message_type == "Welcome":
                message = "Welcome."
            elif message_type == "Welcome_debug":
                message = "Welcome to debug mode."
            command = shlex.split(f"say {message}")
            subprocess.run(command)

    def start_pause(self):
        # is paused: start clock
        if not self.tm.clock_ticking:
            if self.tm.remaining_time == self.tm.set_time:
                self.voice_message("start")
                self.tm.clock_details_sanity_check()
                self.date.config(text=self.tm.clock_details.date)
                self.tm.get_new_clock_entry()
                self.tm.clock_details.start_clock = time.time()
                self.get_goal()
            self.tm.clock_details.start_clock = time.time()
            self._start_pause_button['text'] = "Pause"
            self._start_pause_button['fg'] = "Red"
            self.tm.clock_ticking = True
        # is ticking: pause clock
        else:
            self.voice_message("pause")
            self._start_pause_button['text'] = "Start"
            self._start_pause_button['fg'] = "Green"
            self.tm.clock_ticking = False

    # premature terminate clock
    def terminate(self):
        self._start_pause_button['text'] = "Start"
        self._start_pause_button['fg'] = "Green"
        self._display['fg'] = "Black"
        self.tm.is_break = False
        self.tm.clock_ticking = False
        db.safe_closing_data_entry(self.tm.db_file, self.tm.clock_details)
        self.tm.remaining_time = self.tm.set_time
        # # this clock is shorter than 25 mins
        # self.clock_details.end_clock = time.time()
        self._display.config(text="Click start!")
        self.voice_message("stop")

    def flash_window(self, flashing_seconds=5):
        # check flashing_button.py
        pass


def time_print(timepoint):
    mins, secs = divmod(timepoint, 60)
    print_time = '{:02d}:{:02d}'.format(mins, secs)
    return print_time
