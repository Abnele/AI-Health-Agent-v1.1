# Advice Generator
from input import load_data
from statistics import mean

def analyze():
    advice = []

    data = load_data()
    steps = []
    hours_slept = []
    screen_time = []
    money_lost = []
    for daily_entry in data:

        steps.append(daily_entry["steps"])


        hours_slept.append(daily_entry["hours_slept"])


        screen_time.append(daily_entry["screen_time"])


        money_lost.append(daily_entry["money_spent"] - daily_entry["money_earned"])
    stepsAverage = mean(steps).__round__(2)
    sleepAverage = mean(hours_slept).__round__(2)
    screenAverage = mean(screen_time).__round__(2)
    moneyAverage = mean(money_lost).__round__(2)
    print(len(hours_slept))
    print(len(data))

    dataAverage = {
        "steps": stepsAverage,  # per day
        "hours_slept": sleepAverage,  # per day
        "screen_time": screenAverage,  # in daily hours
        "money_lost": moneyAverage,  # in dollars per day
    }

    if dataAverage["steps"] < 5000:
        advice.append("You are too inactive. Consider walking more")
    if dataAverage["hours_slept"] < 8:
        sleepPercent = (dataAverage["hours_slept"]/8)*100
        advice.append(f"You are getting {sleepPercent}% less sleep per day than recommended. Try to get 8 hours of sleep daily")
    if dataAverage["screen_time"] > 5:
        advice.append(f"Reduce your screen time. You are wasting {dataAverage["screen_time"]} hours per day on average")
    if dataAverage["money_lost"] > 0:
        advice.append(f"You are losing ${dataAverage["money_lost"]} per day. Regulate your spending.")

    return advice