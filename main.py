import pickle
import fpdf
import pandas as pd

data = []


def add_student(reg, name):
    data.append([reg, name])


def save_to_file(file_name):
    pickle.dump(data, open(file_name, 'wb'))


def load_from_file(file_name):
    global data
    data = pickle.load(open('students.txt', 'rb'))
