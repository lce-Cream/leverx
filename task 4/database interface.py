import mysql.connector as connector
from task_1.parser import (JsonFile, XmlFile, Parser)


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
    tables = {}

    tables['rooms'] = \
        '''
        CREATE TABLE rooms(
        id INT PRIMARY KEY,
        name VARCHAR(50)
        )
        '''

    tables['students'] = \
        '''
        CREATE TABLE students(
        birthday DATE,
        id INT PRIMARY KEY,
        name VARCHAR(50),
        room_id INT,
        sex CHARACTER,
        CHECK(sex in ('M', 'F')),
        FOREIGN KEY (room_id) REFERENCES rooms(id)
        )
        '''

    queries = [
            (   # - список комнат и количество студентов в каждой из них
                '''
                SELECT name, students
                FROM 
                    (SELECT room_id, COUNT(name) 'students'
                    FROM students
                    GROUP BY room_id
                    ) as room_id__students
                JOIN rooms ON room_id__students.room_id = rooms.id;
                ''',
                'rooms by students'
            ),
            (   # - top 5 комнат, где самые маленький средний возраст студентов
                '''
                SELECT room_id, floor(avg(year(curdate()) - year(birthday))) AS average_age
                FROM students
                GROUP BY room_id
                ORDER BY average_age LIMIT 5;
                ''',
                'top 5 rooms with the least average age'
            ),
            (   # - top 5 комнат с самой большой разницей в возрасте студентов
                '''
                SELECT room_id, std(birthday) as deviation
                FROM students
                GROUP BY room_id
                ORDER BY deviation DESC LIMIT 5;
                ''',
                'top 5 rooms with the most varience in age'
            ),
            (   # - список комнат где живут разнополые студенты
                '''
                SELECT name FROM
                (
                SELECT distinct males.room_id
                    FROM (SELECT room_id FROM students WHERE sex='M') AS males
                    JOIN (SELECT room_id FROM students WHERE sex='F') AS females
                    ON males.room_id = females.room_id
                ) AS intersex_rooms
                JOIN rooms ON rooms.id = intersex_rooms.room_id;
                ''',
                'rooms with intersex students'
            )
        ]

    config = {
        'host': 'localhost',
        'user': 'user',
        'password': 'user',
        'database': 'dbase',
        }

    args = Parser.parse()
    students_filename, rooms_filename, output_format = args.students, args.rooms, args.format

    db = Database(config)
    db.create_tables(tables)
    db.fill_table(rooms_filename, 'rooms')
    db.fill_table(students_filename, 'students')

    # да да костыль, но путь назад уже слишком длинный
    extension_class_dict = {'json': JsonFile, 'xml': XmlFile}

    for query in queries:
        db.excute_query_to_file(query[0], query[1], extension_class_dict[output_format])

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






