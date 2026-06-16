import pytest
from relativedelta import relativedelta

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


class TestErrors:
    def test_wrong_type_for_diff(self):
        with pytest.raises(TypeError):
            relativedelta(datetime.datetime.now(), 1)


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



        




    







    













