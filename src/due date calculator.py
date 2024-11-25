from datetime import datetime, timedelta

class DateValidator:
    """Class to handle date validation and parsing."""
    @staticmethod
    def validate_date(date_str):
        """
        Validate and parse a date string.
        
        Parameters:
            date_str (str): The date string in 'MM/DD/YYYY' format.
            
        Returns:
            datetime: The parsed datetime object, or an error message if invalid.
        """
        try:
            month, day, year = map(int, date_str.split("/"))
            if month < 1 or month > 12:
                return "Invalid month. Month must be between 01 and 12."
            if not DateValidator.is_valid_day_in_month(month, day, year):
                return f"The date you entered is not valid: {month:02}/{day:02}/{year}. Please double-check and try again."
            date = datetime.strptime(date_str, '%m/%d/%Y')
            if not DateValidator.is_valid_date_range(date):
                start_date = (datetime.now() - timedelta(days=280)).strftime("%m/%d/%Y")
                current_date = datetime.now().strftime("%m/%d/%Y")
                return f"Invalid date range. Please enter a date between {start_date} and today's date ({current_date})."
            return date
        except ValueError:
            return "Invalid date format. Please use 'MM/DD/YYYY'."

    @staticmethod
    def is_valid_day_in_month(month, day, year):
        days_in_month = {
            1: 31, 2: 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28,  
            3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
        }
        return 1 <= day <= days_in_month.get(month, 0)

    @staticmethod
    def is_valid_date_range(date):
        start_date = datetime.now() - timedelta(days=280)
        current_date = datetime.now()
        return start_date <= date <= current_date


class DueDateCalculator:
    """Class to calculate the due date and pregnancy progress."""
    def __init__(self, lmp_date, period_length=28):
        """
        Initialize the calculator with LMP date and period length.

        Parameters:
            lmp_date (datetime): Last menstrual period date.
            period_length (int): Normal menstrual cycle length in days.
        """
        self.lmp_date = lmp_date
        self.period_length = period_length

    def calculate_due_date(self):
        """
        Calculate the due date.

        Returns:
            datetime: The estimated due date.
        """
        # Adjust LMP date based on period length difference from 28 days
        adjusted_lmp = self.lmp_date + timedelta(days=(self.period_length - 28))
        return adjusted_lmp + timedelta(days=280)

    def calculate_current_progress(self):
        """
        Calculate the current pregnancy progress in weeks and days.
        
        Returns:
            tuple: (weeks, days)
        """
        total_days_pregnant = (datetime.now() - self.lmp_date).days
        weeks = total_days_pregnant // 7
        days = total_days_pregnant % 7
        return weeks, days


class DueDatePredictor:
    """Main app to interact with the user."""
    def __init__(self):
        print("Welcome to the BabyLand - A Comprehensive Toolbox for Your Pregnancy Journey!")

    def run(self):
        """Run the application."""
        # Input LMP date
        lmp_date_str = input("Please enter the first day of your last menstrual period (MM/DD/YYYY): ")
        validation_result = DateValidator.validate_date(lmp_date_str)
        if isinstance(validation_result, str):
            print(validation_result)
            return
        
        # Input normal period length
        try:
            period_length = int(input("Please enter your normal menstrual cycle length in days (default is 28): "))
            if period_length < 20 or period_length > 40:
                print("Invalid period length. Please enter a value between 20 and 40.")
                return
        except ValueError:
            print("Invalid input. Please enter an integer value.")
            return

        # Calculate due date and pregnancy progress
        calculator = DueDateCalculator(validation_result, period_length)
        due_date = calculator.calculate_due_date()
        weeks, days = calculator.calculate_current_progress()

        # Output results
        print(f"Congratulations! You are currently {weeks} weeks and {days} days pregnant.")
        print(f"Your baby's estimated due date is: {due_date.strftime('%m/%d/%Y')}")


# Run the app
if __name__ == "__main__":
    app = DueDatePredictor()
    app.run()
