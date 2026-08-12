# Data Collection
from collections import defaultdict
from tkinter import simpledialog
from tkinter import messagebox
import json
from random import *
import os

data = {}
MEMORY_DIR = os.path.join(os.path.dirname(__file__), '..', 'memory')
DATA_FILE = os.path.join(MEMORY_DIR, 'data.json')
GOALS_FILE = os.path.join(MEMORY_DIR, "goals.json")

def convert_export_to_daily(export_data):
    daily_metrics = []
    metrics = export_data.get("data", {}).get("metrics", [])
    global steps_data
    global sleep_data
    global day
    global day_amount
    global previous_day
    steps_data = 0
    sleep_data = 0
    day = False
    day_amount = 0
    previous_day = False

    # Gets the amount of days exported
    for metric in metrics:
        if metric.get("name") == "step_count":
            for point in metric.get("data"):
                if not day: 
                    day = point["date"].split(" ")[0]
                    day_amount = 1
                elif day != point["date"].split(" ")[0]:
                    day = point["date"].split(" ")[0]
                    day_amount += 1
                else:
                    pass
    
    # Gets the metrics for each day
    for i in range(day_amount):
        for metric in metrics:
            if metric.get("name") == "step_count":
                for point in metric.get("data"):
                    if not day: 
                        day = point["date"].split(" ")[0]
                        steps_data += point['qty']
                    elif day == previous_day:
                        # If the previous day is the current day
                        if day == point["date"].split(" ")[0]:
                            # Go on to the next
                            pass
                        # If not
                        else:
                            day = point["date"].split(" ")[0]
                            steps_data += point['qty']

                    elif day != point["date"].split(" ")[0]:
                        pass
                    else:
                        steps_data += point['qty']
            
            if metric.get("name") == "sleep_analysis":
                for point in metric.get("data"):
                    if not day: 
                        day = point["date"].split(" ")[0]
                        sleep_data = point['inBed']
                    elif day != point["date"].split(" ")[0]:
                        pass
                    else:
                        sleep_data = point['inBed']
        daily_metrics.append(
                {
                    "date": day,
                    "steps": int(steps_data),
                    "hours_slept": sleep_data,
                    "screen_time": 0
                }
            )
        previous_day = day
        day = False
        steps_data = 0
        sleep_data = 0

        
    
    
    for item in daily_metrics:
        print(f"item: {item}")
    
    results = []
    for item in daily_metrics:
        results.append(item)

    
    return results


def save_data(daily_entry): # Saves data to Json file
    jsonData = []
    try:
        with open(DATA_FILE, "r") as file:
            jsonData = json.load(file) # Store the current data in a variable
    except:
        jsonData = []
    
    # Override any duplicate dates
    new_data = []
    for entry in jsonData:
        if entry.get("date") != daily_entry.get("date"):
            new_data.append(entry)
    jsonData = new_data
    
    jsonData.append(daily_entry) # Add the given daily entry

    with open(DATA_FILE, "w") as file:
        json.dump(jsonData, file, indent= 4) # Replace old data list with new data list

def load_data(): # loads data from json
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file) # get the data in the json file
    except:
        return []
    


# DEPRECATED METHODS
def get_user_data(dummy_data):
    # Fetch goals
    try:    # Test if there is anything in the goals file
        with open(GOALS_FILE, "r") as file:
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

        with open(GOALS_FILE, "w") as file:
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



