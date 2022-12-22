from datetime import date
import copy


def edit_tasks(index, user_edit):
    with open('tasks.txt', 'r') as f:
        filedata = f.read()
        target_line = ", ".join(my_tasks_list[task_select-1])  # task_select-1 is the index of task in my_tasks_list
        print(target_line)
        my_tasks_list_copy = copy.deepcopy(my_tasks_list)  # copying my_task_list
        print(my_tasks_list_copy)
        my_tasks_list_copy[task_select-1][index] = user_edit  # change completion of copy to yes
        replacement_line = ", ".join(my_tasks_list_copy[task_select-1])
        print(replacement_line)
        filedata = filedata.replace(target_line, replacement_line)  # replace the target string
        with open('tasks.txt', 'w') as f:
            f.write(filedata)  # write the file out again
        # updates lists
        import_users()
        import_tasks()


def convert_month(unknown_date):
    # sets month to corresponding integer
    if unknown_date[1] == "Jan":
        unknown_date[1] = 1
    elif unknown_date[1] == "Feb":
        unknown_date[1] = 2
    elif unknown_date[1] == "Mar":
        unknown_date[1] = 3
    elif unknown_date[1] == "Apr":
        unknown_date[1] = 4
    elif unknown_date[1] == "May":
        unknown_date[1] = 5
    elif unknown_date[1] == "Jun":
        unknown_date[1] = 6
    elif unknown_date[1] == "Jul":
        unknown_date[1] = 7
    elif unknown_date[1] == "Aug":
        unknown_date[1] = 8
    elif unknown_date[1] == "Sep":
        unknown_date[1] = 9
    elif unknown_date[1] == "Oct":
        unknown_date[1] = 10
    elif unknown_date[1] == "Nov":
        unknown_date[1] = 11
    else:
        unknown_date[1] = 12


def determine_overdue(curr_date, due_date):
    for i in range(0, 3):  # cast to int
        due_date[i] = int(due_date[i])
        curr_date[i] = int(curr_date[i])
    # calculate 'days' until due date (not actually calculating days)
    # the value of multipliers don't matter much as long as
    # multiplier for month >= 31 * mult. for day and
    # multiplier for year >= 12 * mult. for month
    # this makes it so I don't have to make if-else statements
    days_till = (due_date[2]-curr_date[2])*1000 + (due_date[1]-curr_date[1])*50 + (due_date[0]-curr_date[0])

    if days_till < 0:  # negative means overdue
        return 1
    else:
        return 0


def reg_user():
    if login_username != "admin":
            print("You are not permitted to register users.")
    else:

        # appends new username and password to user.txt
        while True:
            # checks if username is already taken
            new_username = input("Enter a new username")
            if new_username in usernames:
                print("This username already exists. Please enter another.")
            else:
                break

        while True:
            # checks if passwords match
            new_password = input("Enter a new password")
            check_password = input("Enter password again to confirm")
            if check_password == new_password:
                with open('user.txt', 'a') as f:
                    f.write("\n" + new_username + ", " + new_password)
                import_users()  # update list of users
                break
            else:
                print("The passwords you entered are not identical")
    import_users()  # update list of users


def add_task():
    # checks if username is valid and assigns
    while True:
        assign_username = input("Enter username")
        if assign_username in usernames:
            break
        else:
            print("Invalid username")

    assign_task = input("Enter title of task")
    assign_descrip = input("Enter description of task")
    check_tasks_list = copy.deepcopy(all_tasks_list)  # copy of task list for amendment

    # delete information beyond username, task title, and task description
    for i in range(0, len(check_tasks_list)):
        del check_tasks_list[i][3:]

    # if username, task title, and task description is in task list already, prints so
    if [str(assign_username), str(assign_task), str(assign_descrip)] in check_tasks_list:
        print("The exact information you entered is already on the system.")
        return

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
    
    global tasks_generated
    global my_tasks_generated
    tasks_generated += 1
    if login_username == assign_username:
        my_tasks_generated +=1

    import_tasks()


def view_all():
    # prints tasks to console
        with open('tasks.txt', 'r') as f:
            for line in f:
                tasks_split = line.split(", ")  # splits lines into sections
                tasks_split[5] = tasks_split[5].strip()
                print(u'\u2500' * 70)  # prints continuous line (https://stackoverflow.com/questions/65561243/print-a-horizontal-line-in-python)
                # retrieves and prints index of task in mytask_list
                # automating the spacing for Task line for when number has multiple digits
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


def view_mine():
    while True:
        with open('tasks.txt', 'r') as f:
            global my_tasks_list
            my_tasks_list = []
            tasks_amount = 0 # counts number of tasks assigned to user
            for line in f:
                tasks_split = line.split(", ")  # splits lines into sections
                tasks_split[5] = tasks_split[5].strip()
                if login_username == tasks_split[0]:  # if current username is referenced in line
                    tasks_amount += 1
                    my_tasks_list.append(tasks_split)
                    print(u'\u2500' * 70)
                    # retrieves and prints index of task in mytask_list
                    # automating the spacing for Task line for when number has multiple digits
                    print(f'''
    Task {tasks_amount}: {" "*(17-len("Task :")-len(str(my_tasks_list.index(tasks_split)+1)))} {tasks_split[1]}
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

            while True:
                global task_select
                task_select = input("Select a task. Type -1 to exit.")

                if task_select == "-1":
                    return
                elif task_select.isdigit() != True:  # if not integer, prints invalid
                    print("Invalid input")
                elif 1 <= int(task_select) <= tasks_amount:  # if user selects a task
                    task_select = int(task_select)
                    task_action_select = int(input("Select an action:\n1. Mark task as complete.\n2. Edit task.\n3. Exit."))

                    if task_action_select == 1:
                        edit_tasks(5, "Yes")  # changes completion to Yes
                        break
                    elif task_action_select == 2:
                        if my_tasks_list[task_select-1][5] == "No":
                            user_or_date = int(input("Edit:\n1. User assignment\n2. Due date\n3. Exit"))

                            if user_or_date == 1:
                                new_assigned_user = input("Enter username.")
                                if new_assigned_user not in usernames:
                                    print("Invalid username.")
                                else:
                                    edit_tasks(0, new_assigned_user)
                                    break

                            elif user_or_date == 2:
                                new_date = input("Enter new due date.")
                                edit_tasks(4, new_date)
                                break
                            else:
                                print("Invalid input.")

                        else:
                            print("You cannot edit a completed task.") 
                    elif task_action_select == 3:
                        break
                    else: 
                        print("Invalid input.")
                else:
                    print("Invalid input.")


def display_stats():
    print(u'\u2500' * 70+"\n")
    # prints both overviews
    with open('task_overview.txt', 'r') as f:
        for line in f:
            print(line, end="")
    print("\n"+u'\u2500' * 70+"\n")
    with open('user_overview.txt', 'r') as f:
        for line in f:
            print(line, end="")
    print("\n"+u'\u2500' * 70)


def generate_reports():
    task_overview()
    user_overview()


def task_overview():
    uncompleted_tasks = []
    overdue = 0
    
    # appends uncompleted tasks to respective list
    for i in range(0, len(all_tasks_list)):
        if all_tasks_list[i][5] == "No":
            uncompleted_tasks.append(all_tasks_list[i])
    uncompleted_tasks_copy = copy.deepcopy(uncompleted_tasks)  # copy of list of uncompleted_tasks
    for i in range(0, len(uncompleted_tasks_copy)):
        due_date = uncompleted_tasks_copy[i][4]  # set due and curr date to respective values
        curr_date = uncompleted_tasks_copy[i][3]
        due_date = due_date.split(" ")  # split to use d/m/y
        curr_date = curr_date.split(" ")
        convert_month(due_date)
        convert_month(curr_date)
        overdue += determine_overdue(curr_date, due_date)  # plus 1 if overdue, else 0

    with open('task_overview.txt', 'w') as f:
        f.write(f'''Tasks generated this session:           {tasks_generated}
Total number of tasks:                  {len(all_tasks_list)}
Number of completed tasks:              {len(all_tasks_list) - len(uncompleted_tasks)}
Number of uncompleted tasks:            {len(uncompleted_tasks)}
Number of overdue tasks:                {overdue}
Percentage of tasks incomplete:         {round(100*len(uncompleted_tasks)/len(all_tasks_list), 2)}%
Percentage of tasks overdue:            {round(100*overdue/len(all_tasks_list), 2)}%
''')


def user_overview():
    my_tasks_list = []
    my_uncompleted_tasks = []
    tasks_amount = 0 # counts number of tasks assigned to user
    with open('tasks.txt', 'r') as f:
        for line in f:
            tasks_split = line.split(", ")  # splits lines into sections
            tasks_split[5] = tasks_split[5].strip()
            if login_username == tasks_split[0]:  # if current username is referenced in line
                tasks_amount += 1
                my_tasks_list.append(tasks_split)
                overdue = 0
    
    # appends uncompleted tasks to respective list
    for i in range(0, len(my_tasks_list)):
        if my_tasks_list[i][5] == "No":
            my_uncompleted_tasks.append(my_tasks_list[i])
            my_uncompleted_tasks_copy = copy.deepcopy(my_uncompleted_tasks)  # copy of list of uncompleted_tasks
    for i in range(0, len(my_uncompleted_tasks_copy)):
        due_date = my_uncompleted_tasks_copy[i][4]  # set due and curr date to respective values
        curr_date = my_uncompleted_tasks_copy[i][3]
        due_date = due_date.split(" ")  # split to use d/m/y
        curr_date = curr_date.split(" ")
        convert_month(due_date)
        convert_month(curr_date)
        overdue += determine_overdue(curr_date, due_date)  # plus 1 if overdue, else 0
    with open('user_overview.txt', 'w') as f:
        f.write(f'''Number of users:                        {len(usernames)}
Tasks generated for you this session:   {my_tasks_generated}
Number of completed tasks:              {len(my_tasks_list) - len(my_uncompleted_tasks)}
Number of uncompleted tasks:            {len(my_uncompleted_tasks)}
Number of overdue tasks:                {overdue}
Percentage of tasks incomplete:         {round(100*len(my_uncompleted_tasks)/len(my_tasks_list), 2)}%
Percentage of tasks overdue:            {round(100*overdue/len(my_tasks_list), 2)}%
''')


def import_users():
    # import list of usernames and passwords
    with open('user.txt', 'r') as f:
        global usernames
        global passwords
        usernames = []
        passwords = []
        for line in f:
            line_split = line.split(", ")
            usernames.append(line_split[0].strip())  # strips \n
            passwords.append(line_split[1].strip())


def import_tasks():
    with open('tasks.txt', 'r') as f:
        global all_tasks_list
        all_tasks_list = []
        for line in f:
            tasks_split = line.split(", ")  # splits lines into sections
            tasks_split[5] = tasks_split[5].strip()
            all_tasks_list.append(tasks_split)


import_users()
import_tasks()

tasks_generated = 0
my_tasks_generated = 0

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
vm - View my tasks
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    # menu if not admin
    else:
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my tasks
e - Exit
: ''').lower()
        

    # register a user
    if menu == 'r':
        reg_user()

    # add task
    elif menu == 'a':
        add_task()

    # view all tasks
    elif menu == 'va':
        view_all()

    # view own tasks
    elif menu == 'vm':
        view_mine()

    # display number of tasks and users
    elif menu == 'ds':
        if login_username == "admin":  # only allow access to admin
            generate_reports()
            display_stats()
        else:
            print("You have made a wrong choice, Please Try again")

    # generates txt reports
    elif menu == 'gr':
        if login_username == "admin":
            generate_reports()
        else: print("You have made a wrong choice, Please Try again")

    # exit
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")