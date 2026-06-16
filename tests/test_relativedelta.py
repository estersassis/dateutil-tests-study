import pytest
from src.relativedelta import relativedelta


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

        assert year == None
        assert month == None
        assert day == None
        assert weekday == None
        assert yearday == None
        assert nlyearday == None
        assert hour == None
        assert minute == None
        assert second == None
        assert microsecond == None











