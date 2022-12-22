import math
selection = input("Choose either 'investment' or 'bond' from the menu to proceed: \n \n investment - to calculate the amount of interest you'll earn on your investment \n bond - to calculate the amount you'll have to pay on a home loan")

# investment selected
if selection.lower() == "investment":
    deposit = float(input("How much will you deposit?"))
    interest_rate = float(input("What is the interest rate?"))
    interest_rate = interest_rate * 0.01  # converting from percentage to decimal
    years = int(input("How many years do you plan on investing?"))
    interest_type = input("Do you want simple or compound interest?")
    # simple selected
    if interest_type.lower() == "simple":
        total = deposit * (1+interest_rate*years)  # calculates total amount
        print(round(total,2))
    # compound selected
    elif interest_type.lower() == "compound":
        total = deposit * math.pow((1+interest_rate), years)  # calculates total amount
        print(round(total, 2))
    # invalid
    else:
        print("Invalid selection. Please try again.")
# bond selected
elif selection.lower() == "bond":
    value = float(input("Present value of house?"))
    interest_rate = float(input("What is the annual interest rate?"))
    months = int(input("How many months do you plan to take to repay the bond?"))
    interest_rate = interest_rate / 100  # converting from percentage to decimal (divide 100)
    interest_rate = interest_rate / 12  # converting yearly to monthly (divide 12)
    repayment = (interest_rate*value) / (1-(1+interest_rate)**-months)  # calculates monthly repayment
    print(round(repayment, 2))
# invalid
else:
    print("Invalid selection. Please try again.")