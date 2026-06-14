import datetime
import warnings

import pytest

from src.relativedelta import (
    relativedelta,
    MO, TU, WE, TH, FR, SA, SU,
)


# ---------------------------------------------------------------------------
# Construction with relative arguments and normalization (_fix)
# ---------------------------------------------------------------------------

class TestConstructionRelative:
    def test_empty_relativedelta_is_falsy(self):
        assert not relativedelta()

    def test_simple_relative_values(self):
        rd = relativedelta(years=1, months=2, days=3, hours=4,
                           minutes=5, seconds=6, microseconds=7)
        assert rd.years == 1
        assert rd.months == 2
        assert rd.days == 3
        assert rd.hours == 4
        assert rd.minutes == 5
        assert rd.seconds == 6
        assert rd.microseconds == 7

    def test_weeks_added_to_days(self):
        rd = relativedelta(weeks=2, days=1)
        assert rd.days == 15

    def test_weeks_property_getter(self):
        rd = relativedelta(days=15)
        assert rd.weeks == 2

    def test_weeks_property_negative_getter(self):
        rd = relativedelta(days=-15)
        assert rd.weeks == -2

    def test_weeks_setter(self):
        rd = relativedelta(days=1)
        rd.weeks = 3
        assert rd.days == 22
        assert rd.weeks == 3

    def test_leapdays_stored(self):
        rd = relativedelta(leapdays=1)
        assert rd.leapdays == 1

    def test_absolute_values_stored(self):
        rd = relativedelta(year=2000, month=1, day=2, hour=3,
                           minute=4, second=5, microsecond=6)
        assert rd.year == 2000
        assert rd.month == 1
        assert rd.day == 2
        assert rd.hour == 3
        assert rd.minute == 4
        assert rd.second == 5
        assert rd.microsecond == 6


class TestNormalizationFix:
    def test_microseconds_overflow(self):
        rd = relativedelta(microseconds=1000000)
        assert rd.microseconds == 0
        assert rd.seconds == 1

    def test_microseconds_overflow_with_remainder(self):
        rd = relativedelta(microseconds=2500000)
        assert rd.microseconds == 500000
        assert rd.seconds == 2

    def test_negative_microseconds_overflow(self):
        rd = relativedelta(microseconds=-1000000)
        assert rd.microseconds == 0
        assert rd.seconds == -1

    def test_seconds_overflow(self):
        rd = relativedelta(seconds=60)
        assert rd.seconds == 0
        assert rd.minutes == 1

    def test_seconds_overflow_with_remainder(self):
        rd = relativedelta(seconds=125)
        assert rd.seconds == 5
        assert rd.minutes == 2

    def test_minutes_overflow(self):
        rd = relativedelta(minutes=60)
        assert rd.minutes == 0
        assert rd.hours == 1

    def test_hours_overflow(self):
        rd = relativedelta(hours=24)
        assert rd.hours == 0
        assert rd.days == 1

    def test_months_overflow(self):
        rd = relativedelta(months=12)
        assert rd.months == 0
        assert rd.years == 1

    def test_months_overflow_with_remainder(self):
        rd = relativedelta(months=25)
        assert rd.months == 1
        assert rd.years == 2

    def test_negative_months_overflow(self):
        rd = relativedelta(months=-13)
        assert rd.months == -1
        assert rd.years == -1

    def test_cascade_overflow(self):
        rd = relativedelta(microseconds=1000000 * 60 * 60 * 24 + 1)
        assert rd.microseconds == 1
        assert rd.seconds == 0
        assert rd.minutes == 0
        assert rd.hours == 0
        assert rd.days == 1

    def test_has_time_set_when_time_present(self):
        assert relativedelta(hours=1)._has_time == 1
        assert relativedelta(minute=0)._has_time == 1

    def test_has_time_unset_when_no_time(self):
        assert relativedelta(days=1)._has_time == 0
        assert relativedelta()._has_time == 0


# ---------------------------------------------------------------------------
# Validation / errors / warnings
# ---------------------------------------------------------------------------

class TestValidation:
    def test_non_integer_years_raises(self):
        with pytest.raises(ValueError):
            relativedelta(years=1.5)

    def test_non_integer_months_raises(self):
        with pytest.raises(ValueError):
            relativedelta(months=1.5)

    def test_integer_valued_float_years_ok(self):
        rd = relativedelta(years=2.0)
        assert rd.years == 2

    def test_non_integer_absolute_warns(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            relativedelta(day=1.5)
        assert any(issubclass(w.category, DeprecationWarning) for w in caught)

    def test_diff_with_non_date_raises(self):
        with pytest.raises(TypeError):
            relativedelta("not a date", datetime.date(2000, 1, 1))


# ---------------------------------------------------------------------------
# weekday argument handling
# ---------------------------------------------------------------------------

class TestWeekdayArgument:
    def test_integer_weekday_becomes_weekday_object(self):
        rd = relativedelta(weekday=0)
        assert rd.weekday == MO

    def test_weekday_object_preserved(self):
        rd = relativedelta(weekday=FR)
        assert rd.weekday == FR

    def test_weekday_with_n(self):
        rd = relativedelta(weekday=MO(1))
        assert rd.weekday.weekday == MO.weekday
        assert rd.weekday.n == 1


# ---------------------------------------------------------------------------
# yearday / nlyearday handling
# ---------------------------------------------------------------------------

class TestYearday:
    def test_yearday_january(self):
        rd = relativedelta(yearday=15)
        assert rd.month == 1
        assert rd.day == 15

    def test_yearday_february(self):
        rd = relativedelta(yearday=32)
        assert rd.month == 2
        assert rd.day == 1

    def test_yearday_after_feb_sets_leapdays(self):
        rd = relativedelta(yearday=60)
        assert rd.leapdays == -1

    def test_yearday_end_of_year(self):
        rd = relativedelta(yearday=366)
        assert rd.month == 12
        assert rd.day == 32 - (366 - 334)  # day computed from index table

    def test_invalid_yearday_raises(self):
        with pytest.raises(ValueError):
            relativedelta(yearday=367)

    def test_nlyearday(self):
        rd = relativedelta(nlyearday=60)
        assert rd.month == 3
        assert rd.day == 1
        assert rd.leapdays == 0


# ---------------------------------------------------------------------------
# Difference of two dates
# ---------------------------------------------------------------------------

class TestDateDifference:
    def test_one_year_difference(self):
        rd = relativedelta(datetime.date(2001, 1, 1), datetime.date(2000, 1, 1))
        assert rd == relativedelta(years=1)

    def test_one_month_difference(self):
        rd = relativedelta(datetime.date(2000, 2, 1), datetime.date(2000, 1, 1))
        assert rd == relativedelta(months=1)

    def test_days_difference(self):
        rd = relativedelta(datetime.date(2000, 1, 10), datetime.date(2000, 1, 1))
        assert rd == relativedelta(days=9)

    def test_negative_difference(self):
        rd = relativedelta(datetime.date(2000, 1, 1), datetime.date(2001, 1, 1))
        assert rd == relativedelta(years=-1)

    def test_diff_roundtrip(self):
        d1 = datetime.datetime(2005, 6, 15, 10, 30, 0)
        d2 = datetime.datetime(2003, 2, 1, 8, 0, 0)
        rd = relativedelta(d1, d2)
        assert d2 + rd == d1

    def test_diff_date_and_datetime_mixed(self):
        d1 = datetime.datetime(2000, 1, 2, 12, 0, 0)
        d2 = datetime.date(2000, 1, 1)
        rd = relativedelta(d1, d2)
        assert rd.days == 1
        assert rd.hours == 12

    def test_diff_with_seconds(self):
        d1 = datetime.datetime(2000, 1, 1, 0, 0, 30)
        d2 = datetime.datetime(2000, 1, 1, 0, 0, 0)
        rd = relativedelta(d1, d2)
        assert rd.seconds == 30


# ---------------------------------------------------------------------------
# Addition with dates / datetimes
# ---------------------------------------------------------------------------

class TestAddToDate:
    def test_add_years(self):
        assert datetime.date(2000, 1, 1) + relativedelta(years=1) == \
            datetime.date(2001, 1, 1)

    def test_add_months_wraps_year(self):
        assert datetime.date(2000, 11, 1) + relativedelta(months=3) == \
            datetime.date(2001, 2, 1)

    def test_subtract_months_wraps_year(self):
        assert datetime.date(2000, 2, 1) + relativedelta(months=-3) == \
            datetime.date(1999, 11, 1)

    def test_add_days(self):
        assert datetime.date(2000, 1, 1) + relativedelta(days=40) == \
            datetime.date(2000, 2, 10)

    def test_day_clamped_to_month_end(self):
        # Jan 31 + 1 month -> Feb has no 31, clamp to 28 (2001 not leap)
        assert datetime.date(2001, 1, 31) + relativedelta(months=1) == \
            datetime.date(2001, 2, 28)

    def test_absolute_replacement(self):
        assert datetime.date(2000, 6, 15) + relativedelta(day=1) == \
            datetime.date(2000, 6, 1)

    def test_absolute_year_month_day(self):
        assert datetime.date(2000, 6, 15) + \
            relativedelta(year=1999, month=12, day=25) == \
            datetime.date(1999, 12, 25)

    def test_add_time_to_date_promotes_to_datetime(self):
        result = datetime.date(2000, 1, 1) + relativedelta(hours=5)
        assert result == datetime.datetime(2000, 1, 1, 5, 0, 0)

    def test_radd(self):
        # __radd__ is the date + relativedelta path
        rd = relativedelta(days=1)
        assert rd.__radd__(datetime.date(2000, 1, 1)) == \
            datetime.date(2000, 1, 2)

    def test_leapday_applied(self):
        rd = relativedelta(leapdays=1, month=3, day=1)
        result = datetime.date(2000, 1, 1) + rd
        assert result == datetime.date(2000, 3, 2)

    def test_leapday_not_applied_non_leap_year(self):
        rd = relativedelta(leapdays=1, month=3, day=1)
        result = datetime.date(2001, 1, 1) + rd
        assert result == datetime.date(2001, 3, 1)


class TestWeekdayAddition:
    def test_next_monday(self):
        # 2000-01-01 is a Saturday; next Monday is 2000-01-03
        result = datetime.date(2000, 1, 1) + relativedelta(weekday=MO)
        assert result == datetime.date(2000, 1, 3)

    def test_same_day_weekday_stays(self):
        # 2000-01-01 is Saturday; weekday=SA stays
        result = datetime.date(2000, 1, 1) + relativedelta(weekday=SA)
        assert result == datetime.date(2000, 1, 1)

    def test_second_monday(self):
        result = datetime.date(2000, 1, 1) + relativedelta(weekday=MO(2))
        assert result == datetime.date(2000, 1, 10)

    def test_last_monday_negative_n(self):
        # last Monday on or before 2000-01-15 (a Saturday)
        result = datetime.date(2000, 1, 15) + relativedelta(weekday=MO(-1))
        assert result == datetime.date(2000, 1, 10)


# ---------------------------------------------------------------------------
# Arithmetic between relativedeltas
# ---------------------------------------------------------------------------

class TestRelativedeltaArithmetic:
    def test_add_two_relativedeltas(self):
        rd = relativedelta(years=1, months=2) + relativedelta(years=2, days=3)
        assert rd == relativedelta(years=3, months=2, days=3)

    def test_add_absolute_other_takes_precedence(self):
        rd = relativedelta(day=1) + relativedelta(day=15)
        assert rd.day == 15

    def test_add_absolute_self_used_when_other_none(self):
        rd = relativedelta(day=1) + relativedelta(years=1)
        assert rd.day == 1

    def test_subtract_two_relativedeltas(self):
        rd = relativedelta(years=3, months=2) - relativedelta(years=1, months=1)
        assert rd == relativedelta(years=2, months=1)

    def test_sub_with_non_relativedelta_returns_notimplemented(self):
        rd = relativedelta(days=1)
        assert rd.__sub__(5) is NotImplemented

    def test_add_with_unsupported_type_returns_notimplemented(self):
        rd = relativedelta(days=1)
        assert rd.__add__("foo") is NotImplemented

    def test_add_timedelta(self):
        rd = relativedelta(days=1) + datetime.timedelta(days=2, seconds=30)
        assert rd.days == 3
        assert rd.seconds == 30

    def test_rsub_from_date(self):
        result = datetime.date(2000, 1, 10) - relativedelta(days=5)
        assert result == datetime.date(2000, 1, 5)


# ---------------------------------------------------------------------------
# Unary operations
# ---------------------------------------------------------------------------

class TestUnary:
    def test_negation(self):
        rd = -relativedelta(years=1, months=2, days=3)
        assert rd == relativedelta(years=-1, months=-2, days=-3)

    def test_negation_preserves_absolute(self):
        rd = -relativedelta(year=2000, leapdays=1)
        assert rd.year == 2000
        assert rd.leapdays == 1

    def test_abs(self):
        rd = abs(relativedelta(years=-1, months=-2, days=-3))
        assert rd == relativedelta(years=1, months=2, days=3)

    def test_abs_preserves_absolute(self):
        rd = abs(relativedelta(year=1999, hour=5))
        assert rd.year == 1999
        assert rd.hour == 5


# ---------------------------------------------------------------------------
# Multiplication and division
# ---------------------------------------------------------------------------

class TestMulDiv:
    def test_multiply_int(self):
        rd = relativedelta(years=1, months=2, days=3) * 2
        assert rd == relativedelta(years=2, months=4, days=6)

    def test_rmul(self):
        rd = 2 * relativedelta(days=3)
        assert rd == relativedelta(days=6)

    def test_multiply_float_truncates(self):
        rd = relativedelta(days=5) * 0.5
        assert rd.days == 2

    def test_multiply_unsupported_returns_notimplemented(self):
        rd = relativedelta(days=1)
        assert rd.__mul__("x") is NotImplemented

    def test_truediv(self):
        rd = relativedelta(days=10) / 2
        assert rd == relativedelta(days=5)

    def test_div_unsupported_returns_notimplemented(self):
        rd = relativedelta(days=1)
        assert rd.__div__("x") is NotImplemented


# ---------------------------------------------------------------------------
# Equality, hashing, comparison helpers
# ---------------------------------------------------------------------------

class TestEqualityAndHash:
    def test_equal_same_values(self):
        assert relativedelta(years=1, months=2) == relativedelta(years=1, months=2)

    def test_not_equal_different_values(self):
        assert relativedelta(years=1) != relativedelta(years=2)

    def test_eq_with_non_relativedelta_returns_notimplemented(self):
        rd = relativedelta(days=1)
        assert rd.__eq__(5) is NotImplemented

    def test_ne_with_non_relativedelta(self):
        rd = relativedelta(days=1)
        # __ne__ -> not __eq__, and not NotImplemented is False
        assert (rd != 5) is False

    def test_equal_with_matching_weekday(self):
        assert relativedelta(weekday=MO) == relativedelta(weekday=MO)

    def test_not_equal_one_has_weekday(self):
        assert relativedelta(weekday=MO) != relativedelta(years=0)

    def test_not_equal_different_weekday(self):
        assert relativedelta(weekday=MO) != relativedelta(weekday=TU)

    def test_weekday_n_one_equals_none(self):
        # n == 1 is treated equivalent to n is None
        assert relativedelta(weekday=MO(1)) == relativedelta(weekday=MO)

    def test_weekday_n_two_not_equal_none(self):
        assert relativedelta(weekday=MO(2)) != relativedelta(weekday=MO)

    def test_hash_equal_objects(self):
        a = relativedelta(years=1, days=2)
        b = relativedelta(years=1, days=2)
        assert hash(a) == hash(b)

    def test_usable_in_set(self):
        s = {relativedelta(years=1), relativedelta(years=1), relativedelta(days=2)}
        assert len(s) == 2

    def test_bool_true_with_absolute(self):
        assert bool(relativedelta(year=2000)) is True

    def test_bool_false_empty(self):
        assert bool(relativedelta()) is False


# ---------------------------------------------------------------------------
# normalized()
# ---------------------------------------------------------------------------

class TestNormalized:
    def test_normalized_already_normal(self):
        rd = relativedelta(days=1, hours=2)
        assert rd.normalized() == rd

    def test_normalized_returns_relativedelta(self):
        rd = relativedelta(days=2)
        assert isinstance(rd.normalized(), relativedelta)

    def test_normalized_preserves_equality_when_added(self):
        rd = relativedelta(days=1, hours=12, minutes=30)
        base = datetime.datetime(2000, 1, 1)
        assert base + rd == base + rd.normalized()


# ---------------------------------------------------------------------------
# __repr__
# ---------------------------------------------------------------------------

class TestRepr:
    def test_repr_relative(self):
        assert repr(relativedelta(years=1)) == "relativedelta(years=+1)"

    def test_repr_absolute(self):
        assert repr(relativedelta(year=2000)) == "relativedelta(year=2000)"

    def test_repr_empty(self):
        assert repr(relativedelta()) == "relativedelta()"

    def test_repr_eval_roundtrip(self):
        rd = relativedelta(years=1, months=2, days=3, hour=5)
        evaluated = eval(repr(rd), {"relativedelta": relativedelta})
        assert evaluated == rd


# ---------------------------------------------------------------------------
# Module level weekday constants
# ---------------------------------------------------------------------------

class TestWeekdayConstants:
    def test_weekday_indices(self):
        assert MO.weekday == 0
        assert SU.weekday == 6

    def test_weekday_call_creates_n(self):
        assert MO(3).n == 3
        assert MO(3).weekday == 0
