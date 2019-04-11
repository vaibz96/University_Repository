import os
from collections import defaultdict
from prettytable import PrettyTable
import unittest


def file_reader(path, num_field, sep, header=False):
    """ Open the file path safely """
    try:
        fp = open(path, 'r')
    except FileNotFoundError:
        raise ValueError("Cant' open, {} not found".format(path))
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
                        yield field
                else:
                    raise ValueError("{} has {} fields but on line {} expected {}".format(path,
                                                                                          len(field), i, num_field))


class Student():
    """Class for student summary"""

    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.courses = dict()

    def add_course(self, course, grade):
        self.courses[course] = grade  # key as course and value as grade

    def details(self):
        """return summary in prettytable for single student"""
        return [self.cwid, self.name, sorted(self.courses.keys())]

    @staticmethod
    def fields():
        return ['CWID', 'Name', 'Courses']


class Instructor:
    """Class for instructor summary"""

    def __init__(self, cwid, name, dept):
        self.cwid = cwid
        self.name = name
        self.dept = dept
        # key as course and value as incremented value
        self.courses = defaultdict(int)

    def add_course(self, course):
        self.courses[course] += 1

    def details(self):
        for course, student in self.courses.items():
            """ yield will return single value"""
            yield [self.cwid, self.name, self.dept, course, student]

    @staticmethod
    def fields():
        return ['CWID', 'Name', 'Dept', 'Course', 'Student']


class Respository:
    def __init__(self, dir_path, print_table=False):
        self.dir_path = dir_path
        self.students = dict()      # key as cwid and value as students instance 
        self.instructors = dict()   # key as cwid and value as instructor instance
        self.addstudents(os.path.join(dir_path, 'students.txt'))
        self.addinstructors(os.path.join(dir_path, 'instructors.txt'))
        self.addgrades(os.path.join(dir_path, 'grades.txt'))

        if print_table == True:
            self.student_pt()
            self.instructor_pt()

    def addstudents(self, path):
        for cwid, name, major in file_reader(path, 3, sep='\t', header=False):
            if cwid in self.students:
                print(f"{cwid} already exists")
            else:
                self.students[cwid] = Student(cwid, name, major)

    def addinstructors(self, path):
        for cwid, name, dept in file_reader(path, 3, sep='\t', header=False):
            if cwid in self.instructors:
                print(f"{cwid} already exists")
            else:
                self.instructors[cwid] = Instructor(cwid, name, dept)

    def addgrades(self, path):
        for scwid, course, grade, icwid in file_reader(path, 4, sep='\t', header=False):
            self.students[scwid].add_course(course, grade)
            self.instructors[icwid].add_course(course)

    def student_pt(self):
        pt = PrettyTable(field_names=Student.fields())
        for s in self.students.values():
            pt.add_row(s.details())
        print("Student Summary")
        print(pt)

    def instructor_pt(self):
        pt = PrettyTable(field_names=Instructor.fields())
        for instructor in self.instructors.values():
            for c in instructor.details():
                pt.add_row(c)
        print("Instructor Summary")
        print(pt)


def main():
    dir_path = 'C:\\Users\\shanb\\PycharmProjects\\ 810 SSW'
    Respository(dir_path, True)

class FileRepository(unittest.TestCase):
    def test_repository(self):
        dir_path = 'C:\\Users\\shanb\\PycharmProjects\\ 810 SSW'
        stevens = Respository(dir_path)
        student_expected = []
        instructor_expected = []
        for s in stevens.students.values():
            student_expected.append(s.details())

        for instructor in stevens.instructors.values():
            for c in instructor.details():
                instructor_expected.append(c)

        student_pt = [['10103', 'Baldwin, C', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687']], 
                      ['10115', 'Wyatt, X', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687']], 
                      ['10172', 'Forbes, I', ['SSW 555', 'SSW 567']], 
                      ['10175', 'Erickson, D', ['SSW 564', 'SSW 567', 'SSW 687']], 
                      ['10183', 'Chapman, O', ['SSW 689']], 
                      ['11399', 'Cordova, I', ['SSW 540']], 
                      ['11461', 'Wright, U', ['SYS 611', 'SYS 750', 'SYS 800']], 
                      ['11658', 'Kelly, P', ['SSW 540']], 
                      ['11714', 'Morton, A', ['SYS 611', 'SYS 645']], 
                      ['11788', 'Fuller, E', ['SSW 540']]]
        
        instructor_pt = [['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4], 
                         ['98765', 'Einstein, A', 'SFEN', 'SSW 540', 3], 
                         ['98764', 'Feynman, R', 'SFEN', 'SSW 564', 3], 
                         ['98764', 'Feynman, R', 'SFEN', 'SSW 687', 3], 
                         ['98764', 'Feynman, R', 'SFEN', 'CS 501', 1], 
                         ['98764', 'Feynman, R', 'SFEN', 'CS 545', 1], 
                         ['98763', 'Newton, I', 'SFEN', 'SSW 555', 1], 
                         ['98763', 'Newton, I', 'SFEN', 'SSW 689', 1], 
                         ['98760', 'Darwin, C', 'SYEN', 'SYS 800', 1], 
                         ['98760', 'Darwin, C', 'SYEN', 'SYS 750', 1], 
                         ['98760', 'Darwin, C', 'SYEN', 'SYS 611', 2], 
                         ['98760', 'Darwin, C', 'SYEN', 'SYS 645', 1]] 

        self.assertEqual(student_pt, student_expected)
        self.assertEqual(instructor_pt, instructor_expected)


if __name__ == '__main__':
    main()
    unittest.main(exit=False, verbosity=2)
