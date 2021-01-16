import datetime
import sqlite3
import os 
import pickle
import pathlib

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
        self.database = sqlite3.connect(self.database_name, detect_types=sqlite3.PARSE_DECLTYPES)
        
    def create_table(self, table_name, list_of_objects):
            self.database.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (ID INTEGER PRIMARY KEY AUTOINCREMENT)')
            try:
                for obj in list_of_objects:
                    self.database.execute(f'ALTER TABLE {table_name} ADD COLUMN {obj}')
            except:
                pass

    def back_up(self):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        self.backup_each_run(root_dir)
        self.backup_24H(root_dir)

    def backup_each_run(self, root_dir):
        backup_dir = str(pathlib.Path().joinpath(root_dir, r'__backup\__database_backup.sqlite'))
        if os.path.exists(backup_dir):
            os.remove(backup_dir)
        back_up_database = sqlite3.connect(backup_dir)
        self.database.backup(back_up_database)
        back_up_database.close()

    def backup_24H(self, root_dir):
        backup_dir = str(pathlib.Path().joinpath(root_dir, r'__backup\__24Hdatabase_backup.sqlite'))
        binary_file_location = str(pathlib.Path().joinpath(root_dir, r'__backup\__backup_timer.pickle'))
        write_file = open(binary_file_location, 'wb')
        try:
            read_file = open(binary_file_location, 'rb')
            time_last_backup = pickle.load(read_file)
            if (time_last_backup - datetime.timedelta(days=1))>datetime.datetime.utcnow():
                back_up_database = sqlite3.connect(backup_dir)
                self.database.backup(back_up_database)
                pickle.dump(datetime.datetime.utcnow(), write_file)
                back_up_database.close()
        except EOFError:
            back_up_database = sqlite3.connect(backup_dir)
            self.database.backup(back_up_database)
            pickle.dump(datetime.datetime.utcnow(), write_file)
        read_file.close()
        write_file.close()

    def add_to_transaction(self, table_name, column_list, insert_values):
        placeholder = ','.join('?' * len(column_list))
        columns = ', '.join(column_list)
        self.database.execute(f"INSERT INTO {table_name}({columns}) VALUES({placeholder})", (*insert_values,))

    def create_summary_column(self, table_name, source_table, desired_columns, sum_column, group_by):
        # self.database.execute('CREATE VIEW IF NOT EXISTS total_sales_per_client(Date, Client_Name, Total_Sales) AS SELECT Date, Client_Name, sum(Sales_Transaction) FROM transactions_table GROUP BY Client_Name ORDER BY Client_Name')
        self.database.execute(f'CREATE VIEW IF NOT EXISTS {table_name}({desired_columns}, {table_name}) AS SELECT {desired_columns}, SUM({sum_column}) FROM {source_table} GROUP BY {group_by} ORDER BY {group_by}')

    def commit_and_close(self):
        request = 'Yes'#input('Save the database? ')
        if request.upper() == 'YES':
            self.database.commit()
            self.database.close()