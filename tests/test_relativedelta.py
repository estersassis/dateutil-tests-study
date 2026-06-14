# pylint: disable=protected-access
from datetime import date, datetime, timedelta

import pytest

from src.relativedelta import MO, WE, relativedelta


def test_diff_between_datetimes_roundtrip():
    start = datetime(2020, 1, 15, 8, 3, 5, 123456)
    end = datetime(2022, 5, 20, 16, 18, 55, 654321)
    delta = relativedelta(end, start)
    assert start + delta == end
    assert end - delta == start


def test_diff_raises_type_error_for_non_date():
    with pytest.raises(TypeError):
        relativedelta("2020-01-01", datetime(2020, 1, 1))


def test_non_integer_years_or_months_are_rejected():
    with pytest.raises(ValueError):
        relativedelta(years=1.2)
    with pytest.raises(ValueError):
        relativedelta(months=3.5)


def test_absolute_values_emit_deprecation_warning():
    with pytest.warns(DeprecationWarning):
        relativedelta(year=2021.5)


def test_weekday_integer_becomes_weekday_object():
    delta = relativedelta(weekday=2)
    assert delta.weekday == WE


def test_year_day_and_non_leap_year_day_translate_to_month_day():
    delta = relativedelta(yearday=60)
    assert (delta.month, delta.day) == (3, 1)
    assert delta.leapdays == -1

    delta_nly = relativedelta(nlyearday=365)
    assert (delta_nly.month, delta_nly.day) == (12, 31)


def test_invalid_year_day_raises():
    with pytest.raises(ValueError):
        relativedelta(yearday=400)


def test_weeks_property_adjusts_days():
    delta = relativedelta(days=10)
    delta.weeks = 2
    assert delta.days == 17
    assert delta.weeks == 2


def test_set_months_normalizes_years():
    delta = relativedelta()
    delta._set_months(25)
    assert delta.months == 1
    assert delta.years == 2

    delta._set_months(-14)
    assert delta.months == -2
    assert delta.years == -1


def test_normalized_moves_fractional_units_into_smaller_parts():
    delta = relativedelta(days=1.5, hours=2.0, minutes=30.0, seconds=15.5, microseconds=500000)
    normalized = delta.normalized()
    assert normalized.days == 1
    assert normalized.hours == 14  # 2 + 24 * 0.5
    assert normalized.minutes == 30
    assert normalized.seconds == 16  # seconds gained from overflowing microseconds
    assert normalized.microseconds == 0


def test_add_rel_delta_prefers_other_absolute_fields():
    base = relativedelta(month=5, day=10, leapdays=3)
    override = relativedelta(month=9, day=20, leapdays=0)
    combined = base + override
    assert combined.month == 9
    assert combined.day == 20
    assert combined.leapdays == 3


def test_add_datetime_handles_month_overflow_and_leapdays():
    base = datetime(2020, 1, 31)
    result = base + relativedelta(months=1)
    assert result.month == 2
    assert result.day == 29

    non_leap = datetime(2021, 3, 1)
    non_leap_result = non_leap + relativedelta(leapdays=1)
    assert non_leap_result == non_leap

    leap = datetime(2020, 3, 1)
    leap_result = leap + relativedelta(leapdays=1)
    assert leap_result == datetime(2020, 3, 2)


def test_add_weekday_respects_nth_monday_with_month_shift():
    march_second = datetime(2021, 3, 2)
    result = march_second + relativedelta(months=1, weekday=MO(1))
    assert result == datetime(2021, 4, 5)


def test_add_date_with_time_fields_becomes_datetime():
    base_date = date(2021, 5, 1)
    result = base_date + relativedelta(hours=3)
    assert isinstance(result, datetime)
    assert result.hour == 3


def test_addition_with_timedelta_and_reflected_addition():
    delta = relativedelta(days=2, hours=5)
    addition = delta + timedelta(days=3, seconds=3600)
    assert addition.days == 5
    assert addition.hours == 6
    assert addition.seconds == 0
    reflected = timedelta(days=1) + delta
    assert reflected.days == delta.days + 1


def test_subtract_rel_delta_combines_fields():
    a = relativedelta(days=5, months=2)
    b = relativedelta(days=2, months=1)
    diff = a - b
    assert diff.days == 3
    assert diff.months == 1


def test_abs_and_negate_flip_signs_without_altering_absolute_information():
    delta = relativedelta(months=-3, days=-5, year=2022)
    assert abs(delta).months == 3
    assert (-delta).months == 3
    assert (-delta).year == 2022


def test_bool_behaves_like_non_zero_check():
    assert not relativedelta()
    assert relativedelta(seconds=1)


def test_mul_and_div_use_integer_components():
    delta = relativedelta(days=3, hours=4)
    scaled = delta * 0.5
    assert scaled.days == 1
    assert scaled.hours == 2

    halved = delta / 2
    assert halved == scaled


def test_eq_and_hash_include_weekday_logic():
    a = relativedelta(days=1, weekday=MO(1))
    b = relativedelta(days=1, weekday=MO(1))
    c = relativedelta(days=1, weekday=MO(2))
    assert a == b
    assert hash(a) == hash(b)
    assert a != c


def test_repr_includes_activen_fields():
    delta = relativedelta(months=1, day=5, hours=3)
    text = repr(delta)
    assert "months" in text
    assert "day" in text
    assert "hours" in text