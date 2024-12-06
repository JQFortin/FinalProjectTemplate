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

And below is the part to be reviewed ( adding journal entry):

```python
def add_journal_entry(self) -> None:
    """Allow the user to start or update a pregnancy journal."""
    journal_file = "data/pregnancy_journal.csv"

    # Check if the file exists
    file_exists = exists(journal_file)

    # Write a new entry
    new_entry = input("\nWrite a new entry below (or type 'exit' to cancel):\n> ")
    if new_entry.lower() == 'exit':
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

### Major Challenges
Key aspects could include pieces that your struggled on and/or pieces that you are proud of and want to show off.


## Example Runs
Explain how you documented running the project, and what we need to look for in your repository (text output from the project, small videos, links to videos on youtube of you running it, etc)

## Testing
How did you test your code? What did you do to make sure your code was correct? If you wrote unit tests, you can link to them here. If you did run tests, make sure you document them as text files, and include them in your submission. 

> _Make it easy for us to know you *ran the project* and *tested the project* before you submitted this report!_


## Missing Features / What's Next
Focus on what you didn't get to do, and what you would do if you had more time, or things you would implement in the future. 

(1)Besiding the last menstrual period start date, more ways to calculate the due date can be added , such as using the conception date, IVF 3/5 day transfer date, ultrasound date and weeks/days shown. 

(2)We can also desgin the program to be able to handle multiple journal entries at one time, such as deleting more than one journal entries at the same time

(3) User login information can be more sophiscated, with username, user profile , password, etc. 

(4) It certainly can integrate with GUI to make it more like a website 

## Final Reflection
Write at least a paragraph about your experience in this course. What did you learn? What do you need to do to learn more? Key takeaways? etc.

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