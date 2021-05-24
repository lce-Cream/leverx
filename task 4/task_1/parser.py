import json
import argparse
import sys
from dicttoxml import dicttoxml
from collections import defaultdict


class OpenFile:
    ''' Context manager which handles exceptions '''
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


class File:
    _FORMAT_TYPES = ('json', 'xml')

    def __init__(self, destination: str):
        self.destination = destination.lower()
        self.extension = destination.split('.')[-1]

        if self.extension not in self._FORMAT_TYPES:
            raise NotImplementedError(f'{self.extension} handling is not yet implemented')


class JsonFile(File):
    extension = '.json'
    def __init__(self, destination: str):
        super().__init__(destination)
        if self.extension != 'json':
            raise TypeError(f'{self.destination} is not a json file')

    def read(self):
        with OpenFile(self.destination) as file:
            return json.load(file)

    def write(self, data):
        with OpenFile(self.destination, 'w') as file:
            json.dump(data, file, indent=3)

    @staticmethod
    def merge(first, second):
        '''Merges two json files'''
        students_json = first.read()
        rooms_json = second.read()
        students_by_rooms = defaultdict(list)
        output = {}

        for student in students_json:
            student_room = student['room']
            student_name = student['name']
            students_by_rooms[student_room].append(student_name)

        for room_id in students_by_rooms:
            room = rooms_json[room_id]
            output[str(room['id'])] = {'room': room['name'], 'students': students_by_rooms[room_id]}
        return output


class XmlFile(File):
    extension = '.xml'
    def __init__(self, destination: str):
        super().__init__(destination)
        if self.extension != 'xml':
            raise TypeError(f'{self.destination} is not a xml file')

    def read(self):
        raise NotImplemented('this function is not implemented yet')

    def write(self, data):
        with OpenFile(self.destination, 'w') as file:
            file.write(dicttoxml(data).decode())


class Parser:
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
                            metavar='type', default='json', choices=File._FORMAT_TYPES)

        return parser.parse_args()


if __name__ == '__main__':
    args = Parser.parse()
    students, rooms, format = args.students, args.rooms, args.format

    students_file = JsonFile(students)
    rooms_file = JsonFile(rooms)
    merged = JsonFile.merge(students_file, rooms_file)

    extension_class_map = {ex: cls for ex, cls in zip(File._FORMAT_TYPES, File.__subclasses__())}
    output = extension_class_map[format](f'output.{format}')
    output.write(merged)
