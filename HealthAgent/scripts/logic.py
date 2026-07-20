# Advice Generator
from input import load_data
from statistics import mean
from datetime import datetime, timedelta
import json
import os
import traceback
import google.genai as genai


# Directories
MEMORY_DIR = os.path.join(os.path.dirname(__file__), '..', 'memory')
DATA_FILE = os.path.join(MEMORY_DIR, 'data.json')
GOALS_FILE = os.path.join(MEMORY_DIR, "goals.json")
SETTINGS_FILE = os.path.join(MEMORY_DIR, "settings.json")
                             
# Configure AI
#try:
with open(SETTINGS_FILE, "r") as f:
    key = json.load(f)
client = genai.Client(api_key = key["gemini_api_key"])



                

def analyze():
    advice = []
    weekly_data = []
    report_type = ""
    goals = []

    # Fetch goals
    with open(GOALS_FILE, "r") as file:
        goals = json.load(file) # get the data in the json file
    

    # Fetch data
    data = load_data() # Gets data in json file currently
    
    today = datetime.now().date()
    seven_days_ago = today - timedelta(days= 7)

    weekly_data = []
    for entry in data:
        entry_date = datetime.strptime(entry["date"], "%Y-%m-%d").date()
        if seven_days_ago<= entry_date <= today:
            weekly_data.append(entry)

    if len(weekly_data) > 1:
        report_type = "WEEKLY"
    else:
        data = weekly_data # Only evaluates one day of the week that was logged
        weekly_data =  [] # Clears weekly list
        report_type = "DAILY" 





    # Individual data categories
    steps = []
    hours_slept = []
    screen_time = []
    money_lost = []

    # Get weekly report
    if (report_type == "WEEKLY"):
        for daily_entry in weekly_data:
            steps.append(daily_entry["steps"]) # Add all steps data to steps list
            hours_slept.append(daily_entry["hours_slept"]) # Add all sleep data to sleep list
            screen_time.append(daily_entry["screen_time"]) # Add all screen time data to screen time list

    # Get daily report
    else:
        for daily_entry in data:
            steps.append(daily_entry["steps"])  # Add all steps data to steps list
            hours_slept.append(daily_entry["hours_slept"])  # Add all sleep data to sleep list
            screen_time.append(daily_entry["screen_time"])  # Add all screen time data to screen time list

    stepsAverage = mean(steps).__round__(2) # Get the steps average
    sleepAverage = mean(hours_slept).__round__(2) # Get the sleep average
    screenAverage = mean(screen_time).__round__(2) # Get the screen time average

    # Add averages to a library
    dataAverage = {
        "steps": stepsAverage,  # per day
        "hours_slept": sleepAverage,  # per day
        "screen_time": screenAverage,  # in daily hours
    }

    # Give advice based on the weekly or daily data
    ai_advice = get_ai_advice((weekly_data if report_type == "WEEKLY" else data), goals, report_type)
    print(f"""
        *********AI ADVICE BELOW:
        {ai_advice}
        """)
    advice = []
    
    for item in ai_advice.strip().split("\n"):
        advice.append(item)
    


    # DEPRECATED AND SOON TO BE REMOVED
    # if (report_type == "WEEKLY"):
    #     return make_weekly_advice(weekly_data, dataAverage, goals, advice), report_type
    # else:
    #     if dataAverage["steps"] < goals["steps"]:
    #         advice.append("You are too inactive. Consider getting at least 5000 steps per day.")
    #     if dataAverage["hours_slept"] < goals["hours_slept"]:
    #         sleepPercent = (dataAverage["hours_slept"] / goals["hours_slept"]) * 100
    #         if (sleepPercent.is_integer()):
    #             sleepPercent = int(sleepPercent)
    #         advice.append(f"You are getting {100 - sleepPercent}% less sleep per day than recommended. Try to get {goals["hours_slept"]} hours of sleep daily")
    #     if dataAverage["screen_time"] > goals["screen_time"]:
    #         if (dataAverage["screen_time"].is_integer()):
    #             dataAverage["screen_time"] = int(dataAverage["screen_time"])
    #         advice.append(f"Reduce your screen time. You are wasting {dataAverage["screen_time"]} hours per day on average")
    #     if advice.__len__() == 0:
    #         advice.append("You've been keeping up with your goals. Keep it up.")

    return advice, report_type
    

def make_weekly_advice(weekly_data, dataAverage, goals, advice):
        past_x_days = 0
        previous_day = None
        
        sorted_data = sorted(weekly_data, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse = True)
        print("SORTED DATA: ")
        for day in sorted_data:
            print(day)

    # STEPS GOAL
        # Get the days in a row you've missed your goal starting from the last time you logged a day
        for day in sorted_data:
            if (day["steps"] < goals["steps"]) and \
                (previous_day == None or datetime.strptime(day["date"], "%Y-%m-%d") == previous_day - timedelta(days = 1)):
                
                past_x_days += 1
                previous_day = datetime.strptime(day["date"], "%Y-%m-%d")            
            else:
                break
        


        # If done more than twice, call the user out
        if (past_x_days > 2):
            advice.append(f"You have been under your steps goal for the past {past_x_days} days. Get more steps in")
        # See if they've underperformed on average, and call that out
        if (dataAverage["steps"] < goals["steps"]):
            stepsPercent = (dataAverage["steps"] / goals["steps"]) * 100
            stepsPercent = stepsPercent.__round__(2)

            if stepsPercent.is_integer(): # Turn percentage into integer when possible
                stepsPercent = int(stepsPercent)
            advice.append(f"You've only been taking %{stepsPercent} of your goal steps this week. Increase your step count.")

        # If they've been on track, don't add advice
        else:
            pass

    # SLEEP GOAL
        past_x_days = 0
        # Get the days in a row you've missed your goal starting from the last time the program is run
        previous_day = None
        # Get the days in a row you've missed your goal starting from the last time you logged a day
        for day in sorted_data:
            if (day["hours_slept"] < goals["hours_slept"]) and \
                (previous_day == None or datetime.strptime(day["date"], "%Y-%m-%d") == previous_day - timedelta(days = 1)):
                past_x_days += 1
                previous_day = datetime.strptime(day["date"], "%Y-%m-%d")
            else:
                break

        # If done more than twice, call the user out
        if (past_x_days > 2):
            advice.append(f"You have been under your sleep goal for the past {past_x_days} days. Tighten your sleep schedule")

        # See if they've underperformed on average, and call that out
        if (dataAverage["hours_slept"] < goals["hours_slept"]):
            sleepPercent = (dataAverage["hours_slept"] / goals["hours_slept"]) * 100
            sleepPercent = sleepPercent.__round__(2)

            if sleepPercent.is_integer():  # Turn percentage into integer when possible
                sleepPercent = int(sleepPercent)

            advice.append(f"You are getting {sleepPercent}% less sleep per day than recommended. Try to get 8 hours of sleep daily")

        # If they've been on track, don't add advice
        else:
            pass

    # SCREEN TIME GOAL
        past_x_days = 0
        # Get the days in a row you've missed your goal starting from the last time the program is run
        previous_day = None
        # Get the days in a row you've missed your goal starting from the last time you logged a day
        for day in sorted_data:
            if (day["screen_time"] < goals["screen_time"]) and \
                (previous_day == None or datetime.strptime(day["date"], "%Y-%m-%d") == previous_day - timedelta(days = 1)):
                
                past_x_days += 1
                previous_day = datetime.strptime(day["date"], "%Y-%m-%d")
            else:
                break

        # If done more than twice, call the user out
        if (past_x_days > 2):
            advice.append(f"You have been over your screen time minimum for the past {past_x_days} days. Reduce your phone usage")

        # See if they've underperformed on average, and call that out
        if (dataAverage["screen_time"] > goals["screen_time"]):
            screenPercent = (dataAverage["screen_time"] / goals["screen_time"]) * 100
            screenPercent = screenPercent.__round__(2)

            if screenPercent.is_integer():  # Turn percentage into integer when possible
                screenPercent = int(screenPercent)

            advice.append(f"Reduce your screen time. You are wasting {dataAverage["screen_time"]} hours per day on average, and getting %{screenPercent} more screen time per day than what your goal states")

        # If they've been on track, don't add advice
        else:
            pass
        # If they've been on track with ALL goals, point that out in the report
        if advice.__len__() == 0:
            advice.append("You've been keeping up with your goals. Keep it up.")

        return advice

def get_ai_advice(data, goals, report_type):
    # Prompts Gemini to give advice to the user
    prompt = f"""
        You are a personal health coach. Analyze this user's health data and give specific, actionable advice in 3-5 bullet points. Be encouraging but honest   
        Report type: {report_type}
        User Goals: {goals}
        Health Data: {data}
        Keep advice concise and practical. Focus on what they can improve today.
    """

    response = client.models.generate_content(
        model = "gemini-3.1-flash-lite",
        contents = prompt)
    
    print(f"RESPONSE: {response.text}")
    return response.text