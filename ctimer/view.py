import tkinter as tk
import shlex
import subprocess
import time
from tkinter import simpledialog
from tkinter import messagebox as mbox
import ctimer.ctimer_db as db


class CtimerClockViewBase:
    def get_button_start_pause(self):
        """
        Abstract method of updating the button provided by GUI framework
        """
        raise NotImplementedError

    def get_button_stop(self):
        """
        Abstract method of updating the button provided by GUI framework
        """
        raise NotImplementedError

    def update_label_goal_show(self):
        """
        Abstract method of updating the label provided by GUI framework
        """
        raise NotImplementedError

    def update_label_total_clock_counts(self):
        """
        Abstract method of updating the label provided by GUI framework
        """
        raise NotImplementedError

    def update_label_total_clock_aim(self):
        """
        Abstract method of updating the label provided by GUI framework
        """
        raise NotImplementedError

    def config_label_date(self, text="NA"):
        """
        Abstract method to config the date label provided by GUI framework
        """
        raise NotImplementedError

    def update_label_display(self):
        """
        Abstract method of updating the label provided by GUI framework
        """
        raise NotImplementedError

    def set_bring_to_front(self):
        """
        Abstract method of setting bring_to_front flag
        """
        raise NotImplementedError

    def set_not_bring_to_front(self):
        """
        Abstract method of setting not_bring_to_front flag
        """
        raise NotImplementedError

    def create_widgets(self):
        """
        Abstract method of creating widgest of GUI window
        """
        raise NotImplementedError

    def show_clock_count(self, total_clock_counts: str) -> None:
        """
        Abstract method of showing time_text and total_clock_counts with labels

        :param total_clock_counts: the total clock counts you want to show
        """
        raise NotImplementedError

    def show_pause_button(self):
        """
        Abstract method to render the pause button

        :return: None
        """
        raise NotImplementedError

    def show_start_button(self):
        """
        Abstract method to render the start button
        :return: None
        """
        raise NotImplementedError

    def countdown_display(self, text, is_break):
        """
        Configure the count down timer display

        :param text: text we want to display
        :param is_break: if the counting status is in the break slot
        :return: None
        """
        raise NotImplementedError

    def ask_reached_goal_reason(self):
        """
        Ask users about the reason if they reached their goals

        Ask users via GUI, return a tuple (boolean yes/no, reason in string text)
        :return: tuple
        """
        raise NotImplementedError

    def playback_voice_message(self, message_type):
        """
        Playback voice message according to message types

        By default the message is played by the say tool

        :param message_type: message type in string
        :return: None
        """
        raise NotImplementedError

    def toggle_start_pause(self):
        """
        Toggle between start and pauce status of the clock

        :return: None
        """
        raise NotImplementedError

    def terminate(self):
        """
        Prematurely terminate clocks

        Apply the corresponding when terminate clocks permaturely. This method is uaully used by interrupting a
        ticking clock.

        :return: None
        """
        raise NotImplementedError

    def flash_window(self, flashing_seconds=5):
        """
        Falsh the window

        :param flashing_seconds: how long the window will be flashing
        :return:
        """
        raise NotImplementedError


class CtimerClockView(tk.Frame, CtimerClockViewBase):
    def __init__(self, timer_model, master):
        super().__init__(master)

        labels = [
            tk.Label(self, text="", height=2),
            tk.Label(self, height=1, width=15, textvariable=""),
            tk.Label(self, height=1, width=10, textvariable=""),
            tk.Label(self, height=1, width=10, textvariable=""),
            tk.Label(self, height=3, width=10, font=("Arial", 30), textvariable=""),
        ]

        buttons = [
            tk.Button(
                self,
                text="Start",
                fg="Green",
                width=8,
                height=4,
                command=self.toggle_start_pause,
            ),
            tk.Button(
                self,
                fg="Dark Red",
                activebackground="Dark Red",
                text="Stop",
                width=8,
                height=4,
                command=self.terminate,
            ),
        ]

        self.master = master
        self.tm = timer_model
        master.title(self.tm.title)
        if self.tm.debug:
            self.playback_voice_message("Welcome_debug")
        else:
            self.playback_voice_message("Welcome")
        self.data = self.tm.data

        self._button_start_pause = buttons[0]
        self._button_stop = buttons[1]

        self._label_goal_show = labels[0]
        self._label_total_clock_counts = labels[1]
        self._label_total_clock_aim = labels[2]
        self._label_date = labels[3]
        self._label_display = labels[4]
        self.create_widgets()
        self._label_total_clock_counts.config(
            text=f"Done: {self.tm.clock_details.clock_count}"
        )

    def get_button_start_pause(self):
        return self._button_start_pause

    def config_label_date(self, text="NA"):
        self._label_date.config(text=text)

    def set_bring_to_front(self):
        self.master.attributes("-topmost", 1)

    def set_not_bring_to_front(self):
        self.master.attributes("-topmost", 0)

    def create_widgets(self):
        self.countdown_display("Click start!", self.tm.clock_details.is_break)
        # self._label_display.config(text=self.set_time_print)
        self._label_date.config(text=self.tm.clock_details.date)
        self._label_total_clock_aim.config(text=f"Aim: {self.data.aim_clock_count}")
        self._label_total_clock_counts.config(text=f"Done: ...Loading...")
        self._label_date.grid(row=0, column=0, columnspan=2)
        self._label_total_clock_aim.grid(row=1, column=0, columnspan=2)
        self._label_total_clock_counts.grid(row=2, column=0, columnspan=2)
        self._label_display.grid(row=3, column=0, columnspan=2)
        self._button_start_pause.grid(row=5, column=0)
        self._button_stop.grid(row=5, column=1)
        self._label_goal_show.grid(row=6, column=0, columnspan=2)

        self.pack()

    def show_clock_count(self, total_clock_counts):
        self._label_total_clock_counts.config(
            text=f"Total clocks: {total_clock_counts}"
        )

    def show_pause_button(self):
        self._button_start_pause["text"] = "Pause"
        self._button_start_pause["fg"] = "Red"

    def show_start_button(self):
        self._button_start_pause["text"] = "Start"
        self._button_start_pause["fg"] = "Green"
        self._label_display["fg"] = "Black"

    def countdown_display(self, text, is_break):
        if is_break:
            self._label_display["fg"] = "Green"
        else:
            self._label_display["fg"] = "Black"
        self._label_display.config(text=text)

    def get_goal(self):
        # TODO: get all goals for all clocks for the day
        self.tm.clock_details.task_description = simpledialog.askstring(
            title="Set your goals", prompt="What's your goal for this clock:"
        )
        self._label_goal_show[
            "text"
        ] = f"Goal: {self.tm.clock_details.task_description}"

    def ask_reached_goal_reason(self):
        reason = "N.A."
        reached_bool = mbox.askyesno(
            "Goal reached?", "Did you reach your goal?", parent=self
        )

        if reached_bool is False:
            reason = simpledialog.askstring(
                "Goal reached description",
                "What happened? "
                "What was a suprise? \n"
                "What needs to modify to "
                "have a realistic goal? ",
                parent=self,
            )
        else:
            reason = simpledialog.askstring(
                "Goal reached description",
                "Congratulations! "
                "How did you make it?",
                parent=self,
            )

        return reached_bool, reason

    def playback_voice_message(self, message_type):
        message = ""
        if not self.tm.silence:
            if message_type == "done":
                if self.tm.clock_details.clock_count == 1:
                    message = (
                        f"Beebeebeebee beebee. Done. You have achieved 1 clock today. "
                        f"Did you reach your goal?"
                    )
                elif (
                    self.tm.clock_details.clock_count % self.data.long_break_clock_count
                    == 0
                ):
                    message = (
                        f"Beebeebeebee. Hooray. You achieved {self.tm.clock_details.clock_count} clocks "
                        f"already. "
                        f"Did you finish your goal?."
                    )
                else:
                    message = (
                        f"Beebeebeebee beebee. Done. You have achieved {self.tm.clock_details.clock_count} "
                        f"clocks today. Did you reach your goal?"
                    )
            elif message_type == "start":
                # TODO: if starting a new clock, new message: ready? set your goal
                message = "ready? Start."
            elif message_type == "continue":
                message = "continue"
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

    def toggle_start_pause(self):
        # is paused: start clock
        if not self.tm.clock_ticking:
            if self.tm.fresh_new:
                self.playback_voice_message("start")
                self.get_goal()
                self.config_label_date(text=self.tm.clock_details.date)
                self.tm.clock_details.start_clock = time.time()
                self.tm.fresh_new = False
            else:
                self.playback_voice_message("continue")

            self.tm.clock_details.start_clock = time.time()
            self.show_pause_button()
            self.tm.clock_ticking = True
        # is ticking: pause clock
        else:
            self.playback_voice_message("pause")
            self.tm.clock_details.pause_toggled = True
            self.tm.clock_details.end_clock = time.time()
            self.tm.clock_details.reached_bool, self.tm.clock_details.reason = False, 0
            db.db_add_clock_details(self.tm.db_file, self.tm.clock_details)
            self.show_start_button()
            self.tm.clock_ticking = False

    def terminate(self):
        self.playback_voice_message("stop")
        if not self.tm.clock_details.is_break and not self.tm.fresh_new:
            self.tm.clock_details.reached_bool, self.tm.clock_details.reason = self.ask_reached_goal_reason()
            if self.tm.clock_details.reached_bool:
                self.tm.clock_details.clock_count += 1
                self.countdown_display("Done!", self.tm.clock_details.is_break)
                self.show_clock_count(self.tm.clock_details.clock_count)
                # only if goal is reached, clock count is +1, we want to ask if it is a complete (no break) clock
                self.tm.check_complete()
        # Write to clock details even if it is terminated. (goal not reached)
        self.tm.clock_details.end_clock = time.time()
        db.db_add_clock_details(self.tm.db_file, self.tm.clock_details)
        # set to new status
        self.tm.clock_details.is_break = False
        self.tm.clock_ticking = False
        self.tm.clock_details.get_new_clock_entry()
        self.tm.remaining_time = self.tm.set_time
        self.tm.fresh_new = True
        self.countdown_display("Click start!", self.tm.clock_details.is_break)
        self.show_start_button()


    def flash_window(self, flashing_seconds=5):
        # check flashing_button.py
        pass


class CtimerClockFakeView(CtimerClockView):
    def __init__(self, timer_model, master):
        self.tm = timer_model
        # master won't be used in a fake view as it is a part of GUI framework
        self.master = master
        # GUI labels and buttons from top to bottom.
        self._label_date = None
        self._label_total_clock_aim = None
        self._label_total_clock_counts = None
        self._label_display = None
        self._button_start_pause = "Start"
        self._button_stop = "Stop"
        self._label_goal_show = None

    def config_label_date(self, text="NA"):
        self._label_date = text
        self._show_gui_window_response(f"Date label : {text}")

    def _show_gui_window_response(self, msg):
        print(f"\n[GUI response] {msg}")

    def _show_gui_start_pause_button(self, msg):
        self._show_gui_window_response(f"start/pause button: {msg}")

    @staticmethod
    def _get_fake_goal():
        return "[get goal description]"

    def set_bring_to_front(self):
        self._show_gui_window_response("is set as 'always on the top'.")

    def set_not_bring_to_front(self):
        self._show_gui_window_response("is disabled 'always on the top'.")

    def create_widgets(self):
        self.countdown_display("Click start!", self.tm.clock_details.is_break)
        self._label_date = self.tm.clock_details.date
        self._label_total_clock_aim = f"Aim: {self.data.aim_clock_count}"
        self._label_total_clock_counts = f"Done: ...Loading..."
        self._show_gui_window_response("Widgets are created and arranged by the layout.")


    def show_clock_count(self, total_clock_counts):
        self._show_gui_window_response(f"total_clock_counts: {total_clock_counts}")
        self._label_total_clock_counts = total_clock_counts

    def show_pause_button(self):
        self._show_gui_start_pause_button("text: pause, fg: red")
        self._button_start_pause = "Pause"

    def show_start_button(self):
        self._show_gui_start_pause_button("text: start, fg: green")
        self._button_start_pause = "Start"
        self._show_gui_window_response("fg: black")


    def countdown_display(self, text, is_break):
        if is_break:
            self._show_gui_window_response("fg: green")
        else:
            self._show_gui_window_response("fg: black")
        self._show_gui_window_response(text)
        self._label_display = text

    def get_goal(self):
        self.tm.clock_details.task_description = self._get_fake_goal()
        self._show_gui_window_response(f"text: Goal: {self.tm.clock_details.task_description}")
        self._label_goal_show = self.tm.clock_details.task_description
    def ask_reached_goal_reason(self):
        return True, "fake reached goal reasons"

    def playback_voice_message(self, message_type):
        self._show_gui_window_response(f"Voice: {message_type}")
