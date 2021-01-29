import datetime, sqlite3, os, pickle, pathlib
from Database_Manager import Database_Manager
from client_materials import Client, Material

def initializer(client_name_input = None, client_amount_input = None):
    db = Database_Manager('database.sqlite')
    db.activate_connection()
    db.back_up() #Database backup in case of corruption or dataloss

    #NOTE out of any function, since this is the primary
    item_code = input("Item code: ")
    item_name = input('Item name: ')
    batch_number = input('Batch number: ')
    color = input('Color: ')
    our_material = Material(item_code, item_name, batch_number, color)

    client_name_input = input('Please enter client name: ') #TODO: Fix prior to push
    client_amount_input = int(input('Price of a sale: ')) #TODO: Fix prior to push
    our_client = Client(client_name_input, client_amount_input)

    #Inflow table
    __inflow_talbe = 'Inflow_Table'
    __columns_in_table = ['Item_Code', 'Date', 'Client_Name', 'Sales_Transaction', 'Material', 'Material_Colour', \
                          'Batch_Number']
    db.create_table(__inflow_talbe, __columns_in_table)
    user_interaction(__inflow_talbe, db, __columns_in_table, our_client, our_material)

    #Outflow table with all the information about the client
    __outflow_table = 'Sales_Table'
    __columns_in_table = ['Item_Code', 'Date','Client_Name', 'Sales_Transaction', 'Material', 'Material_Colour', \
                          'Batch_Number']
    db.create_table(__outflow_table, __columns_in_table)
    user_interaction(__outflow_table, db, __columns_in_table, our_client, our_material)

    #Creating VIEW of all sales per customer
    __total_sales_customer = 'Total_Sales_Table_Per_Customer'
    __desired_table = __outflow_table
    __sum_column = 'Sales_Transaction'
    __columns_total_sales_per_cus = [column for column in __columns_in_table if column not in __sum_column]
    __order_by = 'Client_Name'
    db.create_summary_column(__total_sales_customer, __columns_total_sales_per_cus, __sum_column, __desired_table, \
                             __order_by)

    #Creating VIEW of items in stcok
    #FIXME: Not yet functioning, requires a fix
    # __items_in_stock = 'Items_in_Stock'
    # first_table, second_table = __inflow_talbe, __outflow_table
    # __unique_id = 'Sales_Transaction'
    # db.items_in_stock(__items_in_stock, __columns_in_table, first_table, second_table, __unique_id)

    db.commit_and_close()

def user_interaction(table, database_class, columns_in_table, our_client, our_material):
    while True:
        insert_values = [our_material.item_code,datetime.datetime.utcnow(), our_client.name, our_client.amount, \
                         our_material.item_name, our_material.color, our_material.batch_number]
        database_class.add_transaction(table, columns_in_table, insert_values)
        quit_request = input('Are you done with all your requests? ')
        if quit_request.upper() == 'YES':
            break

if __name__ == "__main__":
    initializer()
    while True:
        restart = input('Would you like to restart? ')
        if restart.upper() != "YES":
            break