from datetime import date
import ctimer.ctimer_db as db
import ctimer.utils as utils


class CtimerClockModel:
    """
    Ctimer data model
    """
    def __init__(
        self,
        db_file=None,
        clock_details=None,
        debug=False,
        hide=False,
        silence=False,
        meta=None,
    ):
        #############################
        # none-clock flags/attributes
        #############################
        # cli flags/attributes
        self.debug = debug
        self.db_file = db_file
        # GUI window flags/attributes
        if debug:
            self.title = "Debug mode"
        else:
            self.title = "Ctimer"
        self.hide = hide
        self.silence = silence
        ########################
        # clock flags/attributes
        ########################
        self.meta = meta
        if debug:
            self.data = Meta(
                set_time=5, break_time=5, long_break_time=7, long_break_clock_count=2
            )
        elif self.meta is None:
            self.data = Meta()
        else:
            self.data = self.meta

        self.clock_ticking = False
        self.fresh_new = True
        self.set_time = self.data.set_time
        self.set_time_print = utils.time_print(self.set_time)
        self.set_break_time = self.data.break_time
        self.set_long_break_time = self.data.long_break_time
        self.remaining_time = self.set_time
        self.long_break_clock_count = self.data.long_break_clock_count
        self.clock_details = clock_details
        # get new clock entry
        self.clock_details.get_new_clock_entry()
        self.clock_details.date = f"{date.today()}"
        self.clock_details.clock_count = db.get_clock_count(self.db_file)
        self.goal = None

    def check_complete(self):
        """
        Definition of complete: no pause during the clock. If terminate the clock earlier, it could still be a
        complete clock.
        """
        if self.clock_details.pause_toggled:
            self.clock_details.is_complete = False
        else:
            self.clock_details.is_complete = True



class Meta:
    def __init__(
        self,
        aim_clock_count=8,
        set_time=25 * 60,
        break_time=5 * 60,
        long_break_time=15 * 60,
        long_break_clock_count=4,
    ):
        """
        :param remaining_time: remaining time of the current clock
        :param aim_clock_count: aim for a day (8 clocks)
        :param set_time: the interval of a pomodoro clock (25 mins)
        :param break_time: the interval of a normal break (5 mins)
        :param long_break_time: the interval of a long break (15 mins)
        :param long_break_clock_count: when achieved n clocks, a long break is given (4 clocks, at least 2.)
        """
        self.aim_clock_count = int(round(aim_clock_count))
        self.set_time = int(round(set_time))
        self.break_time = int(round(break_time))
        self.long_break_time = int(round(long_break_time))
        if long_break_clock_count < 2:
            self.long_break_clock_count = 2
        else:
            self.long_break_clock_count = int(round(long_break_clock_count))
