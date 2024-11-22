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
            # Extract month, day, and year
            month, day, year = map(int, date_str.split("/"))
            
            # Check if the month is valid (1-12)
            if month < 1 or month > 12:
                return "Invalid month. Month must be between 01 and 12."
            
            # Check if the day is valid for the given month
            if not DateValidator.is_valid_day_in_month(month, day, year):
                return f"The date you entered is not valid, {month:02}/{day:02}/{year}. Please double check and enter again."
            
            # Now parse the date
            date = datetime.strptime(date_str, '%m/%d/%Y')
            
            # Check if the date is in the valid range
            if not DateValidator.is_valid_date_range(date):
                current_date = datetime.now().strftime("%m/%d/%Y")  # Get today's date in MM/DD/YYYY format
                return f"Invalid date range, please enter a date between 03/15/2024 and today's date ({current_date})."
            
            return date
        except ValueError:
            return "Invalid date format. Please use 'MM/DD/YYYY'."
    
    @staticmethod
    def is_valid_day_in_month(month, day, year):
        """Check if the given day is valid for the given month and year."""
        # Define the days in each month
        days_in_month = {
            1: 31, 2: 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28,  # February, accounting for leap years
            3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
        }
        
        # Check if the day is within the valid range for the given month
        return 1 <= day <= days_in_month.get(month, 0)
    
    @staticmethod
    def is_valid_date_range(date):
        """Check if the date is within the valid date range (03/15/2024 to today)."""
        start_date = datetime.strptime("03/15/2024", "%m/%d/%Y")
        current_date = datetime.now()
        
        return start_date <= date <= current_date


class DueDateCalculator:
    """Class to calculate the due date based on LMP."""
    def __init__(self, lmp_date):
        """
        Initialize the calculator with the LMP date.
        
        Parameters:
            lmp_date (datetime): The datetime object representing the LMP.
        """
        self.lmp_date = lmp_date
        self.start_date = datetime.strptime("03/15/2024", "%m/%d/%Y")
        self.current_date = datetime.now()

    def is_valid_lmp_date(self, lmp_date_str):
        try:
            lmp_date = datetime.strptime(lmp_date_str, "%m/%d/%Y")
            # Check if LMP date is within the range
            if self.start_date <= lmp_date <= self.current_date:
                return True
            else:
                print(f"Error: The date must be between {self.start_date.strftime('%m/%d/%Y')} "
                      f"and {self.current_date.strftime('%m/%d/%Y')}.")
                return False
        except ValueError:
            print("Error: Please enter the date in MM/DD/YYYY format.")
            return False

    def calculate_due_date(self, lmp_date_str):
        """
        Calculate the due date based on the LMP date.
        
        Returns:
            datetime: The due date as a datetime object.
        """
        if self.is_valid_lmp_date(lmp_date_str):
            lmp_date = datetime.strptime(lmp_date_str, "%m/%d/%Y")
            due_date = lmp_date + timedelta(days=280)  # Pregnancy is approximately 280 days.
            return due_date.strftime("%m/%d/%Y")
        else:
            return None


class DueDatePredictor:
    """Main app to interact with the user."""
    def __init__(self):
        print("Welcome to the BabyLand - A Comprehensive Toolbox for Your Pregnancy Journey!")

    def run(self):
        """
        Run the application.
        """
        lmp_date_str = input("Please enter the first day of your last menstrual period (MM/DD/YYYY): ")
        
        # Validate the input date
        validation_result = DateValidator.validate_date(lmp_date_str)
        
        if isinstance(validation_result, str):
            print(validation_result)
            return
        
        # Calculate due date
        calculator = DueDateCalculator(validation_result)
        due_date = calculator.calculate_due_date(lmp_date_str)
        
        if due_date:  # Only print congratulations if date is valid and due date is calculated
            print(f"Congratulations! Your Baby's Estimated Due Date Is: {due_date}")
        else:
            print("Error: Due date calculation failed.")


# Run the app
if __name__ == "__main__":
    app = DueDatePredictor()
    app.run()
