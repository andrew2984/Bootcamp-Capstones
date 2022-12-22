#=====importing libraries===========
'''This is the section where you will import libraries'''
from datetime import date

#====Login Section====
'''Here you will write code that will allow a user to login.
    - Your code must read usernames and password from the user.txt file
    - You can use a list or dictionary to store a list of usernames and passwords from the file.
    - Use a while loop to validate your user name and password.
'''

# import list of usernames and passwords
with open('user.txt', 'r') as f:
    usernames = []
    passwords = []
    for line in f:
        line_split = line.split(", ")
        usernames.append(line_split[0].strip())  # strips \n
        passwords.append(line_split[1].strip())

#login screen
while True:
    login_username = input("Enter your username")
    if login_username not in usernames:
        print("Invalid username")
    else:
        login_password = input("Enter your password")
        # checks if password is in user.txt and if it is next to the inputted username
        if login_password not in passwords or passwords.index(login_password) != usernames.index(login_username):
            print("Invalid password")
        else:
            break

# display menu
while True:
    # menu for admin
    if login_username == "admin":
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
s - Display statistics
e - Exit
: ''').lower()

    # menu if not admin
    else:
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
e - Exit
: ''').lower()
        

    # register a user
    if menu == 'r':
        if login_username != "admin":
            print("You are not permitted to register users.")
        else:
            # appends new username and password to user.txt
            new_username = input("Enter a new username")
            new_password = input("Enter a new password")
            check_password = input("Enter password again to confirm")
            if check_password == new_password:
                with open('user.txt', 'a') as f:
                    f.write("\n" + new_username + ", " + new_password)
            else:
                print("The passwords you entered are not identical")

    # add task
    elif menu == 'a':
        # checks if username is valid and assigns
        while True:
            assign_username = input("Enter username")
            if assign_username in usernames:
                break
            else:
                print("Invalid username")

        assign_task = input("Enter title of task")
        assign_descrip = input("Enter description of task")
        assign_date = input("Enter the due date")
        curr_date = date.today()  # gets current date
        today = curr_date.strftime("%d %b %Y") # formats date

        # user inputs whether task is complete
        while True:
            assign_complete = input("Is the task complete?").lower()
            if assign_complete == "yes":
                complete = ", Yes"
                break
            elif assign_complete == "no":
                complete = ", No"
                break
            else:
                print("Invalid answer")

        # writes variables into tasks.txt
        with open('tasks.txt', 'a') as f:
            f.write(f"\n{assign_username}, {assign_task}, {assign_descrip}, {today}, {assign_date}{complete}")

    # view all tasks
    elif menu == 'va':
        # prints tasks to console
        with open('tasks.txt', 'r') as f:
            for line in f:
                tasks_split = line.split(", ")  # splits lines into sections
                print(u'\u2500' * 70)  # prints continuous line (https://stackoverflow.com/questions/65561243/print-a-horizontal-line-in-python)
                print(f'''
Task:              {tasks_split[1]}
Assigned to:       {tasks_split[0]}
Date assigned:     {tasks_split[3]}
Due date:          {tasks_split[4]}
Task Complete?     {tasks_split[5]}
Task desciption:
    {tasks_split[2]}
                ''')
            print(u'\u2500' * 70)

    # view own tasks
    elif menu == 'vm':
        with open('tasks.txt', 'r') as f:
            tasks_amount = 0 # counts number of tasks assigned to user
            for line in f:
                tasks_split = line.split(", ")  # splits lines into sections
                if login_username == tasks_split[0]:  # if current username is referenced in line
                    tasks_amount += 1
                    print(u'\u2500' * 70)
                    print(f'''
Task:              {tasks_split[1]}
Assigned to:       {tasks_split[0]}
Date assigned:     {tasks_split[3]}
Due date:          {tasks_split[4]}
Task Complete?     {tasks_split[5]}
Task desciption:
    {tasks_split[2]}
                    ''')
            # if no tasks assigned, prints so
            if tasks_amount == 0:
                print(u'\u2500' * 70)
                print("You have no tasks.")
            print(u'\u2500' * 70)

# display number of tasks and users
    elif menu == 's':
        if login_username == "admin":
            tasks_amount = 0
            users_amount = 0
            print(u'\u2500' * 70)
            with open('tasks.txt', 'r') as f:  # each line is a different task
                for line in f:
                    tasks_amount += 1
                print(f"Tasks:      {tasks_amount}")
            with open('user.txt', 'r') as f:  # each line is a different user
                for line in f:
                    users_amount += 1
                print(f"Users:      {users_amount}")
            print(u'\u2500' * 70)
        else:
            print("You have made a wrong choice, Please Try again")

    # exit
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")