from datetime import datetime
date_format = "%d-%m-%Y"
CATEGORIES = {
    'I': 'Income',
    'E': 'Expense'
}


def get_date(prompt, allow_default=False):
    date_val = input(prompt)
    if allow_default and not date_val:
        return datetime.today().strftime(date_format)
    
    try:
        valid_date = datetime.strptime(date_val, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date format! Please enter date in dd-mm-yyyy format.")
        return get_amount(prompt, allow_default)
    ''' finally:
        pass '''

def get_amount():
    try:
        amount = float(input("Enter the amount: (in Rs)"))
        if amount <= 0:
            raise ValueError("Amount must be a value greater than 0.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()


def get_category():
    category = input("Choose a category from the list:\n'I' -> Income\n'E' -> Expense\nCategory: ")
    if category in CATEGORIES:
        return CATEGORIES[category]
    print("Please choose a valid category from the given list.")
    return get_category()

def get_description():
    return input("Enter a description (optional): ")