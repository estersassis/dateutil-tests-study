# Write tests for the relativedelta class here
from dateutil.relativedelta import relativedelta
import datetime
import pytest

# initialization tests

def test_relativedelta_should_initialize_with_datetime():
	dt1 = datetime.datetime(2026, 1, 1)
	dt2 = datetime.datetime(2026, 6, 17)
	rd = relativedelta(dt2, dt1)

	assert rd.years == 0
	assert rd.months == 5
	assert rd.days == 16

def test_relativedelta_should_initialize_with_relative_date():
	rd = relativedelta(years=1, months=2, days=3, weeks=3, hours=5, minutes=6, seconds=7)

	assert rd.years == 1
	assert rd.months == 2
	assert rd.days == 24
	assert rd.hours == 5
	assert rd.minutes == 6
	assert rd.seconds == 7

def test_relativedelta_should_initialize_with_absolute_date():
	rd = relativedelta(year=2026, month=1, day=1, hour=12, minute=30, second=45)

	assert rd.year == 2026
	assert rd.month == 1
	assert rd.day == 1
	assert rd.hour == 12
	assert rd.minute == 30
	assert rd.second == 45

def test_relativedelta_should_throw_on_bad_arguments():
	with pytest.raises(TypeError):
		relativedelta(1, 'a')

	with pytest.raises(ValueError):
		relativedelta(years='not a number', months=3)

def test_relativedelta_should_warn_on_non_integer_absolute_date():
	with pytest.warns(DeprecationWarning):
		relativedelta(year=2026.6, month=3.6, day=5)

def test_relativedelta_should_throw_on_invalid_yearday():
	with pytest.raises(ValueError):
		relativedelta(nlyearday=430)

	with pytest.raises(ValueError):
		relativedelta(yearday=430)

# formatting functions

def test_relativedelta_fix_should_div_correctly():
	rd = relativedelta(years=1, months=11, hours=23, minutes=59, seconds=59, microseconds=1000000)

	assert rd.years == 2
	assert rd.months == 0
	assert rd.hours == 0
	assert rd.minutes == 0
	assert rd.seconds == 0
	assert rd.microseconds == 0

def test_relativedelta_should_normalize():
	rd = relativedelta(days=3.83771875)
	normalized = rd.normalized()
	assert normalized.days == 3
	assert normalized.hours == 20
	assert normalized.minutes == 6
	assert normalized.seconds == 18
	assert normalized.microseconds == 900000

# basic operations functions

def test_relativedelta_should_equal():
	rd1 = relativedelta(years=2026, months=6, days=17)
	rd2 = relativedelta(years=2026, months=6, days=17)

	assert rd1 == rd2

def test_relativedelta_should_add():
	rd1 = relativedelta(years=2003, months=3, days=3)
	rd2 = relativedelta(years=23, months=3, days=14)
	result = rd1 + rd2

	assert result.years == 2026
	assert result.months == 6
	assert result.days == 17

def test_relativedelta_should_subtract():
	rd1 = relativedelta(years=2026, months=6, days=17)
	rd2 = relativedelta(years=2003, months=3, days=3)
	result = rd1 - rd2

	assert result.years == 23
	assert result.months == 3
	assert result.days == 14

def test_relativedelta_should_multiply():
	rd = relativedelta(years=10, months=7, days=3)
	result = rd * 2

	assert result.years == 21
	assert result.months == 2
	assert result.days == 6

def test_relativedelta_should_divide():
	rd = relativedelta(years=10, months=7, days=3)
	result = rd / 2

	test_result = relativedelta(years=5, months=3.5, days=1.5)

	assert result == test_result