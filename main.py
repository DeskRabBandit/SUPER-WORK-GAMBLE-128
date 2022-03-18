from scripts.classes import Task, User
from scripts.functions import time_to_unix, unix_to_time, next_level_xp
from os import system
from time import sleep
from tabulate import tabulate

TASKS_FILEPATH = "savedata/tasks.csv"
USER_DATA_FILEPATH = "savedata/userdata.csv"

current_user = None

def create_user():
    global current_user
    
    while True:
        username = input("Please enter a username: ")
        if len(username) < 3:
            print("Your username must be at least 3 characters long")
            continue
        elif "," in username:
            print("Your username cannot contain commas")
            continue

        break

    current_user = User(username)
    save_user()
    
def save_user():
    global current_user

    file = open(USER_DATA_FILEPATH, "w")
    file.write(current_user.get_all())
    file.close()
    
    print("User data has been saved")

def load_user():
    global current_user
    
    try:
        user_file = open(USER_DATA_FILEPATH, "r")
        user_data = user_file.readline().split(",")
        user_file.close()

        current_user = User(user_data[0], user_data[1], user_data[2])

        print("User data loaded")

    except FileNotFoundError:
        print("No user data found. Please create a new user.")
        create_user()        
        
        

# returns data from tasks.csv as list of Task objects
def open_tasks_file():
    output = []
    
    try:
        
        tasks_file = open(TASKS_FILEPATH, "r")
        for line in tasks_file:
            line = line.strip().split(",")
            output.append(Task(line[0], float(line[1]), float(line[2]), line[3]))
        tasks_file.close()
        return output
    # create file if it doesnt exist
    except FileNotFoundError:
        open(TASKS_FILEPATH, "w").close()
        return []

# saves given list of Tasks to csv
def save_tasks_file(tasks):
    tasks_file = open(TASKS_FILEPATH, "w")
    for task in tasks:
        tasks_file.write(f"{task.get_name()},{task.get_start_time()},{task.get_duration()},{task.get_point_value()}\n")
    tasks_file.close()
    
# allows user inputs and adds a task to the tasks list
def add_task():
    name = input("Enter the task: ")
    start_date = input("Enter the start date in DD/MM/YYYY format: ")
    start_time = input("Enter the start time in HH:MM format: ")
    duration = input("Enter the duration in HH:MM format: ")
    
    unix_start_time = time_to_unix(start_time, start_date)
    unix_duration = time_to_unix(given_time = duration)
    
    tasks.append(Task(name, unix_start_time, unix_duration))
    
# allows user inputs to complete task and acquire points
def complete_task():
    name = input("Type the name of the task you have completed: ")

    for each_task in tasks:
        if each_task.get_name() == name:
            i = tasks.index(each_task)
            break

    current_user.increase_points(tasks.pop(i).get_point_value())
    
# allows user inpu.ts and removes task from tasks list
def remove_task():
    name = input("Type the name of the task you wish to remove: ")

    for each_task in tasks:
        if each_task.get_name() == name:
            tasks.remove(each_task)
            break
    
# allows user inputs and edits one specified property of one task in the tasks 
def edit_task():
    name = input("Type the name of the task you wish to edit: ")

    for each_task in tasks:
        if each_task.get_name() == name:
            print(
                """Type \033[32m1\033[0m to edit the task name
Type \033[32m2\033[0m to edit the start time
Type \033[32m3\033[0m to edit the end time
Type \033[32m4\033[0m to edit the duration"""
            )

            choice = input(">>> ")

            def edit_name():
                each_task.set_name(input("Enter the new task name: "))
            def edit_start_time():
                start_date = input("Enter the start date in DD/MM/YYYY format: ")
                start_time = input("Enter the start time in HH:MM format: ")
                unix_start_time = time_to_unix(start_time, start_date)
                each_task.set_start_time(unix_start_time)
            def edit_end_time():
                end_date = input("Enter the end date in DD/MM/YYYY format: ")
                end_time = input("Enter the end time in HH:MM format: ")
                unix_end_time = time_to_unix(end_time, end_date)
                each_task.set_end_time(unix_end_time)
            def edit_duration():
                duration = input("Enter the duration in HH:MM format: ")
                unix_duration = time_to_unix(given_time = duration)
                each_task.set_duration(unix_duration)
                

            options = {
                "1" : edit_name,
                "2" : edit_start_time,
                "3" : edit_end_time,
                "4" : edit_duration
            }

            choice = input("\033[34m>>>\033[0m ")

            try:
                choices[choice]()
            except KeyError:
                print("\033[31mEnter a valid option\033[0m")
                sleep(1)
    
# saves tasks to tasks.csv and quits the program
def save_and_quit(tasks):
    save_tasks_file(tasks)
    save_user()
    quit()

# open saved tasks

load_user()    
tasks = open_tasks_file()

system('clear')

app_running = True
while app_running:
    print(f"{current_user.get_username()} | Level {current_user.get_level()} | XP: {current_user.get_points()}/{next_level_xp(current_user.get_level())}")
    
    print("TASK LIST")
    if len(tasks) <= 0:
        print("-" * 56)
        print("You have no tasks added")
        print("-" * 56)
    else:
        print(tabulate([[task.get_name() , f"From {unix_to_time(task.get_start_time())}",f" To {unix_to_time(task.get_end_time())}"] for task in tasks]))


    print(
"""
Type \033[32m1\033[0m to add a task
Type \033[32m2\033[0m to complete a task
Type \033[32m3\033[0m to remove a task
Type \033[32m4\033[0m to edit a task
Type \033[32mX\033[0m to save & quit"""
    )

    # case switch (sort of)
    choices = {
        "1" : add_task,
        "2" : complete_task,
        "3" : remove_task,
        "4" : edit_task,
        "X" : lambda: save_and_quit(tasks)
    }
    
    choice = input("\033[34m>>>\033[0m ").upper()

    try:
        choices[choice]()
    except KeyError:
        print("\033[31mEnter a valid option\033[0m")
        sleep(1)

    save_tasks_file(tasks)
    save_user()
    
    system('clear')






# basic test code

# name = "Punch Matthew"
# start_date = "03/11/2022"
# start_time = "16:20"
# duration = "00:10"

# unix_start_time = time_to_unix(start_time, start_date)
# unix_duration = time_to_unix(given_time = duration)

# tasks.append(Task(name, unix_start_time, unix_duration))


# task.get_name(),
# unix_to_time(task.get_start_time()),
# unix_to_time(task.get_duration(), duration = True),
# unix_to_time(task.get_end_time())