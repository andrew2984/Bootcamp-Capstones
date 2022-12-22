#========The beginning of the class==========
class Shoe:

    # initialises
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    
    # returns cost
    def get_cost(self):
        cost = self.cost

        return cost


    # returns quantity
    def get_quantity(self):
        quantity = self.quantity

        return quantity


    # returns string of attributes
    def __str__(self):
        string_rep = f"{self.country}, {self.code}, {self.product}, {self.cost}, {self.quantity}"
        return string_rep


#=============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''
shoe_list = []
#==========Functions outside the class==============
def read_shoes_data():
    '''
    Reads file, creates shoe objects, appends to shoe_list then deletes first element
    '''
    # will clear existing list if called again to overwrite
    shoe_list.clear()
    try:

        with open('inventory.txt', 'r') as f:
            for line in f:
                line = line.strip()
                line = line.split(",")  # attributes are split by , in file
                country, code, product, cost, quantity = line  # multivariable split
                new_shoe = Shoe(country, code, product, cost, quantity)
                shoe_list.append(new_shoe)
        del shoe_list[0]
    
    except FileNotFoundError:
        print("inventory.txt is not found.")
    except ValueError:
        print("One or more lines in inventory.txt are not of the correct format.")


def capture_shoes():
    '''
    This function will allow a user to capture data
    about a shoe and use this data to create a shoe object
    and append this object inside the shoe list.
    '''
    capture_country = input("Where is the shoe from?")
    capture_code = input("What is the shoe's code?")
    # return if code is already in use
    if seach_shoe(capture_code) != None:
        print(f"Code is already taken by {seach_shoe(capture_code).product}")
        return
    capture_product = input("What is the name of the shoe?")
    capture_cost = float(input("What is the price of the shoe?"))
    capture_quantity = input("What is the quantity of the shoe?")
    new_shoe = Shoe(capture_country, capture_code, capture_product, capture_cost, capture_quantity)  # make new shoe object
    shoe_list.append(new_shoe)
    # write new shoe to file
    with open('inventory.txt', 'a') as f:
        append_to_file = f"{new_shoe.country},{new_shoe.code},{new_shoe.product},{new_shoe.cost},{new_shoe.quantity}"
        f.write(f"\n{append_to_file}")


def view_all():
    '''
    This function will iterate over the shoes list and
    print the details of the shoes returned from the __str__
    function. Optional: you can organise your data in a table format
    by using Python’s tabulate module.
    '''
    for shoes in shoe_list:
        print(shoes.__str__())


def re_stock():
    '''
    This function will find the shoe object with the lowest quantity,
    which is the shoes that need to be re-stocked. Ask the user if they
    want to add this quantity of shoes and then update it.
    This quantity should be updated on the file for this shoe.
    '''
    lowest_quantity = get_highest_lowest_quantity(min)  # argument is min to get lowest
    # user can add to quantity
    while True:
        choice_add = input(f"{lowest_quantity.product} has a quantity of {lowest_quantity.quantity}. Would you like to add to this?")
        if choice_add.lower() == "yes":
            try:
                
                quantity_add = int(input("How many would you like to add?"))
                if quantity_add <= 0:  # if input below zero, continue
                    print("Please enter a value above 0.")
                    continue
                overwrite = []
                # makes a copy of inventory.txt in overwrite with addition to shoe with lowest quantity
                # rewrites file using overwrite
                with open('inventory.txt', 'r') as f:
                    for line in f:
                        # if attributes of shoe with lowest quantity matches a line
                        # add user input to quantity
                        if f"{lowest_quantity.country},{lowest_quantity.code},{lowest_quantity.product},{lowest_quantity.cost},{lowest_quantity.quantity}" == line.strip():
                            overwrite.append(f"{lowest_quantity.country},{lowest_quantity.code},{lowest_quantity.product},{lowest_quantity.cost},{int(lowest_quantity.quantity)+quantity_add}\n")     
                        else:
                            overwrite.append(line)
                # rewrite
                with open('inventory.txt', "w") as f:
                    for count, element in enumerate(overwrite, 0):
                        f.write(overwrite[count])
                break

            except FileNotFoundError:
                print("inventory.txt is not found.")
            except ValueError:
                print("Please enter a number.")
        elif choice_add.lower() == "no":
            break
        else:
            print("Invalid input.")
    

def seach_shoe(code):
    '''
     This function will search for a shoe from the list
     using the shoe code and return this object so that it will be printed.
    '''
    for shoes in shoe_list:
        if shoes.code == code:  # if user code matches, return it

            return shoes


def value_per_item():
    '''
    This function will calculate the total value for each item.
    Please keep the formula for value in mind: value = cost * quantity.
    Print this information on the console for all the shoes.
    '''
    for shoes in shoe_list:
        print(f"{shoes.product}: R{float(shoes.cost)*float(shoes.quantity)}")


def highest_qty():
    '''
    Write code to determine the product with the highest quantity and
    print this shoe as being for sale.
    '''
    highest_quantity = get_highest_lowest_quantity(max)  # argumemt is max to get highest
    print(f"{highest_quantity} is on sale.")


def get_highest_lowest_quantity(max_min):
    # appends cost to quantity list and finds max/min
    quantity_list = []
    for shoes in shoe_list:
        quantity_list.append(float(shoes.get_quantity()))
    highest_lowest_quantity = max_min(quantity_list)  # max_min can be max or min depending on argument

    # appends shoes with lowest quantity to list
    highest_lowest_quantity_list = []
    for shoes in shoe_list:
        if float(shoes.get_quantity()) == highest_lowest_quantity:
            highest_lowest_quantity_list.append(shoes)

    # if lowest_quantity_list has length greater than 1, let user select one
    if len(highest_lowest_quantity_list) > 1:
        # display enum and names of shoes in list
        for i in range(0, len(highest_lowest_quantity_list)):
            print(f"{i+1}. {highest_lowest_quantity_list[i].product}")
        while True:
            try:
                choose_lowest = int(input("Choose one of these to continue."))
                if 1 <= choose_lowest <= len(highest_lowest_quantity_list):  # if input corresponds to an option
                    result = highest_lowest_quantity_list[choose_lowest-1]
                    return result
                else:
                    print("Invalid number.")
            except ValueError:
                print("Please enter a number.")
    else:
        result = highest_lowest_quantity_list[0]  # only one element

    return result

#==========Main Menu=============

while True:
    read_shoes_data()  # updates list for current session
    try:
        menu = int(input("""Would you like to:
1. View inventory
2. Add new shoe
3. Seach for shoe
4. Re-stock shoe with lowest quantity
5. Check if shoe with highest quantity is on sale
6. View value of shoes
0. Exit"""))
        if menu == 1:
            view_all()
        elif menu == 2:
            capture_shoes()
        elif menu == 3:
            user_code = input("Enter the code of the shoe you would to search for.")
            print(seach_shoe(user_code).__str__())
        elif menu == 4:
            re_stock()
        elif menu == 5:
            highest_qty()
        elif menu == 6:
            value_per_item()
        elif menu == 0:
            break
        else:
            print("Invalid number.")
    except ValueError:
        print("Please enter a number.")