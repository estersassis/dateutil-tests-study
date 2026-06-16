# Write tests for the relativedelta class here
import datetime, pytest
from src.relativedelta import *

def test_weeks_float_result():
    date = relativedelta(datetime.datetime(2026,1,10), datetime.datetime(2026,1,1))
    assert date.weeks == 1
    date = relativedelta(datetime.datetime(2026,1,25), datetime.datetime(2026,1,1))
    assert date.weeks == 3

def test_inputs_with_hours():
    date = relativedelta(None, None, 2026, 1, 7, 0, 0, 12, 40, 0, 0, 2026, 1, 7, 0, 0, 12, 20, 0, 0)
    assert date.minute == 20