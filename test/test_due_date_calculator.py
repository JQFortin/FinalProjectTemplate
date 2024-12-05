import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from datetime import datetime, timedelta
from due_date_calculator import DateValidator, DueDateCalculator

class TestDateValidator(unittest.TestCase):

    def test_validate_date_valid(self):
        date_str = "10/01/2024"
        result = DateValidator.validate_date(date_str)
        self.assertIsInstance(result, datetime)
        self.assertEqual(result.strftime("%m/%d/%Y"), date_str)

    def test_validate_date_invalid_format_1(self):
        date_str = "2024-10-01"
        result = DateValidator.validate_date(date_str)
        self.assertEqual(result, "Invalid date format. Please use 'MM/DD/YYYY', and only numbers 0-9.")

    def test_validate_date_invalid_format_2(self):
        date_str = "04.24.2024"
        result = DateValidator.validate_date(date_str)
        self.assertEqual(result, "Invalid date format. Please use 'MM/DD/YYYY', and only numbers 0-9.")

    def test_validate_date_invalid_format_3(self):
        date_str = "ABC"
        result = DateValidator.validate_date(date_str)
        self.assertEqual(result, "Invalid date format. Please use 'MM/DD/YYYY', and only numbers 0-9.")

    def test_validate_date_invalid_month(self):
        date_str = "13/01/2024"
        result = DateValidator.validate_date(date_str)
        self.assertEqual(result, "Invalid month. Month must be between 01 and 12.")

    def test_validate_date_invalid_day(self):
        date_str = "02/30/2024"
        result = DateValidator.validate_date(date_str)
        self.assertEqual(result, "The date you entered is not valid: 02/30/2024. Please double-check and try again.")

    def test_validate_date_out_of_range(self):
        # Date more than 280 days ago
        out_of_range_date = (datetime.now() - timedelta(days=281)).strftime("%m/%d/%Y")
        result = DateValidator.validate_date(out_of_range_date)
        start_date = (datetime.now() - timedelta(days=280)).strftime("%m/%d/%Y")
        current_date = datetime.now().strftime("%m/%d/%Y")
        self.assertEqual(
            result,
            f"Invalid date range. Please enter a date between {start_date} and today's date ({current_date})."
        )

    def test_is_valid_day_in_month(self):
        self.assertTrue(DateValidator.is_valid_day_in_month(2, 29, 2024))  # Leap year
        self.assertFalse(DateValidator.is_valid_day_in_month(2, 29, 2023))  # Not a leap year
        self.assertTrue(DateValidator.is_valid_day_in_month(4, 30, 2024))  # April has 30 days
        self.assertFalse(DateValidator.is_valid_day_in_month(4, 31, 2024))  # April does not have 31 days
        self.assertFalse(DateValidator.is_valid_day_in_month(2, 29, 2023))  # Feb 29 is invalid for non-leap year

    def test_is_valid_date_range(self):
        valid_date = datetime.now() - timedelta(days=150)
        self.assertTrue(DateValidator.is_valid_date_range(valid_date))

        invalid_date = datetime.now() - timedelta(days=300)
        self.assertFalse(DateValidator.is_valid_date_range(invalid_date))


class TestDueDateCalculator(unittest.TestCase):

    def setUp(self):
        self.lmp_date = datetime(2024, 1, 1)
        self.default_period_length = 28
        self.calculator = DueDateCalculator(self.lmp_date, self.default_period_length)

    def test_calculate_due_date(self):
        expected_due_date = self.lmp_date + timedelta(days=280)
        self.assertEqual(self.calculator.calculate_due_date(), expected_due_date)

    def test_calculate_due_date_with_non_default_period_length(self):
        period_length = 30
        calculator = DueDateCalculator(self.lmp_date, period_length)
        expected_due_date = self.lmp_date + timedelta(days=(period_length - 28) + 280)
        self.assertEqual(calculator.calculate_due_date(), expected_due_date)

    def test_calculate_due_date_edge_case(self):
        today = datetime.now()
        expected_due_date = today + timedelta(days=280)
        calculator = DueDateCalculator(today, self.default_period_length)
        self.assertEqual(calculator.calculate_due_date(), expected_due_date)

    def test_calculate_current_progress(self):
        current_date = datetime.now()
        total_days_pregnant = (current_date - self.lmp_date).days
        weeks = total_days_pregnant // 7
        days = total_days_pregnant % 7
        self.assertEqual(self.calculator.calculate_current_progress(), (weeks, days))

    def test_calculate_current_progress_edge_case(self):
        today = datetime.now()
        calculator = DueDateCalculator(today, self.default_period_length)
        self.assertEqual(calculator.calculate_current_progress(), (0, 0))  # Should return (0, 0) for the current day

    def test_calculate_due_date_for_shorter_period(self):
        period_length = 26  # Shorter period
        calculator = DueDateCalculator(self.lmp_date, period_length)
        expected_due_date = self.lmp_date + timedelta(days=(280 + (period_length - 28)))
        self.assertEqual(calculator.calculate_due_date(), expected_due_date)

    def test_period_length_validation(self):
        # Valid period length
        valid_period = 30
        calculator = DueDateCalculator(self.lmp_date, valid_period)
        self.assertEqual(calculator.period_length, valid_period)

        # Invalid period lengths
        with self.assertRaises(ValueError):
            DueDateCalculator(self.lmp_date, 19)  # Too short
        with self.assertRaises(ValueError):
            DueDateCalculator(self.lmp_date, 46)  # Too long

        # Boundary conditions
        calculator_lower = DueDateCalculator(self.lmp_date, 20)
        calculator_upper = DueDateCalculator(self.lmp_date, 45)
        self.assertEqual(calculator_lower.period_length, 20)
        self.assertEqual(calculator_upper.period_length, 45)

if __name__ == "__main__":
    unittest.main()
