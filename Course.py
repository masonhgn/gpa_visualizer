
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

    def print_course(self):
        #print ("{:<8} {:<15} {:<10} {:<10}".format('Pos','Lang','Percent','Change'))
        print("{:<15} {:<35} {:<6} {:>6}".format(self.code, self.title, self.grade_spec, self.course_units, self.gpa_units))

