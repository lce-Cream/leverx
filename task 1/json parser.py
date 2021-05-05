import json, argparse, sys
from collections import defaultdict

parser = argparse.ArgumentParser(description='merge two json files into one with students grouped by rooms')
parser.add_argument('-s', '--students', required=False, help='json file containing students', metavar='path',  default='./students.json')
parser.add_argument('-r', '--rooms',    required=False, help='json file containing rooms', 	  metavar='path',  default='./rooms.json')
parser.add_argument('-f', '--format', 	required=False, help='output json file', 			  metavar='path',  default='./format.json')

args = vars(parser.parse_args())
students_json, rooms_json, format_json = args['students'], args['rooms'], args['format']

try:
	with open(students_json) as file:
		students_json = json.load(file)

		students_by_rooms = defaultdict(list)
		# take every student, then make a dictionary with their room id as a key and append to value every student from this room
		for student in students_json:
			student_room = student['room']
			student_name = student['name']
			students_by_rooms[student_room].append(student_name)

except FileNotFoundError as error:
	print(error)
	sys.exit(1)

except Exception as error:
	print(error)
	sys.exit(1)


try:
	with open(rooms_json) as file:
		rooms_json = json.load(file)

		format = {}
		# make a dictionary where room id is a key and value is another dictionary containing room name and a list of students in this room
		# and yeah, it will only work properly if rooms_json is sorted so room_id in 'for' matches actual room id
		for room_id in students_by_rooms:
			room = rooms_json[room_id]
			format[room['id']] = {'room': room['name'], 'students': students_by_rooms[room_id]}

except FileNotFoundError as error:
	print(error)
	sys.exit(1)

except Exception as error:
	print(error)
	sys.exit(1)


with open(format_json, 'w') as file:
	json.dump(format, file, indent=3)