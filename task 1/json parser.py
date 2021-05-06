import json
import argparse
import sys
from dicttoxml import dicttoxml
from collections import defaultdict

FORMAT_TYPES = ('json', 'xml')


def parse():
    """
    Returns dictionary like object with parsed arguments from terminal
    """
    parser = argparse.ArgumentParser(description='merge two json files into one with students grouped by rooms')

    parser.add_argument('-s', '--students', help='json file containing students',
                        metavar='path', default='students.json')

    parser.add_argument('-r', '--rooms', help='json file containing rooms',
                        metavar='path', default='rooms.json')

    parser.add_argument('-f', '--format', help='output file extension',
                        metavar='type', default='json', choices=FORMAT_TYPES)

    return vars(parser.parse_args())


class open_file:
    """
    Context manager which handles exceptions
    """
    def __init__(self, path, mode='r'):
        try:
            self.file = open(path, mode)
        except FileNotFoundError as error:
            print(error)
            sys.exit(1)
        except Exception as error:
            print(error)
            sys.exit(1)

    def __enter__(self):
        return self.file

    def __exit__(self, *exc_info):
        self.file.close()


def merge(students, rooms):
    """
    Returns dictionary of the merged files
    """
    with open_file(students) as students_file:
        students_json = json.load(students_file)

        students_by_rooms = defaultdict(list)
        # take every student, then make a dictionary with their room id as a key and append to value every student
        # from this room
        for student in students_json:
            student_room = student['room']
            student_name = student['name']
            students_by_rooms[student_room].append(student_name)

    with open_file(rooms) as rooms_file:
        rooms_json = json.load(rooms_file)
        output = {}
        # make a dictionary where room id is a key and value is another dictionary containing room name and a list of
        # students in this room and yeah, it will only work properly if rooms_json is sorted so room_id in 'for'
        # matches actual room id
        for room_id in students_by_rooms:
            room = rooms_json[room_id]
            output[str(room['id'])] = {'room': room['name'], 'students': students_by_rooms[room_id]}
    return output


def write_output(output, format):
    """
    Writes output with specified file format
    """
    with open_file(f'output.{format}', 'w') as output_file:
        if format == 'json':
            json.dump(output, output_file, indent=3)
        elif format == 'xml':
            xml = dicttoxml(output)
            output_file.write(xml.decode())
        else:
            print(f'unsupported format: {format}')
            sys.exit(1)


if __name__ == '__main__':
    args = parse()
    students_json, rooms_json, format = args['students'], args['rooms'], args['format']
    output = merge(students_json, rooms_json)
    write_output(output, format)
