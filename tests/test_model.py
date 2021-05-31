"""Tests for `model` module of `ctimer` package."""


import pytest
import datetime
from ctimer.model import Meta
from ctimer import ctimer
from ctimer import utils
from datetime import date, time


def mock_midnight(mocker):
    mocker.patch("date.today", return_value=date(2019, 9, 8))
    mocker.patch("time.time", datetime.combine(date(2019, 9, 8)), time(23, 59, 55))
    mocker.patch(
        "db_path", utils.get_cache_filepath(arg_db=False, debug=False, mock_test=True)
    )
    mocker.patch("ONE_SECOND", 1)  # substitute 1000 with 1
    ctimer.maintk(db_file, hide=False, debug=True, silence=False)


@pytest.fixture
def metadata_class():
    return Meta


def test_metadata_default(metadata_class):
    """Test long_break_clock_count default value."""
    metadata_default = metadata_class()

    assert metadata_default.long_break_clock_count == 4


def test_metadata_long_break_clock_count_1(metadata_class):
    """Test long_break_clock_count <2 (int) round up to 2"""
    metadata_default = metadata_class(long_break_clock_count=1)

    assert metadata_default.long_break_clock_count == 2


def test_metadata_long_break_clock_count_2(metadata_class):
    """Test long_break_clock_count <2 (float) round up to 2"""
    metadata_default = metadata_class(long_break_clock_count=1.5)

    assert metadata_default.long_break_clock_count == 2


def test_metadata_long_break_clock_count_3(metadata_class):
    """Test long_break_clock_count assigned interger stay the same if > 2"""
    metadata_default = metadata_class(long_break_clock_count=3)

    assert metadata_default.long_break_clock_count == 3


def test_metadata_long_break_clock_count_4(metadata_class):
    """Assigned long_break_clock_count value with float K+ 0.5 round down.


    """
    metadata_default = metadata_class(long_break_clock_count=4.4)

    assert metadata_default.long_break_clock_count == 4


def test_metadata_long_break_clock_count_5(metadata_class):
    """Assigned long_break_clock_count value with non-integer >0.5 round up.


    """
    metadata_default = metadata_class(long_break_clock_count=5.5)

    assert metadata_default.long_break_clock_count == 6

