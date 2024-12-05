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
        
        # Input LMP date with validation loop and exit option
        while True:
            lmp_date_str = input("Please enter the first day of your last menstrual period (MM/DD/YYYY), or type 'exit' to quit: ")
            
            if lmp_date_str.lower() == 'exit':  # Check if the user wants to exit
                print("Thank you for using BabyLand. Goodbye!")
                return  # Exit the program
            
            validation_result = DateValidator.validate_date(lmp_date_str)
            if isinstance(validation_result, datetime):  # Valid date
                lmp_date = validation_result
                break
            else:
                print(validation_result)  # Show error message and re-prompt
        
        # Input normal period length with validation loop and exit option
        while True:
            period_length_str = input("Please enter your normal menstrual cycle length in days (default is 28), or type 'exit' to quit: ")
            
            if period_length_str.lower() == 'exit':  # Check if the user wants to exit
                print("Thank you for using BabyLand. Goodbye!")
                return  # Exit the program
            
            try:
                period_length = int(period_length_str)
                if period_length < 20 or period_length > 45:
                    print("Invalid period length. Please enter a value between 20 and 45.")
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a valid integer value.")
        
        # Calculate due date and pregnancy progress
        calculator = DueDateCalculator(lmp_date, period_length)
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
            print("3: Display current journal entries.")
            print("4: Add a new journal entry.")
            print("5: Modify an existing journal entry.")
            print("6: Delete a journal entry.")
            print("7: Exit.")
            choice = input("Please select an option (1-7): ")
            if choice == "1":
                self.display_milestone_info(current_week)
            elif choice == "2":
                self.display_medical_info(current_week)
            elif choice == "3":
                self.display_journal_entires()
            elif choice == "4":
                self.add_journal_entry()
            elif choice == "5":
                self.modify_journal_entry()
            elif choice == "6":
                self.delete_journal_entry()
            elif choice == "7":
                print("Thank you for using BabyLand! Take care.")
                break
            else:
                print("Invalid choice. Please try again.")


    def display_milestone_info(self, week):
        """Display pregnancy milestone information for the given week."""
        file = "milestone_medical_info.csv"
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
        file = "milestone_medical_info.csv"
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


    def display_journal_entires(self):
        """Display current journal entries."""
        journal_file = "pregnancy_journal.csv"

        if not exists(journal_file):
            print("\nNo journal entries found.")
            return

        print("\nCurrent journal entries:")
        with open(journal_file, mode="r") as journal:
            reader = csv.reader(journal)
            entries = list(reader)

        # If there are no entries or only the header exists
        if len(entries) <= 1:
            print("\nNo journal entries found.")
        else:
            for idx, row in enumerate(entries[1:], start=1):  # Skip the header row
                print(f"{idx}. {row[0]} - {row[1]}")


    def add_journal_entry(self):
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

    def modify_journal_entry(self):
        """Modify an existing journal entry."""
        journal_file = "pregnancy_journal.csv"

        if not exists(journal_file):
            print("\nNo journal entries found.")
            return

        # Display current entries
        with open(journal_file, mode="r") as journal:
            reader = csv.reader(journal)
            entries = list(reader)

        if len(entries) <= 1:
            print("\nNo journal entries found.")
            return

        print("\nCurrent journal entries:")
        for idx, row in enumerate(entries[1:], start=1):
            print(f"{idx}. {row[0]} - {row[1]}")

        try:
            entry_num = int(input("\nEnter the number of the entry you want to modify: "))
            if 1 <= entry_num < len(entries):
                new_text = input("Enter the new text for the entry:\n> ")
                entries[entry_num][1] = new_text
                with open(journal_file, mode="w", newline="") as journal:
                    writer = csv.writer(journal)
                    writer.writerows(entries)
                print("Entry updated!")
            else:
                print("Invalid entry number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def delete_journal_entry(self):
        """Allow the user to delete a journal entry by number."""
        journal_file = "pregnancy_journal.csv"
        
        if not exists(journal_file):
            print("\nNo journal entries found.")
            return

        # Read all entries
        with open(journal_file, mode="r") as journal:
            reader = csv.reader(journal)
            entries = list(reader)

        # If there are no entries or only the header exists
        if len(entries) <= 1:
            print("\nNo journal entries found.")
            return

        # Display current journal entries with numbers
        print("\nCurrent journal entries:")
        for idx, row in enumerate(entries[1:], start=1):  # Skip the header row
            print(f"{idx}. {row[0]} - {row[1]}")

        # Prompt the user to enter the journal entry number to delete
        try:
            entry_to_delete = int(input("\nEnter the number of the journal entry you want to delete: "))
            if entry_to_delete < 1 or entry_to_delete >= len(entries):  # Check if the entry exists
                print("Error: Invalid entry number. Please try again.")
                return
        except ValueError:
            print("Error: Invalid input. Please enter a valid number.")
            return

        # Delete the selected journal entry
        del entries[entry_to_delete]  # Delete the entry at the specified index

        # Write the updated entries back to the file
        with open(journal_file, mode="w", newline="") as journal:
            writer = csv.writer(journal)
            writer.writerows(entries)
            print(f"Entry number {entry_to_delete} has been deleted.")


# Run the app
if __name__ == "__main__":
    app = DueDatePredictor()
    app.run()
