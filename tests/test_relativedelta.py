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

	assert rd.years == 2026
	assert rd.months == 1
	assert rd.days == 1
	assert rd.hours == 12
	assert rd.minutes == 30
	assert rd.seconds == 45

def test_relativedelta_should_throw_on_bad_arguments():
	with pytest.raises(TypeError):
		relativedelta(1, 'a')

	with pytest.raises(ValueError):
		relativedelta(years='not a number', months=3)

def test_relativedelta_should_warn_on_non_integer_absolute_date():
	with pytest.warns(DeprecationWarning):
		relativedelta(year='not integer', month=3.6, day=5)

def test_relativedelta_should_throw_on_invalid_yearday():
	with pytest.raises(ValueError):
		relativedelta(nlyearday=430)

	with pytest.raises(ValueError):
		relativedelta(yearday=430)

# tests for _fix

# def test_relativedelta_fix():
#	pass