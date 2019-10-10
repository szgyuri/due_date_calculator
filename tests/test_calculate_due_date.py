import unittest
from datetime import datetime

from calculator.calculate_due_date import calculate_due_date
from calculator.exception_messages import INVALID_DAY_WEEKEND, INVALID_BIGGER_HOUR, INVALID_LESS_HOUR


class TestTurnaroundHoursWithWholeDays(unittest.TestCase):

    def test_with_monday_plus_two_days(self):
        self.submit_date = datetime(2019, 10, 7, 10, 1, 2)
        self.turnaround_hours = 16
        self.expected_date = datetime(2019, 10, 9, 10, 1, 2)

        calculated_date = calculate_due_date(self.submit_date, self.turnaround_hours)

        self.assertEqual(self.expected_date, calculated_date)

    def test_with_friday_plus_one_day(self):
        self.submit_date = datetime(2019, 10, 11, 10, 1, 2)
        self.turnaround_hours = 8
        self.expected_date = datetime(2019, 10, 14, 10, 1, 2)

        calculated_date = calculate_due_date(self.submit_date, self.turnaround_hours)

        self.assertEqual(self.expected_date, calculated_date)

    def test_with_friday_plus_two_days(self):
        self.submit_date = datetime(2019, 10, 11, 10, 0, 0)
        self.turnaround_hours = 16
        self.expected_date = datetime(2019, 10, 15, 10, 0, 0)

        calculated_date = calculate_due_date(self.submit_date, self.turnaround_hours)

        self.assertEqual(self.expected_date, calculated_date)

    def test_with_friday_plus_three_days(self):
        self.submit_date = datetime(2019, 10, 11, 10, 0, 0)
        self.turnaround_hours = 24
        self.expected_date = datetime(2019, 10, 16, 10, 0, 0)

        calculated_date = calculate_due_date(self.submit_date, self.turnaround_hours)

        self.assertEqual(self.expected_date, calculated_date)

    def test_with_friday_with_next_saturday(self):
        self.submit_date = datetime(2019, 10, 11, 10, 0, 0)
        self.turnaround_hours = 48
        self.expected_date = datetime(2019, 10, 21, 10, 0, 0)

        calculated_date = calculate_due_date(self.submit_date, self.turnaround_hours)

        self.assertEqual(self.expected_date, calculated_date)

    def test_with_friday_plus_10_days(self):
        self.submit_date = datetime(2019, 10, 11, 10, 0, 0)
        self.turnaround_hours = 80
        self.expected_date = datetime(2019, 10, 25, 10, 0, 0)

        calculated_date = calculate_due_date(self.submit_date, self.turnaround_hours)

        self.assertEqual(self.expected_date, calculated_date)

    def test_with_start_hour_of_day_on_monday_to_tuesday(self):
        self.submit_date = datetime(2019, 10, 7, 9, 0, 0)
        self.turnaround_hours = 8
        self.expected_date = datetime(2019, 10, 7, 17, 0, 0)

        calculated_date = calculate_due_date(self.submit_date, self.turnaround_hours)

        self.assertEqual(self.expected_date, calculated_date)

    def test_with_start_hour_of_day_on_friday_to_saturday(self):
        self.submit_date = datetime(2019, 10, 4, 9, 0, 0)
        self.turnaround_hours = 8
        self.expected_date = datetime(2019, 10, 4, 17, 0, 0)

        calculated_date = calculate_due_date(self.submit_date, self.turnaround_hours)

        self.assertEqual(self.expected_date, calculated_date)

    def test_with_start_hour_of_day_on_friday_to_sunday(self):
        self.submit_date = datetime(2019, 10, 4, 9, 0, 0)
        self.turnaround_hours = 16
        self.expected_date = datetime(2019, 10, 7, 17, 0, 0)

        calculated_date = calculate_due_date(self.submit_date, self.turnaround_hours)

        self.assertEqual(self.expected_date, calculated_date)


class TestTurnaroundHoursWithHours(unittest.TestCase):

    def test_with_zero_turnaround_hours(self):
        self.submit_date = datetime(2019, 10, 7, 9, 1, 0)
        self.turnaround_hours = 0
        self.expected_date = self.submit_date

        calculated_date = calculate_due_date(self.submit_date, self.turnaround_hours)

        self.assertEqual(self.expected_date, calculated_date)

    def test_with_hours_to_same_day(self):
        self.submit_date = datetime(2019, 10, 7, 10, 0, 0)
        self.turnaround_hours = 7
        self.expected_date = datetime(2019, 10, 7, 17, 0, 0)

        calculated_date = calculate_due_date(self.submit_date, self.turnaround_hours)

        self.assertEqual(self.expected_date, calculated_date)

    def test_with_hours_to_next_day(self):
        self.submit_date = datetime(2019, 10, 7, 10, 1, 2)
        self.turnaround_hours = 7
        self.expected_date = datetime(2019, 10, 8, 9, 1, 2)

        calculated_date = calculate_due_date(self.submit_date, self.turnaround_hours)

        self.assertEqual(self.expected_date, calculated_date)

    def test_with_hours_to_saturday(self):
        self.submit_date = datetime(2019, 10, 11, 10, 1, 0)
        self.turnaround_hours = 7
        self.expected_date = datetime(2019, 10, 14, 9, 1, 0)

        calculated_date = calculate_due_date(self.submit_date, self.turnaround_hours)

        self.assertEqual(self.expected_date, calculated_date)

    def test_with_hours_to_sunday(self):
        self.submit_date = datetime(2019, 10, 11, 10, 1, 0)
        self.turnaround_hours = 17
        self.expected_date = datetime(2019, 10, 15, 11, 1, 0)

        calculated_date = calculate_due_date(self.submit_date, self.turnaround_hours)

        self.assertEqual(self.expected_date, calculated_date)


class TestValidationOfCalculateDueDate(unittest.TestCase):

    def test_with_invalid_day_of_submit_date(self):
        self.submit_date = datetime(2019, 10, 6, 9, 0, 0)
        self.turnaround_hours = 16

        with self.assertRaises(ValueError) as value_error:
            calculate_due_date(self.submit_date, self.turnaround_hours)
        self.assertEqual(INVALID_DAY_WEEKEND, str(value_error.exception))

    def test_with_invalid_bigger_hour_of_submit_date(self):
        self.submit_date = datetime(2019, 10, 7, 18, 0, 0)
        self.turnaround_hours = 16

        with self.assertRaises(ValueError) as value_error:
            calculate_due_date(self.submit_date, self.turnaround_hours)
        self.assertEqual(INVALID_BIGGER_HOUR, str(value_error.exception))

    def test_with_invalid_less_hour_of_submit_date(self):
        self.submit_date = datetime(2019, 10, 7, 8, 0, 0)
        self.turnaround_hours = 16

        with self.assertRaises(ValueError) as value_error:
            calculate_due_date(self.submit_date, self.turnaround_hours)
        self.assertEqual(INVALID_LESS_HOUR, str(value_error.exception))
