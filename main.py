
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from Transcript import *



def main():
    my_transcript = Transcript()
    my_transcript.load_from_csv('csv_files/grades.csv')
    my_transcript.generate_gpa_charts()
    my_transcript.generate_html('html/transcript_template.html', 'html/transcript.html')
    print('Transcript and GPA charts have been generated as transcript.html, cumulative_gpa.png, gpa_units.png, and term_gpa.png')
    


if __name__ == "__main__":
    main()