import os
from collections import defaultdict
from prettytable import PrettyTable
import unittest
import sqlite3


def file_reader(path, num_field, sep, header=False):
    """ Open the file path safely """
    try:
        fp = open(path, 'r', encoding="utf-8")
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
                    raise ValueError("{} has {} fields but on line {} expected {}".format(path, len(field), i, num_field))


class Student():
    """Class for student summary"""

    def __init__(self, cwid, name, major, major_details):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.major_details = major_details
        self.courses = dict()

    def add_course(self, course, grade):
        grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
        if grade in grades:
            self.courses[course] = grade  # key as course and value as grade

    def details(self):
        """return summary in prettytable for single student"""
        completed_courses, remaining_courses, remaining_electives = self.major_details.check_grades(self.courses)
        return [self.cwid, self.name, self.major, sorted(self.courses.keys()), remaining_courses, remaining_electives]#sorted(completed_courses),

    @staticmethod
    def fields():
        return ['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives']


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

    """Static method will have no self in it but will be used with diffrent functions"""
    @staticmethod
    def fields():
        return ['CWID', 'Name', 'Dept', 'Course', 'Student']


class Major:
    """Class for the majors summary"""

    def __init__(self, major, result=None):
        self.major = major
        self.required = set()
        """I have taken set because the table has set of required and elective"""
        self.elective = set()
        #self.passing_grades = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}
        if result is None:
            """ Stduent wants to know the passing grades and I have stored it in the major in a set """
            self.passing_grades = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}
        else:
            self.passing_grades = result

    def add_course(self, flag, course):
        if flag == 'R':
            self.required.add(course)
        elif flag == 'E':
            self.elective.add(course)
        else:
            raise ValueError(f"Wrong {flag} Flag")

    def check_grades(self, courses):
        """ I am storing the list of completed courses for comaprison, if the student fails then 
        that particular course would not be added to the list"""
        completed_courses = {c for c, g in courses.items() if g in self.passing_grades}

        if completed_courses == None:
            return [completed_courses, self.required, self.elective]
        else:
            remaining_courses = self.required - completed_courses
            if self.elective.intersection(completed_courses):
                remaining_electives = None
            else:
                remaining_electives = self.elective

            return [completed_courses, remaining_courses, remaining_electives]

    def details(self):
        return [self.major, self.required, self.elective]

    @staticmethod
    def fields():
        return ['Dept', 'Required', 'Electives']


class Respository:
    def __init__(self, dir_path, print_table=False):
        self.dir_path = dir_path
        self.students = dict()      # key as cwid and value as students instance
        self.instructors = dict()   # key as cwid and value as instructor instance
        self.majors = dict()        # key as major and value as major instance
        """os.path.join will join all the txt files mentioned with the directory directory path"""
        self.addmajors(os.path.join(dir_path, 'majors.txt'))
        self.addstudents(os.path.join(dir_path, 'students.txt'))
        self.addinstructors(os.path.join(dir_path, 'instructors.txt'))
        self.addgrades(os.path.join(dir_path, 'grades.txt'))

        if print_table == True:
            self.student_pt()
            # self.instructor_pt()
            self.major_pt()
            self.instructor_pt_db()

    def addstudents(self, path):
        for cwid, name, major in file_reader(path, 3, sep='\t', header=False):
            if cwid in self.students:
                print(f"{cwid} already exists")
            else:
                self.students[cwid] = Student(cwid, name, major, self.majors[major])

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

    def addmajors(self, path):
        for major, flag, course in file_reader(path, 3, sep='\t', header=False):
            if major in self.majors:
                self.majors[major].add_course(flag, course)
            else:
                """ If major is new it will call the major class summary for new major"""
                self.majors[major] = Major(major)
                """ And after the major is added it will 
                    add the required courses and electives to complete the each major instances"""
                self.majors[major].add_course(flag, course)

    def major_pt(self):
        pt = PrettyTable(field_names=Major.fields())
        for major in self.majors.values():
            pt.add_row(major.details())
        print("Major Summary")
        print(pt)

    def student_pt(self):
        pt = PrettyTable(field_names=Student.fields())
        for s in self.students.values():
            pt.add_row(s.details())
        print("Student Summary")
        print(pt)

    # def instructor_pt(self):
    #     pt = PrettyTable(field_names=Instructor.fields())
    #     for instructor in self.instructors.values():
    #         for c in instructor.details():
    #             pt.add_row(c)
    #     print("Instructor Summary")
    #     print(pt)

    def instructor_pt_db(self):
        DB_file = "C:\\Users\\shanb\\Database\\810_startup.db"

        db = sqlite3.connect(DB_file)

        query = """SELECT I.CWID, I.Name, I.Dept, G.Course, COUNT(G.Student_CWID) Students
                    FROM HW11_instructors I
                    LEFT JOIN HW11_grades G ON  I.CWID = G.Instructor_CWID
                GROUP BY G.COURSE
                ORDER BY COUNT(G.Student_CWID) DESC;"""

        pt = PrettyTable(field_names=Instructor.fields())
        for c in db.execute(query):
            pt.add_row(c)
        print("Instructor Summary")
        print(pt)


def main():
    dir_path = 'C:\\Users\\shanb\\PycharmProjects\\810_SSW'
    Respository(dir_path, True)



class FileRepository(unittest.TestCase):
    def test_repository(self):
        dir_path = 'C:\\Users\\shanb\\PycharmProjects\\810_SSW'
        stevens = Respository(dir_path)
        student_expected = []
        instructor_expected = []
        major_expected = []
        for s in stevens.students.values():
            student_expected.append(s.details())

        for instructor in stevens.instructors.values():
            for c in instructor.details():
                instructor_expected.append(c)
        
        for major in stevens.majors.values():
            major_expected.append(major.details())
        

        student_pt = [["10103", "Baldwin, C", "SFEN", ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], {'SSW 555', 'SSW 540'}, None],
                        ["10115", "Wyatt, X", "SFEN", ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], {'SSW 555', 'SSW 540'}, None],
                        ["10172", "Forbes, I", "SFEN", ['SSW 555', 'SSW 567'], {'SSW 564', 'SSW 540'}, {'CS 545', 'CS 501', 'CS 513'}],
                        ["10175", "Erickson, D", "SFEN", ['SSW 564', 'SSW 567', 'SSW 687'], {'SSW 555', 'SSW 540'}, {'CS 545', 'CS 501', 'CS 513'}],
                        ["10183", "Chapman, O", "SFEN", ['SSW 689'], {'SSW 567', 'SSW 555', 'SSW 564', 'SSW 540'}, {'CS 545', 'CS 501', 'CS 513'}],
                        ["11399", "Cordova, I", "SYEN", ['SSW 540'], {'SYS 612', 'SYS 800', 'SYS 671'}, None],
                        ["11461", "Wright, U", "SYEN", ['SYS 611', 'SYS 750', 'SYS 800'], {'SYS 671', 'SYS 612'}, {'SSW 565', 'SSW 540', 'SSW 810'}],
                        ["11658", "Kelly, P", "SYEN", [], {'SYS 800', 'SYS 612', 'SYS 671'}, {'SSW 565', 'SSW 540', 'SSW 810'}],
                        ["11714", "Morton, A", "SYEN", ['SYS 611', 'SYS 645'], {'SYS 671', 'SYS 612', 'SYS 800'}, {'SSW 565', 'SSW 540', 'SSW 810'}],
                        ["11788", "Fuller, E", "SYEN", ['SSW 540'], {'SYS 671', 'SYS 612', 'SYS 800'}, None]]

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

        major_pt = [["SFEN", {'SSW 540', 'SSW 564', 'SSW 567', 'SSW 555'}, {'CS 545', 'CS 501', 'CS 513'}], 
                     ["SYEN", {'SYS 612', 'SYS 800', 'SYS 671'}, {'SSW 810', 'SSW 565', 'SSW 540'}]]
        self.assertEqual(student_pt, student_expected)
        self.assertEqual(instructor_pt, instructor_expected)
        self.assertEqual(major_pt, major_expected)


if __name__ == '__main__':
    main()
    # unittest.main(exit=False, verbosity=2)
