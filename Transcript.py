import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from Semester import *
import jinja2

class Transcript:
    def __init__(self, semesters=[], gpa=0,total_courses=0):
        self.gpa = gpa
        self.total_courses = total_courses
        self.semesters = semesters
        self.avg_percent_change = 0

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
        self.calculate()
    
    def calculate(self):
        total_score, total_units = 0, 0
        for s in self.semesters:
            total_score += s.total_gpa_points
            total_units += s.total_gpa_units

        self.gpa = total_score/total_units

        total_percent_change, num_semesters = 0, 0
        cum_gpa_points, cum_gpa_units = 0, 0
        prev_cum_gpa = 0
        for semester in self.semesters:
            term_gpa = semester.term_gpa
            cum_gpa_points += semester.total_gpa_points
            cum_gpa_units += semester.total_gpa_units
            cum_gpa = cum_gpa_points / cum_gpa_units if cum_gpa_units != 0 else 0

            if prev_cum_gpa != 0:
                percent_change = ((cum_gpa - prev_cum_gpa) / prev_cum_gpa) * 100
            else:
                percent_change = 0

            prev_cum_gpa = cum_gpa


            total_percent_change += percent_change
            num_semesters += 1
        self.avg_percent_change = round(total_percent_change / max(num_semesters-1, 1),2)
        print(num_semesters-1)


    def generate_dataframe(self):
        transcript_data = []
        cum_gpa_points = 0
        cum_gpa_units = 0

        self.avg_percent_change = 0

        total_percent_change, num_semesters = 0, 0

        for semester in self.semesters:
            term_gpa = semester.term_gpa
            cum_gpa_points += semester.total_gpa_points
            cum_gpa_units += semester.total_gpa_units
            cum_gpa = cum_gpa_points / cum_gpa_units if cum_gpa_units != 0 else 0

            if prev_cum_gpa != 0:
                percent_change = ((cum_gpa - prev_cum_gpa) / prev_cum_gpa) * 100
            else:
                percent_change = 0

            prev_cum_gpa = cum_gpa


            total_percent_change += percent_change
            num_semesters += 1
            self.avg_percent_change = total_percent_change / num_semesters




            transcript_data.append({
                "Semester": semester.semester_period,
                "Term GPA": term_gpa,
                "Cumulative GPA Points": cum_gpa_points,
                "Cumulative GPA Units": cum_gpa_units,
                "Cumulative GPA": cum_gpa,
                "Percentage Change": percent_change,
                "Average % Change per Semester": self.avg_percent_change
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


        sns.set(style="dark", palette="deep", font_scale=2)
        plt.figure(figsize=(12, 6))
        plt.style.use('dark_background')
        # Generating line plots for each GPA metric
        sns.set_context("poster")  # Increase the context to make the font size bigger

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
        plt.savefig('images/term_gpa.png')
        plt.clf()


        # Line plot for Cumulative GPA
        plt.figure(figsize=(12, 6))
        sns.lineplot(x="Semester", y="Cumulative GPA", data=gpa_data, marker='o', color='cyan', label='Cumulative GPA')

        # Styling the Cumulative GPA plot
        plt.ylim(2.4, 4.0)  # Set the y-axis limit to 0 and 4.0
        plt.xlabel("Semester")
        plt.ylabel("GPA")
        plt.title("Cumulative GPA")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()

        # Saving the Cumulative GPA plot as an image
        plt.savefig('images/cumulative_gpa.png')
        plt.clf()


        # Line plot for Cumulative GPA Units
        plt.figure(figsize=(12, 6))
        sns.lineplot(x="Semester", y="Cumulative GPA Units", data=gpa_data, marker='o', color='purple', label='Cumulative GPA Units')

        # Styling the Cumulative GPA Units plot
        plt.xlabel("Semester")
        plt.ylabel("GPA Units")
        plt.title("Cumulative GPA Units")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()

        # Saving the Cumulative GPA Units plot as an image
        plt.savefig('images/cumulative_gpa_units.png')
        plt.clf()


        # Revert back to default seaborn style
        sns.set()



    def generate_html(self, template_file, output_file):
        template_loader = jinja2.FileSystemLoader(searchpath=".")
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(template_file)

        html_output = template.render(semesters=self.semesters,avg_percent_change=self.avg_percent_change)

        with open(output_file, "w") as file:
            file.write(html_output)
