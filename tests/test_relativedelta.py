import pytest
import datetime
from src.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU


class TestRelativeDeltaInit:
    def test_basic_initialization(self):
        rd = relativedelta(years=1, months=2, days=3)
        assert rd.years == 1
        assert rd.months == 2
        assert rd.days == 3
        
    def test_time_initialization(self):
        rd = relativedelta(hours=5, minutes=30, seconds=15, microseconds=1000)
        assert rd.hours == 5
        assert rd.minutes == 30
        assert rd.seconds == 15
        assert rd.microseconds == 1000
        
    def test_absolute_parameters(self):
        rd = relativedelta(year=2020, month=5, day=15, hour=10, minute=30, second=45)
        assert rd.year == 2020
        assert rd.month == 5
        assert rd.day == 15
        assert rd.hour == 10
        assert rd.minute == 30
        assert rd.second == 45
        
    def test_weeks_parameter(self):
        rd = relativedelta(weeks=2, days=3)
        assert rd.days == 17
        
    def test_default_values(self):
        rd = relativedelta()
        assert rd.years == 0
        assert rd.months == 0
        assert rd.days == 0
        assert rd.hours == 0
        assert rd.minutes == 0
        assert rd.seconds == 0
        assert rd.microseconds == 0
        
    def test_two_dates_datetime(self):
        dt1 = datetime.datetime(2020, 3, 15, 10, 30)
        dt2 = datetime.datetime(2019, 1, 10, 8, 20)
        rd = relativedelta(dt1, dt2)
        assert rd.years == 1
        assert rd.months == 2
        
    def test_two_dates_date(self):
        dt1 = datetime.date(2020, 3, 15)
        dt2 = datetime.date(2019, 1, 10)
        rd = relativedelta(dt1, dt2)
        assert rd.years == 1
        assert rd.months == 2
        
    def test_two_dates_mixed_types(self):
        dt1 = datetime.datetime(2020, 3, 15)
        dt2 = datetime.date(2019, 1, 10)
        rd = relativedelta(dt1, dt2)
        assert rd.years == 1
        assert rd.months == 2
        
    def test_two_dates_invalid_type(self):
        with pytest.raises(TypeError):
            relativedelta("2020-01-01", "2019-01-01")
            
    def test_non_integer_years_raises_error(self):
        with pytest.raises(ValueError):
            relativedelta(years=1.5)
            
    def test_non_integer_months_raises_error(self):
        with pytest.raises(ValueError):
            relativedelta(months=2.7)
            
    def test_weekday_with_integer(self):
        rd = relativedelta(weekday=0)
        assert rd.weekday == MO
        
    def test_weekday_with_weekday_object(self):
        rd = relativedelta(weekday=MO)
        assert rd.weekday == MO
        
    def test_yearday_basic(self):
        rd = relativedelta(yearday=100)
        assert rd.month == 4
        assert rd.day == 10
        
    def test_yearday_after_feb(self):
        rd = relativedelta(yearday=60)
        assert rd.month == 3
        assert rd.day == 1
        assert rd.leapdays == -1
        
    def test_nlyearday(self):
        rd = relativedelta(nlyearday=60)
        assert rd.month == 3
        assert rd.day == 1
        
    def test_invalid_yearday(self):
        with pytest.raises(ValueError):
            relativedelta(yearday=400)


class TestRelativeDeltaAddition:
    def test_add_to_datetime(self):
        dt = datetime.datetime(2020, 1, 15, 10, 30)
        rd = relativedelta(months=2, days=5)
        result = dt + rd
        assert result == datetime.datetime(2020, 3, 20, 10, 30)
        
    def test_radd_to_datetime(self):
        dt = datetime.datetime(2020, 1, 15, 10, 30)
        rd = relativedelta(months=2, days=5)
        result = rd + dt
        assert result == datetime.datetime(2020, 3, 20, 10, 30)
        
    def test_add_to_date(self):
        dt = datetime.date(2020, 1, 15)
        rd = relativedelta(months=2, days=5)
        result = dt + rd
        assert result == datetime.date(2020, 3, 20)
        
    def test_add_years(self):
        dt = datetime.date(2020, 1, 15)
        rd = relativedelta(years=2)
        result = dt + rd
        assert result == datetime.date(2022, 1, 15)
        
    def test_add_months_overflow(self):
        dt = datetime.date(2020, 10, 15)
        rd = relativedelta(months=5)
        result = dt + rd
        assert result == datetime.date(2021, 3, 15)
        
    def test_add_days_adjustment_for_month_end(self):
        dt = datetime.date(2020, 1, 31)
        rd = relativedelta(months=1)
        result = dt + rd
        assert result == datetime.date(2020, 2, 29)
        
    def test_add_negative_months(self):
        dt = datetime.date(2020, 3, 15)
        rd = relativedelta(months=-2)
        result = dt + rd
        assert result == datetime.date(2020, 1, 15)
        
    def test_add_with_absolute_year(self):
        dt = datetime.date(2020, 3, 15)
        rd = relativedelta(year=2025)
        result = dt + rd
        assert result.year == 2025
        
    def test_add_with_absolute_month(self):
        dt = datetime.date(2020, 3, 15)
        rd = relativedelta(month=12)
        result = dt + rd
        assert result.month == 12
        
    def test_add_with_absolute_day(self):
        dt = datetime.date(2020, 3, 15)
        rd = relativedelta(day=1)
        result = dt + rd
        assert result.day == 1
        
    def test_add_with_time_components(self):
        dt = datetime.datetime(2020, 1, 15, 10, 30, 45)
        rd = relativedelta(hours=2, minutes=15, seconds=30)
        result = dt + rd
        assert result == datetime.datetime(2020, 1, 15, 12, 46, 15)
        
    def test_add_with_absolute_time(self):
        dt = datetime.datetime(2020, 1, 15, 10, 30, 45)
        rd = relativedelta(hour=15, minute=0, second=0)
        result = dt + rd
        assert result == datetime.datetime(2020, 1, 15, 15, 0, 0)
        
    def test_add_relativedeltas(self):
        rd1 = relativedelta(years=1, months=2)
        rd2 = relativedelta(months=3, days=5)
        result = rd1 + rd2
        assert result.years == 1
        assert result.months == 5
        assert result.days == 5
        
    def test_add_timedelta(self):
        rd = relativedelta(months=1)
        td = datetime.timedelta(days=5, hours=3)
        result = rd + td
        assert result.months == 1
        assert result.days == 5
        assert result.hours == 3
        
    def test_add_with_weekday(self):
        dt = datetime.date(2020, 1, 15)
        rd = relativedelta(weekday=MO)
        result = dt + rd
        assert result.weekday() == 0
        
    def test_add_with_weekday_nth(self):
        dt = datetime.date(2020, 1, 1)
        rd = relativedelta(day=1, weekday=MO(2))
        result = dt + rd
        assert result == datetime.date(2020, 1, 13)
        
    def test_add_with_leapdays(self):
        dt = datetime.date(2020, 1, 1)
        rd = relativedelta(years=1, leapdays=1)
        result = dt + rd
        assert result == datetime.date(2021, 1, 1)


class TestRelativeDeltaSubtraction:
    def test_subtract_relativedeltas(self):
        rd1 = relativedelta(years=3, months=5, days=10)
        rd2 = relativedelta(years=1, months=2, days=3)
        result = rd1 - rd2
        assert result.years == 2
        assert result.months == 3
        assert result.days == 7
        
    def test_rsub_from_datetime(self):
        dt = datetime.datetime(2020, 3, 15, 10, 30)
        rd = relativedelta(months=2, days=5)
        result = dt - rd
        assert result == datetime.datetime(2020, 1, 10, 10, 30)
        
    def test_subtract_with_time(self):
        rd1 = relativedelta(hours=5, minutes=30)
        rd2 = relativedelta(hours=2, minutes=15)
        result = rd1 - rd2
        assert result.hours == 3
        assert result.minutes == 15
        
    def test_subtract_negative_values(self):
        rd1 = relativedelta(months=2)
        rd2 = relativedelta(months=5)
        result = rd1 - rd2
        assert result.months == -3


class TestRelativeDeltaNegation:
    def test_neg_positive_values(self):
        rd = relativedelta(years=1, months=2, days=3, hours=4)
        result = -rd
        assert result.years == -1
        assert result.months == -2
        assert result.days == -3
        assert result.hours == -4
        
    def test_neg_negative_values(self):
        rd = relativedelta(years=-1, months=-2)
        result = -rd
        assert result.years == 1
        assert result.months == 2
        
    def test_neg_preserves_absolute_values(self):
        rd = relativedelta(years=1, year=2025)
        result = -rd
        assert result.years == -1
        assert result.year == 2025


class TestRelativeDeltaAbsolute:
    def test_abs_positive_values(self):
        rd = relativedelta(years=1, months=2, days=3)
        result = abs(rd)
        assert result.years == 1
        assert result.months == 2
        assert result.days == 3
        
    def test_abs_negative_values(self):
        rd = relativedelta(years=-1, months=-2, days=-3, hours=-4)
        result = abs(rd)
        assert result.years == 1
        assert result.months == 2
        assert result.days == 3
        assert result.hours == 4
        
    def test_abs_mixed_values(self):
        rd = relativedelta(years=1, months=-2, days=3)
        result = abs(rd)
        assert result.years == 1
        assert result.months == 2
        assert result.days == 3


class TestRelativeDeltaMultiplication:
    def test_mul_by_integer(self):
        rd = relativedelta(years=1, months=2, days=3)
        result = rd * 2
        assert result.years == 2
        assert result.months == 4
        assert result.days == 6
        
    def test_mul_by_float(self):
        rd = relativedelta(years=2, months=4, days=10)
        result = rd * 0.5
        assert result.years == 1
        assert result.months == 2
        assert result.days == 5
        
    def test_rmul(self):
        rd = relativedelta(years=1, months=2)
        result = 3 * rd
        assert result.years == 3
        assert result.months == 6
        
    def test_mul_preserves_absolute_values(self):
        rd = relativedelta(years=1, year=2025)
        result = rd * 2
        assert result.years == 2
        assert result.year == 2025


class TestRelativeDeltaDivision:
    def test_div_by_integer(self):
        rd = relativedelta(years=4, months=8, days=12)
        result = rd / 2
        assert result.years == 2
        assert result.months == 4
        assert result.days == 6
        
    def test_div_by_float(self):
        rd = relativedelta(years=2, months=6)
        result = rd / 0.5
        assert result.years == 5
        assert result.months == 0
        
    def test_truediv(self):
        rd = relativedelta(days=10)
        result = rd / 2
        assert result.days == 5


class TestRelativeDeltaEquality:
    def test_equality_same_values(self):
        rd1 = relativedelta(years=1, months=2, days=3)
        rd2 = relativedelta(years=1, months=2, days=3)
        assert rd1 == rd2
        
    def test_equality_different_values(self):
        rd1 = relativedelta(years=1, months=2)
        rd2 = relativedelta(years=1, months=3)
        assert rd1 != rd2
        
    def test_equality_with_absolute_values(self):
        rd1 = relativedelta(years=1, year=2025, month=5)
        rd2 = relativedelta(years=1, year=2025, month=5)
        assert rd1 == rd2
        
    def test_inequality(self):
        rd1 = relativedelta(years=1)
        rd2 = relativedelta(years=2)
        assert rd1 != rd2
        
    def test_equality_with_weekday(self):
        rd1 = relativedelta(weeks=1, weekday=MO)
        rd2 = relativedelta(weeks=1, weekday=MO)
        assert rd1 == rd2
        
    def test_inequality_with_weekday(self):
        rd1 = relativedelta(weeks=1, weekday=MO)
        rd2 = relativedelta(weeks=1, weekday=TU)
        assert rd1 != rd2


class TestRelativeDeltaHash:
    def test_hash_consistency(self):
        rd1 = relativedelta(years=1, months=2, days=3)
        rd2 = relativedelta(years=1, months=2, days=3)
        assert hash(rd1) == hash(rd2)
        
    def test_hash_different_values(self):
        rd1 = relativedelta(years=1, months=2)
        rd2 = relativedelta(years=1, months=3)
        assert hash(rd1) != hash(rd2)
        
    def test_hash_allows_set_membership(self):
        rd1 = relativedelta(years=1)
        rd2 = relativedelta(years=1)
        rd3 = relativedelta(years=2)
        s = {rd1, rd2, rd3}
        assert len(s) == 2


class TestRelativeDeltaBoolean:
    def test_bool_empty_relativedelta(self):
        rd = relativedelta()
        assert not rd
        
    def test_bool_with_years(self):
        rd = relativedelta(years=1)
        assert rd
        
    def test_bool_with_months(self):
        rd = relativedelta(months=1)
        assert rd
        
    def test_bool_with_days(self):
        rd = relativedelta(days=1)
        assert rd
        
    def test_bool_with_time(self):
        rd = relativedelta(hours=1)
        assert rd
        
    def test_bool_with_absolute_year(self):
        rd = relativedelta(year=2025)
        assert rd
        
    def test_bool_with_weekday(self):
        rd = relativedelta(weekday=MO)
        assert rd


class TestRelativeDeltaWeeksProperty:
    def test_weeks_getter(self):
        rd = relativedelta(days=14)
        assert rd.weeks == 2
        
    def test_weeks_getter_with_remainder(self):
        rd = relativedelta(days=17)
        assert rd.weeks == 2
        
    def test_weeks_setter(self):
        rd = relativedelta(days=5)
        rd.weeks = 3
        assert rd.days == 26
        
    def test_weeks_setter_replaces_weeks(self):
        rd = relativedelta(days=21)
        rd.weeks = 1
        assert rd.days == 7


class TestRelativeDeltaNormalized:
    def test_normalized_basic(self):
        rd = relativedelta(days=1.5, hours=12)
        normalized = rd.normalized()
        assert normalized.days == 2
        assert normalized.hours == 0
        
    def test_normalized_with_overflow(self):
        rd = relativedelta(hours=25.5)
        normalized = rd.normalized()
        assert normalized.days == 1
        assert normalized.hours == 1
        
    def test_normalized_preserves_other_fields(self):
        rd = relativedelta(years=1, months=2, days=1.5, year=2025)
        normalized = rd.normalized()
        assert normalized.years == 1
        assert normalized.months == 2
        assert normalized.year == 2025


class TestRelativeDeltaFix:
    def test_fix_microseconds_overflow(self):
        rd = relativedelta(microseconds=2000000)
        assert rd.microseconds < 1000000
        assert rd.seconds >= 2
        
    def test_fix_seconds_overflow(self):
        rd = relativedelta(seconds=120)
        assert rd.seconds == 0
        assert rd.minutes == 2
        
    def test_fix_minutes_overflow(self):
        rd = relativedelta(minutes=120)
        assert rd.minutes == 0
        assert rd.hours == 2
        
    def test_fix_hours_overflow(self):
        rd = relativedelta(hours=48)
        assert rd.hours == 0
        assert rd.days == 2
        
    def test_fix_months_overflow(self):
        rd = relativedelta(months=14)
        assert rd.months == 2
        assert rd.years == 1
        
    def test_fix_has_time_flag_with_hours(self):
        rd = relativedelta(hours=1)
        assert rd._has_time == 1
        
    def test_fix_has_time_flag_without_time(self):
        rd = relativedelta(days=1)
        assert rd._has_time == 0


class TestRelativeDeltaRepr:
    def test_repr_basic(self):
        rd = relativedelta(years=1, months=2, days=3)
        repr_str = repr(rd)
        assert "years=+1" in repr_str
        assert "months=+2" in repr_str
        assert "days=+3" in repr_str
        
    def test_repr_with_absolute_values(self):
        rd = relativedelta(years=1, year=2025, month=5)
        repr_str = repr(rd)
        assert "years=+1" in repr_str
        assert "year=2025" in repr_str
        assert "month=5" in repr_str
        
    def test_repr_empty(self):
        rd = relativedelta()
        repr_str = repr(rd)
        assert repr_str == "relativedelta()"


class TestRelativeDeltaEdgeCases:
    def test_leap_year_handling(self):
        dt = datetime.date(2020, 2, 29)
        rd = relativedelta(years=1)
        result = dt + rd
        assert result == datetime.date(2021, 2, 28)
        
    def test_month_end_to_shorter_month(self):
        dt = datetime.date(2020, 1, 31)
        rd = relativedelta(months=1)
        result = dt + rd
        assert result == datetime.date(2020, 2, 29)
        
    def test_month_end_to_even_shorter_month(self):
        dt = datetime.date(2020, 3, 31)
        rd = relativedelta(months=1)
        result = dt + rd
        assert result == datetime.date(2020, 4, 30)
        
    def test_negative_date_arithmetic(self):
        dt = datetime.date(2020, 3, 15)
        rd = relativedelta(years=-1, months=-2)
        result = dt + rd
        assert result == datetime.date(2019, 1, 15)
        
    def test_combine_relative_and_absolute(self):
        dt = datetime.date(2020, 1, 15)
        rd = relativedelta(months=2, day=1)
        result = dt + rd
        assert result == datetime.date(2020, 3, 1)
        
    def test_date_to_datetime_conversion(self):
        dt = datetime.date(2020, 1, 15)
        rd = relativedelta(hours=10)
        result = dt + rd
        assert isinstance(result, datetime.datetime)
        assert result == datetime.datetime(2020, 1, 15, 10, 0)
        
    def test_large_values(self):
        rd = relativedelta(years=100, months=1200)
        assert rd.years == 200
        assert rd.months == 0
        
    def test_microseconds_precision(self):
        rd = relativedelta(microseconds=500000)
        assert rd.microseconds == 500000
        assert rd.seconds == 0
        
    def test_weekday_last_occurrence(self):
        dt = datetime.date(2020, 1, 31)
        rd = relativedelta(day=31, weekday=MO(-1))
        result = dt + rd
        assert result.weekday() == 0
        
    def test_two_dates_backward_difference(self):
        dt1 = datetime.date(2019, 1, 10)
        dt2 = datetime.date(2020, 3, 15)
        rd = relativedelta(dt1, dt2)
        assert rd.years == -1
        assert rd.months == -2