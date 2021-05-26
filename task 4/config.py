config = {
    'host': 'localhost',
    'user': 'user',
    'password': 'user',
    'database': 'dbase',
    }

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
