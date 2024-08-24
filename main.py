import pandas as pd
import csv
from datetime import datetime
from data_entry import *


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ['date', 'amount', 'category', 'description']
    @classmethod    # class decorator 
    def initialize_cvs(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)   # Creating a dataframe if any '.csv' not found
            df.to_csv(cls.CSV_FILE, index=False)
            
            
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }  
        
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, cls.COLUMNS) # Creating csv writer that takes in the dict and writes it into the csv file
            writer.writerow(new_entry)
        print("Entry added succesfully!")  
            
def add():
    CSV.initialize_cvs()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or Enter today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


add()
