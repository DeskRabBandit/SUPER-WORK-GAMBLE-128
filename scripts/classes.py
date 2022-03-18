from scripts.functions import determine_value, time_to_unix, next_level_xp

# task object
class Task(object):
    def __init__(self, name, start_time, duration, point_value = None):
        self.__name = name
        self.__start_time = start_time
        self.__duration = duration
        self.__end_time = self.__start_time + self.__duration
        self.__point_value = determine_value(duration) if point_value == None else int(point_value)

    # getters
    
    def get_name(self):
        return self.__name

    def get_start_time(self):
        return self.__start_time

    def get_end_time(self):
        return self.__end_time

    def get_duration(self):
        return self.__duration 

    def get_point_value(self):
        return self.__point_value

    # setters

    def set_name(self, name):
        self.__name = name

    def set_start_time(self, start_time):
        self.__start_time = start_time
        self.__duration = self.__end_time - start_time

    def set_end_time(self, end_time):
        self.__end_time = end_time
        self.__duration = end_time - self.__start_time

    def set_duration(self, duration):
        self.__duration = duration
        self.__end_time = self.__start_time + duration

    def set_point_value(self, point_value):
        self.__point_value = point_value
        
# user object
class User(object):
    def __init__(self, username, level=1, points=0):
        self.__username = username
        self.__level = int(level)
        self.__points = int(points)

    # getters

    def get_username(self):
        return self.__username

    def get_level(self):
        return self.__level

    def get_points(self):
        return self.__points

    def get_all(self):
        return f"{self.__username},{self.__level},{self.__points}"

    # setters

    def set_username(self, username):
        self.__username = username

    def set_level(self, level):
        self.__level = level

    def set_points(self, points):
        self.__points = points

    # other

    def level_up(self, amount=1):
        self.__level += amount
        self.increase_points(0)

    def increase_points(self, amount):
        self.__points += amount
        req_xp = next_level_xp(self.__level)
        if self.__points >= req_xp:
            self.__points -= req_xp
            self.level_up()