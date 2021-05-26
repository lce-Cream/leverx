import mysql.connector as connector
from myparser import (File, JsonFile, Parser)
import config


class Database:
    def __init__(self, config):
        self.config = config
        self.tables = []

        try:
            self.connection = connector.connect(**config)
            self.cursor = self.connection.cursor()
        except connector.Error as err:
            if err.errno == connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print('Wrong username or password')
            elif err.errno == connector.errorcode.ER_BAD_DB_ERROR:
                print('Database does not exist')
            else:
                print(err)
        else:
            database_name = self.config['database']
            print(f'Database {database_name} connected successfully')
            self.cursor.execute('SHOW TABLES')
            self.tables = [table[0] for table in self.cursor.fetchall()]

    def create_tables(self, tables):
        for table_name in tables:
            self.tables.append(table_name)
            table_description = tables[table_name]
            try:
                print(f'Creating table {table_name}: ', end='')
                self.cursor.execute(table_description)
            except connector.Error as err:
                if err.errno == connector.errorcode.ER_TABLE_EXISTS_ERROR:
                    print('already exists.')
                else:
                    self.connection.rollback()        
                    print(err.msg)
            else:
                print('OK')

    def fill_table(self, file_name, table_name):
        data = JsonFile(file_name).read()
        columns = len(data[0].keys())
        insert_data = f'INSERT INTO {table_name} VALUES(%s' + ', %s'*(columns-1) + ')'

        # I'm not sure I should use threads in this input operation
        try:
            print(f'Filling table {table_name} with data from {file_name}: ', end='')
            self.cursor.executemany(insert_data, map(lambda row: row.values(), data))
        except connector.Error as err:
            print(err)
            self.connection.rollback()
        else:
            print('OK')
            self.connection.commit()

    def excute_query_to_file(self, query, query_name, FileClass):
        try:
            self.cursor.execute(query)
        except connector.Error as err:
            print(err)
        else:
            result = self.cursor.fetchall()
            FileClass(query_name+FileClass.extension).write(result)

    def __del__(self):
        self.connection.disconnect()


if __name__ == '__main__':
    args = Parser.parse()
    students_filename, rooms_filename, output_format = args.students,
                                                       args.rooms,
                                                       args.format

    db = Database(config.config)
    db.create_tables(config.tables)
    db.fill_table(rooms_filename, 'rooms')
    db.fill_table(students_filename, 'students')

    for query in config.queries:
        db.excute_query_to_file(query[0], query[1], File.get_class_by_format(output_format))

    # - Предложить варианты оптимизации запросов с использования индексов
    # - в результате надо сгенерировать SQL запрос который добавить нужные индексы
    '''
    Indexes are automatically created when PRIMARY KEY constraint is defined on table column.
    If you configure a PRIMARY KEY, Database Engine automatically creates a clustered index, unless a clustered index already exists.
    When you try to enforce a PRIMARY KEY constraint on an existing table and a clustered index already exists on that table,
    SQL Server enforces the primary key using a nonclustered index.
    (https://docs.microsoft.com/en-us/sql/relational-databases/indexes/clustered-and-nonclustered-indexes-described?view=sql-server-ver15#indexes-and-constraints)
    Since I've set PRIMARY KEY when tables where created, clustered index is applyed for them already.
    If it wasn't here's SQL code for adding index:
        CREATE INDEX index_name
        ON table_name (column_name);
    As I frequently perform join operation between the tables on the room_id field, thus
    it makes sense to create a nonclustered index in the students table by the room_id field.
    '''






