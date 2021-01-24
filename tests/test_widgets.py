"""Tests for `model` module of `ctimer` package."""

import pytest
import tkinter as tk
from unittest.mock import MagicMock
from unittest.mock import patch
from ctimer import utils
from ctimer import ctimer_db as db
from ctimer.controller import CtimerClockController
from ctimer.view import CtimerClockView
from ctimer.model import CtimerClockModel


@pytest.fixture
def controller():
    print("Setup debugging-controller for testing.")
    db_path_debug = utils.get_cache_filepath(None, debug=True)
    db_file_debug = f"{db_path_debug}/ctimer_debug_2021.db"
    db.create_connection(db_file_debug)
    current_clock_details = db.Clock_details()

    tk_root = tk.Tk()
    tk_root.wait_visibility()
    ccc = CtimerClockController(
        db_file_debug, current_clock_details, False, True, True, None, tk_root
    )

    yield ccc

    print("Teardown the debugging-controller for testing...")
    ccc.master.destroy()
    print("Teardown the debugging-controller for testing. Done.")


def test_init(controller):
    tv = controller.tv
    tm = controller.tm

    assert type(tv) is CtimerClockView
    assert type(tm) is CtimerClockModel

    assert tm.clock_details.reached_bool == "Not Updated"
    assert tm.clock_details.reason == "N.A."


def test_click_start_reached_one_clock(controller):
    expected_goal_string = "test_click_start fake goal for testing"
    tv = controller.tv
    tm = controller.tm

    assert not controller.tm.clock_ticking

    with \
            patch('ctimer.view.simpledialog.askstring', MagicMock(return_value=expected_goal_string)), \
            patch('ctimer.view.CtimerClockView.ask_reached_goal_reason',
                  MagicMock(return_value=(True, "Fake reached reason"))):
        tv._button_start_pause.invoke()
        controller.master.update()

        assert tm.remaining_time > 1
        one_clock_time = tm.remaining_time

        assert tm.clock_details.task_description == expected_goal_string
        assert controller.tm.clock_ticking

        for ticking in range(one_clock_time - 1):
            controller.countdown()

        controller.master.update()
        assert tm.remaining_time == 1

        controller.countdown()
        controller.master.update()
        assert tm.remaining_time == 0

        controller.countdown()
        controller.master.update()
        assert tm.clock_details.reached_bool
        assert tm.clock_details.reason == "Fake reached reason"
