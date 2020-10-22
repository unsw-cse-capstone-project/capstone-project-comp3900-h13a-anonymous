import pandas as pd

timestamp = 1602469828795
date_time = pd.to_datetime(timestamp, unit='ms')
print("Date time object:", date_time)