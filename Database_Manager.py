import datetime, sqlite3, os, pickle, pathlib


# Including all the imported modules for potential debugging purposes

class Database_Manager():
    
    """The following database manager does has a vinurability, utilize table_name and list_of_objects with caution as it
    is vunerable to SQL Injection attack!
    DO NOT LET the user set up table_name, __columns_in_table and list_of_objects!"""

    def __init__(self, database_name, list_of_objects=None):
        self.database_name = database_name
        self.database = None
        self.list_of_objects = list_of_objects

    def activate_connection(self):
        "Activating the connection to the database"
        self.database = sqlite3.connect(self.database_name, detect_types=sqlite3.PARSE_DECLTYPES)

    def create_table(self, table_name, list_of_objects):

        """Creating a table. talbe_name should be set by the operator and not the user! Never give the user ability
        to set table_name and list_of_bojects as the code is vunerable to SQL injection attack.
        NOTE: creation is a single time operations, current there are no intentions to add table header editor."""

        self.database.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (ID INTEGER PRIMARY KEY AUTOINCREMENT)')
        try:
            for obj in list_of_objects:
                self.database.execute(f'ALTER TABLE {table_name} ADD COLUMN {obj}')
        except:
            pass

    def back_up(self):

        """Creation of backup, this code generates a backup of an existing database. 
        Backup consisits of each run backup and 24 hour one, if an operator would like to not include one or both
        he/she can simply comment the following code"""

        root_dir = os.path.dirname(os.path.abspath(__file__))
        self.backup_each_run(root_dir)
        self.backup_24H(root_dir)

    def backup_each_run(self, root_dir):

        "Every single run backup. NOTE: The backups will be saved to the file root location's sub-folder"

        backup_dir = str(pathlib.Path().joinpath(root_dir, "__backup", "__database_backup.sqlite"))
        if os.path.exists(backup_dir):
            os.remove(backup_dir)
        else:
            try:
                os.mkdir('__backup')
            except:
                pass
        back_up_database = sqlite3.connect(backup_dir)
        self.database.backup(back_up_database)
        back_up_database.close()

    def backup_24H(self, root_dir):

        """24 hour backup, this backup will be done every 24 hours, if the code was opened > 24 hours then the
        following code will act as a every single run backup. In order to have 24 hour backup the software
        would need to run in background (no current plans on creating additional software to do so."""

        backup_dir = str(pathlib.Path().joinpath(root_dir, "__backup", "__24Hdatabase_backup.sqlite"))
        binary_file_location = str(pathlib.Path().joinpath(root_dir, '__backup', '__backup_timer.pickle'))
        write_file = open(binary_file_location, 'wb')
        try:
            read_file = open(binary_file_location, 'rb')
            time_last_backup = pickle.load(read_file)
            if (time_last_backup - datetime.timedelta(days=1)) > datetime.datetime.utcnow():
                back_up_database = sqlite3.connect(backup_dir)
                self.database.backup(back_up_database)
                pickle.dump(datetime.datetime.utcnow(), write_file)
                back_up_database.close()
                read_file.close()
        except EOFError:
            back_up_database = sqlite3.connect(backup_dir)
            self.database.backup(back_up_database)
            pickle.dump(datetime.datetime.utcnow(), write_file)
        write_file.close()

    def add_transaction(self, table_name, column_list, insert_values):

        placeholder = ','.join('?' * len(column_list))
        columns = ', '.join(column_list)
        self.database.execute(f"INSERT INTO {table_name}({columns}) VALUES({placeholder})", (*insert_values,))

    def create_summary_column(self, table_name, desired_columns, sum_column, source_table, group_by):
        columns = ', '.join(desired_columns)
        self.database.execute(f'''CREATE VIEW IF NOT EXISTS {table_name}({columns}, {sum_column}) 
                                    AS SELECT {columns}, SUM({sum_column}) 
                                    FROM {source_table} GROUP BY {group_by} ORDER BY {group_by}''')

    def items_in_stock(self, table_name, columns_in_table, first_table, second_table, unique_id):
        pass
        #TODO: Requires a fix, do not use yet
        # print(f'CREATE VIEW IF NOT EXISTS {table_name} AS SELECT * FROM {first_table} INNER JOIN {unique_id} {first_table}.{unique_id} <> {second_table}.{unique_id}')
        # self.database.execute(f'''CREATE VIEW IF NOT EXISTS {table_name} AS SELECT * FROM {first_table} INNER JOIN {unique_id} {first_table}.{unique_id} <> {second_table}.{unique_id}''')

    def commit_and_close(self):
        request = input('Save the database? ')
        if request.upper() == 'YES':
            self.database.commit()
            self.database.close()
