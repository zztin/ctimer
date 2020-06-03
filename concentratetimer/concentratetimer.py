import shlex, subprocess
import time
import tkinter as tk
# TODO: check software licences
# This code is an implementation upon the pomodoro technique from Cirillo, Francesco. If there is any ablation toward
# their copyright, it is not our intention.
# TODO: check pomodoro trademark guidelines
# https://francescocirillo.com/pages/pomodoro-trademark-guidelines
# reference links
# 1. stackoverflow: https://stackoverflow.com/questions/47824017/starting-and-pausing-with-a-countdown-timer-in-tkinter
# 2. stackexchange: https://apple.stackexchange.com/questions/3454/say-in-different-language
# 3. tkinter tutorial


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
#        self.pomodoro = PomodoroData(set_time=8, break_time=3)
        self.data = Meta()
        self.clock_ticking = False
        self.is_break = False
        self.set_time = self.data.set_time
        self.set_time_print = time_print(self.set_time)
        self.set_break_time = self.data.break_time
        self.remaining_time = self.set_time
        self.pack()
        self.create_widgets()

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
        self.total_clock_aim = tk.Label(self, height=1, width=10, textvariable="")
        self.total_clock_aim.config(text=f"Aim: {self.data.aim_clock_count}")
        self.total_clock_counts = tk.Label(self, height=1, width=10, textvariable="")
        self.total_clock_counts.config(text=f"Done: {self.data.total_clock_count}")
        self.total_clock_aim.grid(row=0, column=0, columnspan=2)
        self.total_clock_counts.grid(row=1, column=0, columnspan=2)
        self.display.grid(row=2, column=0, columnspan=2)
        self.start_pause_button.grid(row=3, column=0)
        self.stop_button.grid(row=3, column=1)

    def countdown(self):
        if self.clock_ticking:
            self.remaining_time -= 1
            if self.remaining_time > 0:
                self.display.config(text=time_print(self.remaining_time))
            else:
                self.remaining_time = 0
                # TODO: this Done! appears after the voice...
                # TODO: Sometimes 00:00 does not show.

                if self.is_break == False:
                    self.display.config(text="Done!")
                    self.data.total_clock_count += 1
                    self.total_clock_counts.config(text=f"Total clocks: {self.data.total_clock_count}")
                    self.voice_message("done")
                    self.remaining_time = self.set_break_time
                    self.is_break = True
                    self.display['fg'] = "Green"
                else:
                    self.voice_message("break_over")
                    self.is_break = False
                    self.remaining_time = self.set_time
                    self.display.config(text=time_print(self.remaining_time))
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
            else:
                message = f"Beebeebeebee beebee. Done. You have achieved {self.data.total_clock_count} " \
                          f"clocks today. Enjoy your break!"
        elif message_type == "start":
            message = "ready? go"
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
                 break_time=5*60):
        self.start_time_first_clock = start_time_first_clock
        self.start_time_this_clock = start_time_this_clock
        self.remaining_time = remaining_time
        self.total_clock_count = total_clock_count # should not be access via outside unless special cases
        self.aim_clock_count = aim_clock_count
        self.set_time = set_time
        self.break_time= break_time

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


