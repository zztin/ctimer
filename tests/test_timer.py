"""Tests for `model` module of `ctimer` package."""

import pytest
from ctimer import utils
from ctimer import ctimer_db as db
from ctimer.model import CtimerClockModel
from ctimer.view import CtimerClockFakeView


@pytest.fixture
def fake_timer():
    db_path_debug = utils.get_cache_filepath(None, debug=True)
    db_file_debug = f"{db_path_debug}/ctimer_debug_2021.db"
    db.create_connection(db_file_debug)
    current_clock_details = db.Clock_details(db_file_debug)

    fake_model = CtimerClockModel(
        db_file_debug, current_clock_details, False, False, False, None
    )
    fake_timer = CtimerClockFakeView(fake_model, object())

    return fake_timer


def test_fake_timer_new_clock(fake_timer):
    """
    New launched clock status.
    """
    assert fake_timer.tm.fresh_new
    assert not fake_timer.tm.clock_details.is_break
    assert not fake_timer.tm.clock_details.is_complete


def test_fake_timer_toggle_start_pause(fake_timer):
    """
    Toggle start pause button affects ticking status
    """
    assert not fake_timer.tm.clock_ticking

    fake_timer.toggle_start_pause()

    assert fake_timer.tm.clock_ticking

    fake_timer.toggle_start_pause()

    assert not fake_timer.tm.clock_ticking


def test_fake_timer_countdown(fake_timer):
    """
    A counting down ctimer would stay as not is_break after start / pause / start / pause cycle as long as
    timer countdown hasn't reached.
    """
    assert not fake_timer.tm.clock_ticking

    fake_timer.toggle_start_pause()
    assert fake_timer.tm.clock_ticking
    assert not fake_timer.tm.clock_details.is_break

    fake_timer.toggle_start_pause()
    assert not fake_timer.tm.clock_ticking
    assert not fake_timer.tm.clock_details.is_break


def test_fake_timer_terminate(fake_timer):
    """
    A counting down ctimer would stop ticking after terminate, and reset

    1. The remaining time will become set time.
    2. Start/Pause Button text show "Start"
    3. is_break == False
    """
    assert not fake_timer.tm.clock_ticking

    fake_timer.toggle_start_pause()
    assert fake_timer.tm.clock_ticking
    assert not fake_timer.tm.clock_details.is_break

    fake_timer.terminate()
    assert not fake_timer.tm.clock_ticking
    assert not fake_timer.tm.clock_details.is_break
