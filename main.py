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

    #NOTE out of any function, since this is the primary 
    client_name_input = input('Please enter client name: ')
    client_amount_input = int(input('Price of a sale: '))
    our_client = Client(client_name_input, client_amount_input)

    #Creating our first table with all the information about the client
    __client_table = 'client_table'
    __columns_in_table = ['Date', 'Client_Name', 'Total_Sales']
    __client_column_name = __columns_in_table[1] #"Client_Name"
    changable_column = __columns_in_table[2] #"Total_Sales"
    db.create_table(__client_table, __columns_in_table)
    user_interaction(__client_table, db, __columns_in_table, our_client, __client_column_name, changable_column)

    db.commit_and_close()

def user_interaction(table, database_class, columns_in_table, our_client, index_column, changable_column):
    while True:
        insert_values = [datetime.datetime.utcnow(), our_client.name, our_client.amount]
        database_class.add_to_database(changable_column, table, index_column, our_client.name, our_client.amount, columns_in_table, insert_values)
        quit_request = 'YES'#input('Are you done with all your requests? ')
        if quit_request.upper() == 'YES':
            break

class Database_Manager():

    """The following database manager does has a vinurability, 
    utilize table_name and list_of_objects with caution as it 
    is vunerable to SQL Injection attack!
    DO NOT LET the user set up table_name, __columns_in_table and list_of_objects!"""

    def __init__(self, database_name, list_of_objects = None):
        self.database_name = database_name
        self.database = None
        self.list_of_objects = list_of_objects
    
    def activate_connection(self):
        self.database = sqlite3.connect(self.database_name)

    def add_to_database(self, change_column, table_name, column_name, check_object, amount, column_list, insert_values):
        select_column = self.database.execute(f'SELECT {change_column} FROM {table_name} WHERE {column_name} = ?', (check_object,))
        if select_column.fetchone() == None:
            print(f'{check_object} is a new entry, adding to database.')
            self.new_client(table_name, column_list, insert_values)
        else:
            print(f'{check_object} is an existing entry, changes to {change_column} has been made.')
            cursor = self.database.execute(f'SELECT {change_column} FROM {table_name} WHERE {column_name} = ?', (check_object,))
            new_total_sales = cursor.fetchone()[0] + amount
            self.database.execute(f'UPDATE {table_name} SET {change_column} = {new_total_sales} WHERE {column_name} = ?', (check_object,))

    def new_client(self, table_name, column_list, insert_values):
        placeholder = ','.join('?' * len(column_list))
        columns = ', '.join(column_list)
        self.database.execute(f"INSERT INTO {table_name}({columns}) VALUES({placeholder})", (*insert_values,))

    def create_table(self, table_name, list_of_objects):
        self.database.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (ID INTEGER PRIMARY KEY AUTOINCREMENT)')
        try:
            for obj in list_of_objects:
                self.database.execute(f'ALTER TABLE {table_name} ADD COLUMN {obj}')
        except:
            pass

    def commit_and_close(self):
        request = input('Save the database? ')
        if request.upper() == 'YES':
            self.database.commit()
            self.database.close()


class Client():
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount


if __name__ == "__main__":
    while True:
        initializer()
        restart = input('Would you like to restart? ')
        if restart.upper != "YES":
            break