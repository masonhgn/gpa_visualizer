import pandas as pd

class Course:
    def __init__(self, semester, code, title, grade, grade_spec, course_units, gpa_units, gpa_points):
        self.semester = semester
        self.code = code
        self.title = title
        self.grade = grade
        self.grade_spec = grade_spec
        self.course_units = course_units
        self.gpa_units = gpa_units
        self.gpa_points = gpa_points

    def __str__(self):
        return f"{self.semester}\t{self.code}\t{self.title}\t{self.grade}\t{self.grade_spec}\t{self.course_units}\t{self.gpa_units}\t{self.gpa_points}"





class Semester:
    def __init__(self, semester_period, term_gpa, cum_gpa,courses=[]):
        self.num_courses = num_courses
        self.semester_period = semester_period
        self.term_gpa = term_gpa
        self.cum_gpa = cum_gpa

    def add_course(self, course):
        self.courses.append(course)

    def get_courses(self):
        return self.courses
 
    def get_semester_period(self):
        return self.semester_period
    
    def get_term_gpa(self):
        return self.term_gpa

    def get_cum_gpa(self):
        return self.cum_gpa


class Transcript:
    def __init__(self, semesters=[], gpa=0,total_courses=0):
        self.gpa = gpa
        self.total_courses = total_courses

    def add_semester(self, semester):
        self.semesters.append(semester)
