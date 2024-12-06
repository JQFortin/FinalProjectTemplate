# Final Project Report

* Student Name: Jianqiao Fortin
* Github Username: JQFortin
* Semester: 2024 Fall
* Course: CS 5001



## Description 
General overview of the project, what you did, why you did it, etc. 

This project is a due date calculator which also can be used for pregnancy-related journaling. I came up with this project because as a mom with two young kids, I benefited a lot from using these type of app online, and was very intrigued by how it works. Also from the initial planning, this project seems a great platform to utilize lots of knowledge I learnt in the course CS5001. After discussing it with Estelita ( and receiving her comments and input), I decided to work on it. 

The first part would be write down a general plan for the project. So basically, this app includes two big parts, part #1 is due date predictor and pregnancy progress calculator; while part #2 is giving the users options to read pregnancy info related to the specific week, or to add/modify/delete journals if they wish. For part #1, date validation is a big part, because the nature of this application, we not only have to consider the common date input errors, but also have to specify the date range that makes sense. For part #2, we need to consider file handling, including file reading and writing. For this project, different modules can be nicely organized under different classes, making the code not only neat-looking, but also provide great extendability for future development. 

I also made this project capable of taking different user information. Basically, at the start of the program, it will ask to put in username. If the username is new, it will create a user "profile" by storing the user's last menstruation date as well as the period length. So next time the same user ( with the same username) login, the system will not ask for the same info again, but directly pull out the stored date/period length info to calculate the due date and pregnancy week/day.

For file handling in this project, we used CSV format files because it is more straightforward to handle. We put the weekly milestones info and medical info into one single CSV file, under different columns. Later when we read it, each row form a dictionary and the header becomes the keys and the assocaited info is the value.For the journal , we also add all users' journals into one single CSV, with different user names under "Name" column. When we need to display a specific user's journals, we will use the username to filter the corresponding info. 

At almost every step of running the program, the user can opt out of the program either by typing in "exit" or press an option key to accomplish that. It gives the user a lot of flexibility while using the program. Also error handling is throughout the entire program, taking into consideration all types of scenario where errors may occur. 


## Key Features
Highlight some key features of this project that you want to show off/talk about/focus on. 

The first key features I want to talk about is calculating the pregnancy progress as well as estimated due date based on the last menstruation date (LMP). While seemingly straightforward, it actually involves using a lot of knowledge, including the built-in datetime module in python. Also, the error handling is extensive, because we have to make sure the date was put in with the correct format, and within the correct range. We also need to consider if the month/day number actually makes sense, for example, 13/22/2024 or 02/30/2024 are not a valid dates because no month can be out of the 1-12 range and 02/30 simply does not exist. For 02/29, we also need to carefully define the condition, because apparently only leap year has 02/29, so we have to apply the definition of a leap year to get that included. 

Then there is the user login. The program begins with asking the user to put in her name. If the username is new, it will ask the user her lmp date and period length, then store those info into a CSV file. If the username was put in previously, then it will directly pull out the stored info and calculate/display the pregancy progress and due date automatically. 

The third feature I focused on is the journaling part. The journal serves as an emotional outlet for expectant parents, helping them reflect and document their pregnancy journey. Also, integration with milestone and medical information provides week-specific advice, making the program both functional and meaningful. The design of the code makes checking, adding, modifying and deleting journals very easy, and the operation is limited to that specific user's journals, thus protecting other users' privacy. 


## Guide
How do we run your project? What should we do to see it in action? - Note this isn't installing, this is actual use of the project.. If it is a website, you can point towards the gui, use screenshots, etc talking about features. 

We can run this program directly from terminal. 
From my macbook, the command line is:

python3 "/Users/cindywang/Documents/NEU-Align MSCS/CS5001/Final Project/FinalProjectTemplate FINAL COPY/src/due_date_calculator.py" 

For other local machines, the file path needs to be modified to reflect the actual situtation. 

## Installation Instructions
If we wanted to run this project locally, what would we need to do?  If we need to get API key's include that information, and also command line startup commands to execute the project. If you have a lot of dependencies, you can also include a requirements.txt file, but make sure to include that we need to run `pip install -r requirements.txt` or something similar.

There is no external resources that need to be installed in order to run this program. We can run this program directly from terminal. 
Command line:
python3 "/Users/cindywang/Documents/NEU-Align MSCS/CS5001/Final Project/FinalProjectTemplate FINAL COPY/src/due_date_calculator.py" 

## Code Review
Go over key aspects of code in this section. Both link to the file, include snippets in this report (make sure to use the [coding blocks](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#code)).  Grading wise, we are looking for that you understand your code and what you did. 


Here is the link to the code : https://github.com/JQFortin/FinalProjectTemplate/blob/main/src/due_date_calculator.py

All parts of the code in due_date_calculator.py include detailed docstrings and in-line comments. 
And below is the part to be reviewed ( taking displaying jounrnal entry and adding journal entry as examples, docstrings and in-line comments are mostly removed for easier view):

```python
def display_journal_entries(self) -> None:
    journal_file = "data/pregnancy_journal.csv"

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
            for idx, row in enumerate(entries, start=1):  
                print(f"{idx}. {row['Date']} - {row['Entry']}") 
    except IOError:
        print("Error: Unable to read the journal file.")
    except KeyError as e:
        print(f"Error: Missing expected column in the file: {e}")
```
Review of the above code:

    This method is for displaying the current journal entries for the logged-in user.

    This method reads from the pregnancy journal CSV file and displays all entries related to the logged-in user. The entries are filtered by the user's name. If no entries are found for the user, a corresponding message is shown. The function also handles errors related to file access and missing columns.

    Below is how this section of code would accomplish:
    - If the journal file doesn't exist, a message is displayed and the function exits.
    - If the journal file is missing the expected "Name" column, an error message is displayed.
    - If no entries are found for the logged-in user, a corresponding message is displayed indicating so.
    - If there are entries, they are displayed in a numbered list ( starting from 1), showing the date and entry content.

    The variable journal_file points to the relative path "data/pregnancy_journal.csv". Ensure that this file path is correct and accessible for the function's context. If the directory or file doesn't exist, the function will handle it and print out a message.

    The file is opened in read mode ("r") using csv.DictReader, which reads the file as a dictionary (row by row) with the CSV header as the keys. This allows access to columns by their names (e.g., row['Date'], row['Entry']).

    If there is an error accessing or reading the journal file, an IOError will be raised; if a required column (e.g., "Name") is missing from the journal file, a KeyError will be raised. 

    Also entries are displayed in a numbered list. The enumerate(entries, start=1) function is used to display entries starting from 1 (instead of the default index of 0). This is more user-friendly for display purposes. The formatting of the display (f"{idx}. {row['Date']} - {row['Entry']}") is clear and well-structured.


```python
def add_journal_entry(self) -> None:
        journal_file = "data/pregnancy_journal.csv"  # define the relative file path

        # Check if the file exists
        file_exists = exists(journal_file)

        # Write a new entry
        new_entry = input("\nWrite a new entry below (or type 'exit' to cancel):\n> ")
        if new_entry.lower() == 'exit':  #if input is "exit"
            print("Entry creation canceled.")
            return  # Exit the method

        try:
            with open(journal_file, mode="a", newline="") as journal:  
                writer = csv.writer(journal)  
                if not file_exists:
                    writer.writerow(["Name", "Date", "Entry"]) 
                writer.writerow([self.user.name, datetime.now().strftime("%m/%d/%Y"), new_entry]) 
                print("Entry saved!")
        except IOError:
            print("Error: Unable to save the journal entry.")
```
    
    This method is for logged-in users to add new journal entries to the pregnancy journal file. 

    This function prompts the user to write a new journal entry. If the user types 'exit', the operation is canceled and the method exits. If the user enters a valid entry, the new journal entry is appended to the pregnancy journal file. If the journal file doesn't exist, it is created with appropriate headers for "Name", "Date", and "Entry". The entry is saved with the current date and the user's name.

    Below is how this section of code would accomplish:

    - If the journal file doesn't exist, the function checks this and prepares to create or append to the file, ensuring the journal entries can still be saved.
    -The user is prompted to enter a journal entry or type 'exit' to cancel the operation. If 'exit' is typed, the operation is canceled and the function exits without making changes.
    - If the file does not exist, it writes headers ("Name", "Date", "Entry") to the file before adding the user's new entry.
    - A new journal entry is appended to the file with the current date, the logged-in user's name, and the content provided by the user.
    - If there is an issue accessing or writing to the journal file, an IOError is raised, and an error message is displayed.
    
    The variable journal_file points to the relative path "data/pregnancy_journal.csv". This file path needs to be ensured correct in order for the method to perform as intended. If there is no such file existing yet, the program will create and save it.

    The function uses csv.writer to write the data to the file. In append mode (mode="a"), it allows for the journal entries to be added to the end of the file without overwriting existing data.

    In the case that the file does not yet exist, it writes the header row first (writer.writerow(["Name", "Date", "Entry"])). Then, the new entry is added with the user's name, the current date (formatted as MM/DD/YYYY), and the text of the journal entry.

    If there’s an issue while saving the entry, an IOError will be caught and an error message will be displayed.

    Additionally, the function handles the case where the user decides not to enter an entry by typing 'exit'. This gives the user more flexibility and greater control when using this program. 


### Major Challenges
Key aspects could include pieces that your struggled on and/or pieces that you are proud of and want to show off.

The major challenges I entered include (1) how to handle multiple users information storage and log-in. (2) how to ensure file path is correct; (4) how to properly set up the extensive file handling, including multiple options ( 1-7) offered to the users; (5) proper use of classes and objects . 
In general, class DueDatePredictor and its assocaited methods are the hardest part of the project. 

## Example Runs
Explain how you documented running the project, and what we need to look for in your repository (text output from the project, small videos, links to videos on youtube of you running it, etc)

I run the project in the VS code terminal, then copied the output into .txt files. Also I did screenshot for the same output ( To avoid confusion, screenshots only include the terminal output-1.txt content) . All those are placed under the "Example Runs" folder in my gitHub repo. 

And below is the link for that folder:
https://github.com/JQFortin/FinalProjectTemplate/tree/main/Example%20Runs

## Testing
How did you test your code? What did you do to make sure your code was correct? If you wrote unit tests, you can link to them here. If you did run tests, make sure you document them as text files, and include them in your submission. 

> _Make it easy for us to know you *ran the project* and *tested the project* before you submitted this report!_

I did unit tests mostly for the data validation part, and the unit test link is below:
https://github.com/JQFortin/FinalProjectTemplate/blob/main/test/test_due_date_calculator.py

Also I run the project to test the journal entries part. The .txt output files and screenshots are included under folder " Example Runs". I also visually compared the info display with those on the cvs file, such as  journal entries display for the specific user, week-specific pregnancy milestones and medical info display , etc. 

## Missing Features / What's Next
Focus on what you didn't get to do, and what you would do if you had more time, or things you would implement in the future. 

(1)Besides the last menstrual period start date, more ways to calculate the due date can be added , such as using the conception date, IVF 3/5 day transfer date, ultrasound date and weeks/days shown. 

(2)We can also desgin the program to be able to handle multiple journal entries at one time, such as deleting more than one journal entries at the same time

(3) User login information can be more sophiscated, with username, user profile , password, etc. 

(4) It certainly can integrate with GUI to make it more like a website 

## Final Reflection
Write at least a paragraph about your experience in this course. What did you learn? What do you need to do to learn more? Key takeaways? etc.

From this course CS 5001, I got the opportunity to be exposed in extensive training on the programming language Python. We learnt from the very basics, such as conditionals , arithmetic operators, while loop and for loop, string/list/tuple/set/dictionary, to more advanced part such as error handling and file handling, class/object as well as basics in data structure. It is certainly a lot of knowledge, but most importantly, I learnt the mind set of coding: divide, conquer, glue. I also applied this technique in this final project: thinking about what are the parts that needs to be done, write a list down, then build it one part at a time. Also I learnt good practice in code writing, such as PEP8 style, as well as documenting as much as I can. Besides, we are also exposed to technical-interview style code walks, and were offered online resources that are relevant to tech interviews in our future job hunting. All of those are hyper-useful of course.

If I had more time, I would probably attend more online classes on Python at the same time, as the material covered in class videos are still quite limited, sometimes quite vague too. So I need to check a lot of online resources as I go along. While that was certainly useful, I was hoping to get more systematic training so the knowledge structure would be more solid and long-lasting. Also I get from the course that, in order to progress continuously, I need to take time to practice often to make the knowledge really sunk in. 


## References
https://www.babycenter.com/pregnancy-due-date-calculator ( the principles of calculating due date)

https://www.simplilearn.com/tutorials/python-tutorial/datetime-in-python#:~:text=In%20the%20Python%20programming%20language,a%20built%2Din%20Python%20module. ( what datetime in python is)

https://docs.python.org/3/library/datetime.html ( regarding datetime and timedelta)

https://www.geeksforgeeks.org/built-in-modules-in-python/ ( what are built-in modules in python)

https://www.geeksforgeeks.org/python-datetime-strptime-function/ ( about the strptime function to format date in python )

https://www.datacamp.com/tutorial/converting-strings-datetime-objects ( how to convert date strings to datetime objects)

https://www.digitalocean.com/community/tutorials/parse-csv-files-in-python ( how to parse csv files in python)

https://docs.python.org/pl/3.6/library/typing.html 

https://www.tutorialsteacher.com/python/staticmethod-decorator  ( static methods in python that do not have cls or self parameter)

https://www.geeksforgeeks.org/python-map-function/#converting-the-map-object-to-a-list ( map function in python)

https://www.freecodecamp.org/news/python-datetime-now-how-to-get-todays-date-and-time/

https://www.geeksforgeeks.org/python-check-if-a-file-or-directory-exists/ 

https://www.pythontutorial.net/python-basics/python-check-if-file-exists/ ( how to check if a file exist)

https://www.geeksforgeeks.org/writing-csv-files-in-python/

https://docs.python.org/3/library/csv.html ( read cvs files in python)

https://arcade.makecode.com/courses/csintro2/logic/booleans ( boolean flag)

https://docs.python.org/3/library/csv.html ( csv.writer, csvwriter.writerow , csvwriter.writerows)
