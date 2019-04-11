"""
@author: Vaibhav Vishnu Shanbhag
@homework: HW 05
@date: 03/24/2019
@time: 08:29:11 PM
This code is to practice the date time module, comma seperated files, and scanning directories
"""

import datetime as d
import os
from prettytable import PrettyTable
import unittest
import numpy as np

def date_time():
    date_1 = d.date(2000, 2, 27)
    date_2 = d.date(2017, 2, 27)
    add_days = d.timedelta(3)
    new_day_1 = date_1 + add_days
    print(new_day_1.strftime("%b %d, %Y"))
    new_day_2 = date_2 + add_days
    print(new_day_2.strftime("%b %d, %Y"))
    date_3 = d.date(2017, 1, 1)
    date_4 = d.date(2017, 10, 31)
    new_date = date_4 - date_3
    return new_date

def file_reader(path, num_field,  sep, header=False):
    #path = r"C:\Users\shanb\PycharmProjects\ 810 SSW\file.txt"
    """ Open the file path safely """
    try:
        fp = open(path, 'r')
    except FileNotFoundError:
        #raise e
        print("Cant' open {} not found".format(path))
    else:
        with fp:
            lines = fp.readlines()
            for i, line in enumerate(lines):
                field = line.rstrip("\n").split(sep)
                if len(field) == num_field:
                    if header == True and i == 0:
                        """ The continue will continue to next line and skip the first line if its a header"""
                        continue
                    else:
                        yield (tuple(field))
                else:
                    raise ValueError("{} has {} fields but on line {} expected {}".format(path,
                                                                                          len(field), i, num_field))

def scan_directories(ditr, ext):
    """ ditr is the input for the directory path and ext is the extension"""
    list_of_dir = os.listdir(ditr)
    file_name = []
    for i in list_of_dir:
        if i.endswith(ext):
            file_name.append(i)
    file = []
    for i in file_name:
        file.append(os.path.join(ditr, i))

    ch = []
    ln = []
    cl = []
    func = []
    for f in file:
        infile = open(f, 'r')
        with infile:
            cls = 0
            function = 0
            lines = 0
            words = 0
            characters = 0
            for line in infile:
                wordslist = line.split()
                lines += 1
                words += len(wordslist)
                characters += len(line)
                if line.strip().startswith('def ') and line.strip().endswith(':'):
                    function += 1
                if line.strip().startswith('class ') and line.strip().endswith(':'):
                    cls += 1
            func.append(function)
            ch.append(characters)
            ln.append(lines)
            cl.append(cls)

    list_of_files = list(zip(file, cl, func, ln, ch))
    return list_of_files

def print_pretty_table(ditr, ext):
    if os.path.exists(ditr) == True:
        table_list = scan_directories(ditr, ext)
        pt = PrettyTable(field_names=['File Name', 'Classes', 'Function', 'Lines', 'Characters'])
        for fn, cl, func, ln, ch in table_list:
            pt.add_row([fn, cl, func, ln, ch])
        print(pt)
    else:
        raise NotADirectoryError(f"{ditr} does not exist")

""" The first two files are the ones which are uploaded on canvas according to my logic matches the given criteria """
class ScanDirectory(unittest.TestCase):
    def test_scan_directory(self):
        ditr = r"C:\Users\shanb\PycharmProjects\ 810 SSW"
        ext = '.py'
        expected = [('C:\\Users\\shanb\\PycharmProjects\\ 810 SSW\\0_defs_in_this_file.py', 0, 0, 3, 57),
                    ('C:\\Users\\shanb\\PycharmProjects\\ 810 SSW\\file1.py', 2, 4, 25, 270),
                    ('C:\\Users\\shanb\\PycharmProjects\\ 810 SSW\\hello.py', 0, 1, 23, 479),
                    ('C:\\Users\\shanb\\PycharmProjects\\ 810 SSW\\hgfdfghj.py', 0, 1, 5, 47),
                    ('C:\\Users\\shanb\\PycharmProjects\\ 810 SSW\\Homework04_Vaibhav.py', 3, 6, 68, 1890),
                    ('C:\\Users\\shanb\\PycharmProjects\\ 810 SSW\\Homework05-Vaibhav.py', 4, 8, 106, 3339),
                    ('C:\\Users\\shanb\\PycharmProjects\\ 810 SSW\\Homework1.py', 0, 5, 97, 3018),
                    ('C:\\Users\\shanb\\PycharmProjects\\ 810 SSW\\Homework2.py', 1, 11, 99, 2490),
                    ('C:\\Users\\shanb\\PycharmProjects\\ 810 SSW\\Homework3_Vaibhav.py', 2, 22, 258, 8854),
                    ('C:\\Users\\shanb\\PycharmProjects\\ 810 SSW\\Homework_06_Vaibhav.py', 5, 11, 167, 6110),
                    ('C:\\Users\\shanb\\PycharmProjects\\ 810 SSW\\Homework_07_Vaibhav.py', 5, 10, 104, 4783),
                    ('C:\\Users\\shanb\\PycharmProjects\\ 810 SSW\\Homework_08_Vaibhav.py', 2, 6, 142, 5732)]

        self.assertEqual(scan_directories(ditr, ext), expected)

class FileReader(unittest.TestCase):
    def test_file_reader(self):
        wow = []
        for name, cwid, major in file_reader("file.txt", 3, sep='|', header=True):
            wow.append(["name: {} cwid: {} major: {}".format(name, cwid, major)])

        expected = [['name: Vaibhav cwid: 10433151 major: MIS'],
                    ['name: Karan cwid: 10433152 major: MIS'],
                    ['name: Ronak cwid: 10433153 major: MIS'],
                    ['name: Sam cwid: 10433154 major: CS'],
                    ['name: Samuel cwid: 10433155 major: CS'],
                    ['name: Joey cwid: 10433156 major: EM']]
        self.assertEqual(wow, expected)

if __name__ == '__main__':
    print(date_time())
    print_pretty_table(ditr=input("Please enter the directory:"), ext=input("Please enter the extension:"))
    print()
    unittest.main(exit=False, verbosity=2)



