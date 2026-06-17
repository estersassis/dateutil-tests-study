# Write tests for the relativedelta class here
import datetime

import pytest

from src.relativedelta import relativedelta, MO, TU, FR


def test_constructor_rolls_over_large_relative_values():
    rd = relativedelta(
        years=1,
        months=14,
        days=1,
        weeks=2,
        hours=25,
        minutes=61,
        seconds=61,
        microseconds=1_000_001,
    )

    assert rd.years == 2
    assert rd.months == 2
    assert rd.days == 16
    assert rd.hours == 2
    assert rd.minutes == 2
    assert rd.seconds == 2
    assert rd.microseconds == 1


def test_constructor_accepts_integer_like_years_and_months():
    rd = relativedelta(years=1.0, months=2.0)

    assert rd.years == 1
    assert rd.months == 2


@pytest.mark.parametrize(
    "kwargs",
    [
        {"years": 1.5},
        {"months": 2.25},
    ],
)
def test_non_integer_years_and_months_raise_value_error(kwargs):
    with pytest.raises(ValueError, match="Non-integer years and months"):
        relativedelta(**kwargs)


def test_non_integer_absolute_values_emit_deprecation_warning():
    with pytest.warns(DeprecationWarning, match="Non-integer value passed"):
        rd = relativedelta(day=1.5)

    assert rd.day == 1.5


def test_invalid_yearday_raises_value_error():
    with pytest.raises(ValueError, match="invalid year day"):
        relativedelta(yearday=367)


def test_integer_weekday_is_converted_to_weekday_object():
    rd = relativedelta(weekday=0)

    assert rd.weekday == MO


def test_weeks_property_and_setter():
    rd = relativedelta(days=10)

    assert rd.weeks == 1

    rd.weeks = 3

    assert rd.days == 24


def test_normalized_converts_fractional_values():
    rd = relativedelta(days=1.5, hours=2.25, minutes=3.5, seconds=4.25)
    normalized = rd.normalized()

    assert normalized == relativedelta(
        days=1,
        hours=14,
        minutes=18,
        seconds=34,
        microseconds=250_000,
    )


@pytest.mark.parametrize(
    ("start", "delta", "expected"),
    [
        (datetime.date(2024, 1, 31), relativedelta(months=1), datetime.date(2024, 2, 29)),
        (datetime.date(2023, 1, 31), relativedelta(months=1), datetime.date(2023, 2, 28)),
        (datetime.date(2024, 3, 31), relativedelta(months=-1), datetime.date(2024, 2, 29)),
        (datetime.date(2020, 2, 29), relativedelta(years=1), datetime.date(2021, 2, 28)),
        (datetime.date(2024, 1, 15), relativedelta(months=13), datetime.date(2025, 2, 15)),
        (datetime.date(2024, 1, 15), relativedelta(months=-2), datetime.date(2023, 11, 15)),
    ],
)
def test_add_relative_years_and_months_to_date(start, delta, expected):
    assert start + delta == expected


def test_add_absolute_year_month_day_replaces_date_parts():
    start = datetime.date(2020, 1, 31)

    result = start + relativedelta(year=2022, month=2, day=15)

    assert result == datetime.date(2022, 2, 15)


def test_add_absolute_day_clamps_to_last_day_of_month():
    start = datetime.date(2024, 1, 15)

    result = start + relativedelta(month=2, day=31)

    assert result == datetime.date(2024, 2, 29)


def test_add_time_to_date_returns_datetime():
    start = datetime.date(2024, 1, 1)

    result = start + relativedelta(hours=1, minutes=30)

    assert result == datetime.datetime(2024, 1, 1, 1, 30)


def test_absolute_time_replaces_datetime_parts():
    start = datetime.datetime(2024, 1, 1, 12, 45, 30, 999)

    result = start + relativedelta(hour=8, minute=15, second=0, microsecond=123)

    assert result == datetime.datetime(2024, 1, 1, 8, 15, 0, 123)


@pytest.mark.parametrize(
    ("start", "delta", "expected"),
    [
        (
            datetime.datetime(2024, 1, 1, 23, 30),
            relativedelta(hours=2, minutes=45),
            datetime.datetime(2024, 1, 2, 2, 15),
        ),
        (
            datetime.datetime(2024, 1, 1, 0, 0, 0, 500_000),
            relativedelta(microseconds=750_000),
            datetime.datetime(2024, 1, 1, 0, 0, 1, 250_000),
        ),
    ],
)
def test_add_relative_time_to_datetime(start, delta, expected):
    assert start + delta == expected


def test_leapdays_adds_only_after_february_in_leap_year():
    assert datetime.date(2024, 1, 1) + relativedelta(month=3, day=1, leapdays=1) == datetime.date(2024, 3, 2)
    assert datetime.date(2023, 1, 1) + relativedelta(month=3, day=1, leapdays=1) == datetime.date(2023, 3, 1)
    assert datetime.date(2024, 1, 1) + relativedelta(month=2, day=1, leapdays=1) == datetime.date(2024, 2, 1)


def test_yearday_and_nlyearday():
    assert datetime.date(2024, 1, 1) + relativedelta(yearday=60) == datetime.date(2024, 2, 29)

    assert datetime.date(2024, 1, 1) + relativedelta(nlyearday=60) == datetime.date(2024, 3, 1)
    
    assert datetime.date(2023, 1, 1) + relativedelta(yearday=60) == datetime.date(2023, 3, 1)


@pytest.mark.parametrize(
    ("start", "delta", "expected"),
    [
        (datetime.date(2024, 1, 1), relativedelta(weekday=MO), datetime.date(2024, 1, 1)),
        (datetime.date(2024, 1, 2), relativedelta(weekday=MO), datetime.date(2024, 1, 8)),
        (datetime.date(2024, 1, 10), relativedelta(weekday=MO(-1)), datetime.date(2024, 1, 8)),
        (datetime.date(2024, 1, 1), relativedelta(day=31, weekday=FR(-1)), datetime.date(2024, 1, 26)),
        (datetime.date(2024, 1, 15), relativedelta(day=1, weekday=MO(1)), datetime.date(2024, 1, 1)),
    ],
)
def test_weekday_adjustments(start, delta, expected):
    assert start + delta == expected


def test_relativedelta_between_two_dates():
    rd = relativedelta(datetime.date(2024, 3, 15), datetime.date(2023, 1, 10))

    assert rd.years == 1
    assert rd.months == 2
    assert rd.days == 5
    assert rd.hours == 0
    assert rd.minutes == 0
    assert rd.seconds == 0
    assert rd.microseconds == 0


def test_relativedelta_between_two_datetimes():
    rd = relativedelta(
        datetime.datetime(2024, 3, 15, 12, 30, 45, 123456),
        datetime.datetime(2024, 1, 10, 10, 0, 0, 0),
    )

    assert rd.years == 0
    assert rd.months == 2
    assert rd.days == 5
    assert rd.hours == 2
    assert rd.minutes == 30
    assert rd.seconds == 45
    assert rd.microseconds == 123456


def test_relativedelta_between_date_and_datetime_promotes_to_datetime():
    rd = relativedelta(
        datetime.date(2024, 1, 2),
        datetime.datetime(2024, 1, 1, 12, 0),
    )

    assert rd.days == 0
    assert rd.hours == 12


def test_relativedelta_diff_requires_date_or_datetime_instances():
    with pytest.raises(TypeError, match="relativedelta only diffs datetime/date"):
        relativedelta("2024-01-01", datetime.date(2024, 1, 1))


def test_add_two_relativedeltas_combines_relative_values_and_overrides_absolute_values():
    first = relativedelta(years=1, months=2, days=3, year=2024, month=1, day=10)
    second = relativedelta(years=2, months=3, days=4, month=5)

    result = first + second

    assert result.years == 3
    assert result.months == 5
    assert result.days == 7
    assert result.year == 2024
    assert result.month == 5
    assert result.day == 10


def test_add_timedelta_to_relativedelta():
    result = relativedelta(days=1, seconds=30) + datetime.timedelta(days=2, seconds=40)

    assert result.days == 3
    assert result.minutes == 1
    assert result.seconds == 10


def test_subtract_two_relativedeltas():
    result = relativedelta(years=3, months=5, days=10, hours=7) - relativedelta(
        years=1,
        months=2,
        days=3,
        hours=4,
    )

    assert result == relativedelta(years=2, months=3, days=7, hours=3)


def test_date_minus_relativedelta_uses_negated_delta():
    result = datetime.date(2024, 1, 10) - relativedelta(days=5)

    assert result == datetime.date(2024, 1, 5)


def test_neg_and_abs():
    rd = relativedelta(years=-1, months=2, days=-3, hours=4)

    assert -rd == relativedelta(years=1, months=-2, days=3, hours=-4)
    assert abs(rd) == relativedelta(years=1, months=2, days=3, hours=4)


def test_bool_is_false_only_for_empty_delta():
    assert not relativedelta()
    assert relativedelta(days=1)
    assert relativedelta(year=2024)


def test_multiplication_and_right_multiplication():
    rd = relativedelta(years=1, months=2, days=3, hours=4)

    assert rd * 2 == relativedelta(years=2, months=4, days=6, hours=8)
    assert 3 * rd == relativedelta(years=3, months=6, days=9, hours=12)


def test_multiplication_truncates_fractional_results_to_int():
    result = relativedelta(years=3, months=5, days=9, hours=7) * 0.5

    assert result == relativedelta(years=1, months=2, days=4, hours=3)


def test_division_uses_multiplicative_reciprocal():
    result = relativedelta(years=4, months=6, days=10, hours=8) / 2

    assert result == relativedelta(years=2, months=3, days=5, hours=4)


def test_unsupported_addition_returns_not_implemented_when_called_directly():
    assert relativedelta(days=1).__add__(object()) is NotImplemented


def test_unsupported_subtraction_returns_not_implemented_when_called_directly():
    assert relativedelta(days=1).__sub__(object()) is NotImplemented


def test_unsupported_multiplication_returns_not_implemented_when_called_directly():
    assert relativedelta(days=1).__mul__(object()) is NotImplemented


def test_equality_with_weekday_none_and_one_are_equivalent():
    assert relativedelta(weekday=MO) == relativedelta(weekday=MO(1))


def test_equality_detects_different_weekdays():
    assert relativedelta(weekday=MO) != relativedelta(weekday=TU)
    assert relativedelta(days=1) != relativedelta(days=2)
    assert relativedelta(weekday=MO) != relativedelta()


def test_hash_is_stable_for_equal_simple_deltas():
    first = relativedelta(years=1, months=2, days=3)
    second = relativedelta(years=1, months=2, days=3)

    assert first == second
    assert hash(first) == hash(second)


def test_repr_contains_class_name_and_non_zero_fields():
    value = repr(relativedelta(years=1, months=-2, day=15, weekday=FR(-1)))

    assert value.startswith("relativedelta(")
    assert "years=+1" in value
    assert "months=-2" in value
    assert "day=15" in value
    assert "weekday=FR(-1)" in value
