import sys 
import pandas as pd 
import matplotlib.pyplot as plt
from jinja2 import Template

def generate_student_html(student_id,df=pd.read_csv("data.csv")):
    student_data=df[df['Student id']==student_id]
    if student_data.empty:
        return generate_error_html("Invalid student ID")
    total_marks=student_data['Marks'].sum()
    template=Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Student data</title>
</head>
<body>
    <h1>Student Details</h1>
    <table>
       <tr>
        <th>Student id</th>
        <th>Course id</th>
        <th>Marks</th>
       </tr>
       {% for row in student_data %}
       <tr>
        <td>{{row['Student id']}}</td>
        <td>{{row['Course id']}}</td>
        <td>{{row['Marks']}}</td>
       </tr>
       {% endfor %}
       <tr>
        <td colspan="2"><b>Total marks</b></td>
        <td><b>{{total_marks}}<b></td>
       </tr>
    </table>
   </body>
</html>
""")
    html_content = template.render(student_data=student_data.to_dict(orient='records'), total_marks=total_marks)
    return html_content

def generate_course_html(course_id,df=pd.read_csv("data.csv")):
    course_data=df[df['Course id']==course_id]
    if course_data.empty:
        return generate_error_html("Invalid course ID")
    total_marks=df['Marks'].sum()
    avg_marks=course_data['Marks'].mean()
    max_marks=course_data['Marks'].max()

    template=Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Student data</title>
</head>
<body>
    <h1>Course Details</h1>
    <table broder="1">
        <tr>
            <td>Average Marks</td>
            <td>Maximum Marks</td>
        </tr>
        <tr>
            <td>{{avg_marks]}}</td>
            <td>{{max_marks}}</td>
        </tr>
    </table>
    <img src="histogram.png" alt="Marks Histogram">
</body>
</html>
""")
    html_content = template.render(avg_marks=avg_marks, max_marks=max_marks)
    return html_content

def generate_error_html(error_message):
    template = Template("""
    <html>
    <head>
        <title>Error</title>
    </head>
    <body>
        <h1>Error</h1>
        <p>{{ error_message }}</p>
    </body>
    </html>
    """)

    html_content = template.render(error_message=error_message)
    return html_content

def main():
    if len(sys.argv) != 3:
        print("Usage: python app.py -s|-c ID")
        sys.exit(1)

    option = sys.argv[1]
    identifier = int(sys.argv[2])

    try:
        df = pd.read_csv('input.csv')
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        sys.exit(1)

    if option == '-s':
        html_content = generate_student_html(identifier, df)
    elif option == '-c':
        html_content = generate_course_html(identifier, df)
    else:
        html_content = generate_error_html("Invalid option")

    with open('output.html', 'w') as f:
        f.write(html_content)

if __name__ == "__main__":
    main()
    