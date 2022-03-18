import time
from datetime import datetime

BASE_LVL_XP = 900
LVL_XP = 100

# determines point value of task
def determine_value(duration):
    return duration // 2

# returns given time in unix, takes time and date as separate arguments
# takes time in HH:MM format, date in DD/MM/YYYY
def time_to_unix(given_time="00:00", date="01/01/1970"):
    dt = datetime.strptime(date+given_time, "%d/%m/%Y%H:%M")
    return int(time.mktime(dt.timetuple()))

# returns given unix time in dd/mm/yy hh/mm format (or hh/mm format if duration var is True)
def unix_to_time(unix_time, duration = False):
    return datetime.utcfromtimestamp(unix_time).strftime("%d/%m/%Y %H:%M" if not duration else "%H:%M")

def next_level_xp(level):
    return BASE_LVL_XP + (level * LVL_XP)