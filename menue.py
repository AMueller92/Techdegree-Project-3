import csv
import datetime
import os
import re

from algorithm import Search

start = Search()


def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")


def add_entry():
    clear_screen()
    print("What is the date of the task?")
    raw_date = input("Use the format DD/MM/YYYY  >  ")
    date = datetime.datetime.strptime(raw_date, "%d/%m/%Y")
    
    print("What is the task name?")
    task = input(">  ")
    
    print("How much time in minutes?")
    time = input(">  ")
    
    print("Additional notes...if you dont have any notes please press enter")
    notes = input(">  ")
    print("Thank you! Do you want to submit your entry? Y/N")
    decision = input(">  ")
    if decision.upper() == 'Y':
        start.add_to_file(date, task, time, notes)
        

def search_entry():
    clear_screen()
    input_user = None
    task_name = None
    task_notes = None
    task_minutes = None
    regex = None
    date_search = None
    date1 = None
    date2 = None
    initial_file = []
    search_file = []
    index_track = []
    start.open_file(initial_file)
    print("How would you like to search for an entry?")
    print("a) By Date")
    print("b) Between dates")
    print("c) By Time Spent")
    print("d) By a word")
    print("e) By regex pattern")
    print("f) Back to main menue")
    input_search = input("  > ")

    while True:
        if input_search == "a":
            # search by a date
            clear_screen()
            date_search = 'Date'
            print("Please enter a date")
            raw_date_input = input("Use the format DD/MM/YYYY:  ")
            try:
                input_user = datetime.datetime.strptime(raw_date_input, "%d/%m/%Y")
                start.search(initial_file, search_file, task_name, task_notes, task_minutes, regex, date_search, date1, date2, input_user, index_track)
                result_menue(search_file, index_track)
                break
            except ValueError:
                clear_screen()
                print("Ups! Seems like '{}' isn't a valid date.".format(raw_date_input))
                print("Press any key to try again or 'R' to return to the main menue.")
                user_input = input(">  ")
                if user_input.upper() == "R":
                    break
                else:
                    continue

        elif input_search == "b":
            # search between two dates
            # IDEE suche zwischen der Unix Timestamp
            date_search = 'Date'
            print("Please enter the first date")
            try:
                raw_date1_input = input("Use the format DD/MM/YYYY:  ")
                date1 = datetime.datetime.strptime(raw_date1_input, "%d/%m/%Y")
            except ValueError:
                print("Ups seems like there is something wrong with your date, please try again!")
                raw_date1_input = input("Use the format DD/MM/YYYY:  ")
                date1 = datetime.datetime.strptime(raw_date1_input, "%d/%m/%Y")
            print("Please enter the second date")
            try:
                raw_date2_input = input("Use the format DD/MM/YYYY:  ")
                date2 = datetime.datetime.strptime(raw_date2_input, "%d/%m/%Y")
            except ValueError:
                print("Ups seems like there is something wrong with your date, please try again!")
                raw_date2_input = input("Use the format DD/MM/YYYY:  ")
                date2 = datetime.datetime.strptime(raw_date2_input, "%d/%m/%Y")
            start.search(initial_file, search_file, task_name, task_notes, task_minutes, regex, date_search, date1, date2, input_user, index_track)
            result_menue(search_file, index_track)

        elif input_search == "c":
            # search for time spent
            task_minutes = 'Time spent'
            print("Please enter how much time the task took in minutes")
            input_user = input("EXAMPLE: Use the format 45 for 45 minutes:  ")
            start.search(initial_file, search_file, task_name, task_notes, task_minutes, regex, date_search, date1, date2, input_user, index_track)
            result_menue(search_file, index_track)
            
        elif input_search == "d":
            # search for string title or notes
            task_name = 'Task name'
            task_notes = 'Notes'
            print("Please enter a word")
            input_user = input("It can be in the Title or Notes:  ")
            start.search(initial_file, search_file, task_name, task_notes, task_minutes, regex, date_search, date1, date2, input_user, index_track)
            result_menue(search_file, index_track)
            
        elif input_search == "e":
            # search for regex pattern
            regex = ['Date', 'Task name', 'Time spent', 'Notes']
            print("Please enter a regex pattern")
            input_user = input(":  ")
            start.search(initial_file, search_file, task_name, task_notes, task_minutes, regex, date_search, date1, date2, input_user, index_track)
            result_menue(search_file, index_track)

        elif input_search == "f":
            break


def result_menue(search_file, index_track):
        clear_screen()
        iteration = 0
        total_page = len(search_file)
        current_page = 1
        initial_file = []
        start.open_file(initial_file)
        while True:
            try:
                menue_file = search_file[iteration]
            except IndexError:
                input("No results found, please press enter to continue")
                break
            for key, value in menue_file.items():
                print(key,": ", value)
            print(" Result {} of {}".format(current_page, total_page))
            print("[N]ext, [E]dit, [D]elete, [R]eturn to search menu")
            user_input = input(">  ")
            if user_input.upper() == "N":
                if current_page < total_page:
                    clear_screen()
                    iteration += 1
                    current_page += 1
                    continue
                else:
                    clear_screen()
                    iteration = 0
                    current_page = 1
                    continue
            if user_input.upper() == "E":
                # Menue to edit entrys
                print("Which entry would you like to edit?")
                print("(1)Date, (2)Task name, (3)Time spent, (4)Notes")
                input_key = int(input(">  "))
                print("Please type in your updated entry and press enter")
                input_user = input(">  ")
                delete_index = index_track[iteration]
                start.edit_entry(initial_file, delete_index, input_key, input_user)
                start.backup_file(initial_file)
                start.update_file(initial_file)
                input("Update sucessful! Press enter to continue")
                break
                
            if user_input.upper() == "D":
                # Menue to delete entrys
                clear_screen()
                print("\nAre you sure you want to delete this entry? Y/N")
                user_input = input(">  ")
                if user_input.upper() == "Y":
                    delete_index = index_track[iteration]
                    start.backup_file(initial_file)
                    start.delete_entry(initial_file, delete_index)
                    start.update_file(initial_file)
                    break
                continue
            if user_input.upper() == "R":
                search_entry()
                break


def main_menue():

    while True:
        clear_screen()
        print("WORK LOG")
        print("What would you like to do?")
        print("a) Add new entry")
        print("b) Search for an existing entry")
        print("c) Quit program")
        input_menue = input("  > ")
        if input_menue.upper() == "A":
            add_entry()
            continue
        elif input_menue.upper() == "B":
            search_entry()
            continue
        elif input_menue.upper() == "C":
            break
        else:
            print("Ups '{}' doesn't seem to be a valid input, choose from a, b, c.".format(input_menue))
            input("Press any key to continue")


main_menue()