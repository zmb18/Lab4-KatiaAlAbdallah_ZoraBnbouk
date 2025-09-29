import tkinter as tk
from tkinter import ttk, messagebox
from part1 import Student, Instructor, Course

students = []
instructors = []
courses = []
    


root = tk.Tk() 
root.configure(bg='pink')
root.title("School Management System") 
root.geometry("500x500")

studentC = tk.StringVar()
instructorC = tk.StringVar()

studentdropdown = tk.OptionMenu(root, studentC, "")
studentdropdown.pack(pady=5)
instructordropdown = tk.OptionMenu(root, instructorC, "")
instructordropdown.pack(pady = 5)


tk.Label(root, text = "Student's name", bg = 'yellow').pack()
studentname = tk.Entry(root)
studentname.pack()
tk.Label(root, text = "Student's age", bg = 'yellow').pack()
studentage = tk.Entry(root)
studentage.pack()
tk.Label(root, text = "Student's email", bg = 'yellow').pack()
studentemail = tk.Entry(root)
studentemail.pack()
tk.Label(root, text = "Student's ID", bg = 'yellow').pack()
studentid = tk.Entry(root)
studentid.pack()



def add_student():
    try:
        student = Student(studentname.get(), int(studentage.get()), studentemail.get(), int(studentid.get()))
        students.append(student)
        coursename = studentC.get()
        messagebox.showinfo("Added", f"Student {student.name} has been added successfully.")
    except ValueError as e:
        messagebox.showerror("Invalid, age and ID must be number!", str(e))
    

tk.Button(root, text = "Add a student", command = add_student, bg = 'lightblue').pack(pady = 5)


tk.Label(root, text = "Instructor's name", bg = 'yellow').pack()
instructorname = tk.Entry(root)
instructorname.pack()
tk.Label(root, text = "Instructor's age", bg = 'yellow').pack()
instructorage = tk.Entry(root)
instructorage.pack()
tk.Label(root, text = "Instructor's email", bg = 'yellow').pack()
instructoremail = tk.Entry(root)
instructoremail.pack()
tk.Label(root, text = "Instructor's ID", bg = 'yellow').pack()
instructorid = tk.Entry(root)
instructorid.pack()

tk.Label(root, text = "Select course", bg = 'yellow').pack()
instructordropdown = tk.OptionMenu(root, instructorC, "")
instructordropdown.pack()
instructorC.set("")



def add_instructor():
    try: 
        instructor = Instructor(instructorname.get(), int(instructorage.get()), instructoremail.get(), int(instructorid.get()))
        instructors.append(instructor)
        coursename = instructorC.get()
        messagebox.showinfo("Added", f"Instructor {instructor.name} has been added successfully.")
    except ValueError as e:
        messagebox.showerror("Invalid, age and ID must be number!", str(e))


tk.Button(root, text = "Add an instructor", command = add_instructor, bg='lightblue').pack(pady = 5)


tk.Label(root, text = "Course ID", bg = 'yellow').pack()
courseid = tk.Entry(root)
courseid.pack()
tk.Label(root, text = "Course Name", bg = 'yellow').pack()
coursename = tk.Entry(root)
coursename.pack()
tk.Label(root, text = "Instructor", bg = 'yellow').pack()
courseinstructor = tk.Entry(root)
courseinstructor.pack()

def coursedropdown():
    # for student
    menu1 = studentdropdown["menu"]
    menu1.delete(0, "end")
    for course in courses:
        menu1.add_command(label = course.courename, command = lambda value = course.coursename: studentC.set(value))
    
    if courses: studentC.set(courses[0].set(courses[0].coursename))

    # for instructor
    menu2 = instructordropdown["menu"]
    menu2.delete(0, "end")
    for course in courses: 
        menu2.add_command(label = course.coursename, command = lambda value = course.cousename: instructorC.set(value))
    
    if courses:
        instructorC.set(courses[0].coursename)




def add_course():
    prof = next((x for x in instructors if x.name == courseinstructor.get()), None)
    course = Course(courseid.get(), coursename.get(), prof)
    if prof: prof.assign_course(course)
    messagebox.showinfo("Added", f"Course {course.course_name} has been added successfully.")
    courses.append(course)
    coursedropdown()
    messagebox.showinfo("Added", f"Course {course.coursename} has been added successfully.")
    courseid.set("")
    coursename.set("")
    coursename.set("")


tk.Button(root, text = "Add a course", command = add_course, bg = 'lightblue').pack(pady = 5)

root.mainloop()




    
