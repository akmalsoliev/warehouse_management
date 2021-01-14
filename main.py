"""
#1
main
DATE
UNIQUE ID
CLIENT NAME
TOTAL SALES 
MODIFY
DETAILS OF TRANSACTIONS

#2
details of transactions
ITEM CODE 
ITEM NAME
BATCH NUMBER 
COLOR
COLOR NAME 

"""
import datetime
import sqlite3

def initializer():
    db = Database_Manager('database.sqlite')
    db.activate_connection()
    columns_in_main = ['Date', 'Client_Name', 'Total_Sales']
    db.create_table('MAIN', columns_in_main)
    client_name_input = "Jack"#input('Please enter client name: ')
    client_amount_input = int(1200)#int(input('Price of a sale: '))
    insert_values = [datetime.datetime.utcnow(), client_name_input, client_amount_input]
    print(insert_values)
    db.add_to_database('MAIN', columns_in_main, insert_values)

    # commit_database = input('Would you like to commit all the changes?')
    # if commit_database.upper() == 'YES':
    db.commit_and_close()

class Database_Manager():

    """The following database manager does has a vinurability, 
    utilize table_name and list_of_objects with caution as it 
    is vunerable to SQL Injection attack!
    DO NOT LET the user set up table_name, columns_in_main and list_of_objects!"""

    def __init__(self, database_name, list_of_objects = None):
        self.database_name = database_name
        self.database = None
        self.list_of_objects = list_of_objects

    def activate_connection(self):
        self.database = sqlite3.connect(self.database_name)

    def create_table(self, table_name, list_of_objects):
        self.database.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (ID INTEGER PRIMARY KEY AUTOINCREMENT)')
        try:
            for obj in list_of_objects:
                self.database.execute(f'ALTER TABLE {table_name} ADD COLUMN {obj}')
        except:
            pass

    def add_to_database(self, table_name, column_list, insert_values):
        placeholder = ','.join('?' * len(column_list))
        columns = ', '.join(column_list)
        self.database.execute(f"INSERT INTO {table_name}({columns}) VALUES({placeholder})", (*insert_values,))
  
    def check_if_exists(self, table_name, check_object, column_name):
        if self.database.execute(f'SELECT ? FROM {table_name} WHERE ? = ?', (column_name, column_name, check_object)):
            pass
    def commit_and_close(self):
        self.database.commit()
        self.database.close()

class Client():
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount


if __name__ == "__main__":
    initializer()