import pandas as pd
import csv
import numpy as np
from datetime import datetime
from data_entry import *
import matplotlib.pyplot as plt
# import matplotlib.axes as ax
class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ['date', 'amount', 'category', 'description']
    FORMAT = "%d-%m-%Y"
    
    
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
        
        
    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)
        
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]
        
        if filtered_df.empty:
            print("No transactions found in the given date range.")
        else:
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\nSummary:")
            print(f"Total Income: Rs{total_income:.2f}")
            print(f"Total Expense: Rs{total_expense:.2f}")
            print(f"Net Savings: Rs{(total_income - total_expense):.2f}")
    
        return df

     
    
            
def add():
    CSV.initialize_cvs()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or Enter today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def plot_transactions(df):
    df.set_index("date", inplace=True)
    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)
    
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="green")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="red")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income V/s Expense over time")
    plt.xticks(ticks=df.index, labels=df.index.strftime('%d-%m-%Y'), rotation=90, fontsize=8)
    plt.yticks(ticks=np.arange(0, max(df["amount"].max(), 1), step=500))
    plt.legend()
    plt.grid(True)
    plt.show()   

    
    
# CSV.get_transactions("24-08-2024", "31-08-2024")
# add()

def main():
    while True:
        print("\n1. Add a new Transaction")
        print("\n2. View transactions and summary within a date range")
        print("\n3. Exit")
        
        choice = input("Enter your choice (1 - 3): ")
        
        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see a plot? (y/n): ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("\nInvalid choice!\nProvide the number in (1 - 3)")


if __name__ == '__main__':
    main()
            
