# Write tests for the relativedelta class here
import datetime, pytest
from src.relativedelta import *

def test_weeks_float_result():
    date = datetime.datetime(2026,1,7)
    assert relativedelta.weeks(date.date()) == 1