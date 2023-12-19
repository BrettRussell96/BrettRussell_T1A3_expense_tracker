import json 
import readchar
from classes import Income, User, primary_income, supplementary_income
from lists import occurrence_options, basic_options, home_expense_options, food_expense_options, transport_expense_options, other_expense_options


saved_users = [] 
filename = "users.json"   


def display_menu(options, title = "menu"):
    current_selection = 0

    while True:
        print("\033[H\033[J", end = "")

        print(title)
        for i, option in enumerate(options):
            prefix = "-> " if i == current_selection else "   "
            print(f"{prefix}{option}")

        key = readchar.readkey()

        if key == readchar.key.UP and current_selection > 0:
            current_selection -= 1
        elif key == readchar.key.DOWN and current_selection < len(options) - 1:
            current_selection += 1
        elif key == readchar.key.ENTER:
            break

    return current_selection



def load_users(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return {name: (info if isinstance(info, dict) else {}) for name, info in data.items()}
    except FileNotFoundError:
        print("Welcome to the Budget Tracker!")
        return {}
users_data = load_users(filename)



def save_users(users,filename):
    with open(filename, "w") as file:
        json.dump(users, file, indent=4)



def user_selection_menu(saved_users):
    user_names = [user.name for user in saved_users]
    user_menu_options = user_names + ["New User"]
    selected_option = display_menu(user_menu_options, "Select User")
    return selected_option



def new_user_creation():
    create_new_user = display_menu(basic_options, "Would you like to create a new user?")
    if create_new_user == 0:
        user_name = input("Please enter a name: ")
        new_user = User(user_name)
        return new_user
    else:
        return None



def save_user_data(users_data, user, filename):
    users_data[user.name] = user.to_dict()
    with open(filename, 'w') as file:
        json.dump(users_data, file, indent=4)



def generate_income_info(income_data):
    income_info = ""
    for income_type, details in income_data.items():
        amount = int(details['amount'])
        occurrence = details['occurrence']
        income_info += f"{income_type}: ${amount} ({occurrence})\n "
    return income_info



def generate_expense_info(category_data):
    expense_info = ""
    for expense_type, details in category_data.items():
        amount = int(details['amount'])
        occurrence = details['occurrence']
        expense_info += f"{expense_type}: ${amount} ({occurrence})\n     "
    return expense_info.rstrip()



def add_income(user, income_type):
    occurrence = display_menu(occurrence_options, "How often do you receive this income source?")

    if occurrence_options[occurrence] == "Previous Section":
        return
    
    while True:
        income_value_input = input("Enter the value of the income (press q to return): ")
        if income_value_input.lower() == 'q':
            return
        try:
            income_value = float(income_value_input)
            income_info = {
                "amount": income_value,
                "occurrence": occurrence_options[occurrence]
            }

            if income_type == 'primary':
                user.primary_income = income_info
            else: 
                user.supplementary_income = income_info
            save_user_data(users_data, user, filename)
            break
        except ValueError:
            print("Invalid input, please use only numbers.")
    



def add_expenses(user, expense_category):
    while True:
        match expense_category:
            case "home":
                options = home_expense_options
            case "food":
                options = food_expense_options
            case "transport":
                options = transport_expense_options
            case "other":
                options = other_expense_options

        option = display_menu(options, "Select an expense:")        
        if option == len(options) - 1:
                    break
        
        expense_name = options[option]

        occurrence = display_menu(occurrence_options, "How frequent is this expense?")
        if occurrence_options[occurrence] == "Previous Section":
            return
        
        while True:
            expense_value_input = input("Enter the value of the expense (press 'q' to return): ")
            if expense_value_input.lower() == 'q':
                return
            try:
                expense_value = float(expense_value_input)
                user.expense[expense_category][expense_name] = {
                    "amount": expense_value,
                    "occurrence": occurrence_options[occurrence]
                }
                save_user_data(users_data, user, filename)
                break
            except ValueError:
                print("Invalid input, please use only numbers.")
            

def calculate_finance(user, time_frame):
    conversion = {
        "Weekly": {"Weekly": 1, "Fortnightly": 0.5, "Monthly": 12 / 52},
        "Fortnightly": { "Weekly": 2, "Fortnightly": 1, "Monthly": 12 / 26},
        "Monthly": { "Weekly": 52 / 12, "Fortnightly": 26 / 12, "Monthly": 1}
    }
    total_income = 0
    total_expense = 0

    for income in [user.primary_income, user.supplementary_income]:
        if income['amount'] > 0:
            total_income += income['amount'] * conversion[time_frame][income['occurrence']]
    
    for category, expenses in user.expense.items():
        for expense in expenses.values():
            if expense['amount'] > 0:
                total_expense += expense['amount'] * conversion[time_frame][expense['occurrence']]
    
    remaining_funds = total_income - total_expense

    user.total_income = {"amount": total_income, "occurrence": time_frame}
    user.total_expense = {"amount": total_expense, "occurrence": time_frame}
    user.remaining_funds = {"amount": remaining_funds, "occurrence": time_frame}

    return total_income, total_expense, remaining_funds



def create_budget():
    pass


def new_user():
    pass


def switch_user():
    pass


def delete_user():
    pass

