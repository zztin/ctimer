#!/usr/bin/env python

"""Tests for `ctimer` package."""

import pytest
from ctimer.model import Meta
from ctimer import ctimer
from ctimer import utils
import datetime
from datetime import date, time
from pathlib import Path


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
    """long_break_clock_count default value"""
    metadata_default = metadata_class()

    assert metadata_default.long_break_clock_count == 4


def test_metadata_long_break_clock_count_1(metadata_class):
    """assigned long_break_clock_count value with integer less than 2"""
    metadata_default = metadata_class(long_break_clock_count=1)

    assert metadata_default.long_break_clock_count == 2


def test_metadata_long_break_clock_count_2(metadata_class):
    """assigned long_break_clock_count value with non-integer less than 2"""
    metadata_default = metadata_class(long_break_clock_count=1.5)

    assert metadata_default.long_break_clock_count == 2


def test_metadata_long_break_clock_count_3(metadata_class):
    """assigned long_break_clock_count value with integer larger than 2"""
    metadata_default = metadata_class(long_break_clock_count=3)

    assert metadata_default.long_break_clock_count == 3


def test_metadata_long_break_clock_count_4(metadata_class):
    """assigned long_break_clock_count value with non-integer larger than 2

    Besides, testing downward rounding
    """
    metadata_default = metadata_class(long_break_clock_count=4.4)

    assert metadata_default.long_break_clock_count == 4


def test_metadata_long_break_clock_count_5(metadata_class):
    """assigned long_break_clock_count value with non-integer larger than 2

    Besides, testing upward rounding
    """
    metadata_default = metadata_class(long_break_clock_count=5.5)

    assert metadata_default.long_break_clock_count == 6
