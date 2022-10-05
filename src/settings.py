import json, os

if "settings.json" in os.listdir():
    print("Success!")

d = {"1": 1, "2" : 2}

with open("settings.json", "w") as file:
    json.dump(d, file)

def loop():
    pass