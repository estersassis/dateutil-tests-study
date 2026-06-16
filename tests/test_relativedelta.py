# Write tests for the relativedelta class here
import datetime, pytest
from src.relativedelta import *

def test_weeks_float_result():
    assert relativedelta.weeks(datetime(1,7,2026)) == 1