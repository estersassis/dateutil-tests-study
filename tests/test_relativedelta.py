# Write tests for the relativedelta class here
import datetime, pytest
from src.relativedelta import *

def test_weeks_float_result():
    date = relativedelta(datetime.datetime(2026,1,10), datetime.datetime(2026,1,1))
    assert date.weeks == 1
    date = relativedelta(datetime.datetime(2026,1,28), datetime.datetime(2026,1,14))
    assert date.weeks == 2

def test_input_with_hours_and_minutes():
    date = datetime.datetime(2026,1,7,12,20) + relativedelta(hours=1, minutes=20)
    assert (date.hour == 13) & (date.minute == 40)

def test_add_week():
    date = datetime.datetime(2026,1,7,12,20) + relativedelta(days=7)
    assert date.day == 14

def test_add_month():
    date = datetime.datetime(2026,1,30,12,20) + relativedelta(months=1)
    assert date.day == 28

def test_add_year():
    date = datetime.datetime(2026,1,30,12,20) + relativedelta(years=2,months=1)
    assert date.day == 29

def test_add_minutes():
    date = datetime.datetime(2026,1,30,12,20) + relativedelta(minutes=60)   assert date.minute == 20