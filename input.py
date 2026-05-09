# Data Collection
from tkinter import simpledialog
from tkinter import messagebox
import json
from random import *

data = {}

def get_user_data(dummy_data):
    # Fetch goals
    try:    # Test if there is anything in the goals file
        with open("goals.json", "r") as file:
            goals = json.load(file)
        for goal, value in dict(goals).items():
            print(f"{goal}, {value}")
            if value == None or len(goals) == 0:
                raise Exception

    except: # Ask the user for goals if there isn't any
        goals = {}
        invalid_goals = None
        messagebox.showinfo("Goals", "Please provide your habit goals\nEnter numbers only")
        goals = {
            "steps": simpledialog.askinteger("Input", "Steps per day:"),
            "hours_slept": simpledialog.askinteger("Input", "Hours slept per day: "),
            "screen_time": simpledialog.askinteger("Input", "Screen time per day (in hours): ")
        }


        for key, value in goals.items():
            print(key, value)
            if (value == None):
                invalid_goals = True
        while (invalid_goals):
            messagebox.showinfo("Goals", "Please provide your habit goals\nEnter numbers only")
            goals = {
                "steps": simpledialog.askinteger("Input", "Steps per day:"),
                "hours_slept": simpledialog.askinteger("Input", "Hours slept per day: "),
                "screen_time": simpledialog.askinteger("Input", "Screen time per day (in hours): ")
            }
            invalid_count = 0
            for key, value in goals.items():
                print(key, value)
                if (value == None):
                    invalid_count+=1
                    invalid_goals = True
                if (invalid_count == 0 and key == "screen_time" and value != None):
                    invalid_goals = False
                    break
        invalid_goals = None

        with open("goals.JSON", "w") as file:
            json.dump(goals, file)

    if (not dummy_data):
        # Get data
        invalid_data = None
        messagebox.showinfo("Data","Input Today's Data")
        data = {
            "steps" : simpledialog.askfloat("Steps", "steps: "), # per day
            "hours_slept" : simpledialog.askfloat("Sleep", "Hours Slept: ") , # per day
            "screen_time" : simpledialog.askfloat("Phone Usage","Screen Time: ")   # in daily hours
        }

        for key, value in data.items():
            print(key, value)
            if (value == None):
                invalid_data = True
        while (invalid_data):
            messagebox.showinfo("Data", "Please provide today's data\nEnter numbers only")
            data = {
                "steps": simpledialog.askfloat("Steps", "steps: "),  # per day
                "hours_slept": simpledialog.askfloat("Sleep", "Hours Slept: "),  # per day
                "screen_time": simpledialog.askfloat("Phone Usage", "Screen Time: ")  # in daily hours
            }
            invalid_count = 0
            for key, value in data.items():
                print(key, value)
                if (value == None):
                    invalid_count+=1
                    invalid_data = True
                if (invalid_count == 0 and key == "screen_time" and value != None):
                    invalid_data = False
                    break


        return data
    else:
        data = {
            "steps": randint(1000, 7000),  # per day
            "hours_slept": randint(4, 9),  # per day
            "screen_time": randint(1, 9),  # in daily hours
            "money_spent": randint(15, 80),  # in dollars per day
            "money_earned": randint(15, 80)  # in dollars per day
        }
        return data

def save_data(daily_entry): # Saves data to Json file
    jsonData = []
    try:
        with open("data.JSON", "r") as file:
            jsonData = json.load(file) # Store the current data in a variable
    except:
        jsonData = []

    jsonData.append(daily_entry) # Add the given daily entry

    with open("data.JSON", "w") as file:
        json.dump(jsonData, file, indent= 4) # Replace old data list with new data list

def load_data(): # loads data from json
    try:
        with open("data.JSON", "r") as file:
            return json.load(file) # get the data in the json file
    except:
        return []






