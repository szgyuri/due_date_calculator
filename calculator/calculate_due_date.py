from datetime import datetime, timedelta

from calculator.constants import END_HOUR_OF_DAY, START_HOUR_OF_DAY
from calculator.exception_messages import INVALID_DAY_WEEKEND, INVALID_BIGGER_HOUR, INVALID_LESS_HOUR


def calculate_due_date(submit_date: datetime, turnaround_hour: int) -> datetime:
    """ Calculate due date based on submit date and turnaround hour and return it"""
    _validate_submit_date(submit_date)

    turnaround_days_count = _get_days_of_turnaround_hour(turnaround_hour)
    turnaround_hours_count = _get_hours_of_turnaround_hour(turnaround_hour)

    due_date = submit_date

    if turnaround_days_count > 0:
        due_date = _add_days_for_calc_due_date(due_date, turnaround_days_count)
    if turnaround_hours_count > 0:
        due_date = _add_hours_for_calc_due_date(due_date, turnaround_hours_count)

    # In this case the issue was resolved on previous day of end hour
    if due_date.hour == START_HOUR_OF_DAY.hour and due_date.minute == START_HOUR_OF_DAY.minute:
        due_date = _set_previous_day_end_hour(due_date)

    return due_date


def _validate_submit_date(submit_date: datetime) -> None:
    """ Check weekend day and hour range (5AM-7PM) of submit_date """
    if submit_date.isoweekday() > 5:
        raise ValueError(INVALID_DAY_WEEKEND)
    if submit_date.hour > 17:
        raise ValueError(INVALID_BIGGER_HOUR)
    if submit_date.hour < 9:
        raise ValueError(INVALID_LESS_HOUR)


def _get_days_of_turnaround_hour(turnaround_hour: int) -> int:
    return int(turnaround_hour / 8)


def _get_hours_of_turnaround_hour(turnaround_hour: int) -> int:
    return turnaround_hour % 8


def _add_days_for_calc_due_date(due_date: datetime, turnaround_days_count: int) -> datetime:
    """ Add days with number of weekend days to due date and return it """
    weekend_days_count = _get_weekend_days_count(due_date, turnaround_days_count)

    due_date = due_date + timedelta(days=turnaround_days_count + weekend_days_count)
    due_date = _set_due_date_when_is_weekend_day(due_date, num_of_days_to_saturday=2, num_of_days_to_sunday=1)

    return due_date


def _get_weekend_days_count(due_date: datetime, turnaround_days_count: int) -> int:
    """ Get weekend days count from due date to due date plus turnaround days count """
    weekend_days_count = 0

    for current_day in range(1, turnaround_days_count + 1):
        current_date = due_date + timedelta(days=current_day)
        if current_date.isoweekday() > 5:
            weekend_days_count += 1

    return weekend_days_count


def _add_hours_for_calc_due_date(due_date: datetime, turnaround_hours_count: int) -> datetime:
    """ Add remaining hours to due date with checking weekend days and return it """
    date_with_added_hours = due_date + timedelta(hours=turnaround_hours_count)

    if date_with_added_hours.time() > END_HOUR_OF_DAY:
        hour_delta = date_with_added_hours.hour - 17

        due_date += timedelta(days=1)
        due_date = due_date.replace(hour=9)
        due_date += timedelta(hours=hour_delta)
    else:
        due_date = date_with_added_hours

    due_date = _set_due_date_when_is_weekend_day(due_date, num_of_days_to_saturday=2, num_of_days_to_sunday=1)

    return due_date


def _set_previous_day_end_hour(due_date: datetime) -> datetime:
    """ Set end hour (5PM) of previous workday to due date and return it """
    due_date += timedelta(days=-1)
    due_date = due_date.replace(hour=17)
    due_date = _set_due_date_when_is_weekend_day(due_date, num_of_days_to_saturday=-1, num_of_days_to_sunday=-2)

    return due_date


def _set_due_date_when_is_weekend_day(due_date: datetime, num_of_days_to_saturday: int,
                                      num_of_days_to_sunday: int) -> datetime:
    """ Set due date when it's saturday by num_of_days_to_saturday or sunday by num_of_days_to_sunday """
    if due_date.isoweekday() == 6:
        due_date += timedelta(days=num_of_days_to_saturday)
    elif due_date.isoweekday() == 7:
        due_date += timedelta(days=num_of_days_to_sunday)

    return due_date
