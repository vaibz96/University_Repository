from flask import Flask, render_template
import sqlite3
import os 
app = Flask(__name__)

@app.route('/hi')
def hello():
    return "Hello world! This is Flask!"

@app.route('/Goodbye')
def see_you():
    return "See you later!"

@app.route('/instructor_courses')
def template_demo():
    return render_template('parameters.html',
                            title = "Stevens Repository",
                            my_header = "My Stevens Repository")

@app.route('/instructor_table')
def instructore_table():

    db = sqlite3.connect("C:\\Users\\shanb\\Database\\810_startup.db")

    query = """ SELECT I.CWID, I.Name, I.Dept, G.Course, COUNT(G.Student_CWID) Students
                FROM HW11_instructors I
                    JOIN HW11_grades G ON  I.CWID = G.Instructor_CWID
                GROUP BY G.COURSE
                ORDER BY COUNT(G.Student_CWID) DESC"""

    results = db.execute(query)

    # convert the query into a list of dictionary to pass it into the template

    data = [{ "cwid": cwid, "name": name, "dept": dept, "courses":courses, "count": count}\
    for cwid, name, dept, courses, count in results]

    return render_template('instructor_table.html',
                        title = "Stevens Repository",
                        table_title = "Number of students by course and instructor",
                        instructors = data)

app.run(debug = True)
