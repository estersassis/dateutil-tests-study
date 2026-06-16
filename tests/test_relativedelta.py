import pytest
from relativedelta import (
    relativedelta, SU, MO, TU, WE, TH, FR, SA
)

import datetime


# Test default behaviours
class TestDefaults:
    def test_empty(self):
        subject = relativedelta()
        assert isinstance(subject, relativedelta)

    def test_is_falsy(self):
        assert not relativedelta()

    def test_default_zeroes(self):
        subject = relativedelta()

        assert subject.years == 0
        assert subject.months == 0
        assert subject.days == 0
        assert subject.leapdays == 0
        assert subject.hours == 0
        assert subject.minutes == 0
        assert subject.seconds == 0
        assert subject.microseconds == 0

    def test_default_nones(self):
        subject = relativedelta()

        assert subject.year == None
        assert subject.month == None
        assert subject.day == None
        assert subject.weekday == None
        assert subject.hour == None
        assert subject.minute == None
        assert subject.second == None
        assert subject.microsecond == None


class TestYearDay:
    def test_year_day(self):
        assert relativedelta(yearday=25).day == 25
        assert relativedelta(yearday=60).day == 1
        assert relativedelta(yearday=61).day == 2

    def test_nlyearday_ignores_yearday(self):
        assert relativedelta(nlyearday=60, yearday=61).day == 1
        assert relativedelta(nlyearday=61, yearday=61).day == 2

    def test_yearday_affects_leapdays(self):
        assert relativedelta(leapdays=1, yearday=59).leapdays == 1


class TestNotImplemented:
    def test_add_relativedelta_with_date(self):
        relativedelta() + datetime.date.today() == NotImplemented


class TestErrors:
    def test_wrong_type_for_diff(self):
        with pytest.raises(TypeError):
            relativedelta(datetime.datetime.now(), 1)

    def test_wrong_type_of_years(self):
        with pytest.raises(ValueError):
            relativedelta(years="2026")

    def test_wrong_type_of_months(self):
        with pytest.raises(ValueError):
            relativedelta(months="11")

    def test_wrong_type_of_days(self):
        with pytest.raises(TypeError):
            relativedelta(days="11")


class TestNormalization:
    def test_microseconds(self):
        rd = relativedelta(microseconds=1000000)
        assert rd.microseconds == 0
        assert rd.seconds == 1

    def test_seconds(self):
        rd = relativedelta(seconds=61)
        assert rd.seconds == 1
        assert rd.minutes == 1

    def test_hours(self):
        rd = relativedelta(hours=25)
        assert rd.hours == 1
        assert rd.days == 1

    def test_months(self):
        rd = relativedelta(months=14)
        assert rd.months == 2
        assert rd.years == 1

    def test_has_time(self):
        assert relativedelta()._has_time == 0
        assert relativedelta(hours=1)._has_time == 1


class TestWeeks:
    def test_weeks(self):
        assert relativedelta(days=14).weeks == 2

    def test_weeks_setter_with_empty_relativedelta(self):
        rd = relativedelta()
        rd.weeks = 3

        assert rd.days == 21

    def test_weeks_setter_with_days_already_set(self):
        rd = relativedelta(days=4)
        rd.weeks = 5

        assert rd.days == 39

    def test_weeks_setter_with_weeks_already_set(self):
        rd = relativedelta(weeks=2)
        rd.weeks = 3

        assert rd.days == 21

    def test_weeks_setter_with_weeks_and_days_already_set(self):
        rd = relativedelta(weeks=2, days=2)
        rd.weeks = 3

        assert rd.days == 23


class TestAddRelativeDelta:
    def test_add_empty(self):
        rd = relativedelta() + relativedelta()
        assert rd.hours == 0
        assert rd.minutes == 0
        assert rd.seconds == 0
        assert rd.microseconds == 0
        assert rd.years == 0
        assert rd.months == 0
        assert rd.days == 0

    def test_add_years(self):
        rd = relativedelta() + relativedelta(years=1)
        assert rd.years == 1

    def test_add_months(self):
        rd = relativedelta() + relativedelta(months=1)
        assert rd.months == 1

    def test_add_days(self):
        rd = relativedelta() + relativedelta(days=1)
        assert rd.days == 1

    def test_add_hours(self):
        rd = relativedelta(hours=1) + relativedelta(hours=2)
        assert rd.hours == 3

    def test_add_minutes(self):
        rd = relativedelta(hours=1) + relativedelta(minutes=30)
        assert rd.minutes == 30
        assert rd.hours == 1

    def test_add_hours_to_overflow(self):
        rd = relativedelta(hours=23) + relativedelta(hours=2)
        assert rd.hours == 1
        assert rd.days == 1

    def test_add_weekday(self):
        assert (relativedelta(weekday=0)).weekday == MO
        assert (relativedelta() + relativedelta(weekday=1)).weekday == TU
        assert (relativedelta() + relativedelta(weekday=2)).weekday == WE
        assert (relativedelta() + relativedelta(weekday=3)).weekday == TH
        assert (relativedelta() + relativedelta(weekday=4)).weekday == FR
        assert (relativedelta() + relativedelta(weekday=5)).weekday == SA
        assert (relativedelta() + relativedelta(weekday=6)).weekday == SU





    


    



        




    







    













