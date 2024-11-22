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
            datetime: The parsed datetime object, or None if invalid.
        """
        try:
            return datetime.strptime(date_str, '%m/%d/%Y')
        except ValueError:
            return None


class DueDateCalculator:
    """Class to calculate the due date based on LMP."""
    def __init__(self,lmp_date):
        """
        Initialize the calculator with the LMP date.
        
        Parameters:
            lmp_date (datetime): The datetime object representing the LMP.
        """
        self.lmp_date=lmp_date  
        self.start_date = datetime.strptime("03/01/2024", "%m/%d/%Y")
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


    def calculate_due_date(self,lmp_date_str):
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
        print("Welcome to the BabyLand - A Comprehensive Toolbox for Your Pregancy Journey! ")

    def run(self):
        """
        Run the application.
        """
        lmp_date_str = input("Please enter the first day of your last menstrual period (MM/DD/YYYY): ")
        
        # Validate the input date
        lmp_date = DateValidator.validate_date(lmp_date_str)
        if not lmp_date:
            print("Invalid date format. Please use 'MM/DD/YYYY'.")
            return
        
        # Calculate due date
        calculator = DueDateCalculator(lmp_date)
        due_date = calculator.calculate_due_date(lmp_date_str)
        print(f"Congratulations! Your Baby's Estimated Due Date Is: {due_date}")


# Run the app
if __name__ == "__main__":
    app = DueDatePredictor()
    app.run()
