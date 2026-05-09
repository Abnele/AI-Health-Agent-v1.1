# Advice Generator
from input import load_data
from statistics import mean
import json

def analyze():
    advice = []
    weekly_data = []
    report_type = ""
    goals = []

    # Fetch goals
    try:
        with open("goals.json", "r") as file:
            goals = json.load(file) # get the data in the json file
    except:
        print("Please provide your habit goals")
        print("Enter numbers only")
        goals = {
          "steps" : float(input("Steps per day: " )),
          "hours_slept" : float(input("Hours slept per day: " )),
          "screen_time" : float(input("Screen time per day (in hours): " )),
        }
        with open("goals.JSON", "w") as file:
            json.dump(goals, file)

    # Fetch data
    data = load_data() # Gets data in json file currently
    if (len(data)) > 7:
        weekly_data = data[-7:] # Gets 7-day data
        report_type = "WEEKLY"
    elif (len(data) < 7 and len(data) > 1):
        weekly_data = data # Gets <7 day data
        report_type = "WEEKLY"
    else:
        weekly_data = []
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

    # Give advice based on the data
    if (report_type == "WEEKLY"):
        return make_weekly_advice(weekly_data, dataAverage, goals, advice), report_type
    else:
        if dataAverage["steps"] < goals["steps"]:
            advice.append("You are too inactive. Consider getting at least 5000 steps per day.")
        if dataAverage["hours_slept"] < goals["hours_slept"]:
            sleepPercent = (dataAverage["hours_slept"] / 8) * 100
            if (sleepPercent.is_integer()):
                sleepPercent = int(sleepPercent)
            advice.append(f"You are getting {sleepPercent}% less sleep per day than recommended. Try to get 8 hours of sleep daily")
        if dataAverage["screen_time"] > goals["screen_time"]:
            if (dataAverage["screen_time"].is_integer()):
                dataAverage["screen_time"] = int(dataAverage["screen_time"])
            advice.append(f"Reduce your screen time. You are wasting {dataAverage["screen_time"]} hours per day on average")
        if advice.__len__() == 0:
            advice.append("You've been keeping up with your goals. Keep it up.")

        return advice, report_type

def make_weekly_advice(weekly_data, dataAverage, goals, advice):
        past_x_days = 0
        try:

            # STEPS GOAL
                # Get the days in a row you've missed your goal starting from the last time the program is run
                for day in reversed(weekly_data):
                    if (day["steps"] < goals["steps"]):
                        past_x_days += 1
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
                    advice.append(f"You've been taking %{stepsPercent} less steps than your goal this week. Increase your step count.")

                # If they've been on track, don't add advice
                else:
                    pass

            # SLEEP GOAL
                past_x_days = 0
                # Get the days in a row you've missed your goal starting from the last time the program is run
                for day in reversed(weekly_data):
                    if (day["steps"] < goals["steps"]):
                        past_x_days += 1
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
                for day in reversed(weekly_data):
                    if (day["screen_time"] > goals["screen_time"]):
                        past_x_days += 1
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
        except:
            return "ADVICE CANNOT BE GENERATED"



