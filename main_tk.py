import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
from Data_Management import DatabaseBoss
db =  DatabaseBoss() 
from Student import Student
from Instructor import Instructor
from Course import Course
import csv
import json

def  row_to_student(d):  return Student(d["student_id"], d["name"], d["age"], d["email"])

def  row_to_instructor(d): return Instructor(d["instructor_id"], d["name"], d["age"], d["email"])

def  row_to_course(d, instructor_by_id): 
    instr =  instructor_by_id.get(d.get("instructor_id"))
    return Course(d["course_id"], d["course_name"], instr)

def  clear_student_form(): 
    """Clear all student form fields"""
    name_input.delete(0, tk.END)
    ag_input.delete(0, tk.END)
    e_input.delete(0, tk.END)
    sid_input.delete(0, tk.END)

def  clear_instructor_form(): 
    """Clear all instructor form fields"""
    ninput.delete(0, tk.END)
    aginput.delete(0, tk.END)
    e2input.delete(0, tk.END)
    iidinput.delete(0, tk.END)

def  clear_course_form(): 
    """Clear all course form fields"""
    cid3input.delete(0, tk.END)
    crs_input.delete(0, tk.END)

def  clear_register_form(): 
    """Clear registration form fields"""
    sid2_input.delete(0, tk.END)
    cid_input.delete(0, tk.END)
def  clear_assign_form(): 
    """Clear assignment form fields"""
    iid2input.delete(0, tk.END)
    cid2input.delete(0, tk.END)
def  validating_the_inputs(inputs): 
    """Validate that all inputs are not empty"""
    for field_name, value in inputs.items(): 
        if not value.strip(): 
            messagebox.showerror("There is an error",  f"{field_name} cannot be empty!")
            return False
    return True
def  validating_the__age(age_str, field_name= "Age"): 
    """Validate age input"""
    try: 
        age =  int(age_str.strip())
        if age <=  0: 
            messagebox.showerror("There is an error",  f"{field_name} must be a positive number!")
            return None
        return age
    except ValueError: 
        messagebox.showerror("There is an error",  f"{field_name} must be a valid number!")
        return None


def  building_display() : 

    # Students Section
    students_label =  tk.Label(  data_scrollable_frame, text= "STUDENTS",  font= ("Times New Roman",  12, "bold"))
    students_label.pack(fill= 'x', padx= 5, pady=  5)
    
    students_frame =  tk.Frame(data_scrollable_frame, relief= "raised",  bd= 1)
    students_frame.pack(fill= 'x', padx= 5, pady=  5)
    
    students =  db.readallstudents()
    if students: 
        # Headers
        header_frame =  tk.Frame(students_frame, bg= "gray90")
        header_frame.pack(fill= 'x')
        tk.Label(  header_frame, text= "ID",  width= 12, font= ("Times New Roman",  8, "bold"), bg= "gray90").pack(side= 'left')
        tk.Label(  header_frame, text= "Name",  width= 15, font= ("Times New Roman",  8, "bold"), bg= "gray90").pack(side= 'left')
        tk.Label(  header_frame, text= "Age",  width= 5, font= ("Times New Roman",  8, "bold"), bg= "gray90").pack(side= 'left')
        tk.Label(  header_frame, text= "Email",  width= 20, font= ("Times New Roman",  8, "bold"), bg= "gray90").pack(side= 'left')
        
        for student in students: 
            row_frame =  tk.Frame(students_frame)
            row_frame.pack(fill= 'x')
            tk.Label(  row_frame, text= student['student_id'], width= 12, anchor= 'w', font= ("Times New Roman",  8)).pack(side= 'left')
            tk.Label(  row_frame, text= student['name'], width= 15, anchor= 'w', font= ("Times New Roman",  8)).pack(side= 'left')
            tk.Label(  row_frame, text= student['age'], width= 5, anchor= 'w', font= ("Times New Roman",  8)).pack(side= 'left')
            tk.Label(  row_frame, text= student['email'], width= 20, anchor= 'w', font= ("Times New Roman",  8)).pack(side= 'left')
    else: 
        tk.Label(  students_frame, text= "No students found",  font= ("Times New Roman",  9, "italic")).pack()
    
    # Instructors Section
    instructors_label =  tk.Label(  data_scrollable_frame, text= "INSTRUCTORS",  font= ("Times New Roman",  12, "bold"))
    instructors_label.pack(fill= 'x', padx= 5, pady=  5)
    
    instructors_frame =  tk.Frame(data_scrollable_frame, relief= "raised",  bd= 1)
    instructors_frame.pack(fill= 'x', padx= 5, pady=  5)
    
    instructors =  db.readallinstructors()
    if instructors: 
        # Headers
        header_frame =  tk.Frame(instructors_frame, bg= "gray90")
        header_frame.pack(fill= 'x')
        tk.Label(  header_frame, text= "ID",  width= 12, font= ("Times New Roman",  8, "bold"), bg= "gray90").pack(side= 'left')
        tk.Label(  header_frame, text= "Name",  width= 15, font= ("Times New Roman",  8, "bold"), bg= "gray90").pack(side= 'left')
        tk.Label(  header_frame, text= "Age",  width= 5, font= ("Times New Roman",  8, "bold"), bg= "gray90").pack(side= 'left')
        tk.Label(  header_frame, text= "Email",  width= 20, font= ("Times New Roman",  8, "bold"), bg= "gray90").pack(side= 'left')
        
        for instructor in instructors: 
            row_frame =  tk.Frame(instructors_frame)
            row_frame.pack(fill= 'x')
            tk.Label(  row_frame, text= instructor['instructor_id'], width= 12, anchor= 'w', font= ("Times New Roman",  8)).pack(side= 'left')
            tk.Label(  row_frame, text= instructor['name'], width= 15, anchor= 'w', font= ("Times New Roman",  8)).pack(side= 'left')
            tk.Label(  row_frame, text= instructor['age'], width= 5, anchor= 'w', font= ("Times New Roman",  8)).pack(side= 'left')
            tk.Label(  row_frame, text= instructor['email'], width= 20, anchor= 'w', font= ("Times New Roman",  8)).pack(side= 'left')
    else: 
        tk.Label(  instructors_frame, text= "No instructors found",  font= ("Times New Roman",  9)).pack()
    
    # Courses Section
    courses_label =  tk.Label(  data_scrollable_frame, text= "COURSES",  font= ("Times New Roman",  12, "bold"))
    courses_label.pack(fill= 'x', padx= 5, pady=  5)
    
    courses_frame =  tk.Frame(data_scrollable_frame, relief= "raised",  bd= 1)
    courses_frame.pack(fill= 'x', padx= 5, pady=  5)
    
    courses =  db.readallcourses()
    if courses: 
        # Headers
        header_frame =  tk.Frame(courses_frame, bg= "gray90")
        header_frame.pack(fill= 'x')
        tk.Label(  header_frame, text= "Course ID",  width= 12, font= ("Times New Roman",  8, "bold"), bg= "gray90").pack(side= 'left')
        tk.Label(  header_frame, text= "Course Name",  width= 20, font= ("Times New Roman",  8, "bold"), bg= "gray90").pack(side= 'left')
        tk.Label(  header_frame, text= "Instructor",  width= 15, font= ("Times New Roman",  8, "bold"), bg= "gray90").pack(side= 'left')
        
        for course in courses: 
            row_frame =  tk.Frame(courses_frame)
            row_frame.pack(fill= 'x')
            tk.Label(  row_frame, text= course['course_id'], width= 12, anchor= 'w', font= ("Times New Roman",  8)).pack(side= 'left')
            tk.Label(  row_frame, text= course['course_name'], width= 20, anchor= 'w', font= ("Times New Roman",  8)).pack(side= 'left')
            tk.Label(  row_frame, text= course.get('instructor_name', 'Unassigned'), width= 15, anchor= 'w', font= ("Times New Roman",  8)).pack(side= 'left')
    else: 
        tk.Label(  courses_frame, text= "No courses found",  font= ("Times New Roman",  9, "italic")).pack()
    
    # Export buttons
    export_frame =  tk.Frame(data_scrollable_frame)
    export_frame.pack(fill= 'x', padx= 5, pady= 10)
    
    def  export_to_json(): 
        success =  db.exporttojson()
        if success: 
            messagebox.showinfo("Success",  "Data exported to JSON file successfully!")
        else: 
            messagebox.showerror("Error",  "Failed to export data")
    
    def  backup_database(): 
        success =  db.backupdb()
        if success: 
            messagebox.showinfo("Success",  "Database backed up successfully!")
        else: 
            messagebox.showerror("Error",  "Failed to backup database")
    
    tk.Button(export_frame, text= "Export to JSON",  command= export_to_json, fg= "black",  font= ("Times New Roman",  8)).pack(side= 'left', padx= 5)
    tk.Button(export_frame, text= "Backup Database",  command= backup_database, fg= "black",  font= ("Times New Roman",  8)).pack(side= 'left', padx= 5)
    tk.Button(export_frame, text= "Refresh Data",  command= refresh_data_display,  fg= "black",  font= ("Times New Roman",  8)).pack(side= 'left', padx= 5)
def  refresh_data_display(): 
    """Refresh the data display after any changes"""

    for widget in data_scrollable_frame.winfo_children(): 
        widget.destroy()
    
    # Rebuild the data display
    building_display()

def  add_student(): 
    sid =  sid_input.get().strip()
    name =  name_input.get().strip()
    age_str =  ag_input.get().strip()
    email =  e_input.get().strip()
    
    inputs =  {
        "Student ID":  sid,
        "Name":  name,
        "Age":  age_str,
        "Email":  email
    }
    
    if not validating_the_inputs(inputs): 
        return
    
    age =  validating_the__age(age_str)
    if age is None: 
        return

    st =  Student(sid, name, age, email)
    ok =  db.createnewstudent(st.id, st.name, st.age, st._email)
    
    if ok: 
        messagebox.showinfo("Success",  f"Student {name} added successfully!")
        clear_student_form()
        refresh_data_display()  # Refresh the data display
    else: 
        messagebox.showerror("There is an error",  f"Failed to add student. Student ID {sid} might already exist.")

def  add_instructor(): 
    iid =  iidinput.get().strip()
    name =  ninput.get().strip()
    age_str =  aginput.get().strip()
    email =  e2input.get().strip()
    
    inputs =  {
        "Instructor ID":  iid,
        "Name":  name,
        "Age":  age_str,
        "Email":  email
    }
    
    if not validating_the_inputs(inputs): 
        return
    
    age =  validating_the__age(age_str)
    if age is None: 
        return
    
    ins =  Instructor(iid, name, age, email)

    ok =  db.createinstructor(ins.instructor_id, ins.name, ins.age, ins._email)
    
    if ok: 
        messagebox.showinfo("Success",  f"Instructor {name} added successfully!")
        clear_instructor_form()
        refresh_data_display()  # Refresh the data display
    else: 
        messagebox.showerror("There is an error",  f"Failed to add instructor. Instructor ID {iid} might already exist.")

def  add_course(): 
    cid =  cid3input.get().strip()
    cname =  crs_input.get().strip()
    
    inputs =  {
        "Course ID":  cid,
        "Course Name":  cname
    }
    
    if not validating_the_inputs(inputs): 
        return
    
    crs =  Course(cid, cname, None)
    ok =  db.createnewcourse(crs.course_id, crs.course_name, None)
    
    if ok: 
        messagebox.showinfo("Success",  f"Course {cname} added successfully!")
        clear_course_form()
        refresh_data_display()  # Refresh the data display
    else: 
        messagebox.showerror("There is an error",  f"Failed to add course. Course ID {cid} might already exist.")

def  register_student(): 
    """Register a student to a course"""
    sid =  sid2_input.get().strip()
    cid =  cid_input.get().strip()
    
    # Validate inputs
    inputs =  {
        "Student ID":  sid,
        "Course ID":  cid
    }
    
    if not validating_the_inputs(inputs): 
        return
    
    # Check if student exists
    student_data =  db.readstudent(sid)
    if not student_data: 
        messagebox.showerror("There is an error",  f"Student with ID {sid} does not exist!")
        return
    
    # Check if course exists
    course_data =  db.readcourse(cid)
    if not course_data: 
        messagebox.showerror("There is an error",  f"Course with ID {cid} does not exist!")
        return
    
    # Register student to course
    ok =  db.registerstudenttocourse(sid, cid)
    
    if ok: 
        messagebox.showinfo("Success",  f"Student {student_data['name']} registered to course {course_data['course_name']} successfully!")
        clear_register_form()
        refresh_data_display()  # Refresh the data display
    else: 
        messagebox.showerror("There is an error",  "Registration failed. Student might already be registered to this course.")

def  assigning_instructor(): 
    """Assign an instructor to a course"""
    iid =  iid2input.get().strip()
    cid =  cid2input.get().strip()
    
    # Validate inputs
    inputs =  {
        "Instructor ID":  iid,
        "Course ID":  cid
    }
    
    if not validating_the_inputs(inputs): 
        return
    
    # Checking if instructor exists
    instructor_data =  db.readinstructor(iid)
    if not instructor_data: 
        messagebox.showerror("There is an error",  f"Instructor with ID {iid} does not exist!")
        return
    
    # Check if course exists
    course_data =  db.readcourse(cid)
    if not course_data: 
        messagebox.showerror("There is an error",  f"Course with ID {cid} does not exist!")
        return
    
    # Assign instructor to course
    ok =  db.updatecourse(cid, course_data['course_name'], iid)
    
    if ok: 
        messagebox.showinfo("Success",  f"Instructor {instructor_data['name']} assigned to course {course_data['course_name']} successfully!")
        clear_assign_form()
        refresh_data_display()  # Refresh the data display
    else: 
        messagebox.showerror("There is an error",  "Assignment failed.")



def  edit_student(): 
    """Edit selected student"""
    def  on_student_select(): 
        selected =  student_listbox.curselection()
        if not selected: 
            messagebox.showerror("Error",  "Please select a student to edit")
            return
        
        student_data =  students_list[selected[0]]
        
        # Pre-fill the main form with selected student data
        clear_student_form()
        name_input.insert(0, student_data['name'])
        ag_input.insert(0, str(student_data['age']))
        e_input.insert(0, student_data['email'])
        sid_input.insert(0, student_data['student_id'])
        sid_input.config(state= 'disabled')  # Don't allow ID changes
        
        # Change submit button to update
        submitbtn1.config(text= "Update",  command= lambda:  update_student(student_data['student_id']))
        edit_window.destroy()
    
    edit_window =  tk.Toplevel(root)
    edit_window.title("Select Student to Edit")
    edit_window.geometry("400x300")
    
    tk.Label(  edit_window, text= "Select a student to edit: ",  font= ("Times New Roman",  12)).pack(pady= 10)
    
    student_listbox =  tk.Listbox(edit_window, height= 10)
    student_listbox.pack(fill= 'both', expand= True, padx= 20, pady= 10)
    
    students_list =  db.readallstudents()
    for student in students_list: 
        student_listbox.insert(tk.END, f"{student['student_id']} - {student['name']}")
    
    tk.Button(edit_window, text= "Edit Selected",  command= on_student_select, bg= "orange").pack(pady= 10)

def  load_objects(): 
    # read dicts from DB
    student_rows =  db.readallstudents()       # list[dict]
    instructor_rows =  db.readallinstructors() # list[dict]
    course_rows =  db.readallcourses()         # list[dict] with instructor_name/id

    # map to objects
    students =  [row_to_student(d) for d in student_rows]
    instructors =  [row_to_instructor(d) for d in instructor_rows]
    instr_by_id =  {i.instructor_id:  i for i in instructors}
    courses =  [row_to_course(d, instr_by_id) for d in course_rows]

    return students, instructors, courses
def  update_student(original_id): 
    """Update student with new information"""
    name =  name_input.get().strip()
    age_str =  ag_input.get().strip()
    email =  e_input.get().strip()
    
    inputs =  {
        "Name":  name,
        "Age":  age_str,
        "Email":  email
    }
    
    if not validating_the_inputs(inputs): 
        return
    
    age =  validating_the__age(age_str)
    if age is None: 
        return
    
    ok =  db.updatestudent(original_id, name, age, email)
    
    if ok: 
        messagebox.showinfo("Success",  f"Student {name} updated successfully!")
        # Reset form
        clear_student_form()
        sid_input.config(state= 'normal')
        submitbtn1.config(text= "Submit",  command= add_student)
        refresh_data_display()
    else: 
        messagebox.showerror("Error",  "Failed to update student")

def  delete_student(): 
    """Delete selected student"""
    def  on_student_delete(): 
        selected =  student_listbox.curselection()
        if not selected: 
            messagebox.showerror("Error",  "Please select a student to delete")
            return
        
        student_data =  students_list[selected[0]]
        
        if messagebox.askyesno("Confirm Delete",  f"Are you sure you want to delete student {student_data['name']}?"): 
            ok =  db.deletestudentfromdb(student_data['student_id'])
            if ok: 
                messagebox.showinfo("Success",  "Student deleted successfully!")
                refresh_data_display()
                delete_window.destroy()
            else: 
                messagebox.showerror("Error",  "Failed to delete student")
    
    delete_window =  tk.Toplevel(root)
    delete_window.title("Delete Student")
    delete_window.geometry("400x300")
    
    tk.Label(  delete_window, text= "Select a student to delete: ",  font= ("Times New Roman",  12)).pack(pady= 10)
    
    student_listbox =  tk.Listbox(delete_window, height= 10)
    student_listbox.pack(fill= 'both', expand= True, padx= 20, pady= 10)
    
    students_list =  db.readallstudents()
    for student in students_list: 
        student_listbox.insert(tk.END, f"{student['student_id']} - {student['name']}")
    
    tk.Button(delete_window, text= "Delete Selected",  command= on_student_delete, bg= "red",  fg= "white").pack(pady= 10)

def  edit_instructor(): 
    """Edit selected instructor"""
    def  on_instructor_select(): 
        selected =  instructor_listbox.curselection()
        if not selected: 
            messagebox.showerror("Error",  "Please select an instructor to edit")
            return
        
        instructor_data =  instructors_list[selected[0]]
        
        # Pre-fill the main form with selected instructor data
        clear_instructor_form()
        ninput.insert(0, instructor_data['name'])
        aginput.insert(0, str(instructor_data['age']))
        e2input.insert(0, instructor_data['email'])
        iidinput.insert(0, instructor_data['instructor_id'])
        iidinput.config(state= 'disabled')
        
        # Change submit button to update
        submitbtn3.config(text= "Update",  command= lambda:  edit_instructor_info(instructor_data['instructor_id']))
        edit_window.destroy()
    
    edit_window =  tk.Toplevel(root)
    edit_window.title("Select Instructor to Edit")
    edit_window.geometry("400x300")
    
    tk.Label(  edit_window, text= "Select an instructor to edit: ",  font= ("Times New Roman",  12)).pack(pady= 10)
    
    instructor_listbox =  tk.Listbox(edit_window, height= 10)
    instructor_listbox.pack(fill= 'both', expand= True, padx= 20, pady= 10)
    
    instructors_list =  db.readallinstructors()
    for instructor in instructors_list: 
        instructor_listbox.insert(tk.END, f"{instructor['instructor_id']} - {instructor['name']}")
    
    tk.Button(edit_window, text= "Edit Selected",  command= on_instructor_select, bg= "orange").pack(pady= 10)

def  edit_instructor_info(original_id): 
    """Update instructor with new information"""
    name =  ninput.get().strip()
    age_str =  aginput.get().strip()
    email =  e2input.get().strip()
    
    inputs =  {
        "Name":  name ,
        "Age":  age_str ,
        "Email":  email
    }
    
    if not validating_the_inputs(inputs): 
        return
    
    age =  validating_the__age(age_str)
    if age is None: 
        return
    
    ok =  db.updateinstructor(original_id, name, age, email)
    
    if ok: 
        messagebox.showinfo("Success",  f"Instructor {name} updated successfully!")
        # Reset form
        clear_instructor_form()
        iidinput.config(state= 'normal')
        submitbtn3.config(text= "Submit",  command= add_instructor)
        refresh_data_display()
    else: 
        messagebox.showerror("Error",  "Failed to update instructor")


def view_student_courses(): 
    """View courses for selected student"""
    def show_courses(): 
        selected =  student_listbox.curselection()
        if not selected: 
            messagebox.showerror("Error",  "Please select a student")
            return
        
        student_data =  students_list[selected[0]]
        print(f"Debug:  Looking for courses for student ID:  {student_data['student_id']}")
        
        # Get courses from database
        courses =  db.gettingstudentcourses(student_data['student_id'])
        print(f"Debug:  Found {len(courses)} courses")
        
        courses_window =  tk.Toplevel(root)
        courses_window.title(f"Courses for {student_data['name']}")
        courses_window.geometry("600x400")
        
        # Header
        header_frame =  tk.Frame(courses_window)
        header_frame.pack(fill= 'x', padx= 10, pady= 10)
        tk.Label(  header_frame, text= f"Courses for {student_data['name']}",  
                font= ("Times New Roman",  14, "bold")).pack()
        
        # Create scrollable frame for courses
        main_frame =  tk.Frame(courses_window)
        main_frame.pack(fill= 'both', expand= True, padx= 10, pady= 10)
        
        if courses: 
            # Headers
            header_frame =  tk.Frame(main_frame, bg= "gray90")
            header_frame.pack(fill= 'x', pady= (0, 5))
            tk.Label(  header_frame, text= "Course ID",  width= 12, font= ("Times New Roman",  10, "bold"), 
                    bg= "gray90").pack(side= 'left', padx= 5)
            tk.Label(  header_frame, text= "Course Name",  width= 25, font= ("Times New Roman",  10, "bold"), 
                    bg= "gray90").pack(side= 'left', padx= 5)
            tk.Label(  header_frame, text= "Registration Date",  width= 20, font= ("Times New Roman",  10, "bold"), 
                    bg= "gray90").pack(side= 'left', padx= 5)
            
            # Course rows
            for course in courses: 
                row_frame =  tk.Frame(main_frame, relief= "raised",  bd= 1)
                row_frame.pack(fill= 'x', pady= 2)
                
                tk.Label(  row_frame, text= course['course_id'], width= 12, anchor= 'w', 
                        font= ("Times New Roman",  10)).pack(side= 'left', padx= 5, pady=  5)
                tk.Label(  row_frame, text= course['course_name'], width= 25, anchor= 'w', 
                        font= ("Times New Roman",  10)).pack(side= 'left', padx= 5, pady=  5)
                
                # Format registration date
                reg_date =  course.get('registration_date', 'N/A')
                if reg_date and reg_date !=  'N/A': 
                    try: 
                        # Handle different date formats
                        if 'T' in str(reg_date): 
                            reg_date =  str(reg_date).split('T')[0]
                    except: 
                        reg_date =  str(reg_date)[: 10] if len(str(reg_date)) > 10 else str(reg_date)
                
                tk.Label(  row_frame, text= reg_date, width= 20, anchor= 'w', 
                        font= ("Times New Roman",  10)).pack(side= 'left', padx= 5, pady=  5)
        else: 
            tk.Label(  main_frame, text= "This student is not registered for any courses.",  
                    font= ("Times New Roman",  12), fg= "gray").pack(pady= 20)
            
            # Show available courses for registration
            tk.Label(  main_frame, text= "Available courses: ",  
                    font= ("Times New Roman",  12, "bold")).pack(pady= (20, 10))
            
            all_courses =  db.readallcourses()
            if all_courses: 
                for course in all_courses: 
                    tk.Label(  main_frame, text= f"• {course['course_id']} - {course['course_name']}",  
                            font= ("Times New Roman",  10)).pack(anchor= 'w', padx= 20)
    
    # Create selection window
    view_window =  tk.Toplevel(root)
    view_window.title("View Student Courses")
    view_window.geometry("450x350")
    
    tk.Label(  view_window, text= "Select a student to view their courses: ",  
            font= ("Times New Roman",  12)).pack(pady= 10)
    
    # Create listbox with scrollbar
    listbox_frame =  tk.Frame(view_window)
    listbox_frame.pack(fill= 'both', expand= True, padx= 20, pady= 10)
    
    student_listbox =  tk.Listbox(listbox_frame, height= 12)
    scrollbar =  tk.Scrollbar(listbox_frame, orient= "vertical")
    student_listbox.config(yscrollcommand= scrollbar.set)
    scrollbar.config(command= student_listbox.yview)
    
    student_listbox.pack(side= "left",  fill= "both",  expand= True)
    scrollbar.pack(side= "right",  fill= "y")
    
    # Load students
    students_list =  db.readallstudents()
    for student in students_list: 
        student_listbox.insert(tk.END, f"{student['student_id']} - {student['name']} ({student['email']})")
    
    # Buttons
    button_frame =  tk.Frame(view_window)
    button_frame.pack(pady= 10)
    
    tk.Button(button_frame, text= "View Courses",  command= show_courses, 
             bg= "purple",  fg= "white",  font= ("Times New Roman",  10)).pack(side= 'left', padx= 5)
    tk.Button(button_frame, text= "Close",  command= view_window.destroy, 
             bg= "gray",  fg= "white",  font= ("Times New Roman",  10)).pack(side= 'left', padx= 5)

def  delete_instructor(): 
    """Delete selected instructor"""
    def  on_instructor_delete(): 
        selected =  instructor_listbox.curselection()
        if not selected: 
            messagebox.showerror("Error",  "Please select an instructor to delete")
            return
        
        instructor_data =  instructors_list[selected[0]]
        
        if messagebox.askyesno("Confirm Delete",  f"Are you sure you want to delete instructor {instructor_data['name']}?"): 
            ok =  db.deleteinstructorfromdb(instructor_data['instructor_id'])
            if ok: 
                messagebox.showinfo("Success",  "Instructor deleted successfully!")
                refresh_data_display()
                delete_window.destroy()
            else: 
                messagebox.showerror("Error",  "Failed to delete instructor")
    
    delete_window =  tk.Toplevel(root)
    delete_window.title("Delete Instructor")
    delete_window.geometry("400x300")
    
    tk.Label(  delete_window, text= "Select an instructor to delete: ",  font= ("Times New Roman",  12)).pack(pady= 10)
    
    instructor_listbox =  tk.Listbox(delete_window, height= 10)
    instructor_listbox.pack(fill= 'both', expand= True, padx= 20, pady= 10)
    
    instructors_list =  db.readallinstructors()
    for instructor in instructors_list: 
        instructor_listbox.insert(tk.END, f"{instructor['instructor_id']} - {instructor['name']}")
    
    tk.Button(delete_window, text= "Delete Selected",  command= on_instructor_delete, bg= "red",  fg= "white").pack(pady= 10)
def view_course_students(): 
    """View students for selected course"""
    def show_students(): 
        selected =  course_listbox.curselection()
        if not selected: 
            messagebox.showerror("Error",  "Please select a course")
            return
        
        course_data =  courses_list[selected[0]]
        print(f"Debug:  Looking for students in course ID:  {course_data['course_id']}")
        
        # Getring students from database
        students =  db.gettingcoursestudents(course_data['course_id'])
        print(f"Debug:  Found {len(students)} students")
        
        students_window =  tk.Toplevel(root)
        students_window.title(f"Students in {course_data['course_name']}")
        students_window.geometry("700x400")
        
        # Header
        header_frame =  tk.Frame(students_window)
        header_frame.pack(fill= 'x', padx= 10, pady= 10)
        tk.Label(  header_frame, text= f"Students in {course_data['course_name']}",  
                font= ("Times New Roman",  14, "bold")).pack()
        
        # Create scrollable frame for students
        main_frame =  tk.Frame(students_window)
        main_frame.pack(fill= 'both', expand= True, padx= 10, pady= 10)
        
        if students: 
            # Headers
            header_frame =  tk.Frame(main_frame, bg= "gray90")
            header_frame.pack(fill= 'x', pady= (0, 5))
            tk.Label(  header_frame, text= "Student ID",  width= 12, font= ("Times New Roman",  10, "bold"), 
                    bg= "gray90").pack(side= 'left', padx= 5)
            tk.Label(  header_frame, text= "Name",  width= 20, font= ("Times New Roman",  10, "bold"), 
                    bg= "gray90").pack(side= 'left', padx= 5)
            tk.Label(  header_frame, text= "Email",  width= 25, font= ("Times New Roman",  10, "bold"), 
                    bg= "gray90").pack(side= 'left', padx= 5)
            tk.Label(  header_frame, text= "Registration Date",  width= 18, font= ("Times New Roman",  10, "bold"), 
                    bg= "gray90").pack(side= 'left', padx= 5)
            
            # Student rows
            for student in students: 
                row_frame =  tk.Frame(main_frame, relief= "raised",  bd= 1)
                row_frame.pack(fill= 'x', pady= 2)
                
                tk.Label(  row_frame, text= student['student_id'], width= 12, anchor= 'w', 
                        font= ("Times New Roman",  10)).pack(side= 'left', padx= 5, pady=  5)
                tk.Label(  row_frame, text= student['name'], width= 20, anchor= 'w', 
                        font= ("Times New Roman",  10)).pack(side= 'left', padx= 5, pady=  5)
                tk.Label(  row_frame, text= student['email'], width= 25, anchor= 'w', 
                        font= ("Times New Roman",  10)).pack(side= 'left', padx= 5, pady=  5)
                
                # Format registration date
                reg_date =  student.get('registration_date', 'N/A')
                if reg_date and reg_date !=  'N/A': 
                    try: 
                        if 'T' in str(reg_date): 
                            reg_date =  str(reg_date).split('T')[0]
                    except: 
                        reg_date =  str(reg_date)[: 10] if len(str(reg_date)) > 10 else str(reg_date)
                
                tk.Label(  row_frame, text= reg_date, width= 18, anchor= 'w', 
                        font= ("Times New Roman",  10)).pack(side= 'left', padx= 5, pady=  5)
        else: 
            tk.Label(  main_frame, text= "No students are registered for this course.",  
                    font= ("Times New Roman",  12), fg= "gray").pack(pady= 20)
            
            # Show available students
            tk.Label(  main_frame, text= "Available students: ",  
                    font= ("Times New Roman",  12, "bold")).pack(pady= (20, 10))
            
            all_students =  db.readallstudents()
            if all_students: 
                for student in all_students[: 10]:   # Show first 10 students
                    tk.Label(  main_frame, text= f"• {student['student_id']} - {student['name']}",  
                            font= ("Times New Roman",  10)).pack(anchor= 'w', padx= 20)
    
    # Create selection window
    view_window =  tk.Toplevel(root)
    view_window.title("View Course Students")
    view_window.geometry("450x350")
    
    tk.Label(  view_window, text= "Select a course to view its students: ",  
            font= ("Times New Roman",  12)).pack(pady= 10)
    
    # Create listbox with scrollbar
    listbox_frame =  tk.Frame(view_window)
    listbox_frame.pack(fill= 'both', expand= True, padx= 20, pady= 10)
    
    course_listbox =  tk.Listbox(listbox_frame, height= 12)
    scrollbar =  tk.Scrollbar(listbox_frame, orient= "vertical")
    course_listbox.config(yscrollcommand= scrollbar.set)
    scrollbar.config(command= course_listbox.yview)
    
    course_listbox.pack(side= "left",  fill= "both",  expand= True)
    scrollbar.pack(side= "right",  fill= "y")
    
    # Load courses
    courses_list =  db.readallcourses()
    for course in courses_list: 
        instructor_name =  course.get('instructor_name', 'Unassigned')
        course_listbox.insert(tk.END, f"{course['course_id']} - {course['course_name']} (Instructor:  {instructor_name})")
    
    # Buttons
    button_frame =  tk.Frame(view_window)
    button_frame.pack(pady= 10)
    
    tk.Button(button_frame, text= "View Students",  command= show_students, 
             bg= "purple",  fg= "white",  font= ("Times New Roman",  10)).pack(side= 'left', padx= 5)
    tk.Button(button_frame, text= "Close",  command= view_window.destroy, 
             bg= "gray",  fg= "white",  font= ("Times New Roman",  10)).pack(side= 'left', padx= 5)

# Create main window
root =  tk.Tk()
root.title ("School Management System")
root.geometry("1200x800")
# Create main container with two sides
main_container =  tk.Frame(root)
main_container.pack(fill= 'both', expand= True, padx= 10, pady= 10)
# Left side - Forms
forms_scrollable_frame =  tk.Frame(main_container, width= 400)
forms_scrollable_frame.pack(side= 'left', fill= 'y', padx= (0, 10))
forms_scrollable_frame.pack_propagate(False) 
# Make forms frame scrollable
forms_canvas =  tk.Canvas(forms_scrollable_frame)
forms_scrollbar =  tk.Scrollbar(forms_scrollable_frame, orient= "vertical",  command= forms_canvas.yview)
forms_scrollable_frame =  tk.Frame(forms_canvas)

forms_scrollable_frame.bind(
    "<Configure>", 
    lambda e:  forms_canvas.configure(scrollregion= forms_canvas.bbox("all"))
)

forms_canvas.create_window((0, 0), window= forms_scrollable_frame, anchor= "nw")
forms_canvas.configure(yscrollcommand= forms_scrollbar.set)

forms_canvas.pack(side= "left",  fill= "both",  expand= True)
forms_scrollbar.pack(side= "right",  fill= "y")
data_frame =  tk.Frame(main_container, bg= 'white', relief= 'sunken', bd= 2)
data_frame.pack(side= 'right', fill= 'both', expand= True)
data_header =  tk.Label(  data_frame, text= "CURRENT DATA",  font= ("Times New Roman",  14, "bold"), bg= "lightgray")
data_header.pack(fill= 'x', pady= (0, 5))
data_canvas =  tk.Canvas(data_frame)
data_scrollbar =  tk.Scrollbar(data_frame, orient= "vertical",  command= data_canvas.yview)
data_scrollable_frame =  tk.Frame(data_canvas)

data_scrollable_frame.bind(
    "<Configure>", 
    lambda e:  data_canvas.configure(scrollregion= data_canvas.bbox("all"))
)

data_canvas.create_window((0, 0), window= data_scrollable_frame, anchor= "nw")
data_canvas.configure(yscrollcommand= data_scrollbar.set)

data_canvas.pack(side= "left",  fill= "both",  expand= True)
data_scrollbar.pack(side= "right",  fill= "y")

# Student Form
student_fr =  tk.LabelFrame(forms_scrollable_frame, text= "Student Form",  bg= '#f0f0f0', font= ("Times New Roman",  10, "bold"))
student_fr.pack(fill= 'x', pady=  5)

tag1 =  tk.Label(  student_fr, text= "Name: ")
tag1.grid(row= 0, column= 0, padx= 5, pady= 5, sticky= 'w')
name_input =  tk.Entry(student_fr, bg= "white",  fg= "black",  font= ("Times New Roman",  11))
name_input.grid(row= 0, column= 1, padx= 5, pady= 5, sticky= 'ew')

tag2 =  tk.Label(  student_fr, text= "Age: ")
tag2.grid(row= 1, column= 0, padx= 5, pady= 5, sticky= 'w')
ag_input =  tk.Entry(student_fr, bg= "white",  fg= "black",  font= ("Times New Roman",  11))
ag_input.grid(row= 1, column= 1, padx= 5, pady= 5, sticky= 'ew')

tag3 =  tk.Label(  student_fr, text= "Email: ")
tag3.grid(row= 2, column= 0, padx= 5, pady= 5, sticky= 'w')
e_input =  tk.Entry(student_fr, bg= "white",  fg= "black",  font= ("Times New Roman",  11))
e_input.grid(row= 2, column= 1, padx= 5, pady= 5, sticky= 'ew')

tag4 =  tk.Label(  student_fr, text= "Student ID: ")
tag4.grid(row= 3, column= 0, padx= 5, pady= 5, sticky= 'w')
sid_input =  tk.Entry(student_fr, bg= "white",  fg= "black",  font= ("Times New Roman",  11))
sid_input.grid(row= 3, column= 1, padx= 5, pady= 5, sticky= 'ew')

submitbtn1 =  tk.Button(student_fr, text= "Submit",  font= ("Times New Roman",  8), command= add_student)
submitbtn1.grid(row= 4, column= 1, padx= 5, pady= 5, sticky= 'e')

# Configure grid weights for student form
student_fr.columnconfigure(1, weight= 1)

# Register Student to Course
register_fr =  tk.LabelFrame(forms_scrollable_frame, text= "Register Student to Course",  bg= '#f0f0f0', font= ("Times New Roman",  10, "bold"))
register_fr.pack(fill= 'x', pady=  5)

tag5 =  tk.Label(  register_fr, text= "Student ID: ")
tag5.grid(row= 0, column= 0, padx= 5, pady= 5, sticky= 'w')
sid2_input =  tk.Entry(register_fr, bg= "white",  fg= "black",  font= ("Times New Roman",  11))
sid2_input.grid(row= 0, column= 1, padx= 5, pady= 5, sticky= 'ew')

tag6 =  tk.Label(  register_fr, text= "Course ID: ")
tag6.grid(row= 1, column= 0, padx= 5, pady= 5, sticky= 'w')
cid_input =  tk.Entry(register_fr, bg= "white",  fg= "black",  font= ("Times New Roman",  11))
cid_input.grid(row= 1, column= 1, padx= 5, pady= 5, sticky= 'ew')

submitbtn2 =  tk.Button(register_fr, text= "Submit",   font= ("Times New Roman",  8), command= register_student)
submitbtn2.grid(row= 2, column= 1, padx= 5, pady= 5, sticky= 'e')

register_fr.columnconfigure(1, weight= 1)

# Instructor Form
instructor_fr =  tk.LabelFrame(forms_scrollable_frame, text= "Instructor Form",  bg= '#f0f0f0', font= ("Times New Roman",  10, "bold"))
instructor_fr.pack(fill= 'x', pady=  5)

tag7 =  tk.Label(  instructor_fr, text= "Name: ")
tag7.grid(row= 0, column= 0, padx= 5, pady= 5, sticky= 'w')
ninput =  tk.Entry(instructor_fr, bg= "white",  fg= "black",  font= ("Times New Roman",  11))
ninput.grid(row= 0, column= 1, padx= 5, pady= 5, sticky= 'ew')

tag8 =  tk.Label(  instructor_fr, text= "Age: ")
tag8.grid(row= 1, column= 0, padx= 5, pady= 5, sticky= 'w')
aginput =  tk.Entry(instructor_fr, bg= "white",  fg= "black",  font= ("Times New Roman",  11))
aginput.grid(row= 1, column= 1, padx= 5, pady= 5, sticky= 'ew')

tag9 =  tk.Label(  instructor_fr, text= "Email: ")
tag9.grid(row= 2, column= 0, padx= 5, pady= 5, sticky= 'w')
e2input =  tk.Entry(instructor_fr, bg= "white",  fg= "black",  font= ("Times New Roman",  11))
e2input.grid(row= 2, column= 1, padx= 5, pady= 5, sticky= 'ew')

tag10 =  tk.Label(  instructor_fr, text= "Instructor ID: ")
tag10.grid(row= 3, column= 0, padx= 5, pady= 5, sticky= 'w')
iidinput =  tk.Entry(instructor_fr, bg= "white",  fg= "black",  font= ("Times New Roman",  11))
iidinput.grid(row= 3, column= 1, padx= 5, pady= 5, sticky= 'ew')
submitbtn3 =  tk.Button(instructor_fr, text= "Submit",  font= ("Times New Roman",  8), command= add_instructor)
submitbtn3.grid(row= 4, column= 1, padx= 5, pady= 5, sticky= 'e')
instructor_fr.columnconfigure(1, weight= 1)
# Assign Instructor to Course
course_prof =  tk.LabelFrame(forms_scrollable_frame, text= "Assign Instructor to Course",  bg= '#f0f0f0', font= ("Times New Roman",  10, "bold"))
course_prof.pack(fill= 'x', pady=  5)
tag11 =  tk.Label(  course_prof, text= "Instructor ID: ")
tag11.grid(row= 0, column= 0, padx= 5, pady= 5, sticky= 'w')
iid2input =  tk.Entry(course_prof, bg= "white",  fg= "black",  font= ("Times New Roman",  11))
iid2input.grid(row= 0, column= 1, padx= 5, pady= 5, sticky= 'ew')
tag12 =  tk.Label(  course_prof, text= "Course ID: ")
tag12.grid(row= 1, column= 0, padx= 5, pady= 5, sticky= 'w')
cid2input =  tk.Entry(course_prof, bg= "white",  fg= "black",  font= ("Times New Roman",  11))
cid2input.grid(row= 1, column= 1, padx= 5, pady= 5, sticky= 'ew')
submitbtn4 =  tk.Button(course_prof, text= "Submit",  font= ("Times New Roman",  8), command= assigning_instructor)
submitbtn4.grid(row= 2, column= 1, padx= 5, pady= 5, sticky= 'e')
course_prof.columnconfigure(1, weight= 1)
# Course Form
course_form =  tk.LabelFrame(forms_scrollable_frame, text= "Course Form",  bg= '#f0f0f0', font= ("Times New Roman",  10, "bold"))
course_form.pack(fill= 'x', pady=  5)
tag13 =  tk.Label(  course_form, text= "Course ID: ")
tag13.grid(row= 0, column= 0, padx= 5, pady= 5, sticky= 'w')
cid3input =  tk.Entry(course_form, bg= "white",  fg= "black",  font= ("Times New Roman",  11))
cid3input.grid(row= 0, column= 1, padx= 5, pady= 5, sticky= 'ew')

tag14 =  tk.Label(  course_form, text= "Course Name: ")
tag14.grid(row= 1, column= 0, padx= 5, pady= 5, sticky= 'w')
crs_input =  tk.Entry(course_form, bg= "white",  fg= "black",  font= ("Times New Roman",  11))
crs_input.grid(row= 1, column= 1, padx= 5, pady= 5, sticky= 'ew')

submitbtn5 =  tk.Button(course_form, text= "Submit",   font= ("Times New Roman",  8), command= add_course)
submitbtn5.grid(row= 2, column= 1, padx= 5, pady= 5, sticky= 'e')

course_form.columnconfigure(1, weight= 1)

# Action Buttons Frame
actions_frame =  tk.LabelFrame(forms_scrollable_frame, text= "Actions",  bg= '#f0f0f0', font= ("Times New Roman",  10, "bold"))
actions_frame.pack(fill= 'x', pady=  5)

# Student actions
student_actions =  tk.Frame(actions_frame)
student_actions.pack(fill= 'x', padx= 5, pady=  5)
tk.Label(  student_actions, text= "Student Actions: ",  font= ("Times New Roman",  9, "bold")).pack(anchor= 'w')

student_btn_frame =  tk.Frame(student_actions)
student_btn_frame.pack(fill= 'x')
tk.Button(student_btn_frame, text= "Edit Student",  command= edit_student, fg= "black",  font= ("Times New Roman",  8)).pack(side= 'left', padx= 2, pady= 2)
tk.Button(student_btn_frame, text= "Delete Student",  command= delete_student, fg= "black",  font= ("Times New Roman",  8)).pack(side= 'left', padx= 2, pady= 2)
tk.Button(student_btn_frame, text= "View Student Courses",  command= view_student_courses,  fg= "black",  font= ("Times New Roman",  8)).pack(side= 'left', padx= 2, pady= 2)
instructor_actions =  tk.Frame(actions_frame)
instructor_actions.pack(fill= 'x', padx= 5, pady=  5)
tk.Label(  instructor_actions, text= "Instructor Actions: ",  font= ("Times New Roman",  9, "bold")).pack(anchor= 'w')
instructor_btn_frame =  tk.Frame(instructor_actions)
instructor_btn_frame.pack(fill= 'x')
tk.Button(instructor_btn_frame, text= "Edit Instructor",  command= edit_instructor,   fg= "black",  font= ("Times New Roman",  8)).pack(side= 'left', padx= 2, pady= 2)
tk.Button(instructor_btn_frame, text= "Delete Instructor",  command= delete_instructor,  fg= "black",  font= ("Times New Roman",  8)).pack(side= 'left', padx= 2, pady= 2)
course_actions =  tk.Frame(actions_frame)
course_actions.pack(fill= 'x', padx= 5, pady=  5)
tk.Label(  course_actions, text= "Course Actions: ",  font= ("Times New Roman",  9, "bold")).pack(anchor= 'w')
course_btn_frame =  tk.Frame(course_actions)
course_btn_frame.pack(fill= 'x')
tk.Button(course_btn_frame, text= "View Course Students",  command= view_course_students,   fg= "black",  font= ("Times New Roman",  8)).pack(side= 'left', padx= 2, pady= 2)

# Build initial data display
building_display()

root.mainloop()