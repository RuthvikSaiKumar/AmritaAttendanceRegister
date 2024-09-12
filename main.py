import pickle

data = []


def add_student(reg, name):
    data.append([reg, name])


def save_to_file(file_name):
    pickle.dump(data, open(file_name, 'wb'))


def load_from_file(file_name):
    global data
    data = pickle.load(open('students.txt', 'rb'))


students = int(input('Enter number of students: '))

#
# for i in range(students):
#     student_reg, student_name = input('Enter REG and Name').split()
#
#     data.append([student_reg, student_name])
#
# pickle.dump(data, open('students.txt', 'wb'))

data = pickle.load(open('students.txt', 'rb'))

print(data)
