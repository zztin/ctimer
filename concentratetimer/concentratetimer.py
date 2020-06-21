import shlex, subprocess
import time
from datetime import date
import tkinter as tk
from tkinter import simpledialog
# TODO: check software licences
# This code is an implementation upon the pomodoro technique from Cirillo, Francesco. If there is any ablation toward
# their copyright, it is not our intention.
# TODO: check pomodoro trademark guidelines
# https://francescocirillo.com/pages/pomodoro-trademark-guidelines

def time_print(time):
    mins, secs = divmod(time, 60)
    print_time = '{:02d}:{:02d}'.format(mins, secs)
    return print_time


class ConcentrateTimer(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.title("Pomodoro Timer")
        self.test_volume()
        #self.data = Meta(set_time=2, break_time=2, long_break_time=5, long_break_clock_count=2)
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
        self.create_widgets()
        self.goal = None

    def create_widgets(self):
        self.display = tk.Label(self, height=3, width=10, font=("Arial", 30), textvariable="")
        self.display.config(text=self.set_time_print)
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
        self.date.config(text=f"{date.today()}")
        self.total_clock_aim = tk.Label(self, height=1, width=10, textvariable="")
        self.total_clock_aim.config(text=f"Aim: {self.data.aim_clock_count}")
        self.total_clock_counts = tk.Label(self, height=1, width=15, textvariable="")
        self.total_clock_counts.config(text=f"Done: {self.data.total_clock_count}")
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
        self.goal = simpledialog.askstring(title="Set your goals",
                                      prompt="What's your goal for this clock:")
        self.goal_show_label["text"] = f"Goal: {self.goal}"

    def countdown(self):
        if self.clock_ticking:
            self.remaining_time -= 1
            if self.remaining_time > 0:
                self.display.config(text=time_print(self.remaining_time))
            else:
                self.remaining_time = 0
                # TODO: self.display.config updates appears after the voice_messages (os.subprocess("say ..."))
                # TODO: 00:00 does not show.
                if self.is_break == False:
                    self.display.config(text="Done!")
                    self.data.total_clock_count += 1
                    self.total_clock_counts.config(text=f"Total clocks: {self.data.total_clock_count}")
                    if self.data.total_clock_count % self.long_break_clock_count == 0:
                        self.remaining_time = self.set_long_break_time
                    else:
                        self.remaining_time = self.set_break_time
                    self.voice_message("done")
                    self.is_break = True
                    self.display['fg'] = "Green"
                else:
                    self.voice_message("break_over")
                    self.is_break = False
                    self.remaining_time = self.set_time
                    self.display.config(text=time_print(self.set_time))
                    self.start_pause_button['text'] = "Start"
                    self.start_pause_button['fg'] = "Green"
                    self.display['fg'] = "Black"
                    self.clock_ticking = False

            self.master.after(1000, self.countdown) # after: call this function in 1000 ms = 1 s. Recursive.

    def voice_message(self, message_type):
        if message_type == "done":
            if self.data.total_clock_count == 1:
                message = f"Beebeebeebee beebee. Done. You have achieved 1 clock today. " \
                          f"Enjoy your break!"
            elif self.data.total_clock_count % self.data.long_break_clock_count == 0:
                message = f"Beebeebeebee. Hooray. You achieved {self.data.total_clock_count} clocks already. " \
                          f"Enjoy your long break."
            else:
                message = f"Beebeebeebee beebee. Done. You have achieved {self.data.total_clock_count} " \
                          f"clocks today. Enjoy your break."
        elif message_type == "start":
            message = "ready? set your goal."
        elif message_type == "pause":
            message = "Pause"
        elif message_type == "stop":
            message = "Stop and recharge"
        elif message_type == "break_over":
            message = "Times up"
        command = shlex.split(f"say {message}")
        subprocess.run(command)

    def start_pause(self):
        # start clock
        if self.clock_ticking == False:
            self.voice_message("start")
            if self.remaining_time == self.set_time:
                self.get_goal()
            self.data.start_time_first_clock = time.time()
            self.data.start_time_this_clock = time.time()
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
        self.display['fg'] = "Black"
        self.clock_ticking = False
        self.remaining_time = self.set_time
        #self.display.config(text="00:00")
        self.display.config(text=self.set_time_print)
        self.voice_message("stop")

    def test_volume(self):
        message = "Welcome"
        print(message)
        command = shlex.split(f"say {message}")
        subprocess.run(command)
        print("Did you hear something? \n"
              "If not, check your volume and sound system. \n"
              "This is essential for getting notice from pomodoro when time's up. \n"
              "Also, find PomodroTimer GUI window somewhere and interact there. :)")


class Meta():
    def __init__(self, start_time_first_clock=None,
                 start_time_this_clock=None,
                 remaining_time=None,
                 total_clock_count=0,
                 aim_clock_count=8,
                 set_time=25*60,
                 break_time=5*60,
                 long_break_time=15*60,
                 long_break_clock_count=4):
        '''

        :param start_time_first_clock: start time of the first clock of the day.
        :param start_time_this_clock: start time of the current clock
        :param remaining_time: remaining time of the current clock
        :param total_clock_count: achieved clock count while initializing the app
        :param aim_clock_count: aim for a day (8 clocks)
        :param set_time: the interval of a pomodoro clock (25 mins)
        :param break_time: the interval of a normal break (5 mins)
        :param long_break_time: the interval of a long break (15 mins)
        :param long_break_clock_count: when achieved n clocks, a long break is given (4 clocks, at least 2.)
        '''
        self.start_time_first_clock = start_time_first_clock
        self.start_time_this_clock = start_time_this_clock
        self.total_clock_count = int(round(total_clock_count)) # should not be access via outside unless special cases
        self.aim_clock_count = int(round(aim_clock_count))
        self.set_time = int(round(set_time))
        self.remaining_time = remaining_time # Deprecated (used below)
        self.break_time= int(round(break_time))
        self.long_break_time = int(round(long_break_time))
        if long_break_clock_count < 2:
            self.long_break_clock_count = 2
        else:
            self.long_break_clock_count = int(round(long_break_clock_count))



    # Deprecated
    def pomodoro_loop(self):
        while True:
            self.countdown(self)
            self.total_clock_count += 1
            print("Done! Next clock starting")

    # Deprecated
    def countdown(self):
        while self.remaining_time:
            print(time_print(self.remaining_time), end='\r')
            time.sleep(1)
            self.remaining_time -= 1


