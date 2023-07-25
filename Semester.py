import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from Course import *


grade_weights = {
    'A':4,
    'A-':3.75,
    'B+':3.25,
    'B':3,
    'B-':2.75,
    'C+':2.25,
    'C':2,
    'C-':1.75,
    'D+':1.25,
    'D':1,
    'D-':0.75,
    'F':0,
    'W':0,
    'I':0,
    'S':0
}


class Semester:
    def __init__(self, semester_period, term_gpa=0, cum_gpa=0, total_gpa_points=0, total_gpa_units=0, courses=None):
        self.semester_period = semester_period
        self.total_gpa_points = total_gpa_points
        self.total_gpa_units = total_gpa_units
        self.term_gpa = term_gpa
        self.cum_gpa = cum_gpa
        self.courses = courses if courses is not None else []

    def __str__(self):
            courses_str = "\n".join(str(course) for course in self.courses)
            return f"{self.semester_period}\t{self.term_gpa}\n{courses_str}"

    def print_semester(self):
        print(self.semester_period)
        print("Term GPA: ",self.term_gpa)
        print("Cum GPA: ",self.cum_gpa)
        for c in self.courses:
            c.print_course()
        print()

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

    def calculate_term_gpa(self):
        total_score, total_units = 0, 0
        for c in self.courses:
            total_score += grade_weights[c.grade_spec] * c.course_units
            total_units += c.gpa_units if c.grade_spec != 'S' else 0
        self.total_gpa_points = total_score
        self.total_gpa_units = total_units
        total_score /= total_units

        self.term_gpa = total_score