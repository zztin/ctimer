import time
import datetime
import ctimer.view as cv
import ctimer.model as cm
import ctimer.ctimer_db as db
import ctimer.utils as utils

ONE_SECOND = 1000


class CtimerClockController:
    def __init__(self, db_file, clock_details, hide, debug, silence, meta, master=None):

        self.master = master
        self.tm = cm.CtimerClockModel(
            db_file, clock_details, debug, hide, silence, meta
        )
        self.tv = cv.CtimerClockView(self.tm, master)

    def countdown(self):
        """
        Countdown the clock

        This function is a callback of tk so the controller could tell the viewer what to do next according to the
        content of model.

        3 flags decide the counting-down status in order:
            clock_ticking
            remaining_time
            is_break
        """
        # clock is running (either focus time or break)
        if self.tm.clock_ticking:
            self.tm.fresh_new = False
            self.tv.show_pause_button()
            # counting down
            if self.tm.remaining_time > 0:
                self.tm.remaining_time -= 1
                self.tv.countdown_display(utils.time_print(self.tm.remaining_time), self.tm.clock_details.is_break)
            # finish counting. clock stops.
            else:
                self.tm.clock_ticking = False
                # is a ctimer clock
                if not self.tm.clock_details.is_break:
                    timestamp = time.time()
                    self.tm.clock_details.end_clock = timestamp
                    self.tm.check_complete()
                    self.tm.clock_details.clock_count += 1
                    self.tv.countdown_display("Done!", self.tm.clock_details.is_break)
                    self.tv.show_clock_count(self.tm.clock_details.clock_count)
                    self.tv.show_latest_pomodoro_completed_timestamp(
                        datetime.datetime.fromtimestamp(timestamp).strftime("%H:%M:%S"))
                    # TODO: if end_break == end_clock :
                    # the app has been force ended during the clock. Update the break time while termination.
                    # check break length
                    self.tv.playback_voice_message("done")
                    if self.tm.hide:
                        self.tv.set_bring_to_front()
                    self.tm.clock_details.reached_bool, self.tm.clock_details.reason = self.tv.ask_reached_goal_reason()

                    db.db_add_clock_details(self.tm.db_file, self.tm.clock_details)
                    if (
                        self.tm.clock_details.clock_count
                        % self.tm.long_break_clock_count
                        == 0
                    ):
                        self.tm.remaining_time = self.tm.set_long_break_time
                        self.tv.playback_voice_message("enjoy_long")
                    else:
                        self.tm.remaining_time = self.tm.set_break_time
                        self.tv.playback_voice_message("enjoy")
                    self.tm.clock_ticking = True
                    self.tm.clock_details.is_break = True

                # is counting break
                else:
                    # break is over. Record break-over time.
                    if self.tm.hide:
                        self.tv.set_bring_to_front()
                        self.tv.set_not_bring_to_front()
                    if self.tm.silence:
                        self.tv.flash_window()
                    self.tv.playback_voice_message("break_over")
                    self.tm.clock_details.end_clock = time.time()
                    db.db_add_clock_details(self.tm.db_file, self.tm.clock_details)
                    self.tm.clock_details.get_new_clock_entry()
                    self.tm.remaining_time = self.tm.set_time
                    self.tm.fresh_new = True
                    self.tv.countdown_display("Click start!", self.tm.clock_details.is_break)
                    self.tv.show_start_button()
                    self.tm.clock_ticking = False
                    self.tm.clock_details.is_break = False

        self.master.after(ONE_SECOND, self.countdown)
