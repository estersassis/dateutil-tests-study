import pytest
import datetime
import warnings
import operator
from src.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU

def test_constructor_dt1_dt2_type_error():
    # dt1 and dt2 must be date/datetime
    with pytest.raises(TypeError):
        relativedelta("2020-01-01", datetime.date(2020, 1, 1))
    with pytest.raises(TypeError):
        relativedelta(datetime.date(2020, 1, 1), "2020-01-01")

def test_constructor_dt1_dt2_mix():
    # dt1 is date, dt2 is datetime
    rd1 = relativedelta(datetime.date(2020, 1, 1), datetime.datetime(2020, 1, 1, 12, 0))
    assert rd1.hours == -12

    # dt1 is datetime, dt2 is date
    rd2 = relativedelta(datetime.datetime(2020, 1, 1, 12, 0), datetime.date(2020, 1, 1))
    assert rd2.hours == 12

    # Both are date
    rd3 = relativedelta(datetime.date(2020, 1, 1), datetime.date(2019, 1, 1))
    assert rd3.years == 1

    # Both are datetime
    rd4 = relativedelta(datetime.datetime(2020, 1, 1, 12, 0), datetime.datetime(2019, 1, 1, 12, 0))
    assert rd4.years == 1

def test_constructor_dt1_dt2_diff():
    # dt1 > dt2
    rd = relativedelta(datetime.datetime(2020, 2, 29, 12, 30, 15, 100),
                       datetime.datetime(2019, 1, 1, 10, 15, 10, 50))
    assert rd.years == 1
    assert rd.months == 1
    assert rd.days == 28
    assert rd.hours == 2
    assert rd.minutes == 15
    assert rd.seconds == 5
    assert rd.microseconds == 50

    # dt1 < dt2 (negative difference)
    rd_neg = relativedelta(datetime.datetime(2019, 1, 1, 10, 15, 10, 50),
                           datetime.datetime(2020, 2, 29, 12, 30, 15, 100))
    assert rd_neg.years == -1
    assert rd_neg.months == -1
    assert rd_neg.days == -28
    assert rd_neg.hours == -2
    assert rd_neg.minutes == -15
    assert rd_neg.seconds == -6
    assert rd_neg.microseconds == 999950

def test_constructor_dt1_dt2_while_loops():
    # Trigger the while loop in dt1 >= dt2 (compare is operator.lt, increment = -1)
    # Jan 31st to Feb 28th
    rd1 = relativedelta(datetime.date(2020, 2, 28), datetime.date(2020, 1, 31))
    assert rd1.months == 0
    assert rd1.days == 28

    # Trigger the while loop in dt1 < dt2 (compare is operator.gt, increment = 1)
    # Feb 28th to Jan 31st
    rd2 = relativedelta(datetime.date(2020, 1, 31), datetime.date(2020, 2, 28))
    assert rd2.months == 0
    assert rd2.days == -28

def test_constructor_non_integer_error():
    with pytest.raises(ValueError):
        relativedelta(years=1.5)
    with pytest.raises(ValueError):
        relativedelta(months=2.5)

def test_constructor_non_integer_absolute_warning():
    with pytest.warns(DeprecationWarning):
        relativedelta(year=2020.5)
    with pytest.warns(DeprecationWarning):
        relativedelta(month=2.5)
    with pytest.warns(DeprecationWarning):
        relativedelta(day=15.5)
    with pytest.warns(DeprecationWarning):
        relativedelta(hour=12.5)
    with pytest.warns(DeprecationWarning):
        relativedelta(minute=30.5)
    with pytest.warns(DeprecationWarning):
        relativedelta(second=30.5)
    with pytest.warns(DeprecationWarning):
        relativedelta(microsecond=500.5)

def test_constructor_weekday():
    # weekday as integer
    rd = relativedelta(weekday=0)
    assert rd.weekday == MO
    # weekday as weekday object
    rd2 = relativedelta(weekday=TU)
    assert rd2.weekday == TU

def test_constructor_yearday():
    # nlyearday
    rd = relativedelta(nlyearday=100)
    assert rd.month == 4
    assert rd.day == 10
    assert rd.leapdays == 0

    # yearday <= 59
    rd2 = relativedelta(yearday=50)
    assert rd2.month == 2
    assert rd2.day == 19
    assert rd2.leapdays == 0

    # yearday > 59
    rd3 = relativedelta(yearday=100)
    assert rd3.month == 4
    assert rd3.day == 10
    assert rd3.leapdays == -1

    # invalid yearday
    with pytest.raises(ValueError):
        relativedelta(yearday=367)
    with pytest.raises(ValueError):
        relativedelta(nlyearday=367)

    # negative yearday
    rd_neg = relativedelta(yearday=-5)
    assert rd_neg.month == 1
    assert rd_neg.day == -5

def test_fix_normalization():
    # microseconds > 999999
    rd = relativedelta(microseconds=1500000)
    assert rd.microseconds == 500000
    assert rd.seconds == 1

    # microseconds < -999999
    rd = relativedelta(microseconds=-1500000)
    assert rd.microseconds == -500000
    assert rd.seconds == -1

    # seconds > 59
    rd = relativedelta(seconds=125)
    assert rd.seconds == 5
    assert rd.minutes == 2

    # seconds < -59
    rd = relativedelta(seconds=-125)
    assert rd.seconds == -5
    assert rd.minutes == -2

    # minutes > 59
    rd = relativedelta(minutes=125)
    assert rd.minutes == 5
    assert rd.hours == 2

    # minutes < -59
    rd = relativedelta(minutes=-125)
    assert rd.minutes == -5
    assert rd.hours == -2

    # hours > 23
    rd = relativedelta(hours=50)
    assert rd.hours == 2
    assert rd.days == 2

    # hours < -23
    rd = relativedelta(hours=-50)
    assert rd.hours == -2
    assert rd.days == -2

    # months > 11
    rd = relativedelta(months=25)
    assert rd.months == 1
    assert rd.years == 2

    # months < -11
    rd = relativedelta(months=-25)
    assert rd.months == -1
    assert rd.years == -2

def test_has_time():
    # No time components
    assert relativedelta(days=1)._has_time == 0
    # Relative time components
    assert relativedelta(hours=1)._has_time == 1
    assert relativedelta(minutes=1)._has_time == 1
    assert relativedelta(seconds=1)._has_time == 1
    assert relativedelta(microseconds=1)._has_time == 1
    # Absolute time components
    assert relativedelta(hour=1)._has_time == 1
    assert relativedelta(minute=1)._has_time == 1
    assert relativedelta(second=1)._has_time == 1
    assert relativedelta(microsecond=1)._has_time == 1
