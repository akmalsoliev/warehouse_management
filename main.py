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
import os 
import pickle
import pathlib
from Database_Manager import Database_Manager
from client_materials import Client, Material

def initializer():
    db = Database_Manager('database.sqlite')
    db.activate_connection()
    db.back_up() #Database backup in case of corruption or dataloss

    #NOTE out of any function, since this is the primary 
    client_name_input = input('Please enter client name: ')
    client_amount_input = 13234#int(input('Price of a sale: '))
    our_client = Client(client_name_input, client_amount_input)

    #Creating our first table with all the information about the client
    __transactions_table = 'transactions_table'
    __columns_in_table = ['Date ','Client_Name', 'Sales_Transaction']
    db.create_table(__transactions_table, __columns_in_table)
    user_interaction(__transactions_table, db, __columns_in_table, our_client)

    #Creating VIEW
    __total_sales_client = 'total_sales_per_client'
    __columns_in_table = ['Date','Client_Name']
    __sum_column = ['Sales_Transaction']
    __order_by = ['Client_Name']
    db.create_summary_column(__total_sales_client, __transactions_table, __columns_in_table, __sum_column, __order_by)
    db.commit_and_close()

def user_interaction(table, database_class, columns_in_table, our_client):
    while True:
        insert_values = [datetime.datetime.utcnow(), our_client.name, our_client.amount]
        database_class.add_to_transaction(table, columns_in_table, insert_values)
        quit_request = 'YES'#input('Are you done with all your requests? ')
        if quit_request.upper() == 'YES':
            break

if __name__ == "__main__":
    while True:
        initializer()
        restart = 'No'#input('Would you like to restart? ')
        if restart.upper() != "YES":
            break