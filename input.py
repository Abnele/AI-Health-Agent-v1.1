# Data Collection
import json

data = {}

def get_user_data(): # Dummy data
    data = {
        "steps" : 6767, # per day
        "hours_slept" : 5, # per day
        "screen_time" : 7, # in daily hours
        "money_spent" : 67, # in dollars per day
        "money_earned": 6.7 # in dollars per day
    }
    return data

def save_data(daily_entry): # Saves data to Json file
    jsonData = []
    try:
        with open("data.JSON", "r") as file:
            jsonData = json.load(file)
    except:
        jsonData = []

    jsonData.append(daily_entry)

    with open("data.JSON", "w") as file:
        json.dump(jsonData, file, indent= 4)



def load_data(): # loads data from json
    try:
        with open("data.JSON", "r") as file:
            return json.load(file)
    except:
        return []

