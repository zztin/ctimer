"""Tests for `model` module of `ctimer` package."""

import pytest
from ctimer import utils
from ctimer import ctimer_db as db
from ctimer.model import CtimerClockModel
from ctimer.view import CtimerClockFakeView


@pytest.fixture
def fake_timer():
    db_path_debug = utils.get_cache_filepath(None, debug=True)
    db_file_debug = f"{db_path_debug}/ctimer_debug.db"
    db.create_connection(db_file_debug)
    current_clock_details= db.Clock_details()

    fake_model = CtimerClockModel(
        db_file_debug, current_clock_details, False, False, False, None
    )
    fake_timer = CtimerClockFakeView(fake_model, object())

    return fake_timer


def test_fake_timer_toggle_start_pause(fake_timer):
    assert not fake_timer.tm.clock_ticking

    fake_timer.toggle_start_pause()

    assert fake_timer.tm.clock_ticking

    fake_timer.toggle_start_pause()

    assert not fake_timer.tm.clock_ticking
