import shlex, subprocess
import time
from datetime import date
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox as mbox
import ctimer.ctimer_db as db
# This code is an implementation upon the pomodoro technique from Cirillo, Francesco. If there is any ablation toward
# their copyright, it is not our intention.

def time_print(time):
    mins, secs = divmod(time, 60)
    print_time = '{:02d}:{:02d}'.format(mins, secs)
    return print_time


class ConcentrateTimer(tk.Frame):
    def __init__(self, master=None, db_file=None, debug=False, hide=False, silence=False):
        super().__init__(master)
        self.db_file = db_file
        self.master = master
        self.hide = hide
        self.silence = silence
        master.title("Concentration Timer")
        self.test_volume(debug=debug)
        if debug:
            self.data = Meta(set_time=3, break_time=3, long_break_time=5, long_break_clock_count=2)
        else:
            self.data = Meta()
        self.clock_ticking = False
        self.is_break = False
        self.set_time = self.data.set_time
        self.set_time_print = time_print(self.set_time)
        self.set_break_time = self.data.break_time
        self.set_long_break_time = self.data.long_break_time
        self.remaining_time = self.set_time
        self.long_break_clock_count = self.data.long_break_clock_count
        self.pack()
        self.clock_details = db.Clock_details()
        self.clock_details.date = f"{date.today()}"
        self.create_widgets()
        self.goal = None
        self.clock_details = db.Clock_details()
        self.clock_details.clock_count = db.get_clock_count(self.db_file)
        self.total_clock_counts.config(text=f"Done: {self.clock_details.clock_count}")

    def bring_to_front(self):
        self.master.attributes('-topmost', 1)
    def not_bring_to_front(self):
        self.master.attributes('-topmost', 0)

    def flash_window(self, flashing_seconds=5):
        # check flasshing_button.py
        pass

    def create_widgets(self):
        self.display = tk.Label(self, height=3, width=10, font=("Arial", 30), textvariable="")
        self.display.config(text="Click start!")
        # self.display.config(text=self.set_time_print)
        self.start_pause_button = tk.Button(self,
                                            text="Start",
                                            fg="Green",
                                            width=8,
                                            height=4,
                                            command=self.start_pause)
        self.stop_button = tk.Button(self,
                                     fg="Dark Red",
                                     activebackground="Dark Red",
                                     text="Stop",
                                     width=8,
                                     height=4,
                                     command=self.terminate)
        self.date = tk.Label(self, height=1, width=10, textvariable="")
        self.date.config(text=self.clock_details.date)
        self.total_clock_aim = tk.Label(self, height=1, width=10, textvariable="")
        self.total_clock_aim.config(text=f"Aim: {self.data.aim_clock_count}")
        self.total_clock_counts = tk.Label(self, height=1, width=15, textvariable="")
        self.total_clock_counts.config(text=f"Done: ...Loading...")
        self.goal_show_label = tk.Label(self, text="", height=2)

        self.date.grid(row=0, column=0, columnspan=2)
        self.total_clock_aim.grid(row=1, column=0, columnspan=2)
        self.total_clock_counts.grid(row=2, column=0, columnspan=2)
        self.display.grid(row=3, column=0, columnspan=2)
        self.start_pause_button.grid(row=5, column=0)
        self.stop_button.grid(row=5, column=1)
        self.goal_show_label.grid(row=6, column=0, columnspan=2)

    def get_goal(self):
        # TODO: get all goals for all clocks for the day
        self.clock_details.task_description = simpledialog.askstring(title="Set your goals",
                                                                     prompt="What's your goal for this clock:")
        self.goal_show_label["text"] = f"Goal: {self.clock_details.task_description}"

    def ask_reached_goal_reason(self):
        self.clock_details.reached_bool = mbox.askyesno("Goal reached?",
                                                        "Did you reach your goal?",
                                                        parent=self)

        if self.clock_details.reached_bool is False:
            self.clock_details.reason = simpledialog.askstring("Goal reached description",
                                                               "What happened? "
                                                               "What was a suprise? \n"
                                                               "What needs to modify to "
                                                               "have a realistic goal? ",
                                                               parent=self)


    def countdown(self):
        if self.clock_ticking:
            self.remaining_time -= 1
            if self.remaining_time > 0:
                self.display.config(text=time_print(self.remaining_time))
            else:
                self.remaining_time = 0
                # Finish a clock
                if self.is_break == False:
                    self.display.config(text="Done!")
                    self.clock_details.clock_count += 1
                    self.clock_details.end_clock = time.time()
                    self.total_clock_counts.config(text=f"Total clocks: {self.clock_details.clock_count}")
                    if self.clock_details.clock_count % self.long_break_clock_count == 0:
                        self.remaining_time = self.set_long_break_time
                        long = True
                    else:
                        self.remaining_time = self.set_break_time
                        long = False
                    self.voice_message("done")
                    self.is_break = True
                    self.display['fg'] = "Green"
                    if self.hide:
                        self.bring_to_front()
                    self.ask_reached_goal_reason()
                    if long:
                        self.voice_message("enjoy_long")
                    else:
                        self.voice_message("enjoy")
                else:
                    # break is over. Record break over time.
                    if self.hide:
                        self.bring_to_front()
                        self.not_bring_to_front()
                    if self.silence:
                        self.flash_window()
                    self.voice_message("break_over")
                    self.clock_details.end_break = time.time()
                    # TODO: Bug fix --This is reached before reason is filled. check line 134
                    db.db_add_clock_details(self.db_file, self.clock_details)
                    self.is_break = False
                    self.remaining_time = self.set_time
                    self.display.config(text="Break's over!")
                    # self.display.config(text=time_print(self.set_time))
                    self.start_pause_button['text'] = "Start"
                    self.start_pause_button['fg'] = "Green"
                    self.display['fg'] = "Black"
                    self.clock_ticking = False

            self.master.after(1000, self.countdown) # after: call this function in 1000 ms = 1 s. Recursive.

    def voice_message(self, message_type):
        if self.silence:
            pass
        else:
            if message_type == "done":
                if self.clock_details.clock_count == 1:
                    message = f"Beebeebeebee beebee. Done. You have achieved 1 clock today. " \
                              f"Did you reach your goal?"
                elif self.clock_details.clock_count % self.data.long_break_clock_count == 0:
                    message = f"Beebeebeebee. Hooray. You achieved {self.clock_details.clock_count} clocks already. " \
                              f"Did you finish your goal?."
                else:
                    message = f"Beebeebeebee beebee. Done. You have achieved {self.clock_details.clock_count} " \
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
            command = shlex.split(f"say {message}")
            subprocess.run(command)

    def start_pause(self):
        if self.clock_ticking == False:
            self.voice_message("start")
            ### starting a new clock

            if self.remaining_time == self.set_time:
                if self.clock_details.date != f"{date.today()}":
                    self.clock_details.date = f"{date.today()}"
                    self.clock_details.clock_count = db.get_clock_count(self.db_file)
                self.date.config(text=self.clock_details.date)
                self.clock_details.start_clock = time.time()
                self.get_goal()
            self.clock_details.start_clock = time.time()
            self.start_pause_button['text'] = "Pause"
            self.start_pause_button['fg'] = "Red"
            self.clock_ticking = True
            self.countdown()
        # pause clock
        else:
            self.voice_message("pause")
            self.start_pause_button['text'] = "Start"
            self.start_pause_button['fg'] = "Green"
            self.clock_ticking = False
    # premature terminate clock
    def terminate(self):
        self.start_pause_button['text'] = "Start"
        self.start_pause_button['fg'] = "Green"
        self.is_break = False
        self.display['fg'] = "Black"
        self.clock_ticking = False
        self.remaining_time = self.set_time
        self.display.config(text="Click start!")
        #self.display.config(text=self.set_time_print)
        self.voice_message("stop")

    def test_volume(self, debug=False):
        if debug:
            message = "Welcome to debug mode."
        else:
            message = "Welcome"
        print(message)
        command = shlex.split(f"say {message}")
        subprocess.run(command)




class Meta():
    def __init__(self,
                 aim_clock_count=8,
                 set_time=25*60,
                 break_time=5*60,
                 long_break_time=15*60,
                 long_break_clock_count=4):
        '''
        :param remaining_time: remaining time of the current clock
        :param aim_clock_count: aim for a day (8 clocks)
        :param set_time: the interval of a pomodoro clock (25 mins)
        :param break_time: the interval of a normal break (5 mins)
        :param long_break_time: the interval of a long break (15 mins)
        :param long_break_clock_count: when achieved n clocks, a long break is given (4 clocks, at least 2.)
        '''
        self.aim_clock_count = int(round(aim_clock_count))
        self.set_time = int(round(set_time))
        self.break_time= int(round(break_time))
        self.long_break_time = int(round(long_break_time))
        if long_break_clock_count < 2:
            self.long_break_clock_count = 2
        else:
            self.long_break_clock_count = int(round(long_break_clock_count))


