
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import jinja2

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




class Transcript:
    def __init__(self, semesters=[], gpa=0,total_courses=0):
        self.gpa = gpa
        self.total_courses = total_courses
        self.semesters = semesters

    def print_transcript(self):
        for s in self.semesters:
            s.print_semester()

    def add_semester(self, semester):
        self.semesters.append(semester)

    def load_from_csv(self, file_name):
        df = pd.read_csv(file_name)

        for index, row in df.iterrows():
            semester = row['Semester']
            code = row['Class Code']
            title = row['Class Name']
            grade = row['Grade']
            grade_spec = row['Grade Specification']
            course_units = row['Course Units']
            gpa_units = row['GPA Units']
            gpa_points = row['GPA Points Earned']

            temp_course = Course(semester, code, title, grade, grade_spec, course_units, gpa_units, gpa_points)

            found_semester = False
            for existing_semester in self.semesters:
                if existing_semester.semester_period == semester:
                    existing_semester.add_course(temp_course)
                    found_semester = True
                    break

            if not found_semester:
                new_semester = Semester(semester)
                new_semester.add_course(temp_course)
                self.add_semester(new_semester)


        total_units, total_points = 0,0
        for s in self.semesters: #calculate every term gpa
            s.calculate_term_gpa()
            total_units += s.total_gpa_units
            total_points += s.total_gpa_points
            s.cum_gpa = total_points / total_units
    
    def calculate_cum_gpa(self):
        for s in self.semesters:
            total_score += s.total_gpa_points
            total_units += s.total_gpa_units

        self.gpa = total_score/total_units


    def generate_dataframe(self):
        transcript_data = []
        cum_gpa_points = 0
        cum_gpa_units = 0

        for semester in self.semesters:
            term_gpa = semester.term_gpa
            cum_gpa_points += semester.total_gpa_points
            cum_gpa_units += semester.total_gpa_units
            cum_gpa = cum_gpa_points / cum_gpa_units if cum_gpa_units != 0 else 0

            transcript_data.append({
                "Semester": semester.semester_period,
                "Term GPA": term_gpa,
                "Cumulative GPA Points": cum_gpa_points,
                "Cumulative GPA Units": cum_gpa_units,
                "Cumulative GPA": cum_gpa
            })

        return pd.DataFrame(transcript_data)

    

    def generate_gpa_charts(self):
# Extracting data for GPA charts
        semester_periods = [semester.semester_period for semester in self.semesters]
        term_gpas = [semester.term_gpa for semester in self.semesters]
        cum_gpas = [semester.cum_gpa for semester in self.semesters]
        cum_gpa_points = [semester.total_gpa_points for semester in self.semesters]
        cum_gpa_units = [semester.total_gpa_units for semester in self.semesters]

        # Creating a DataFrame for GPA data
        gpa_data = pd.DataFrame({
            'Semester': semester_periods,
            'Term GPA': term_gpas,
            'Cumulative GPA': cum_gpas,
            'Cumulative GPA Points': cum_gpa_points,
            'Cumulative GPA Units': cum_gpa_units
        })

        # Generating line plots for each GPA metric
        sns.set(style="dark", palette="deep", font_scale=3.0)
        plt.figure(figsize=(24, 6))

        # Line plot for Term GPA
        sns.lineplot(x="Semester", y="Term GPA", data=gpa_data, marker='o', color='green', label='Term GPA')

        # Styling the Term GPA plot
        plt.xlabel("Semester")
        plt.ylabel("GPA")
        plt.title("Term GPA")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()

        # Saving the Term GPA plot as an image
        plt.savefig('term_gpa.png')
        plt.clf()

        # Line plot for Cumulative GPA
        plt.figure(figsize=(24, 6))
        sns.lineplot(x="Semester", y="Cumulative GPA", data=gpa_data, marker='o', color='blue', label='Cumulative GPA')

        # Styling the Cumulative GPA plot
        plt.xlabel("Semester")
        plt.ylabel("GPA")
        plt.title("Cumulative GPA")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()

        # Saving the Cumulative GPA plot as an image
        plt.savefig('cumulative_gpa.png')
        plt.clf()

        # Line plot for Cumulative GPA Points
        plt.figure(figsize=(24, 6))
        sns.lineplot(x="Semester", y="Cumulative GPA Points", data=gpa_data, marker='o', color='red', label='Cumulative GPA Points')

        # Styling the Cumulative GPA Points plot
        plt.xlabel("Semester")
        plt.ylabel("GPA Points")
        plt.title("Cumulative GPA Points")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()

        # Saving the Cumulative GPA Points plot as an image
        plt.savefig('cumulative_gpa_points.png')
        plt.clf()

        # Line plot for Cumulative GPA Units
        plt.figure(figsize=(18, 6))
        sns.lineplot(x="Semester", y="Cumulative GPA Units", data=gpa_data, marker='o', color='purple', label='Cumulative GPA Units')

        # Styling the Cumulative GPA Units plot
        plt.xlabel("Semester")
        plt.ylabel("GPA Units")
        plt.title("Cumulative GPA Units")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()

        # Saving the Cumulative GPA Units plot as an image
        plt.savefig('cumulative_gpa_units.png')
        plt.clf()

        # Revert back to default seaborn style
        sns.set()



    def generate_html(self, template_file, output_file):
        template_loader = jinja2.FileSystemLoader(searchpath=".")
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(template_file)

        html_output = template.render(semesters=self.semesters)

        with open(output_file, "w") as file:
            file.write(html_output)






def plot_cumulative_gpa(transcript_df):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=transcript_df, x="Semester", y="Cumulative GPA", marker="o")
    plt.xticks(rotation=45)
    plt.title("Change in Cumulative GPA")
    plt.xlabel("Semester")
    plt.ylabel("Cumulative GPA")
    plt.tight_layout()
    plt.savefig("cumulative_gpa_plot.png")  # Save the plot as an image file
    plt.close()

def plot_cumulative_gpa_units(transcript_df):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=transcript_df, x="Semester", y="Cumulative GPA Units", palette="coolwarm")
    plt.xticks(rotation=45)
    plt.title("Change in Cumulative GPA Units")
    plt.xlabel("Semester")
    plt.ylabel("Cumulative GPA Units")
    plt.tight_layout()
    plt.savefig("cumulative_gpa_units_plot.png")  # Save the plot as an image file
    plt.close()

def plot_term_gpa(transcript_df):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=transcript_df, x="Semester", y="Term GPA", palette="muted")
    plt.xticks(rotation=45)
    plt.title("Change in Term GPA")
    plt.xlabel("Semester")
    plt.ylabel("Term GPA")
    plt.tight_layout()
    plt.savefig("term_gpa_plot.png")  # Save the plot as an image file
    plt.close()





def main():
    my_transcript = Transcript()
    my_transcript.load_from_csv('grades.csv')
    my_transcript.print_transcript()
    my_transcript.generate_gpa_charts()
    my_transcript.generate_html('transcript_template.html', 'transcript.html')
    print('Transcript and GPA charts have been generated as transcript.html, cumulative_gpa.png, gpa_units.png, and term_gpa.png')
    


if __name__ == "__main__":
    main()