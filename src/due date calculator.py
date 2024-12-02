from datetime import datetime, timedelta
from typing import Union, List, Dict, Tuple, Any, NoReturn
import csv
from os.path import exists

class DateValidator:
    """Class to handle date validation and parsing."""
    @staticmethod
    def validate_date(date_str: str) -> Union[datetime, str]:        
        """
        Validate and parse a date string.
        
        Parameters:
            date_str (str): The date string in 'MM/DD/YYYY' format.
            
        Returns:
            datetime: The parsed datetime object, or an error message if invalid.
        """
        try:
            month, day, year = map(int, date_str.split("/"))  
            # Tuple unpacking. split input string-type date data in the format of MM/DD/YYYY into a string tuple (based on the separator "/"), then turn each of the element in the tuple into an integer type ( no leading 0 padding) ) and assign it to the corresponding variable ( month, day, or year). 
            if month < 1 or month > 12:
                return "Invalid month. Month must be between 01 and 12."
            if not DateValidator.is_valid_day_in_month(month, day, year):
                return f"The date you entered is not valid: {month:02}/{day:02}/{year}. Please double-check and try again."  # :02 ensure the 0 padding at the leading position of the month and day entry
            date = datetime.strptime(date_str, '%m/%d/%Y')  # format date using the strftime function
            if not DateValidator.is_valid_date_range(date):
                start_date = (datetime.now() - timedelta(days=280)).strftime("%m/%d/%Y")
                current_date = datetime.now().strftime("%m/%d/%Y")
                return f"Invalid date range. Please enter a date between {start_date} and today's date ({current_date})."
            return date
        except ValueError:
            return "Invalid date format. Please use 'MM/DD/YYYY', and only numbers 0-9."

    @staticmethod
    def is_valid_day_in_month(month: int, day: int, year: int) -> bool:
        """
        Check if a day is valid for a given month and year.

        Parameters:
            month (int): The month number (1-12).
            day (int): The day number.
            year (int): The year number.
    
        Returns:
            bool: True if the day is within the valid range for the specified month and year, False otherwise.
        """
        days_in_month = {
            1: 31, 2: 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28,  
            3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
        }  # dictionary to match days number values to month keys
        return 1 <= day <= days_in_month.get(month, 0)

    @staticmethod
    def is_valid_date_range(date: datetime) -> bool:  #date is a datetime object
        """
        Check if a given date is within a valid range.

        Parameters:
            date (datetime): the date to check
    
        Returns:
            bool: True if the date is within the valid range, False otherwise.
        """
        start_date = datetime.now() - timedelta(days=280)  # define the earliest valid start date using the timedelta class
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
    def __init__(self):
        print("Welcome to BabyLand - A Comprehensive Toolbox for Your Pregnancy Journey!")

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

        # Display options
        self.display_options(weeks)

    def display_options(self, current_week):
        """Display options to the user."""
        while True:
            print("\nOptions:")
            print("1: Display pregnancy milestone info corresponding to the week.")
            print("2: Display weekly medical info corresponding to the week.")
            print("3: Add to your pregnancy journal.")
            print("4: Exit.")
            choice = input("Please select an option (1-4): ")
            if choice == "1":
                self.display_milestone_info(current_week)
            elif choice == "2":
                self.display_medical_info(current_week)
            elif choice == "3":
                self.user_journal()
            elif choice == "4":
                print("Thank you for using BabyLand! Take care.")
                break
            else:
                print("Invalid choice. Please try again.")


    def display_milestone_info(self, week):
        """Display pregnancy milestone information for the given week."""
        file = "FinalProjectTemplate/src/milestone_medical_info.csv"
        if not exists(file):
            print("Data file not found.")
            return

        with open(file, mode="r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if int(row["Week"]) == week:
                    print(f"Week {row['Week']}: {row['Milestone']}")
                    return
            print(f"No milestone info found for week {week}.")

    def display_medical_info(self, week):
        """Display weekly medical information for the given week."""
        file = "FinalProjectTemplate/src/milestone_medical_info.csv"
        if not exists(file):
            print("Data file not found.")
            return

        with open(file, mode="r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if int(row["Week"]) == week:
                    print(f"Week {row['Week']}: {row['Medical_Info']}")
                    return
            print(f"No medical info found for week {week}.")

    def user_journal(self):
        """Allow the user to start or update a pregnancy journal."""
        print("\nPregnancy Journal:")
        journal_file = "pregnancy_journal.csv"

        # Check if the file exists
        file_exists = exists(journal_file)

        # Read and display existing entries
        if file_exists:
            print("\nCurrent journal entries:")
            with open(journal_file, mode="r") as journal:
                reader = csv.reader(journal)
                for row in reader:
                    print(f"{row[0]} - {row[1]}")
        else:
            print("\nNo journal entries found. Start by adding a new one!")

        # Write a new entry
        new_entry = input("\nWrite a new entry below:\n> ")
        try:
            with open(journal_file, mode="a", newline="") as journal:
                writer = csv.writer(journal)
                if not file_exists:
                    writer.writerow(["Date", "Entry"])
                writer.writerow([datetime.now().strftime("%m/%d/%Y"), new_entry])
                print("Entry saved!")
        except IOError:
            print("Error: Unable to save the journal entry.")


# Run the app
if __name__ == "__main__":
    app = DueDatePredictor()
    app.run()
