'''
1. categorize expense
2. monthly budget
3. save and load file (expense data)
4. menu driven interface
    The date of the expense in the format YYYY-MM-DD
    The category of the expense, such as Food or Travel
        Pre-defined category, default value is None
    The amount spent
    A brief description of the expense
        

    data structure:
        {'date': '2024-09-18', 'category': 'Food', 'amount': 15.50, 'description': 'Lunch with friends'}
5. view expense:
    display all stored expenses
    ***validate the data before displaying it (validation can happen at recording process as well)
        all fields are required
    * when recording expense, validate budget
6. Set & track budget:
    create budget
        prompt to enter budget for month
    * when recording expense, validate budget,display warning
    * if within the budget, display the remaining balance
7. save to CSV
8. menu:
    create a list, assign number to each item, input number to choose function
'''

__all__ = ['ExpenseTracker']

import json
from datetime import datetime
import csv

class ExpenseTracker:
    def __init__(self):
        self.expense_list = self.load_expense()
        self.mainMenu = {
            "1": {
                "key": "add_expense",
                "display_name": "Add xpense"
            },
            "2": {
                "key": "view_expenses",
                "display_name": "View expenses"
            },
            "3": {
                "key": "track_budget",
                "display_name": "Track budget"
            },
            "4": {
                "key": "save_expenses",
                "display_name": "Save expenses"
            },
            "5": {
                "key": "exit",
                "display_name": "Exit"
            }
        }
        self.category = {
            "1": {
                "key": "general",
                "display_name": "General"
            },
            "2": {
                "key": "food",
                "display_name": "Food & Dining"
            },
            "3": {
                "key": "utility",
                "display_name": "Utilities"
            },
            "4": {
                "key": "transportation",
                "display_name": "Transportation"
            },
            "5": {
                "key": "finance",
                "display_name": "Financial"
            },
            "6": {
                "key": "life_style",
                "display_name": "Life Style & Entertainment"
            }
        }
    
    def displayMenu(self):
        print("\n=====MAIN MENU=====")
        for i in self.mainMenu:
            print(f'{i}. {self.mainMenu[i]["display_name"]}')
    
    def main(self):
        while True: 
            self.displayMenu()
            choice = input("Enter you choice (1 - 5): ")
            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.view_expense()
            elif choice == '3':
                self.track_buget()
            elif choice == '4':
                self.save_expense()
            else:
                break

  
    def add_expense(self):
        while True: 
            print("\nAdd an expense: ")
            expDate = input("Please input the date of the expense in the format YYYY-MM-DD: ")
            print("Category:  ")
            for i in self.category:
                print(f'{i}. {self.category[i]['display_name']}')
            category = input("Enter your choice (1 - 5): ")
            amount = input("Enter the amount spent: ")
            description = input("Enter the description of the expense: ")

            curExp = {
                'date': expDate,
                'category': category,
                'amount': amount,
                'description': description
            }
            self.expense_list.append(curExp)
            print('- Add another expense, choose 1;')
            print('- Go back to main menu, choose 2.')
            next = input("Enter your choice: ")
            if next == "1":
                self.add_expense()
            else:
                break


    def view_expense(self):
        print(self.expense_list[0])
        

    def load_expense(self):
        expenses = []
        with open("my_expenses.csv", mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if 'amount' in row:
                    row['amount'] = float(row['amount'])
                expenses.append(row.copy())
        self.expense_list = expenses
        return self.expense_list
    
    def save_expense(self):
        fieldNames = ["date", "category", "amount", "description"]
        print(self.expense_list)
        with open("my_expenses.csv", mode="w", newline='', encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
            writer.writeheader()
            writer.writerows(self.expense_list)
    
    # def set_buget(self):
    #     budget = input("Enter the total amount you want to budget for the month.")
    #     self.budget = budget

    def get_total_expense_by_date(self, curr_date):
        if not self.expense_list:
            self.load_expense()
        total = 0
        for exp in self.expense_list:
            exp_date = self.convert_datetime_obj(exp['date'])
            if self.same_month(curr_date, exp_date):
                total += float(exp['amount'])
        return total
            
    def convert_datetime_obj(self, date_string):
        date_list = date_string.split("-")
        date_object = datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        return date_object
    
    def same_month(self, date1, date2):
        return True if (date1.year == date2.year) & (date1.month == date2.month) else False
    
    def track_buget(self):
        now = datetime.now()
        budget = float(input('Enter the total amount they want to budget for the month: '))
        total_exp = self.get_total_expense_by_date(now)
        diff = budget - total_exp
        if diff < 0:
            print(f"!!You have exceeded your budget by {diff * -1}!")
        else:
            print(f'You have {diff} dollars left for the month')
    
        
expenseTracker = ExpenseTracker()

expenseTracker.main()