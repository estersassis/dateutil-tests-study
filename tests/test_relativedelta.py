import datetime

import pytest

from src.relativedelta import FR, MO, SA, SU, TU, relativedelta


def test_relative_fields_are_normalized_on_construction():
    delta = relativedelta(
        months=14,
        days=1,
        hours=49,
        minutes=121,
        seconds=122,
        microseconds=2_000_001,
    )

    assert delta.years == 1
    assert delta.months == 2
    assert delta.days == 3
    assert delta.hours == 3
    assert delta.minutes == 3
    assert delta.seconds == 4
    assert delta.microseconds == 1


def test_negative_relative_fields_are_normalized_on_construction():
    delta = relativedelta(
        months=-14,
        hours=-25,
        minutes=-61,
        seconds=-61,
        microseconds=-1_000_001,
    )

    assert delta.years == -1
    assert delta.months == -2
    assert delta.days == -1
    assert delta.hours == -2
    assert delta.minutes == -2
    assert delta.seconds == -2
    assert delta.microseconds == -1


@pytest.mark.parametrize(
    "kwargs",
    [
        {"years": 1.5},
        {"months": 2.25},
    ],
)
def test_fractional_years_and_months_are_rejected(kwargs):
    with pytest.raises(ValueError, match="Non-integer years and months"):
        relativedelta(**kwargs)


def test_fractional_absolute_values_warn_but_are_stored():
    with pytest.warns(DeprecationWarning, match="Non-integer value"):
        delta = relativedelta(year=2024.0, day=1.5, hour=9.0)

    assert delta.year == 2024.0
    assert delta.day == 1.5
    assert delta.hour == 9.0


def test_weeks_are_stored_as_days_and_can_be_reassigned():
    delta = relativedelta(days=3, weeks=2)

    assert delta.days == 17
    assert delta.weeks == 2

    delta.weeks = 5

    assert delta.days == 38
    assert delta.weeks == 5


@pytest.mark.parametrize(
    ("kwargs", "expected_month", "expected_day", "expected_leapdays"),
    [
        ({"yearday": 60}, 3, 1, -1),
        ({"yearday": 32}, 2, 1, 0),
        ({"nlyearday": 60}, 3, 1, 0),
    ],
)
def test_year_day_arguments_are_converted_to_month_and_day(
    kwargs, expected_month, expected_day, expected_leapdays
):
    delta = relativedelta(**kwargs)

    assert delta.month == expected_month
    assert delta.day == expected_day
    assert delta.leapdays == expected_leapdays


def test_invalid_year_day_raises_value_error():
    with pytest.raises(ValueError, match="invalid year day"):
        relativedelta(yearday=367)


def test_integer_weekday_argument_maps_to_weekday_instance():
    delta = relativedelta(weekday=0)

    assert delta.weekday == MO


@pytest.mark.parametrize(
    ("start", "delta", "expected"),
    [
        (datetime.date(2024, 1, 31), relativedelta(months=1), datetime.date(2024, 2, 29)),
        (datetime.date(2023, 1, 31), relativedelta(months=1), datetime.date(2023, 2, 28)),
        (datetime.date(2024, 3, 31), relativedelta(months=-1), datetime.date(2024, 2, 29)),
        (datetime.date(2023, 12, 31), relativedelta(months=2), datetime.date(2024, 2, 29)),
        (datetime.date(2024, 1, 15), relativedelta(year=2025, month=2, day=31), datetime.date(2025, 2, 28)),
    ],
)
def test_adding_months_and_absolute_date_fields_clamps_to_month_end(
    start, delta, expected
):
    assert start + delta == expected


def test_relative_fields_are_applied_after_absolute_fields():
    start = datetime.datetime(2024, 5, 20, 10, 30, 45, 123456)
    delta = relativedelta(
        year=2025,
        month=2,
        day=28,
        hour=23,
        minute=59,
        second=58,
        microsecond=9,
        days=1,
        seconds=2,
    )

    assert start + delta == datetime.datetime(2025, 3, 1, 0, 0, 0, 9)


def test_time_delta_turns_date_into_datetime():
    result = datetime.date(2024, 1, 1) + relativedelta(hours=2, minutes=30)

    assert result == datetime.datetime(2024, 1, 1, 2, 30)


@pytest.mark.parametrize(
    ("start", "delta", "expected"),
    [
        (datetime.date(2024, 3, 1), relativedelta(years=1, leapdays=1), datetime.date(2025, 3, 1)),
        (datetime.date(2023, 3, 1), relativedelta(years=1, leapdays=1), datetime.date(2024, 3, 2)),
        (datetime.date(2024, 2, 1), relativedelta(leapdays=1), datetime.date(2024, 2, 1)),
    ],
)
def test_leapdays_apply_only_after_february_in_leap_years(start, delta, expected):
    assert start + delta == expected


@pytest.mark.parametrize(
    ("start", "weekday", "expected"),
    [
        (datetime.date(2024, 6, 10), MO, datetime.date(2024, 6, 10)),
        (datetime.date(2024, 6, 10), TU, datetime.date(2024, 6, 11)),
        (datetime.date(2024, 6, 10), FR(+2), datetime.date(2024, 6, 21)),
        (datetime.date(2024, 6, 10), FR(-1), datetime.date(2024, 6, 7)),
        (datetime.date(2024, 6, 10), SU(-2), datetime.date(2024, 6, 2)),
    ],
)
def test_weekday_adjustments_move_to_requested_occurrence(start, weekday, expected):
    assert start + relativedelta(weekday=weekday) == expected


def test_addition_with_relativedelta_merges_relative_and_absolute_fields():
    combined = relativedelta(years=1, months=2, day=10, hour=8) + relativedelta(
        months=3,
        days=4,
        leapdays=1,
        day=20,
        minute=30,
    )

    assert combined == relativedelta(
        years=1,
        months=5,
        days=4,
        leapdays=1,
        day=20,
        hour=8,
        minute=30,
    )


def test_addition_with_timedelta_merges_day_second_and_microsecond_fields():
    combined = relativedelta(days=2, seconds=3, microseconds=4) + datetime.timedelta(
        days=5,
        seconds=6,
        microseconds=7,
    )

    assert combined == relativedelta(days=7, seconds=9, microseconds=11)


def test_subtracting_relativedeltas_preserves_left_absolute_values():
    result = relativedelta(years=3, months=5, day=10, hour=8) - relativedelta(
        years=1,
        months=2,
        days=4,
        day=20,
        minute=30,
    )

    assert result == relativedelta(years=2, months=3, days=-4, day=10, hour=8, minute=30)


def test_date_minus_relativedelta_uses_negated_relative_values():
    assert datetime.date(2024, 5, 31) - relativedelta(months=3, days=1) == datetime.date(
        2024,
        2,
        28,
    )


def test_neg_abs_and_bool_use_relative_fields():
    delta = relativedelta(years=-1, months=2, days=-3, hours=4, minute=30)

    assert -delta == relativedelta(years=1, months=-2, days=3, hours=-4, minute=30)
    assert abs(delta) == relativedelta(years=1, months=2, days=3, hours=4, minute=30)
    assert bool(delta)
    assert not relativedelta()
    assert bool(relativedelta(year=2024))


@pytest.mark.parametrize(
    ("operation", "expected"),
    [
        (lambda delta: delta * 2, relativedelta(years=2, months=4, days=6, hours=8)),
        (lambda delta: 2 * delta, relativedelta(years=2, months=4, days=6, hours=8)),
        (lambda delta: delta * 1.5, relativedelta(years=1, months=3, days=4, hours=6)),
        (lambda delta: delta / 2, relativedelta(months=1, days=1, hours=2)),
    ],
)
def test_multiplication_and_division_scale_relative_fields(operation, expected):
    delta = relativedelta(years=1, months=2, days=3, hours=4)

    assert operation(delta) == expected


def test_unsupported_arithmetic_operands_return_not_implemented():
    delta = relativedelta(days=1)

    assert delta.__add__(object()) is NotImplemented
    assert delta.__sub__(object()) is NotImplemented
    assert delta.__mul__(object()) is NotImplemented
    assert delta.__div__(object()) is NotImplemented


def test_normalized_converts_fractional_relative_units():
    delta = relativedelta(days=1.5, hours=2.25, minutes=3.5, seconds=4.25).normalized()

    assert delta == relativedelta(days=1, hours=14, minutes=18, seconds=34, microseconds=250000)


def test_difference_between_datetimes_reconstructs_target():
    start = datetime.datetime(2022, 1, 31, 23, 0, 0, 500)
    end = datetime.datetime(2024, 3, 1, 1, 2, 3, 900)

    delta = relativedelta(end, start)

    assert start + delta == end
    assert delta.years == 2
    assert delta.months == 1
    assert delta.days == 1
    assert delta.hours == 2
    assert delta.minutes == 2
    assert delta.seconds == 3
    assert delta.microseconds == 400


def test_difference_between_date_and_datetime_promotes_date_to_datetime():
    date_value = datetime.date(2024, 1, 1)
    datetime_value = datetime.datetime(2024, 1, 2, 3, 4)

    delta = relativedelta(datetime_value, date_value)

    assert date_value + delta == datetime_value
    assert delta.days == 1
    assert delta.hours == 3
    assert delta.minutes == 4


def test_difference_can_be_negative_and_reconstruct_original_datetime():
    start = datetime.datetime(2024, 5, 15, 12, 30)
    end = datetime.datetime(2023, 2, 10, 6, 15)

    delta = relativedelta(end, start)

    assert start + delta == end
    assert delta.years == -1
    assert delta.months == -3
    assert delta.days == -5
    assert delta.hours == -6
    assert delta.minutes == -15


@pytest.mark.parametrize(
    ("dt1", "dt2"),
    [
        ("2024-01-01", datetime.date(2024, 1, 1)),
        (datetime.date(2024, 1, 1), object()),
    ],
)
def test_difference_requires_date_or_datetime_operands(dt1, dt2):
    with pytest.raises(TypeError, match="relativedelta only diffs datetime/date"):
        relativedelta(dt1, dt2)


def test_weekday_equality_treats_unspecified_n_as_first_occurrence():
    assert relativedelta(weekday=MO) == relativedelta(weekday=MO(+1))
    assert relativedelta(weekday=MO) != relativedelta(weekday=MO(+2))
    assert relativedelta(weekday=MO) != relativedelta(weekday=TU)
    assert relativedelta(weekday=MO) != relativedelta()
    assert relativedelta(days=1).__eq__(object()) is NotImplemented


def test_hash_is_consistent_for_equal_deltas():
    assert hash(relativedelta(days=1, weekday=SA)) == hash(relativedelta(days=1, weekday=SA))


def test_repr_includes_non_zero_relative_and_absolute_values():
    value = repr(
        relativedelta(
            years=1,
            months=-2,
            days=3,
            leapdays=-1,
            hour=10,
            weekday=FR(-1),
        )
    )

    assert value == "relativedelta(years=+1, months=-2, days=+3, leapdays=-1, weekday=FR(-1), hour=10)"