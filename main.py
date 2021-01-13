"""
main
DATE
UNIQUE ID
CLIENT NAME
TOTAL SALES 
MODIFY
DETAILS OF TRANSACTIONS

details of transactions
ITEM CODE 
ITEM NAME
BATCH NUMBER 
COLOR
COLOR NAME 

"""
import datetime
import sqlite3

class main_window():
    def __init__(self):
        # db.execute('CREATE TABLE IF NOT EXISTS goods' \
        #     '(material TEXT NOT NULL, length INTEGER NOT NULL, kg INTEGER NOT NULL,' \
        #     ' color TEXT NOT NULL)')
        db.execute('CREATE TABLE IF NOT EXISTS main_window' \
            '(Unique_ID INTEGER PRIMARY KEY NOT NULL, Date TIMESTAMP NOT NULL, Client_Name TEXT NOT NULL, Total_Sales INTEGER NOT NULL)')
        self.user_input = input("Client's name and amount (format: name, amount): ")
        self.__name, self.__amount = self.user_input.split(', ')
        self.client = self.Client(self.__name, int(self.__amount))
        cursor = db.execute('SELECT Unique_ID FROM main_window ORDER BY Unique_ID DESC')
        self.unique_id = cursor.fetchone()[0] + 1
        db.execute('INSERT INTO main_window VALUES(?, ?, ?, ?)', (self.client.transactions[0][0], int(self.unique_id), self.client.name, self.client.transactions[0][1]))


    class Client():
        def __init__(self, name, amount):
            self.name = name
            self.amount = amount
            self.transactions = []
            self.transactions.append([datetime.datetime.utcnow(), self.amount])
    
        def add_amount(self, amount):
            for list_ in self.transactions:
                for _, transaction in list_:
                    sales_total += transaction


if __name__ == "__main__":
    db = sqlite3.connect('database.sqlite')
    main_window()
    commit_ = input('Would you like to commit?')
    if commit_.upper() == 'YES':
        db.commit()
    else:
        db.rollback()
    db.close()