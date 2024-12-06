from datetime import datetime, timedelta
from typing import Union
import csv
from os.path import exists


class User:
    """
        This class stores the user's name, the date of their last menstrual period (LMP),
        and the length of their menstrual cycle. It provides methods to set the LMP date,
        set the period length, save user data to a CSV file, and load user data from a CSV file.

        Attributes:
        name (str): The name of the user.
        lmp_date (datetime): The date of the user's last menstrual period (LMP), stored as a datetime object.
        period_length (int): The length of the user's menstrual cycle, default is 28 days.

        Methods:
        set_lmp_date(lmp_date: datetime) -> None:
            Sets the LMP date for the user.

        set_period_length(period_length: int) -> None:
            Sets the period length for the user.

        save_to_file(file_name: str = "data/user_data.csv") -> None:
            Saves the user's data to a CSV file. If the file does not exist, it creates it.

        load_from_file(user_name: str, file_name: str = "data/user_data.csv") -> Union[User, None]:
            Loads a user's data from a CSV file based on the provided user name. Returns a User object
            if found, or None if the user is not found or the file cannot be read.
    """
    
    def __init__(self, name: str) -> None :
        self.name = name
        self.lmp_date = None  # Last menstrual period (lmp) date (datetime object)
        self.period_length = 28  # Default to 28 days
        
    def set_lmp_date(self, lmp_date: datetime) -> None:
        self.lmp_date = lmp_date

    def set_period_length(self, period_length: int) -> None:
        self.period_length = period_length

    def save_to_file(self, file_name: str = "data/user_data.csv") -> None:
        """Save user data to a CSV file."""
        file_exists = exists(file_name)
        try:
            # append mode, if the file already exists, the new data will be added to the end of the file. If the file doesn't exist, it will be created.
            # the variable user_file is a file object representing the opened file. 
            with open(file_name, mode="a", newline="") as user_file:  
                writer = csv.writer(user_file)  #creates a CSV writer object that is used to write data to the user_file in CSV
                if not file_exists:
                    writer.writerow(["Name", "LMP Date", "Period Length"])  # create the header if the specified cvs file does not exist
                writer.writerow([self.name, self.lmp_date.strftime("%m/%d/%Y"), self.period_length])  #if the specified csv file already exist, add new entry to the file along with the current date info
        except IOError:
            print("Error: Unable to save user data.")

    @staticmethod
    def load_from_file(user_name: str, file_name: str ="data/user_data.csv") -> None:
        """Load user data from a CSV file if it exists."""
        if not exists(file_name):
            return None

        try:
            with open(file_name, mode="r") as user_file:
                reader = csv.DictReader(user_file)  # reads the contents of a CSV file and returns each row as a dictionary. "Name", "LMP date" and "Period Length" are keys and the corresponding input are values.
                for row in reader:
                    if row["Name"] == user_name:  # access the value from a dictionary by its key ("Name")
                        user = User(name=user_name)  # creating a new instance (or object) of the User class and assigning it to the variable user.
                        user.set_lmp_date(datetime.strptime(row["LMP Date"], "%m/%d/%Y"))  # accesses the value of last menstruation period (lmp) from the row dictionary using key "LMP date"
                        user.set_period_length(int(row["Period Length"]))  # access the value of period length from the row dictionary using key "Period Length"
                        return user
        except IOError:
            print("Error: Unable to load user data.")
        return None


class DateValidator:
    """Class to handle date validation and parsing."""
    @staticmethod
    def is_valid_day_in_month(month: int, day: int, year: int) -> bool:
        """
        Checks if the given day is a valid day in the specified month and year, also considering leap years when checking for the validity of February 29th.

        Args:
            month (int): The month of the year (1-12).
            day (int): The day of the month (1-31).
            year (int): The year to check for leap year (e.g., 2024).

        Returns:
            bool: True if the day is a valid day in the specified month and year, False otherwise.
        """
        days_in_month = {
            1: 31, 2: 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28,
            3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
        }
        return 1 <= day <= days_in_month.get(month, 0)  # if the month number does not exist, get 0 instead of raising error

    @staticmethod
    def is_valid_date_range(date: datetime) -> bool:
        """
        Checks if the given date is within a valid range for a Last Menstrual Period (LMP) date.

        The valid date range is between 280 days ago from the current date and the current date itself,
        as a Last Menstrual Period (LMP) must be within this period to ensure the user is currently pregnant, not in the past or in the future.

        Args:
            date (datetime): The LMP date to check.

        Returns:
            bool: True if the given date is within the valid range, False otherwise.
        """
        start_date = datetime.now() - timedelta(days=280)  # the earliest last menstruation date allowed by the program
        current_date = datetime.now()  # getting the current date as a datetime object
        return start_date <= date <= current_date  # the input lmp date must be between the two date limits to make sense

    @staticmethod
    def validate_date(date_str: str) -> Union[datetime, str]:
        """
        Validates a date string in the format 'MM/DD/YYYY'.

        Args:
            date_str (str): A string representing the date in 'MM/DD/YYYY' format.

        Returns:
            Union[datetime, str]: 
                - If the date is valid, returns a `datetime` object representing the input date.
                - If the date is invalid, returns an error message as a string indicating the corresponding issue.
        """
        try:
            month, day, year = map(int, date_str.split("/"))  # # Split the date string (format: 'MM/DD/YYYY') by '/' and convert each part to an integer (month, day, year)
            if month < 1 or month > 12:
                return "Invalid month. Month must be between 01 and 12."
            if not DateValidator.is_valid_day_in_month(month, day, year):
                return f"The date you entered is not valid: {month:02}/{day:02}/{year}. Please double-check and try again."
            date = datetime.strptime(date_str, '%m/%d/%Y')
            if not DateValidator.is_valid_date_range(date):
                start_date = (datetime.now() - timedelta(days=280)).strftime("%m/%d/%Y")
                current_date = datetime.now().strftime("%m/%d/%Y")
                return f"Invalid date range. Please enter a date between {start_date} and today's date ({current_date})."
            # If the date entered in invalid, give the valid date range suggestion, which is between today's date and the date 280 days before today)
            return date
        except ValueError:  # for any input that is not in the format of MM/DD/YYYY with MM DD YYYY only being decimal digits
            return "Invalid date format. Please use 'MM/DD/YYYY', and only numbers 0-9."
        

class DueDateCalculator:
    """Class to calculate the due date and pregnancy progress."""
    def __init__(self, lmp_date: datetime, period_length: int = 28) -> None:
        """
        Initializes an instance of the DueDateCalculator class.

        Args:
            lmp_date (datetime): The date of the Last Menstrual Period (LMP).
            period_length (int, optional): The length of the menstrual cycle in days. Defaults to 28.
        """
        if not isinstance(period_length, int) or not (20 <= period_length <= 45):
            raise ValueError("Period length must be an integer between 20 and 45 days.")  # Enforce validation of the period_length attribute
        self.lmp_date = lmp_date
        self.period_length = period_length

    def calculate_due_date(self) -> datetime:
        """
        The estimated due date is calculated by adjusting the LMP date based on the difference between the user's period length and the default 28-day cycle. 
        Then, 280 days is added to the adjusted LMP to estimate the due date.

        Returns:
            datetime: The estimated due date of the pregnancy.
        """
        adjusted_lmp = self.lmp_date + timedelta(days=(self.period_length - 28))
        return adjusted_lmp + timedelta(days=280)

    def calculate_current_progress(self) -> tuple:
        """
        Calculates the current progress in pregnancy, in terms of weeks and days, based on the LMP and period length.

        Returns:
            tuple: A tuple containing the number of weeks and days of pregnancy.
        """
        adjusted_lmp = self.lmp_date + timedelta(days=(self.period_length - 28))  # Adjusted LMP date
        total_days_pregnant = (datetime.now() - adjusted_lmp).days
        weeks = total_days_pregnant // 7
        days = total_days_pregnant % 7
        return weeks, days  # weeks and days are returned as a tuple


class DueDatePredictor:
    """Class to run the program and get the predicted due date with user input."""
    def __init__(self) -> None:
        """
        Initializes the DueDatePredictor class.

            - Greets the user with an opening message.
            - Prompts the user to enter their name.
            - Attempts to load an existing user profile using the provided name.
            - Sets the `is_new_user` flag to `True` if no existing user data is found, otherwise `False`.
            - If the user is new, guides them to set up their profile by creating a new User object with the entered name.

        Attributes:
            - self.user (User): The user's profile loaded from file or created for new users.
            - self.is_new_user (bool): A flag indicating whether the user is new (True) or returning (False).
        """
        print("Welcome to BabyLand - A Comprehensive Toolbox for Your Pregnancy Journey!")  # opening greeting
        user_name = input("Please enter your name: ").strip()
        self.user = User.load_from_file(user_name)  # load user data from file if already exists
        self.is_new_user = self.user is None  # Flag to determine if user is new. True If self.user does not exist; false if otherwise
        if self.is_new_user:
            print("No previous data found. Let's set up your profile.")
            self.user = User(name=user_name)  # create a new User object for the new user


    def run(self) -> None:
        """
        Executes the main workflow of the DueDatePredictor program.
        
        Steps:
            
            - Collects user data if LMP date is missing.
            - Terminates if the user exits during data collection.
            - Calculates the due date and pregnancy progress.
            - Displays a personalized greeting and pregnancy information.
            - Offers additional options via `display_options()`.

        Attributes:
            - self.user (User): object under class User to represent the user's profile containing LMP date and other details.
            - self.is_new_user (bool): A flag indicating if the user is new (True) or returning (False).
        """

        if not self.user.lmp_date:  # if user does not already exist, then collect user data by running method collect_user_data()
            self.collect_user_data()

        # If the user exited during data collection, terminate the program
        if not self.user.lmp_date:
            return

        calculator = DueDateCalculator(self.user.lmp_date, self.user.period_length)  # calculate due date based on user lmp date and period length input
        due_date = calculator.calculate_due_date()  
        weeks, days = calculator.calculate_current_progress()

        
        if self.is_new_user:  # Use the is_new_user flag to determine the message
            print(f"\nWelcome, {self.user.name}!")  # greeting for new user
        else:
            print(f"\nWelcome back, {self.user.name}!")  # greeting for returning user

        print(f"You are currently {weeks} weeks and {days} days pregnant.")
        print(f"Your baby's estimated due date is: {due_date.strftime('%m/%d/%Y')}")
        self.display_options(weeks)


    def collect_user_data(self) -> None:
        """
        Collects and validates the user's LMP and period length for pregnancy due date prediction.

        Prompts the user to input:
            - The first day of their last menstrual period (LMP) in MM/DD/YYYY format.
            - Their normal menstrual cycle length (default 28 days if left blank).

        If valid, the data is saved to the user's profile. If the user types 'exit' at any point, the process terminates without saving data.

        Attributes:
            - self.user.lmp_date (datetime): The user's LMP date.
            - self.user.period_length (int): The user's menstrual cycle length in days.
        """
        while True:
            lmp_date_str = input("Please enter the first day of your last menstrual period (MM/DD/YYYY), or type 'exit' to quit: ")
            if lmp_date_str.lower() == 'exit':  # if input is "exit"
                print("Thank you for using BabyLand. Goodbye!")
                return  # Exit immediately without saving the lmp info, also automatically breaks the while loop

            validation_result = DateValidator.validate_date(lmp_date_str)
            if isinstance(validation_result, datetime):
                self.user.set_lmp_date(validation_result)  # if the user input of lmp date is valid, program takes the input
                break  # exit the while loop
            else:
                print(validation_result)  # if the user input of lmp date is invalid, bounce back to the beginning of the loop to ask user input one more time

        while True:
            period_length_str = input("Please enter your normal menstrual cycle length in days (default is 28), or type 'exit' to quit: ")
            if period_length_str.lower() == 'exit':  # if input is "exit"
                print("Thank you for using BabyLand. Goodbye!")
                self.user.lmp_date = None  # Reset LMP date to avoid saving incomplete data ( need both valid lmp date and period length to store user info)
                return  # Exit immediately without saving period length, also automatically breaks the while loop

            if period_length_str.strip() == "":  # If the user presses Enter without input
                self.user.set_period_length(28)  # Use the default value
                self.user.save_to_file()  # utilize the method save_to_file under class User to save the period length info
                break

            try:
                period_length = int(period_length_str)  # convert the type of input from str to int
                if 20 <= period_length <= 45:  # check if the period length is within the set range
                    self.user.set_period_length(period_length)  # set the period length to user input 
                    self.user.save_to_file()
                    break
                else:
                    print("Invalid period length. Please enter a value between 20 and 45.")  # print the error message, then return to the beginning of the while loop to ask user input again
            except ValueError:
                print("Invalid input. Please enter a valid integer value.")


    def display_options(self, current_week : int) -> None:
        """
        Displays a menu of options for the user to interact with the program.

        Prompts the user to select an option to:
            - View pregnancy milestones, medical info, or journal entries.
            - Add, modify, or delete journal entries.
            - Exit the program.

        Args:
            current_week (int): The current week of pregnancy to display relevant information.
        """
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
                self.display_journal_entries()
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


    def display_milestone_info(self, week : int) -> None:
        """
        Displays the pregnancy milestone for the given week.

        Searches the 'milestone_medical_info.csv' file for the milestone corresponding to the specified week to display.
        If the file is missing or no data is found for the week, a corresponding error message is displayed.

        Args:
            week (int): The week of pregnancy for which to display milestone information.
        """
        file = "data/milestone_medical_info.csv"  # specify the relative file path
        if not exists(file):
            print("Data file not found.")
            return

        with open(file, mode="r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if int(row["Week"]) == week:  # find corresponding week information
                    print(f"Week {row['Week']}: {row['Milestone']}")  # print values associated with keys "Week" and "Milestone"
                    return
            print(f"No milestone info found for week {week}.")  # output if no info stored in the csv file for a specific week

    def display_medical_info(self, week: int) -> None:
        """Display weekly medical information for the given week.

        Searches the 'milestone_medical_info.csv' file for the medical info corresponding to the specified week to display.
        If the file is missing or no data is found for the week, a corresponding error message is displayed.

        Args:
            week (int): The week of pregnancy for which to display milestone information.
        """
        file = "data/milestone_medical_info.csv"  # specify the relative file path
        if not exists(file):
            print("Data file not found.")
            return

        with open(file, mode="r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:  # find corresponding week information
                if int(row["Week"]) == week:
                    print(f"Week {row['Week']}: {row['Medical_Info']}") # print values associated with keys "Week" and "Milestone"
                    return
            print(f"No medical info found for week {week}.")  # output if no info stored in the csv file for a specific week


    def display_journal_entries(self) -> None:
        """Display current journal entries specific to the logged-in user."""
        journal_file = "data/pregnancy_journal.csv"  # define the relative file path

        if not exists(journal_file):
            print("\nNo journal entries found.")
            return

        print(f"\nJournal entries for {self.user.name}:")
        try:
            with open(journal_file, mode="r") as journal:
                reader = csv.DictReader(journal)
                
                # Check if "Name" column exists in the header
                if "Name" not in reader.fieldnames:
                    print("Error: The journal file is missing the 'Name' column in its header.")
                    return

                entries = [row for row in reader if row["Name"] == self.user.name]

            # If there are no entries for the current user
            if not entries:
                print("\nNo journal entries found for your profile.")
            else:
                for idx, row in enumerate(entries, start=1):  # by default the enumerate function index starts with 0, but here we specify it starts from 1 instead
                    print(f"{idx}. {row['Date']} - {row['Entry']}")  # define the format in which the journal entries are displayed
        except IOError:
            print("Error: Unable to read the journal file.")
        except KeyError as e:
            print(f"Error: Missing expected column in the file: {e}")


    def add_journal_entry(self) -> None:
        """
        Allow the user to start or update a pregnancy journal.
        If the user types 'exit', the operation is canceled. If the journal file does not exist, it will be created with the appropriate headers. 
        
        Attributes:
        self.user.name (str): The name of the logged-in user.
        """
        journal_file = "data/pregnancy_journal.csv"  # define the relative file path

        # Check if the file exists
        file_exists = exists(journal_file)

        # Write a new entry
        new_entry = input("\nWrite a new entry below (or type 'exit' to cancel):\n> ")
        if new_entry.lower() == 'exit':  #if input is "exit"
            print("Entry creation canceled.")
            return  # Exit the method

        try:
            # append mode, if the file already exists, the new data will be added to the end of the file. If the file doesn't exist, it will be created. 
            # The variable journal is the file object representing the opened file.
            with open(journal_file, mode="a", newline="") as journal:  
                writer = csv.writer(journal)  #creates a CSV writer object that is used to write data to the journal in CSV
                if not file_exists:
                    writer.writerow(["Name", "Date", "Entry"])  # create the header if the specified cvs file does not exist
                writer.writerow([self.user.name, datetime.now().strftime("%m/%d/%Y"), new_entry]) # if the specified csv file already exist, add new entry to the file along with the current date info
                print("Entry saved!")
        except IOError:
            print("Error: Unable to save the journal entry.")


    def modify_journal_entry(self):
        """
        Modify an existing journal entry.
        
        If the user types 'exit', the operation is canceled. If the journal entry does not exist, it will exit the method and prompt user to start the option menu all over again. 
        If the journal entry does exist, modification will overwrite the original entry. 

        Attributes:
        self.user.name (str): The name of the logged-in user.
        """
        journal_file = "data/pregnancy_journal.csv"  # define the relative file path

        if not exists(journal_file):
            print("\nNo journal entries found.")
            return

        # Display current entries
        with open(journal_file, mode="r") as journal:
            reader = csv.reader(journal)  # Create a CSV reader object to read the content of the journal file
            entries = list(reader)  # Convert the CSV reader object into a list of rows (entries)

        if len(entries) <= 1:  # if the file is empty or only contain header row
            print("\nNo journal entries found.")
            return

        # Filter entries for the current user
        user_entries = [row for row in entries[1:] if row[0] == self.user.name]  # slices the entries list, excluding the first element (index 0), which is excluding the header row

        # handle situation when there is no user entried found
        if not user_entries:  
            print("\nNo journal entries found for your profile.")
            return

        # For user journal entries found, display them
        print("\nCurrent journal entries:")
        for idx, row in enumerate(user_entries, start=1):
            print(f"{idx}. {row[1]} - {row[2]}")  # Assuming columns: Name, Date, Entry. row[1] represents Date and row[2] represents Entry

        try:
            entry_num = input("\nEnter the number of the entry you want to modify (or type 'exit' to cancel): ")
            if entry_num.lower() == 'exit':  #if user put in "exit" then program end without modifying any journal entries
                print("Modification canceled.")  
                return  # Exit the method
            
            entry_num = int(entry_num)
            if 1 <= entry_num <= len(user_entries):
                new_text = input("Enter the new text for the entry (or type 'exit' to cancel):\n> ")
                if new_text.lower() == 'exit':  # handle the case where the input is "exit"
                    print("Modification canceled.")
                    return  # Exit the method
                
                user_entries[entry_num - 1][2] = new_text  # Update the entry text. user_entries[entry_num - 1][2] allow access to the 3rd column in the csv file of the selected entry number, which is the corresponding journal entry. 
                # Write the modified entries back to the file
                with open(journal_file, mode="w", newline="") as journal:
                    writer = csv.writer(journal)  # Creates a csv.writer object, which is used to write rows of data to the journal file in CSV format.
                    writer.writerows(entries)  # write back all rows, including the updated one, to the file.
                print("Entry updated!")
            else:
                print("Invalid entry number. Please try again from the menu below.")
        except ValueError:
            print("Invalid input. Please enter a number.")


    def delete_journal_entry(self):
        """
        Allow the user to delete a journal entry by number.
        
        If the user types 'exit', the operation is canceled. If the journal entry does not exist, it will exit the method and prompt user to start the option menu all over again. 
        If the journal entry does exist, the original entry will be removed from the journal file. 

        Attributes:
        self.user.name (str): The name of the logged-in user.
        """
        journal_file = "data/pregnancy_journal.csv"  # define the relative file path
        
        if not exists(journal_file):
            print("\nNo journal entries found.")
            return

        # Read all entries
        with open(journal_file, mode="r") as journal:
            reader = csv.reader(journal)  # Create a CSV reader object to read the content of the journal file
            entries = list(reader)  # Convert the CSV reader object into a list of rows (entries)

        # If there are no entries or only the header exists
        if len(entries) <= 1:
            print("\nNo journal entries found.")
            return

        # Filter entries for the current user
        user_entries = [row for row in entries[1:] if row[0] == self.user.name]  #slices the entries list, excluding the first element (index 0), which is excluding the header row

        # handle situation when there is no user entried found
        if not user_entries:
            print("\nNo journal entries found for your profile.")
            return

        # Display current journal entries with numbers
        print("\nCurrent journal entries:")
        for idx, row in enumerate(user_entries, start=1):
            print(f"{idx}. {row[1]} - {row[2]}")  # Assuming columns: Name, Date, Entry. row[1] represents Date and row[2] represents Entry

        # Prompt the user to enter the journal entry number to delete
        try:
            entry_to_delete = input("\nEnter the number of the journal entry you want to delete (or type 'exit' to cancel): ")
            if entry_to_delete.lower() == 'exit':  #if user put in "exit" then program end without deleting any journal entries
                print("Deletion canceled.")
                return  # Exit the method

            entry_to_delete = int(entry_to_delete)
            if entry_to_delete < 1 or entry_to_delete > len(user_entries):  # Check if the entry exists
                print("Error: Invalid entry number. Please try again from the menu below.")
                return
        except ValueError:
            print("Error: Invalid input. Please enter a valid number.")
            return

        # Delete the selected journal entry
        entry_to_delete = user_entries[entry_to_delete - 1]
        entries.remove(entry_to_delete)

        # Write the updated entries back to the file
        with open(journal_file, mode="w", newline="") as journal:
            writer = csv.writer(journal)  # Creates a csv.writer object, which is used to write rows of data to the journal file in CSV format.
            writer.writerows(entries)  # write back all rows, including the updated one, to the file.
            print(f"Entry {entry_to_delete[1]} has been deleted.")  


# Run the app
if __name__ == "__main__":
    app = DueDatePredictor()
    app.run()
