from flask import Flask,redirect,url_for,render_template,request
app = Flask(__name__)
from setup_db import execute_query

@app.route('/')
def index():
    return redirect(url_for("add_course"))


@app.route('/register/<student_id>/<course_id>')
def register(student_id ,course_id):
    """"
  this endpoit inserts a student into students_courses table so student_id is registred to
  course_id.then shoe all courses for this student.

    """
    execute_query(F"INSERT INTO students_courses(student_id ,course_id) VALUES ('{student_id}','{course_id}')")
    return redirect(url_for('registrations',student_id=student_id))

@app.route('/registrations/<student_id>')
def registrations(student_id):
    course_ids=execute_query(f"SELECT course_id FROM students_courses WHERE student_id='{student_id}'")
    clean_ids=[ c[0] for c in course_ids ]
    course_names=[]
    for i in clean_ids:
      course_names.append(execute_query(f"SELECT name FROM courses WHERE course_id={i}"))
    student_name=execute_query(f"SELECT name FROM students WHERE student_id={student_id}")
    return render_template("registrations.html", student_name=student_name, course_names=course_names)


@app.route("/add-student",methods=["POST","GET"])
def add_student():   
  courses=execute_query("SELECT * FROM courses")
  students=execute_query("SELECT * FROM students")
  if request.method =="POST":
    course_id=request.form["course_id"]
    student_id=request.form["student_id"]
    execute_query(F"INSERT INTO students_courses(student_id ,course_id) VALUES ('{student_id}','{course_id}')")
    return redirect(url_for('add_student'))
  return render_template("add_student.html" ,courses=courses ,students=students)

@app.route("/add-course",methods=["POST" ,"GET"])
def add_course():
   teachers=execute_query("SELECT * FROM teachers")
   if request.method =='POST':
      course_name =request.form["course"].capitalize()
      teacher_id=request.form["teacher_id"]
      exists=execute_query(f"SELECT name FROM courses WHERE teacher_id='{teacher_id}'and name= '{course_name}'")
      if exists :
         return render_template("add_course.html",teachers=teachers,text="you already in the course")
      else:
        execute_query(f"INSERT INTO courses (name , teacher_id) VALUES ('{course_name}','{teacher_id}')")
        return redirect(url_for("add_course"))
   return render_template("add_course.html", teachers=teachers)



@app.route("/students", methods=["POST", "GET"])
def students():
    students=execute_query("SELECT * FROM students")
    if request.method == "POST":
       student=[[ s for s in student ]for student in execute_query(f"SELECT name, email FROM students WHERE student_id={request.form['student_id']}")]
       return render_template("students.html",students=students,student=student)
    return render_template("students.html", students=students, student=[])

      
