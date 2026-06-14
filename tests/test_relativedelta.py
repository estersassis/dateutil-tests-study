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


class TestRelativeDeltaComplexScenarios:
    def test_multiple_month_additions_over_year_boundary(self):
        dt = datetime.date(2020, 11, 15)
        rd = relativedelta(months=3)
        result = dt + rd
        assert result == datetime.date(2021, 2, 15)
        
    def test_negative_months_under_year_boundary(self):
        dt = datetime.date(2021, 2, 15)
        rd = relativedelta(months=-4)
        result = dt + rd
        assert result == datetime.date(2020, 10, 15)
        
    def test_chained_additions(self):
        dt = datetime.date(2020, 1, 15)
        rd1 = relativedelta(months=2)
        rd2 = relativedelta(days=10)
        result = dt + rd1 + rd2
        assert result == datetime.date(2020, 3, 25)
        
    def test_addition_with_multiple_absolute_values(self):
        dt = datetime.datetime(2020, 3, 15, 10, 30, 45)
        rd = relativedelta(year=2025, month=12, day=25, hour=15, minute=0, second=0)
        result = dt + rd
        assert result == datetime.datetime(2025, 12, 25, 15, 0, 0)
        
    def test_relative_and_absolute_combined(self):
        dt = datetime.date(2020, 1, 15)
        rd = relativedelta(years=1, months=2, day=1)
        result = dt + rd
        assert result == datetime.date(2021, 3, 1)
        
    def test_subtraction_resulting_in_negative(self):
        dt = datetime.date(2020, 1, 15)
        rd = relativedelta(months=6)
        result = dt - rd
        assert result == datetime.date(2019, 7, 15)
        
    def test_weekday_with_specific_occurrence(self):
        dt = datetime.date(2020, 1, 1)
        rd = relativedelta(day=1, weekday=FR(3))
        result = dt + rd
        assert result == datetime.date(2020, 1, 17)
        
    def test_last_weekday_of_month(self):
        dt = datetime.date(2020, 1, 1)
        rd = relativedelta(day=31, weekday=FR(-1))
        result = dt + rd
        assert result == datetime.date(2020, 1, 31)
        
    def test_microsecond_precision_in_datetime(self):
        dt = datetime.datetime(2020, 1, 1, 0, 0, 0, 100000)
        rd = relativedelta(microseconds=50000)
        result = dt + rd
        assert result.microsecond == 150000
        
    def test_leap_year_february_29(self):
        dt = datetime.date(2020, 2, 29)
        rd = relativedelta(years=4)
        result = dt + rd
        assert result == datetime.date(2024, 2, 29)
        
    def test_non_leap_year_february_adjustment(self):
        dt = datetime.date(2020, 2, 29)
        rd = relativedelta(years=1)
        result = dt + rd
        assert result == datetime.date(2021, 2, 28)
        
    def test_month_end_adjustment_january_to_february(self):
        dt = datetime.date(2019, 1, 31)
        rd = relativedelta(months=1)
        result = dt + rd
        assert result == datetime.date(2019, 2, 28)
        
    def test_add_zero_relativedelta(self):
        dt = datetime.date(2020, 1, 15)
        rd = relativedelta()
        result = dt + rd
        assert result == datetime.date(2020, 1, 15)
        
    def test_complex_time_calculation(self):
        dt = datetime.datetime(2020, 1, 1, 23, 50, 30)
        rd = relativedelta(hours=2, minutes=20, seconds=45)
        result = dt + rd
        assert result == datetime.datetime(2020, 1, 2, 2, 11, 15)
        
    def test_large_day_values(self):
        rd = relativedelta(days=365)
        dt = datetime.date(2020, 1, 1)
        result = dt + rd
        assert result == datetime.date(2020, 12, 31)
        
    def test_negative_years_subtraction(self):
        dt = datetime.date(2020, 1, 15)
        rd = relativedelta(years=-5)
        result = dt + rd
        assert result == datetime.date(2015, 1, 15)


class TestRelativeDeltaWeekdays:
    def test_all_weekdays_exist(self):
        assert MO is not None
        assert TU is not None
        assert WE is not None
        assert TH is not None
        assert FR is not None
        assert SA is not None
        assert SU is not None
        
    def test_weekday_monday(self):
        dt = datetime.date(2020, 1, 1)
        rd = relativedelta(weekday=MO)
        result = dt + rd
        assert result.weekday() == 0
        
    def test_weekday_tuesday(self):
        dt = datetime.date(2020, 1, 1)
        rd = relativedelta(weekday=TU)
        result = dt + rd
        assert result.weekday() == 1
        
    def test_weekday_wednesday(self):
        dt = datetime.date(2020, 1, 1)
        rd = relativedelta(weekday=WE)
        result = dt + rd
        assert result.weekday() == 2
        
    def test_weekday_thursday(self):
        dt = datetime.date(2020, 1, 1)
        rd = relativedelta(weekday=TH)
        result = dt + rd
        assert result.weekday() == 3
        
    def test_weekday_friday(self):
        dt = datetime.date(2020, 1, 1)
        rd = relativedelta(weekday=FR)
        result = dt + rd
        assert result.weekday() == 4
        
    def test_weekday_saturday(self):
        dt = datetime.date(2020, 1, 1)
        rd = relativedelta(weekday=SA)
        result = dt + rd
        assert result.weekday() == 5
        
    def test_weekday_sunday(self):
        dt = datetime.date(2020, 1, 1)
        rd = relativedelta(weekday=SU)
        result = dt + rd
        assert result.weekday() == 6
        
    def test_second_monday_of_month(self):
        dt = datetime.date(2020, 1, 1)
        rd = relativedelta(day=1, weekday=MO(2))
        result = dt + rd
        assert result == datetime.date(2020, 1, 13)
        
    def test_third_friday_of_month(self):
        dt = datetime.date(2020, 1, 1)
        rd = relativedelta(day=1, weekday=FR(3))
        result = dt + rd
        assert result == datetime.date(2020, 1, 17)


class TestRelativeDeltaDateTimeMixed:
    def test_date_with_time_components_becomes_datetime(self):
        dt = datetime.date(2020, 1, 15)
        rd = relativedelta(hours=10, minutes=30)
        result = dt + rd
        assert isinstance(result, datetime.datetime)
        assert result.hour == 10
        assert result.minute == 30
        
    def test_datetime_with_date_only_delta(self):
        dt = datetime.datetime(2020, 1, 15, 10, 30)
        rd = relativedelta(months=2)
        result = dt + rd
        assert isinstance(result, datetime.datetime)
        assert result.hour == 10
        assert result.minute == 30
        
    def test_mixed_date_types_in_diff(self):
        dt1 = datetime.datetime(2020, 3, 15, 10, 30)
        dt2 = datetime.date(2019, 1, 10)
        rd = relativedelta(dt1, dt2)
        assert rd.years == 1
        assert rd.months == 2


class TestRelativeDeltaYearDay:
    def test_yearday_january(self):
        rd = relativedelta(yearday=15)
        assert rd.month == 1
        assert rd.day == 15
        
    def test_yearday_february(self):
        rd = relativedelta(yearday=45)
        assert rd.month == 2
        assert rd.day == 14
        
    def test_yearday_march(self):
        rd = relativedelta(yearday=75)
        assert rd.month == 3
        assert rd.day == 16
        
    def test_yearday_december(self):
        rd = relativedelta(yearday=365)
        assert rd.month == 12
        assert rd.day == 31
        
    def test_yearday_end_of_february_nonleap(self):
        rd = relativedelta(yearday=59)
        assert rd.month == 2
        assert rd.day == 28
        
    def test_nlyearday_no_leapday_adjustment(self):
        rd = relativedelta(nlyearday=60)
        assert rd.month == 3
        assert rd.day == 1
        assert rd.leapdays == 0


class TestRelativeDeltaArithmeticCombinations:
    def test_add_three_relativedeltas(self):
        rd1 = relativedelta(years=1)
        rd2 = relativedelta(months=2)
        rd3 = relativedelta(days=3)
        result = rd1 + rd2 + rd3
        assert result.years == 1
        assert result.months == 2
        assert result.days == 3
        
    def test_subtract_and_add_relativedeltas(self):
        rd1 = relativedelta(years=5, months=10)
        rd2 = relativedelta(years=2, months=3)
        rd3 = relativedelta(months=1)
        result = rd1 - rd2 + rd3
        assert result.years == 3
        assert result.months == 8
        
    def test_multiply_then_add(self):
        rd1 = relativedelta(months=2)
        rd2 = rd1 * 3
        rd3 = relativedelta(days=5)
        result = rd2 + rd3
        assert result.months == 6
        assert result.days == 5
        
    def test_divide_then_subtract(self):
        rd1 = relativedelta(days=20)
        rd2 = rd1 / 2
        rd3 = relativedelta(days=3)
        result = rd2 - rd3
        assert result.days == 7


class TestRelativeDeltaOverflow:
    def test_seconds_to_minutes_conversion(self):
        rd = relativedelta(seconds=180)
        assert rd.minutes == 3
        assert rd.seconds == 0
        
    def test_minutes_to_hours_conversion(self):
        rd = relativedelta(minutes=180)
        assert rd.hours == 3
        assert rd.minutes == 0
        
    def test_hours_to_days_conversion(self):
        rd = relativedelta(hours=72)
        assert rd.days == 3
        assert rd.hours == 0
        
    def test_months_to_years_conversion(self):
        rd = relativedelta(months=24)
        assert rd.years == 2
        assert rd.months == 0
        
    def test_combined_overflow(self):
        rd = relativedelta(months=13, hours=25, minutes=61, seconds=61)
        assert rd.years == 1
        assert rd.months == 1
        assert rd.days == 1
        assert rd.hours == 2
        assert rd.minutes == 2
        assert rd.seconds == 1
        
    def test_negative_overflow(self):
        rd = relativedelta(seconds=-120)
        assert rd.minutes == -2
        assert rd.seconds == 0


class TestRelativeDeltaNotImplemented:
    def test_add_unsupported_type_raises_typeerror(self):
        rd = relativedelta(days=1)
        with pytest.raises(TypeError):
            rd + "invalid"
        
    def test_subtract_unsupported_type_raises_typeerror(self):
        rd = relativedelta(days=1)
        with pytest.raises(TypeError):
            rd - "invalid"
        
    def test_multiply_unsupported_type_raises_error(self):
        rd = relativedelta(days=1)
        with pytest.raises(ValueError):
            rd * "invalid"
        
    def test_divide_unsupported_type_raises_error(self):
        rd = relativedelta(days=1)
        with pytest.raises(ValueError):
            rd / "invalid"
        
    def test_equality_with_different_type(self):
        rd = relativedelta(days=1)
        result = rd == "invalid"
        assert result is False


class TestRelativeDeltaLeapDays:
    def test_leapdays_parameter(self):
        rd = relativedelta(leapdays=1)
        assert rd.leapdays == 1
        
    def test_leapdays_in_leap_year(self):
        dt = datetime.date(2020, 1, 1)
        rd = relativedelta(years=1, leapdays=1)
        result = dt + rd
        assert result == datetime.date(2021, 1, 1)
        
    def test_leapdays_applied_after_february(self):
        dt = datetime.date(2020, 3, 1)
        rd = relativedelta(years=1, leapdays=1)
        result = dt + rd
        assert result == datetime.date(2021, 3, 1)


class TestRelativeDeltaAbsoluteTimeFields:
    def test_absolute_hour_replaces_current(self):
        dt = datetime.datetime(2020, 1, 1, 10, 30, 45)
        rd = relativedelta(hour=15)
        result = dt + rd
        assert result.hour == 15
        assert result.minute == 30
        assert result.second == 45
        
    def test_absolute_minute_replaces_current(self):
        dt = datetime.datetime(2020, 1, 1, 10, 30, 45)
        rd = relativedelta(minute=0)
        result = dt + rd
        assert result.minute == 0
        
    def test_absolute_second_replaces_current(self):
        dt = datetime.datetime(2020, 1, 1, 10, 30, 45)
        rd = relativedelta(second=0)
        result = dt + rd
        assert result.second == 0
        
    def test_absolute_microsecond_replaces_current(self):
        dt = datetime.datetime(2020, 1, 1, 10, 30, 45, 500000)
        rd = relativedelta(microsecond=0)
        result = dt + rd
        assert result.microsecond == 0


class TestRelativeDeltaMonthBoundaries:
    def test_january_31_to_february(self):
        dt = datetime.date(2020, 1, 31)
        rd = relativedelta(months=1)
        result = dt + rd
        assert result == datetime.date(2020, 2, 29)
        
    def test_march_31_to_april(self):
        dt = datetime.date(2020, 3, 31)
        rd = relativedelta(months=1)
        result = dt + rd
        assert result == datetime.date(2020, 4, 30)
        
    def test_may_31_to_june(self):
        dt = datetime.date(2020, 5, 31)
        rd = relativedelta(months=1)
        result = dt + rd
        assert result == datetime.date(2020, 6, 30)
        
    def test_august_31_to_september(self):
        dt = datetime.date(2020, 8, 31)
        rd = relativedelta(months=1)
        result = dt + rd
        assert result == datetime.date(2020, 9, 30)
        
    def test_october_31_to_november(self):
        dt = datetime.date(2020, 10, 31)
        rd = relativedelta(months=1)
        result = dt + rd
        assert result == datetime.date(2020, 11, 30)


class TestRelativeDeltaZeroValues:
    def test_zero_years(self):
        rd = relativedelta(years=0)
        assert rd.years == 0
        assert not rd
        
    def test_zero_all_values(self):
        rd = relativedelta(years=0, months=0, days=0, hours=0, minutes=0, seconds=0)
        assert not rd
        
    def test_add_zero_to_datetime(self):
        dt = datetime.datetime(2020, 1, 1, 10, 30)
        rd = relativedelta()
        result = dt + rd
        assert result == dt


class TestRelativeDeltaCopy:
    def test_addition_creates_new_instance(self):
        rd1 = relativedelta(years=1)
        rd2 = relativedelta(months=2)
        rd3 = rd1 + rd2
        assert rd3 is not rd1
        assert rd3 is not rd2
        
    def test_subtraction_creates_new_instance(self):
        rd1 = relativedelta(years=3)
        rd2 = relativedelta(years=1)
        rd3 = rd1 - rd2
        assert rd3 is not rd1
        assert rd3 is not rd2
        
    def test_negation_creates_new_instance(self):
        rd1 = relativedelta(years=1)
        rd2 = -rd1
        assert rd2 is not rd1
        
    def test_multiplication_creates_new_instance(self):
        rd1 = relativedelta(years=1)
        rd2 = rd1 * 2
        assert rd2 is not rd1


class TestRelativeDeltaTwoDatesDifference:
    def test_same_dates(self):
        dt = datetime.date(2020, 1, 15)
        rd = relativedelta(dt, dt)
        assert rd.years == 0
        assert rd.months == 0
        
    def test_one_month_difference(self):
        dt1 = datetime.date(2020, 2, 15)
        dt2 = datetime.date(2020, 1, 15)
        rd = relativedelta(dt1, dt2)
        assert rd.months == 1
        
    def test_one_year_difference(self):
        dt1 = datetime.date(2021, 1, 15)
        dt2 = datetime.date(2020, 1, 15)
        rd = relativedelta(dt1, dt2)
        assert rd.years == 1
        
    def test_difference_with_day_adjustment(self):
        dt1 = datetime.date(2020, 3, 1)
        dt2 = datetime.date(2020, 1, 31)
        rd = relativedelta(dt1, dt2)
        assert rd.months == 1
        
    def test_difference_with_time_components(self):
        dt1 = datetime.datetime(2020, 1, 15, 14, 30, 45)
        dt2 = datetime.datetime(2020, 1, 15, 10, 20, 30)
        rd = relativedelta(dt1, dt2)
        assert rd.hours == 4
        assert rd.minutes == 10
        assert rd.seconds == 15
        
    def test_difference_across_year_boundary(self):
        dt1 = datetime.date(2021, 2, 1)
        dt2 = datetime.date(2020, 11, 1)
        rd = relativedelta(dt1, dt2)
        assert rd.months == 3
        
    def test_difference_with_datetime_and_date(self):
        dt1 = datetime.datetime(2020, 3, 15, 10, 30)
        dt2 = datetime.date(2020, 1, 10)
        rd = relativedelta(dt1, dt2)
        assert rd.years == 0
        assert rd.months == 2


class TestRelativeDeltaMultipleOperations:
    def test_chain_multiple_additions_to_date(self):
        dt = datetime.date(2020, 1, 1)
        rd1 = relativedelta(months=1)
        rd2 = relativedelta(days=10)
        rd3 = relativedelta(years=1)
        result = dt + rd1 + rd2 + rd3
        assert result == datetime.date(2021, 2, 11)
        
    def test_add_and_subtract_chain(self):
        dt = datetime.date(2020, 6, 15)
        rd1 = relativedelta(months=3)
        rd2 = relativedelta(days=10)
        result = dt + rd1 - rd2
        assert result == datetime.date(2020, 9, 5)
        
    def test_multiple_absolute_values_last_wins(self):
        rd1 = relativedelta(year=2020)
        rd2 = relativedelta(year=2025)
        result = rd1 + rd2
        assert result.year == 2025


class TestRelativeDeltaNegativeValues:
    def test_negative_years(self):
        rd = relativedelta(years=-5)
        assert rd.years == -5
        
    def test_negative_months(self):
        rd = relativedelta(months=-3)
        assert rd.months == -3
        
    def test_negative_days(self):
        rd = relativedelta(days=-10)
        assert rd.days == -10
        
    def test_negative_time_components(self):
        rd = relativedelta(hours=-5, minutes=-30, seconds=-45)
        assert rd.hours == -5
        assert rd.minutes == -30
        assert rd.seconds == -45
        
    def test_add_negative_to_date(self):
        dt = datetime.date(2020, 6, 15)
        rd = relativedelta(months=-3)
        result = dt + rd
        assert result == datetime.date(2020, 3, 15)


class TestRelativeDeltaSpecialDates:
    def test_february_29_leap_year(self):
        dt = datetime.date(2020, 2, 29)
        assert dt.day == 29
        
    def test_add_to_february_29(self):
        dt = datetime.date(2020, 2, 29)
        rd = relativedelta(days=1)
        result = dt + rd
        assert result == datetime.date(2020, 3, 1)
        
    def test_subtract_from_february_29(self):
        dt = datetime.date(2020, 2, 29)
        rd = relativedelta(days=1)
        result = dt - rd
        assert result == datetime.date(2020, 2, 28)
        
    def test_year_end_date(self):
        dt = datetime.date(2020, 12, 31)
        rd = relativedelta(days=1)
        result = dt + rd
        assert result == datetime.date(2021, 1, 1)
        
    def test_year_start_date(self):
        dt = datetime.date(2020, 1, 1)
        rd = relativedelta(days=-1)
        result = dt + rd
        assert result == datetime.date(2019, 12, 31)


class TestRelativeDeltaPrecision:
    def test_microsecond_precision(self):
        dt = datetime.datetime(2020, 1, 1, 0, 0, 0, 0)
        rd = relativedelta(microseconds=1)
        result = dt + rd
        assert result.microsecond == 1
        
    def test_large_microseconds(self):
        dt = datetime.datetime(2020, 1, 1, 0, 0, 0, 0)
        rd = relativedelta(microseconds=999999)
        result = dt + rd
        assert result.microsecond == 999999
        
    def test_microseconds_overflow_to_seconds(self):
        rd = relativedelta(microseconds=1500000)
        assert rd.seconds == 1
        assert rd.microseconds == 500000


class TestRelativeDeltaWeekdayEdgeCases:
    def test_weekday_same_day(self):
        dt = datetime.date(2020, 1, 6)
        rd = relativedelta(weekday=MO)
        result = dt + rd
        assert result == datetime.date(2020, 1, 6)
        
    def test_first_weekday_of_month(self):
        dt = datetime.date(2020, 1, 1)
        rd = relativedelta(day=1, weekday=MO(1))
        result = dt + rd
        assert result.weekday() == 0
        assert result.day <= 7
        
    def test_fourth_weekday_of_month(self):
        dt = datetime.date(2020, 1, 1)
        rd = relativedelta(day=1, weekday=WE(4))
        result = dt + rd
        assert result.weekday() == 2
        assert 22 <= result.day <= 28


class TestRelativeDeltaAbsoluteAndRelativeMix:
    def test_relative_years_with_absolute_month(self):
        dt = datetime.date(2020, 6, 15)
        rd = relativedelta(years=1, month=12)
        result = dt + rd
        assert result.year == 2021
        assert result.month == 12
        
    def test_relative_months_with_absolute_day(self):
        dt = datetime.date(2020, 1, 31)
        rd = relativedelta(months=1, day=15)
        result = dt + rd
        assert result == datetime.date(2020, 2, 15)
        
    def test_multiple_relative_with_multiple_absolute(self):
        dt = datetime.datetime(2020, 6, 15, 10, 30, 45)
        rd = relativedelta(years=1, months=2, hour=15, minute=0)
        result = dt + rd
        assert result == datetime.datetime(2021, 8, 15, 15, 0, 45)


class TestRelativeDeltaMonthOverflowEdgeCases:
    def test_eleven_months_no_year_increment(self):
        dt = datetime.date(2020, 1, 15)
        rd = relativedelta(months=11)
        result = dt + rd
        assert result == datetime.date(2020, 12, 15)
        
    def test_twelve_months_equals_one_year(self):
        dt = datetime.date(2020, 1, 15)
        rd = relativedelta(months=12)
        result = dt + rd
        assert result == datetime.date(2021, 1, 15)
        
    def test_thirteen_months(self):
        dt = datetime.date(2020, 1, 15)
        rd = relativedelta(months=13)
        result = dt + rd
        assert result == datetime.date(2021, 2, 15)
        
    def test_negative_month_underflow(self):
        dt = datetime.date(2020, 3, 15)
        rd = relativedelta(months=-3)
        result = dt + rd
        assert result == datetime.date(2019, 12, 15)


class TestRelativeDeltaTimeOverflowEdgeCases:
    def test_59_seconds_no_overflow(self):
        rd = relativedelta(seconds=59)
        assert rd.minutes == 0
        assert rd.seconds == 59
        
    def test_60_seconds_overflow(self):
        rd = relativedelta(seconds=60)
        assert rd.minutes == 1
        assert rd.seconds == 0
        
    def test_59_minutes_no_overflow(self):
        rd = relativedelta(minutes=59)
        assert rd.hours == 0
        assert rd.minutes == 59
        
    def test_60_minutes_overflow(self):
        rd = relativedelta(minutes=60)
        assert rd.hours == 1
        assert rd.minutes == 0
        
    def test_23_hours_no_overflow(self):
        rd = relativedelta(hours=23)
        assert rd.days == 0
        assert rd.hours == 23
        
    def test_24_hours_overflow(self):
        rd = relativedelta(hours=24)
        assert rd.days == 1
        assert rd.hours == 0


class TestRelativeDeltaComplexDateOperations:
    def test_add_year_to_leap_day(self):
        dt = datetime.date(2020, 2, 29)
        rd = relativedelta(years=1)
        result = dt + rd
        assert result == datetime.date(2021, 2, 28)
        
    def test_add_four_years_to_leap_day(self):
        dt = datetime.date(2020, 2, 29)
        rd = relativedelta(years=4)
        result = dt + rd
        assert result == datetime.date(2024, 2, 29)
        
    def test_month_end_chain(self):
        dt = datetime.date(2020, 1, 31)
        rd = relativedelta(months=1)
        result1 = dt + rd
        result2 = result1 + rd
        assert result1 == datetime.date(2020, 2, 29)
        assert result2 == datetime.date(2020, 3, 29)


class TestRelativeDeltaMixedTypes:
    def test_add_relativedelta_and_timedelta_to_date(self):
        dt = datetime.date(2020, 1, 15)
        rd = relativedelta(months=1)
        td = datetime.timedelta(days=5)
        result = dt + rd + td
        assert result == datetime.date(2020, 2, 20)
        
    def test_combine_multiple_types(self):
        dt = datetime.datetime(2020, 1, 15, 10, 0)
        rd1 = relativedelta(months=2)
        rd2 = relativedelta(days=5)
        td = datetime.timedelta(hours=3)
        result = dt + rd1 + rd2 + td
        assert result == datetime.datetime(2020, 3, 20, 13, 0)


class TestRelativeDeltaHashAndSet:
    def test_relativedelta_in_set(self):
        rd1 = relativedelta(years=1, months=2)
        rd2 = relativedelta(years=1, months=2)
        rd3 = relativedelta(years=2, months=3)
        s = {rd1, rd2, rd3}
        assert len(s) == 2
        
    def test_relativedelta_as_dict_key(self):
        rd1 = relativedelta(years=1)
        rd2 = relativedelta(years=1)
        d = {rd1: "value1"}
        assert d[rd2] == "value1"


class TestRelativeDeltaBoundaryValues:
    def test_max_month_value(self):
        rd = relativedelta(months=11)
        assert rd.months == 11
        assert rd.years == 0
        
    def test_min_month_value(self):
        rd = relativedelta(months=-11)
        assert rd.months == -11
        assert rd.years == 0
        
    def test_large_positive_values(self):
        rd = relativedelta(years=1000, months=5, days=100)
        assert rd.years == 1000
        assert rd.months == 5
        assert rd.days == 100
        
    def test_large_negative_values(self):
        rd = relativedelta(years=-1000, months=-5, days=-100)
        assert rd.years == -1000
        assert rd.months == -5
        assert rd.days == -100


class TestRelativeDeltaReprVariations:
    def test_repr_positive_values(self):
        rd = relativedelta(years=1, months=2, days=3)
        repr_str = repr(rd)
        assert "relativedelta" in repr_str
        assert "years=+1" in repr_str
        
    def test_repr_negative_values(self):
        rd = relativedelta(years=-1, months=-2)
        repr_str = repr(rd)
        assert "years=-1" in repr_str
        assert "months=-2" in repr_str
        
    def test_repr_with_weekday(self):
        rd = relativedelta(weekday=MO)
        repr_str = repr(rd)
        assert "weekday=" in repr_str
        
    def test_repr_mixed_values(self):
        rd = relativedelta(years=1, year=2025, months=2, month=6)
        repr_str = repr(rd)
        assert "years=+1" in repr_str
        assert "year=2025" in repr_str


class TestRelativeDeltaNormalizedAdvanced:
    def test_normalized_with_fractional_hours(self):
        rd = relativedelta(hours=2.5)
        normalized = rd.normalized()
        assert normalized.hours == 2
        assert normalized.minutes == 30
        
    def test_normalized_with_fractional_minutes(self):
        rd = relativedelta(minutes=2.5)
        normalized = rd.normalized()
        assert normalized.minutes == 2
        assert normalized.seconds == 30
        
    def test_normalized_with_fractional_days_and_hours(self):
        rd = relativedelta(days=1.25, hours=6)
        normalized = rd.normalized()
        assert normalized.days == 1
        assert normalized.hours == 12
        
    def test_normalized_preserves_absolute_values(self):
        rd = relativedelta(days=1.5, year=2025, month=6)
        normalized = rd.normalized()
        assert normalized.year == 2025
        assert normalized.month == 6


class TestRelativeDeltaWeekdayNthValues:
    def test_weekday_first_monday(self):
        dt = datetime.date(2020, 1, 1)
        rd = relativedelta(day=1, weekday=MO(1))
        result = dt + rd
        assert result == datetime.date(2020, 1, 6)
        
    def test_weekday_second_tuesday(self):
        dt = datetime.date(2020, 1, 1)
        rd = relativedelta(day=1, weekday=TU(2))
        result = dt + rd
        assert result == datetime.date(2020, 1, 14)
        
    def test_weekday_last_friday(self):
        dt = datetime.date(2020, 1, 1)
        rd = relativedelta(day=31, weekday=FR(-1))
        result = dt + rd
        assert result == datetime.date(2020, 1, 31)
        
    def test_weekday_last_sunday(self):
        dt = datetime.date(2020, 2, 1)
        rd = relativedelta(day=29, weekday=SU(-1))
        result = dt + rd
        assert result == datetime.date(2020, 2, 23)


class TestRelativeDeltaComplexArithmetic:
    def test_subtract_larger_from_smaller(self):
        rd1 = relativedelta(months=3)
        rd2 = relativedelta(months=5)
        result = rd1 - rd2
        assert result.months == -2
        
    def test_add_positive_and_negative(self):
        rd1 = relativedelta(years=5, months=-3)
        rd2 = relativedelta(years=-2, months=6)
        result = rd1 + rd2
        assert result.years == 3
        assert result.months == 3
        
    def test_multiply_by_zero(self):
        rd = relativedelta(years=5, months=10)
        result = rd * 0
        assert result.years == 0
        assert result.months == 0
        
    def test_multiply_by_negative(self):
        rd = relativedelta(years=2, months=3)
        result = rd * -1
        assert result.years == -2
        assert result.months == -3
        
    def test_divide_by_negative(self):
        rd = relativedelta(days=10)
        result = rd / -2
        assert result.days == -5


class TestRelativeDeltaDateTimeConversions:
    def test_date_becomes_datetime_with_hour(self):
        dt = datetime.date(2020, 1, 15)
        rd = relativedelta(hour=10)
        result = dt + rd
        assert isinstance(result, datetime.datetime)
        assert result.hour == 10
        
    def test_date_becomes_datetime_with_minute(self):
        dt = datetime.date(2020, 1, 15)
        rd = relativedelta(minute=30)
        result = dt + rd
        assert isinstance(result, datetime.datetime)
        assert result.minute == 30
        
    def test_date_becomes_datetime_with_second(self):
        dt = datetime.date(2020, 1, 15)
        rd = relativedelta(second=45)
        result = dt + rd
        assert isinstance(result, datetime.datetime)
        assert result.second == 45
        
    def test_date_becomes_datetime_with_microsecond(self):
        dt = datetime.date(2020, 1, 15)
        rd = relativedelta(microsecond=500000)
        result = dt + rd
        assert isinstance(result, datetime.datetime)
        assert result.microsecond == 500000


class TestRelativeDeltaYearDayVariations:
    def test_yearday_first_day(self):
        rd = relativedelta(yearday=1)
        assert rd.month == 1
        assert rd.day == 1
        
    def test_yearday_last_day_of_january(self):
        rd = relativedelta(yearday=31)
        assert rd.month == 1
        assert rd.day == 31
        
    def test_yearday_first_day_of_february(self):
        rd = relativedelta(yearday=32)
        assert rd.month == 2
        assert rd.day == 1
        
    def test_yearday_middle_of_year(self):
        rd = relativedelta(yearday=182)
        assert rd.month == 7
        assert rd.day == 1
        
    def test_yearday_sets_leapdays(self):
        rd = relativedelta(yearday=70)
        assert rd.leapdays == -1


class TestRelativeDeltaTimeDeltaInteraction:
    def test_add_timedelta_days_only(self):
        rd = relativedelta(months=1)
        td = datetime.timedelta(days=10)
        result = rd + td
        assert result.months == 1
        assert result.days == 10
        
    def test_add_timedelta_with_seconds(self):
        rd = relativedelta(months=1)
        td = datetime.timedelta(seconds=3600)
        result = rd + td
        assert result.months == 1
        assert result.hours == 1
        
    def test_add_timedelta_with_microseconds(self):
        rd = relativedelta(days=5)
        td = datetime.timedelta(microseconds=500000)
        result = rd + td
        assert result.days == 5
        assert result.microseconds == 500000


class TestRelativeDeltaMonthDayAdjustments:
    def test_december_31_plus_month(self):
        dt = datetime.date(2020, 12, 31)
        rd = relativedelta(months=1)
        result = dt + rd
        assert result == datetime.date(2021, 1, 31)
        
    def test_january_31_plus_two_months(self):
        dt = datetime.date(2020, 1, 31)
        rd = relativedelta(months=2)
        result = dt + rd
        assert result == datetime.date(2020, 3, 31)
        
    def test_january_30_plus_month(self):
        dt = datetime.date(2020, 1, 30)
        rd = relativedelta(months=1)
        result = dt + rd
        assert result == datetime.date(2020, 2, 29)


class TestRelativeDeltaEqualityEdgeCases:
    def test_equality_with_different_weekday_n(self):
        rd1 = relativedelta(weekday=MO(1))
        rd2 = relativedelta(weekday=MO(2))
        assert rd1 != rd2
        
    def test_equality_weekday_n_none_vs_one(self):
        rd1 = relativedelta(weekday=MO)
        rd2 = relativedelta(weekday=MO(1))
        assert rd1 == rd2
        
    def test_equality_all_fields_match(self):
        rd1 = relativedelta(years=1, months=2, days=3, hours=4, minutes=5, seconds=6, microseconds=7)
        rd2 = relativedelta(years=1, months=2, days=3, hours=4, minutes=5, seconds=6, microseconds=7)
        assert rd1 == rd2
        
    def test_inequality_one_field_different(self):
        rd1 = relativedelta(years=1, months=2, days=3)
        rd2 = relativedelta(years=1, months=2, days=4)
        assert rd1 != rd2


class TestRelativeDeltaAbsoluteValuesPreservation:
    def test_addition_preserves_absolute_values(self):
        rd1 = relativedelta(years=1, year=2025)
        rd2 = relativedelta(months=2)
        result = rd1 + rd2
        assert result.year == 2025
        
    def test_subtraction_preserves_first_absolute_values(self):
        rd1 = relativedelta(years=3, year=2025)
        rd2 = relativedelta(years=1, year=2020)
        result = rd1 - rd2
        assert result.year == 2025
        
    def test_negation_preserves_absolute_values(self):
        rd = relativedelta(years=-1, year=2025, month=6)
        result = -rd
        assert result.year == 2025
        assert result.month == 6
        
    def test_abs_preserves_absolute_values(self):
        rd = relativedelta(years=-1, year=2025)
        result = abs(rd)
        assert result.year == 2025


class TestRelativeDeltaZeroAndEmptyComparisons:
    def test_empty_equals_empty(self):
        rd1 = relativedelta()
        rd2 = relativedelta()
        assert rd1 == rd2
        
    def test_zero_values_equal(self):
        rd1 = relativedelta(years=0, months=0, days=0)
        rd2 = relativedelta()
        assert rd1 == rd2
        
    def test_empty_hash_consistent(self):
        rd1 = relativedelta()
        rd2 = relativedelta()
        assert hash(rd1) == hash(rd2)


class TestRelativeDeltaComplexDateScenarios:
    def test_add_13_months_to_january(self):
        dt = datetime.date(2020, 1, 15)
        rd = relativedelta(months=13)
        result = dt + rd
        assert result == datetime.date(2021, 2, 15)
        
    def test_add_25_months(self):
        dt = datetime.date(2020, 1, 15)
        rd = relativedelta(months=25)
        result = dt + rd
        assert result == datetime.date(2022, 2, 15)
        
    def test_subtract_13_months(self):
        dt = datetime.date(2021, 2, 15)
        rd = relativedelta(months=-13)
        result = dt + rd
        assert result == datetime.date(2020, 1, 15)


class TestRelativeDeltaWeeksPropertyAdvanced:
    def test_weeks_property_zero_days(self):
        rd = relativedelta(days=0)
        assert rd.weeks == 0
        
    def test_weeks_property_partial_week(self):
        rd = relativedelta(days=5)
        assert rd.weeks == 0
        
    def test_weeks_property_exact_weeks(self):
        rd = relativedelta(days=21)
        assert rd.weeks == 3
        
    def test_weeks_setter_on_zero(self):
        rd = relativedelta()
        rd.weeks = 2
        assert rd.days == 14


class TestRelativeDeltaReverseOperations:
    def test_rsub_with_datetime(self):
        dt = datetime.datetime(2020, 5, 15, 10, 30)
        rd = relativedelta(months=2, days=5)
        result = dt - rd
        assert result == datetime.datetime(2020, 3, 10, 10, 30)
        
    def test_rmul_with_integer(self):
        rd = relativedelta(days=5)
        result = 3 * rd
        assert result.days == 15


class TestRelativeDeltaHasTimeFlag:
    def test_has_time_with_hours(self):
        rd = relativedelta(hours=5)
        assert rd._has_time == 1
        
    def test_has_time_with_absolute_hour(self):
        rd = relativedelta(hour=10)
        assert rd._has_time == 1
        
    def test_no_has_time_with_only_days(self):
        rd = relativedelta(days=5)
        assert rd._has_time == 0
        
    def test_no_has_time_with_years_months(self):
        rd = relativedelta(years=1, months=2)
        assert rd._has_time == 0