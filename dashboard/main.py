
import numpy as np
import pandas as pd 
from taipy.gui import Gui
from datetime import datetime


page = """
# HawkEye

<|layout|columns=1fr 1fr|

## Your Eyeblinks
## Time Between Eyeblinks
<|{eye_blink_data}|chart|mode=markers|x=Time|y[1]=Eye Blink|>

<|{blink_difference_data}|type=bar|chart|x=Keys|y=Values|>

|>

<|layout|columns=1fr 1fr|
## Standard Deviation Between Eyeblinks
<|{std}|>
|>
"""
raw_timestamps = []
formatted_timestamps = [ ] # Time range of blinks
time_diff_counts = {}  # Dictionary to hold time differences and their counts
eye_blink = []


def process_csv():
    data = pd.read_csv('./blink.csv', header=None, names=['eye', 'blinked', 'timestamp'])
    for index, row in data.iterrows():
        print(row)
        blinked = row["blinked"] # this is either True or False - blink or not
        eye = row["eye"] # this is either left or right
        timestamp = row["timestamp"] # unix timestamp, convert to time 

        if blinked == "True":
            if eye == "left":
                eye_blink.append("Left Blink")
            else:
                eye_blink.append("Right Blink")
            
            raw_timestamps.append(timestamp)
            dt = datetime.fromtimestamp(float(timestamp))
            formatted_timestamps.append(dt.strftime('%H:%M:%S'))

# Calculate time between blinks
def time_between_blinks():
    for i in range(len(raw_timestamps) - 1):
        end_time = float(raw_timestamps[i + 1])
        initial_time = float(raw_timestamps[i])
        print(end_time, initial_time)
        time_between =  round(end_time - initial_time, 2)
        if time_between in time_diff_counts:
            time_diff_counts[time_between] += 1
        else:
            time_diff_counts[time_between] = 1


process_csv()
time_between_blinks()
std = np.std(list(time_diff_counts.keys()))
print(std)

eye_blink_data = pd.DataFrame({
  "Time" : formatted_timestamps,
  "Eye Blink" : eye_blink,
})
blink_difference_data = pd.DataFrame(list(time_diff_counts.items()), columns=['Keys', 'Values'])



pages = {"/":"<|toggle|theme|>\n<center>\n<|navbar|>\n</center>",
         "View":page,}

Gui(pages=pages).run(use_reloader=True)