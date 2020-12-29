import time
import ctimer.view as cv
import ctimer.model as cm

import ctimer.ctimer_db as db


class CtimerClockController:
    def __init__(self, db_file, clock_details, hide, debug, silence, meta, master=None):

        self.master = master
        self.tm = cm.CtimerClockModel(db_file, clock_details, debug, hide, silence, meta)
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
            self.tv.show_pause_button()
            # counting down
            if self.tm.remaining_time > 0:
                self.tm.remaining_time -= 1
                self.tv.show_time(self.tm.remaining_time,
                                  self.tm.clock_details.clock_count)
            # finish counting. clock stops.
            else:
                self.tm.clock_ticking = False
                # is a ctimer clock
                if not self.tm.is_break:
                    self.tv.configure_display("Done!", self.tm.is_break)
                    self.tm.clock_details.clock_count += 1
                    self.tm.clock_details.end_clock = time.time()
                    # if end_break == end_clock :
                    # the app has been force ended during the clock. Update the break time while termination.
                    self.tm.clock_details.end_break = self.tm.clock_details.end_clock
                    # check break length
                    self.tv.voice_message("done")
                    self.tm.is_break = True
                    if self.tm.hide:
                        self.tv.bring_to_front()
                    self.tm.reached_bool, self.tm.reason = self.tv.ask_reached_goal_reason()
                    if self.tm.clock_details.clock_count % self.tm.long_break_clock_count == 0:
                        self.tm.remaining_time = self.tm.set_long_break_time
                        self.tv.voice_message("enjoy_long")
                    else:
                        self.tm.remaining_time = self.tm.set_break_time
                        self.tv.voice_message("enjoy")
                    self.tm.clock_ticking = True

                # is counting break
                else:
                    # break is over. Record break-over time.
                    if self.tm.hide:
                        self.tv.bring_to_front()
                        self.tv.not_bring_to_front()
                    if self.tm.silence:
                        self.tv.flash_window()
                    self.tv.voice_message("break_over")
                    self.tm.clock_details.end_break = time.time()
                    # TODO: Bug fix --This is reached before reason is filled. check line 134
                    db.db_add_clock_details(self.tm.db_file, self.tm.clock_details)
                    self.tm.is_break = False
                    self.tm.remaining_time = self.tm.set_time
                    self.tv.configure_display("Break is over!", self.tm.is_break)
                    self.tv.show_start_button()
                    self.tm.clock_ticking = False

        self.master.after(1000, self.countdown)
