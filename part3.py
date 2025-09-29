from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QLineEdit, QComboBox, QMessageBox, QTableWidget, QTableWidgetItem
import sys
from part1 import Student, Instructor, Course
import json
import csv

students = []
instructors = []
courses = []

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("School Management System")
    window.setGeometry(100, 200, 400, 400)

    studentname = QLineEdit(window)
    studentname.setPlaceholderText("Student name")
    studentname.move(50, 20)

    studentage = QLineEdit(window)
    studentage.setPlaceholderText("Student age")
    studentage.move(50, 40)

    studentemail = QLineEdit(window)
    studentemail.setPlaceholderText("Student email")
    studentemail.move(50, 60)

    studentid = QLineEdit(window)
    studentid.setPlaceholderText("Student ID")
    studentid.move(50, 80)

    studentdrop = QComboBox(window)
    studentdrop.move(50, 100)

    def studentC():
        studentdrop.clear()
        for c in courses:
            studentdrop.addItem(c.coursename)

    def studentadd():
        try: 
            s = Student(studentname.text(), int(studentage.text()), studentemail.text(), int(studentid.text()))
            students.append(s)
            coursename = studentdrop.currentText()
            coursechosen = next((c for c in courses if c.coursename == coursename), None)
            if coursechosen: coursechosen.studentadd(s)
            QMessageBox.information(window, "SUCCESS", f"{s.name} has been added successfully.")
        except Exception as e:
            QMessageBox.critical(window, "Error!", str(e))


    studentaddbutton = QPushButton("Add student", window)
    studentaddbutton.move(50, 120)
    studentaddbutton.clicked.connect(studentadd)




    instructorname = QLineEdit(window)
    instructorname.setPlaceholderText("Instructor name")
    instructorname.move(50,140)

    instructorage = QLineEdit(window)
    instructorage.setPlaceholderText("Instructor age")
    instructorage.move(50, 160)

    instructoremail = QLineEdit(window)
    instructoremail.setPlaceholderText("Instructor email")
    instructoremail.move(50, 180)

    instructorid = QLineEdit(window)
    instructorid.setPlaceholderText("Instructor ID")
    instructorid.move(50, 200)

    instructordrop = QComboBox(window)
    instructordrop.move(50, 220)

    def instructorC():
        instructordrop.clear()
        for c in courses: instructordrop.addItem(c.coursename)

    def instructoradd():
        try:
            i = Instructor(instructorname.text(), int(instructorage.text(), instructoremail.text(), int(instructorid.text())))
            instructors.append(i)
            coursename = instructordrop.currentText()
            coursechosen = next((c for c in courses if c.coursename == coursename), None)
            if coursechosen:
                i.assign_course(coursechosen)
            QMessageBox.information(window, "SUCCESS", f"{i.name} has been added successfully.")
        except Exception as e:
            QMessageBox.critical(window, "Error!", str(e))

    instructoraddbutton = QPushButton("Add instructor", window)
    instructoraddbutton.move(50, 240)
    instructoraddbutton.clicked.connect(instructoradd)


    courseid = QLineEdit(window)
    courseid.setPlaceholderText("Course ID")
    courseid.move(50, 260)

    coursename = QLineEdit(window)
    coursename.setPlaceholderText("Course name")
    coursename.move(50, 280)

    courseinstructor = QLineEdit(window)
    courseinstructor.setPlaceholderText("Instructor for this course")
    courseinstructor.move(50, 300)

    def courseadd():
        profname = courseinstructor.text()
        prof = next((x for x in instructors if x.name == profname), None)
        c = Course(courseid.text(), coursename.text(), prof)
        if prof: prof.assign_course(c)
        courses.append(c)
        studentC()
        instructorC()
        QMessageBox.information(window, "SUCCESS", f"{c.course_name} has been added successfully!")

    courseaddbutton = QPushButton("Add course", window)
    courseaddbutton.move(50, 320)
    courseaddbutton.clicked.connect(courseadd)


    # part 5
    studenttable = QTableWidget(window)
    studenttable.setColumnCount(4)
    studenttable.setHorizontalHeaderLabels(["Name", "Age", "ID", "Email"])
    studenttable.setGeometry(500, 50, 250, 200)

    instructortable = QTableWidget(window)
    instructortable.setColumnCount(4)
    instructortable.setHorizontalHeaderLabels(["Name", "Age", "ID", "Email"])
    instructortable.setGeometry(500, 50, 250, 200)

    coursetable = QTableWidget(window)
    coursetable.setColumnCount(3)
    coursetable.setHorizontalHeaderLabels(["Name", "ID", "Instructor"])
    coursetable.setGeometry(500, 50, 250, 200)

    

    window.show()
    sys.exit(app.exec_())        

if __name__ == '__main__':
    main()