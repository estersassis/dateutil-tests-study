# Write tests for the relativedelta class here
import datetime, pytest
from src.relativedelta import *

def test_weeks_float_result():
    date = relativedelta(datetime.datetime(2026,1,10), datetime.datetime(2026,1,1))
    assert date.weeks == 1
    date = relativedelta(datetime.datetime(2026,1,28), datetime.datetime(2026,1,14))
    assert date.weeks == 2

def test_inputs_with_hours():
    date = relativedelta(datetime.datetime(2026,1,7,12,20), datetime.datetime(2026,1,7,12,40))
    assert date.minute == 20