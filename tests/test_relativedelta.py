# Write tests for the relativedelta class here
import datetime, pytest
from src.relativedelta import *

def test_weeks_float_result():
    date = relativedelta(datetime.datetime(2026,1,8), datetime.datetime(2026,1,1))
    assert date.weeks == 1