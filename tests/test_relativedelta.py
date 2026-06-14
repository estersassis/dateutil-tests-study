import pytest
import datetime
import warnings
import operator
from src.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU

# ==================== Constructor Tests ====================

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


# ==================== Arithmetic Tests ====================

def test_add_relativedelta():
    rd1 = relativedelta(years=1, months=2, year=2020)
    rd2 = relativedelta(years=2, months=3, month=5)
    
    res = rd1 + rd2
    assert res.years == 3
    assert res.months == 5
    assert res.year == 2020
    assert res.month == 5

def test_add_timedelta():
    rd = relativedelta(years=1, days=2, seconds=10)
    td = datetime.timedelta(days=3, seconds=20, microseconds=100)
    res = rd + td
    assert res.years == 1
    assert res.days == 5
    assert res.seconds == 30
    assert res.microseconds == 100

def test_add_unsupported():
    rd = relativedelta(days=1)
    with pytest.raises(TypeError):
        rd + "invalid"

def test_add_date_datetime():
    # Adding relativedelta with time to date converts date to datetime
    rd = relativedelta(hours=1)
    dt = datetime.date(2020, 1, 1)
    res = dt + rd
    assert isinstance(res, datetime.datetime)
    assert res == datetime.datetime(2020, 1, 1, 1)

    # Normal addition
    rd2 = relativedelta(years=1, months=2, days=3)
    dt2 = datetime.date(2020, 1, 1)
    assert dt2 + rd2 == datetime.date(2021, 3, 4)

def test_add_month_overflow_underflow():
    # month > 12
    rd = relativedelta(months=10)
    dt = datetime.date(2020, 5, 1)
    assert dt + rd == datetime.date(2021, 3, 1)

    # month < 1
    rd2 = relativedelta(months=-10)
    dt2 = datetime.date(2020, 5, 1)
    assert dt2 + rd2 == datetime.date(2019, 7, 1)

def test_add_day_clamping():
    rd = relativedelta(months=1)
    dt = datetime.date(2020, 1, 31)
    assert dt + rd == datetime.date(2020, 2, 29)

    dt2 = datetime.date(2021, 1, 31)
    assert dt2 + rd == datetime.date(2021, 2, 28)

def test_add_leapdays():
    # leapdays added when month > 2 and year is leap year
    rd = relativedelta(months=1, leapdays=1)
    dt = datetime.date(2020, 1, 15)  # 2020 is leap year
    # month becomes 2 (not > 2), so leapdays not added
    assert dt + rd == datetime.date(2020, 2, 15)

    rd2 = relativedelta(months=2, leapdays=1)
    dt2 = datetime.date(2020, 1, 15)
    # month becomes 3 (> 2), leap year, so leapdays (+1) is added to days
    assert dt2 + rd2 == datetime.date(2020, 3, 16)

    # Not leap year
    dt3 = datetime.date(2021, 1, 15)
    assert dt3 + rd2 == datetime.date(2021, 3, 15)

def test_add_weekday():
    # 2020-01-01 is Wednesday (2)
    # MO is Monday (0)
    dt = datetime.date(2020, 1, 1)
    assert dt + relativedelta(weekday=MO) == datetime.date(2020, 1, 6)
    assert dt + relativedelta(weekday=MO(1)) == datetime.date(2020, 1, 6)

    # MO(+2): Wednesday + 12 days = Monday (2020-01-13)
    assert dt + relativedelta(weekday=MO(2)) == datetime.date(2020, 1, 13)

    # MO(-1): Wednesday - 2 days = Monday (2019-12-30)
    assert dt + relativedelta(weekday=MO(-1)) == datetime.date(2019, 12, 30)

    # MO(-2): Wednesday - 9 days = Monday (2019-12-23)
    assert dt + relativedelta(weekday=MO(-2)) == datetime.date(2019, 12, 23)

def test_sub_relativedelta():
    rd1 = relativedelta(years=2, months=3, year=2020)
    rd2 = relativedelta(years=1, months=1, month=5)
    
    res = rd1 - rd2
    assert res.years == 1
    assert res.months == 2
    assert res.year == 2020
    assert res.month == 5

def test_sub_unsupported():
    rd = relativedelta(days=1)
    with pytest.raises(TypeError):
        rd - "invalid"

def test_rsub_date_datetime():
    dt = datetime.date(2020, 1, 10)
    rd = relativedelta(days=3)
    assert dt - rd == datetime.date(2020, 1, 7)

def test_neg():
    rd = relativedelta(years=1, months=-2, day=5)
    res = -rd
    assert res.years == -1
    assert res.months == 2
    assert res.day == 5

def test_abs():
    rd = relativedelta(years=-1, months=-2, day=5)
    res = abs(rd)
    assert res.years == 1
    assert res.months == 2
    assert res.day == 5

def test_mul_rmul():
    rd = relativedelta(years=1, months=2, day=5)
    
    res1 = rd * 2
    assert res1.years == 2
    assert res1.months == 4
    assert res1.day == 5

    res2 = 2.5 * rd
    assert res2.years == 2
    assert res2.months == 5
    assert res2.day == 5

    with pytest.raises(ValueError):
        rd * "invalid"
    with pytest.raises(TypeError):
        rd * None
    with pytest.raises(TypeError):
        "invalid" * rd

def test_div_truediv():
    rd = relativedelta(years=4, months=6, day=5)
    
    res1 = rd / 2
    assert res1.years == 2
    assert res1.months == 3
    assert res1.day == 5

    res2 = rd / 2.0
    assert res2.years == 2
    assert res2.months == 3
    assert res2.day == 5

    with pytest.raises(ValueError):
        rd / "invalid"

    with pytest.raises(TypeError):
        rd / None

    with pytest.raises(ZeroDivisionError):
        rd / 0
