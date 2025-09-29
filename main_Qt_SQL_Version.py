"""
School Management System - Main GUI Application Module

This module contains the main PyQt5 GUI application for managing students, instructors, 
and courses in a school database system. It provides a comprehensive interface for 
CRUD operations and relationship management.

:author: Your Name
:version: 1.0.0
:date: 2025
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Data_Management import DatabaseBoss
from Student import Student
from Instructor import Instructor
from Course import Course


class SelectionDialog(QDialog):
    """
    A dialog window for selecting items from a list of data objects.
    
    This dialog provides a user-friendly interface for selecting students, 
    instructors, or courses from the database with proper display formatting.
    
    :param title: The window title for the dialog
    :type title: str
    :param data_list: List of dictionaries containing the data to display
    :type data_list: list
    :param data_type: Type of data being displayed ("student", "instructor", "course")
    :type data_type: str
    :param parent: Parent widget, defaults to None
    :type parent: QWidget, optional
    """
    
    def __init__(self, title, data_list, data_type, parent=None):
        """
        Initialize the selection dialog with data and configuration.
        
        :param title: Dialog window title
        :type title: str
        :param data_list: List of data dictionaries to display
        :type data_list: list
        :param data_type: Type of data ("student", "instructor", "course")  
        :type data_type: str
        :param parent: Parent widget, defaults to None
        :type parent: QWidget, optional
        """
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setGeometry(200, 200, 500, 400)
        self.data_list = data_list
        self.selected_data = None
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Select a {data_type}:"))
        
        self.list_widget = QListWidget()
        for item in data_list:
            if data_type == "student":
                text = f"{item['student_id']} - {item['name']}"
            elif data_type == "instructor":
                text = f"{item['instructor_id']} - {item['name']}"
            else:  # course
                text = f"{item['course_id']} - {item['course_name']}"
            self.list_widget.addItem(text)
        layout.addWidget(self.list_widget)
        
        btn_layout = QHBoxLayout()
        select_btn = QPushButton("Select")
        select_btn.clicked.connect(self.accept_selection)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(select_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def accept_selection(self):
        """
        Handle the selection acceptance when user clicks Select button.
        
        Validates that an item is selected and stores the selected data.
        Shows warning message if no item is selected.
        
        :raises: Shows QMessageBox warning if no selection made
        """
        row = self.list_widget.currentRow()
        if row >= 0:
            self.selected_data = self.data_list[row]
            self.accept()
        else:
            QMessageBox.warning(self, "No Selection", "Please select an item.")
    
    def get_selected_data(self):
        """
        Retrieve the selected data object.
        
        :return: The selected data dictionary or None if nothing selected
        :rtype: dict or None
        """
        return self.selected_data


class SchoolManagementSystem(QMainWindow):
    """
    Main application window for the School Management System.
    
    This class provides a comprehensive GUI interface for managing school data
    including students, instructors, courses, and their relationships. It handles
    all CRUD operations, data display, and user interactions.
    
    The interface is split into two main sections:
    - Left side: Forms for data entry and actions
    - Right side: Current data display with real-time updates
    
    :ivar db: Database connection and operations handler
    :vartype db: DatabaseBoss
    :ivar editing_student: Flag indicating if currently editing a student
    :vartype editing_student: bool
    :ivar editing_instructor: Flag indicating if currently editing an instructor  
    :vartype editing_instructor: bool
    :ivar original_id: Stores original ID during edit operations
    :vartype original_id: str or None
    """
    
    def __init__(self):
        """
        Initialize the main application window.
        
        Sets up the database connection, initializes UI components,
        and loads initial data display.
        """
        super().__init__()
        self.db = DatabaseBoss()
        self.editing_student = False
        self.editing_instructor = False
        self.original_id = None
        self.init_ui()
        self.refreshing_the_data()
        
    def init_ui(self):
        """
        Initialize the user interface layout and components.
        
        Creates the main window layout with:
        - Splitter for left/right sections
        - Forms section on the left
        - Data display section on the right
        - Proper sizing and stretch factors
        """
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 1200, 800)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left side - Forms
        forms_scroll = QScrollArea()
        forms_scroll.setWidgetResizable(True)
        forms_scroll.setMaximumWidth(400)
        forms_widget = QWidget()
        forms_scroll.setWidget(forms_widget)
        self.forms_layout = QVBoxLayout(forms_widget)
        self.creating_the_forms()
        splitter.addWidget(forms_scroll)
        
        # Right side - Data
        data_scroll = QScrollArea()
        data_scroll.setWidgetResizable(True)
        self.data_widget = QWidget()
        data_scroll.setWidget(self.data_widget)
        self.data_layout = QVBoxLayout(self.data_widget)
        splitter.addWidget(data_scroll)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
    
    def creating_the_forms(self):
        """
        Create all input forms and action buttons in the left panel.
        
        Sets up the following form sections:
        - Student Form: Add/edit student information
        - Registration Form: Register students to courses
        - Instructor Form: Add/edit instructor information  
        - Assignment Form: Assign instructors to courses
        - Course Form: Add new courses
        - Actions Section: Edit, delete, and view operations
        - Export Actions: JSON export, database backup, refresh
        """
        # Student Form
        student_group = QGroupBox("Student Form")
        student_layout = QFormLayout()
        self.student_inputs = {
            'name': QLineEdit(),
            'age': QLineEdit(),
            'email': QLineEdit(),
            'id': QLineEdit()
        }
        student_layout.addRow("Name:", self.student_inputs['name'])
        student_layout.addRow("Age:", self.student_inputs['age'])
        student_layout.addRow("Email:", self.student_inputs['email'])
        student_layout.addRow("ID:", self.student_inputs['id'])
        
        self.student_btn = QPushButton("Submit")
        self.student_btn.clicked.connect(self.handle_student)
        student_layout.addRow("", self.student_btn)
        student_group.setLayout(student_layout)
        self.forms_layout.addWidget(student_group)
        
        # Registration Form
        reg_group = QGroupBox("Register Student to Course")
        reg_layout = QFormLayout()
        self.reg_inputs = {'student_id': QLineEdit(), 'course_id': QLineEdit()}
        reg_layout.addRow("Student ID:", self.reg_inputs['student_id'])
        reg_layout.addRow("Course ID:", self.reg_inputs['course_id'])
        reg_btn = QPushButton("Register")
        reg_btn.clicked.connect(self.register_student)
        reg_layout.addRow("", reg_btn)
        reg_group.setLayout(reg_layout)
        self.forms_layout.addWidget(reg_group)
        
        # Instructor Form
        instructor_group = QGroupBox("Instructor Form")
        instructor_layout = QFormLayout()
        self.instructor_inputs = {
            'name': QLineEdit(),
            'age': QLineEdit(),
            'email': QLineEdit(),
            'id': QLineEdit()
        }
        instructor_layout.addRow("Name:", self.instructor_inputs['name'])
        instructor_layout.addRow("Age:", self.instructor_inputs['age'])
        instructor_layout.addRow("Email:", self.instructor_inputs['email'])
        instructor_layout.addRow("ID:", self.instructor_inputs['id'])
        
        self.instructor_btn = QPushButton("Submit")
        self.instructor_btn.clicked.connect(self.handle_instructor)
        instructor_layout.addRow("", self.instructor_btn)
        instructor_group.setLayout(instructor_layout)
        self.forms_layout.addWidget(instructor_group)
        
        # Assignment Form
        assign_group = QGroupBox("Assign Instructor to Course")
        assign_layout = QFormLayout()
        self.assign_inputs = {'instructor_id': QLineEdit(), 'course_id': QLineEdit()}
        assign_layout.addRow("Instructor ID:", self.assign_inputs['instructor_id'])
        assign_layout.addRow("Course ID:", self.assign_inputs['course_id'])
        assign_btn = QPushButton("Assign")
        assign_btn.clicked.connect(self.assign_instructor)
        assign_layout.addRow("", assign_btn)
        assign_group.setLayout(assign_layout)
        self.forms_layout.addWidget(assign_group)
        
        # Course Form
        course_group = QGroupBox("Course Form")
        course_layout = QFormLayout()
        self.course_inputs = {'id': QLineEdit(), 'name': QLineEdit()}
        course_layout.addRow("Course ID:", self.course_inputs['id'])
        course_layout.addRow("Course Name:", self.course_inputs['name'])
        course_btn = QPushButton("Add Course")
        course_btn.clicked.connect(self.add_course)
        course_layout.addRow("", course_btn)
        course_group.setLayout(course_layout)
        self.forms_layout.addWidget(course_group)
        
        # Actions
        actions_group = QGroupBox("Actions")
        actions_layout = QVBoxLayout()
        actions_layout.addWidget(QLabel("Student Actions:"))
        student_actions = QHBoxLayout()
        btn_edit_student = QPushButton("Edit")
        btn_edit_student.clicked.connect(self.edit_student)
        btn_delete_student = QPushButton("Delete")
        btn_delete_student.clicked.connect(self.delete_student)
        btn_view_courses = QPushButton("View Courses")
        btn_view_courses.clicked.connect(self.view_student_courses)
        student_actions.addWidget(btn_edit_student)
        student_actions.addWidget(btn_delete_student)
        student_actions.addWidget(btn_view_courses)
        actions_layout.addLayout(student_actions)
        
        # Instructor actions
        actions_layout.addWidget(QLabel("Instructor Actions:"))
        instructor_actions = QHBoxLayout()
        btn_edit_instructor = QPushButton("Edit")
        btn_edit_instructor.clicked.connect(self.edit_instructor)
        btn_delete_instructor = QPushButton("Delete")
        btn_delete_instructor.clicked.connect(self.delete_instructor)
        instructor_actions.addWidget(btn_edit_instructor)
        instructor_actions.addWidget(btn_delete_instructor)
        actions_layout.addLayout(instructor_actions)
        
        # Course actions
        actions_layout.addWidget(QLabel("Course Actions:"))
        btn_view_students = QPushButton("View Students")
        btn_view_students.clicked.connect(self.view_course_students)
        actions_layout.addWidget(btn_view_students)
        
        # Export actions
        export_actions = QHBoxLayout()
        btn_export = QPushButton("Export JSON")
        btn_export.clicked.connect(self.export_json)
        btn_backup = QPushButton("Backup DB")
        btn_backup.clicked.connect(self.backup_db)
        btn_refresh = QPushButton("Refresh")
        btn_refresh.clicked.connect(self.refreshing_the_data)
        export_actions.addWidget(btn_export)
        export_actions.addWidget(btn_backup)
        export_actions.addWidget(btn_refresh)
        actions_layout.addLayout(export_actions)
        
        actions_group.setLayout(actions_layout)
        self.forms_layout.addWidget(actions_group)
    
    def validate_inputs(self, inputs):
        """
        Validate that all required input fields contain data.
        
        :param inputs: Dictionary of field names and their values
        :type inputs: dict
        :return: True if all fields valid, False otherwise
        :rtype: bool
        :raises: Shows QMessageBox critical error for empty fields
        """
        for field, value in inputs.items():
            if not value.strip():
                QMessageBox.critical(self, "Error", f"{field} cannot be empty!")
                return False
        return True
    
    def validate_age(self, age_str):
        """
        Validate and convert age string to integer.
        
        :param age_str: Age value as string from input field
        :type age_str: str
        :return: Valid age as integer or None if invalid
        :rtype: int or None
        :raises: Shows QMessageBox critical error for invalid age
        """
        try:
            age = int(age_str.strip())
            if age <= 0:
                QMessageBox.critical(self, "Error", "Age must be positive!")
                return None
            return age
        except ValueError:
            QMessageBox.critical(self, "Error", "Age must be a number!")
            return None
    
    def clear_inputs(self, inputs_dict):
        """
        Clear all input fields in the given dictionary.
        
        :param inputs_dict: Dictionary of input widgets to clear
        :type inputs_dict: dict
        """
        for inp in inputs_dict.values():
            inp.clear()
    
    def handle_student(self):
        """
        Handle student form submission for both add and update operations.
        
        Routes to appropriate method based on current editing state.
        """
        if self.editing_student:
            self.update_student()
        else:
            self.add_student()
    
    def add_student(self):
        """
        Add a new student to the database.
        
        Validates input data, creates Student object, and saves to database.
        Shows success/error messages and refreshes data display on success.
        
        :raises: Shows QMessageBox for validation errors or database failures
        """
        inputs = {k: v.text() for k, v in self.student_inputs.items()}
        if not self.validate_inputs(inputs):
            return
        
        age = self.validate_age(inputs['age'])
        if age is None:
            return
        
        student = Student(inputs['id'], inputs['name'], age, inputs['email'])
        if self.db.createnewstudent(student.id, student.name, student.age, student._email):
            QMessageBox.information(self, "Success", f"Student {inputs['name']} added!")
            self.clear_inputs(self.student_inputs)
            self.refreshing_the_data()
        else:
            QMessageBox.critical(self, "Error", f"Failed to add student. ID {inputs['id']} might exist.")
    
    def edit_student(self):
        """
        Initiate student editing by showing selection dialog.
        
        Displays dialog to select student, then populates form fields
        with existing data and switches to edit mode.
        """
        dialog = SelectionDialog("Edit Student", self.db.readallstudents(), "student")
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_selected_data()
            if data:
                self.student_inputs['name'].setText(data['name'])
                self.student_inputs['age'].setText(str(data['age']))
                self.student_inputs['email'].setText(data['email'])
                self.student_inputs['id'].setText(data['student_id'])
                self.student_inputs['id'].setEnabled(False)
                self.student_btn.setText("Update")
                self.editing_student = True
                self.original_id = data['student_id']
    
    def update_student(self):
        """
        Update existing student information in the database.
        
        Validates input data and updates student record using original ID.
        Resets form to add mode and refreshes display on success.
        
        :raises: Shows QMessageBox for validation errors or database failures
        """
        inputs = {k: v.text() for k, v in self.student_inputs.items()}
        if not self.validate_inputs({k: v for k, v in inputs.items() if k != 'id'}):
            return
        
        age = self.validate_age(inputs['age'])
        if age is None:
            return
        
        if self.db.updatestudent(self.original_id, inputs['name'], age, inputs['email']):
            QMessageBox.information(self, "Success", "Student updated!")
            self.reset_student_form()
            self.refreshing_the_data()
        else:
            QMessageBox.critical(self, "Error", "Failed to update student")
    
    def reset_student_form(self):
        """
        Reset student form to add mode.
        
        Clears all fields, enables ID field, resets button text,
        and clears editing flags.
        """
        self.clear_inputs(self.student_inputs)
        self.student_inputs['id'].setEnabled(True)
        self.student_btn.setText("Submit")
        self.editing_student = False
        self.original_id = None
    
    def delete_student(self):
        """
        Delete a student from the database after confirmation.
        
        Shows selection dialog, confirms deletion with user,
        then removes student and refreshes display.
        
        :raises: Shows QMessageBox for confirmation and result feedback
        """
        dialog = SelectionDialog("Delete Student", self.db.readallstudents(), "student")
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_selected_data()
            if data:
                reply = QMessageBox.question(self, 'Confirm', f"Delete {data['name']}?")
                if reply == QMessageBox.Yes:
                    if self.db.deletestudentfromdb(data['student_id']):
                        QMessageBox.information(self, "Success", "Student deleted!")
                        self.refreshing_the_data()
    
    def handle_instructor(self):
        """
        Handle instructor form submission for both add and update operations.
        
        Routes to appropriate method based on current editing state.
        """
        if self.editing_instructor:
            self.update_instructor()
        else:
            self.add_instructor()
    
    def add_instructor(self):
        """
        Add a new instructor to the database.
        
        Validates input data, creates Instructor object, and saves to database.
        Shows success/error messages and refreshes data display on success.
        
        :raises: Shows QMessageBox for validation errors or database failures
        """
        inputs = {k: v.text() for k, v in self.instructor_inputs.items()}
        if not self.validate_inputs(inputs):
            return
        
        age = self.validate_age(inputs['age'])
        if age is None:
            return
        
        instructor = Instructor(inputs['id'], inputs['name'], age, inputs['email'])
        if self.db.createinstructor(instructor.instructor_id, instructor.name, instructor.age, instructor._email):
            QMessageBox.information(self, "Success", f"Instructor {inputs['name']} added!")
            self.clear_inputs(self.instructor_inputs)
            self.refreshing_the_data()
        else:
            QMessageBox.critical(self, "Error", f"Failed to add instructor. ID {inputs['id']} might exist.")
    
    def edit_instructor(self):
        """
        Initiate instructor editing by showing selection dialog.
        
        Displays dialog to select instructor, then populates form fields
        with existing data and switches to edit mode.
        """
        dialog = SelectionDialog("Edit Instructor", self.db.readallinstructors(), "instructor")
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_selected_data()
            if data:
                self.instructor_inputs['name'].setText(data['name'])
                self.instructor_inputs['age'].setText(str(data['age']))
                self.instructor_inputs['email'].setText(data['email'])
                self.instructor_inputs['id'].setText(data['instructor_id'])
                self.instructor_inputs['id'].setEnabled(False)
                self.instructor_btn.setText("Update")
                self.editing_instructor = True
                self.original_id = data['instructor_id']
    
    def update_instructor(self):
        """
        Update existing instructor information in the database.
        
        Validates input data and updates instructor record using original ID.
        Resets form to add mode and refreshes display on success.
        
        :raises: Shows QMessageBox for validation errors or database failures
        """
        inputs = {k: v.text() for k, v in self.instructor_inputs.items()}
        if not self.validate_inputs({k: v for k, v in inputs.items() if k != 'id'}):
            return
        
        age = self.validate_age(inputs['age'])
        if age is None:
            return
        
        if self.db.updateinstructor(self.original_id, inputs['name'], age, inputs['email']):
            QMessageBox.information(self, "Success", "Instructor updated!")
            self.reset_instructor_form()
            self.refreshing_the_data()
        else:
            QMessageBox.critical(self, "Error", "Failed to update instructor")
    
    def reset_instructor_form(self):
        """
        Reset instructor form to add mode.
        
        Clears all fields, enables ID field, resets button text,
        and clears editing flags.
        """
        self.clear_inputs(self.instructor_inputs)
        self.instructor_inputs['id'].setEnabled(True)
        self.instructor_btn.setText("Submit")
        self.editing_instructor = False
        self.original_id = None
    
    def delete_instructor(self):
        """
        Delete an instructor from the database after confirmation.
        
        Shows selection dialog, confirms deletion with user,
        then removes instructor and refreshes display.
        
        :raises: Shows QMessageBox for confirmation and result feedback
        """
        dialog = SelectionDialog("Delete Instructor", self.db.readallinstructors(), "instructor")
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_selected_data()
            if data:
                reply = QMessageBox.question(self, 'Confirm', f"Delete {data['name']}?")
                if reply == QMessageBox.Yes:
                    if self.db.deleteinstructorfromdb(data['instructor_id']):
                        QMessageBox.information(self, "Success", "Instructor deleted!")
                        self.refreshing_the_data()
    
    def add_course(self):
        """
        Add a new course to the database.
        
        Validates input data, creates Course object, and saves to database.
        Shows success/error messages and refreshes data display on success.
        
        :raises: Shows QMessageBox for validation errors or database failures
        """
        inputs = {k: v.text() for k, v in self.course_inputs.items()}
        if not self.validate_inputs(inputs):
            return
        course = Course(inputs['id'], inputs['name'], None)
        if self.db.createnewcourse(course.course_id, course.course_name, None):
            QMessageBox.information(self, "Success", f"Course {inputs['name']} added!")
            self.clear_inputs(self.course_inputs)
            self.refreshing_the_data()
        else:
            QMessageBox.critical(self, "Error", f"Failed to add course. ID {inputs['id']} might exist.")
    
    def register_student(self):
        """
        Register a student to a course.
        
        Validates that both student and course exist in database,
        then creates registration relationship.
        
        :raises: Shows QMessageBox for validation errors or registration failures
        """
        inputs = {k: v.text() for k, v in self.reg_inputs.items()}
        if not self.validate_inputs(inputs):
            return
        
        student_data = self.db.readstudent(inputs['student_id'])
        course_data = self.db.readcourse(inputs['course_id'])
        
        if not student_data:
            QMessageBox.critical(self, "Error", f"Student ID {inputs['student_id']} not found!")
            return
        if not course_data:
            QMessageBox.critical(self, "Error", f"Course ID {inputs['course_id']} not found!")
            return
        
        if self.db.registerstudenttocourse(inputs['student_id'], inputs['course_id']):
            QMessageBox.information(self, "Success", f"Student registered to {course_data['course_name']}!")
            self.clear_inputs(self.reg_inputs)
            self.refreshing_the_data()
        else:
            QMessageBox.critical(self, "Error", "Registration failed!")
    
    def assign_instructor(self):
        """
        Assign an instructor to a course.
        
        Validates that both instructor and course exist in database,
        then updates course with instructor assignment.
        
        :raises: Shows QMessageBox for validation errors or assignment failures
        """
        inputs = {k: v.text() for k, v in self.assign_inputs.items()}
        if not self.validate_inputs(inputs):
            return
        
        instructor_data = self.db.readinstructor(inputs['instructor_id'])
        course_data = self.db.readcourse(inputs['course_id'])
        
        if not instructor_data:
            QMessageBox.critical(self, "Error", f"Instructor ID {inputs['instructor_id']} not found!")
            return
        if not course_data:
            QMessageBox.critical(self, "Error", f"Course ID {inputs['course_id']} not found!")
            return
        
        if self.db.updatecourse(inputs['course_id'], course_data['course_name'], inputs['instructor_id']):
            QMessageBox.information(self, "Success", f"Instructor assigned to {course_data['course_name']}!")
            self.clear_inputs(self.assign_inputs)
            self.refreshing_the_data()
        else:
            QMessageBox.critical(self, "Error", "Assignment failed!")
    
    def view_student_courses(self):
        """
        Display courses enrolled by a selected student.
        
        Shows selection dialog for students, then displays
        their enrolled courses in a separate dialog.
        """
        dialog = SelectionDialog("View Student Courses", self.db.readallstudents(), "student")
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_selected_data()
            if data:
                self.show_courses(data)
    
    def show_courses(self, student_data):
        """
        Display courses for a specific student in a dialog window.
        
        :param student_data: Dictionary containing student information
        :type student_data: dict
        """
        courses = self.db.gettingstudentcourses(student_data['student_id'])
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Courses for {student_data['name']}")
        dialog.setGeometry(300, 300, 600, 400)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Courses for {student_data['name']}"))
        
        if courses:
            for course in courses:
                reg_date = str(course.get('registration_date', 'N/A'))
                if 'T' in reg_date:
                    reg_date = reg_date.split('T')[0]
                text = f"{course['course_id']} - {course['course_name']} (Registered: {reg_date})"
                layout.addWidget(QLabel(text))
        else:
            layout.addWidget(QLabel("No courses found for this student"))
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def view_course_students(self):
        """
        Display students enrolled in a selected course.
        
        Shows selection dialog for courses, then displays
        enrolled students in a separate dialog.
        """
        dialog = SelectionDialog("View Course Students", self.db.readallcourses(), "course")
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_selected_data()
            if data:
                self.show_students(data)
    
    def show_students(self, course_data):
        """
        Display students for a specific course in a dialog window.
        
        :param course_data: Dictionary containing course information
        :type course_data: dict
        """
        students = self.db.gettingcoursestudents(course_data['course_id'])
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Students in {course_data['course_name']}")
        dialog.setGeometry(300, 300, 600, 400)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Students in {course_data['course_name']}"))
        
        if students:
            for student in students:
                reg_date = str(student.get('registration_date', 'N/A'))
                if 'T' in reg_date:
                    reg_date = reg_date.split('T')[0]
                text = f"{student['student_id']} - {student['name']} (Registered: {reg_date})"
                layout.addWidget(QLabel(text))
        else:
            layout.addWidget(QLabel("No students found for this course"))
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        dialog.exec_()

    def refreshing_the_data(self):
        """
        Refresh and update the data display in the right panel.
        
        Clears existing data widgets and reloads current information
        from database for students, instructors, and courses.
        """
        for i in reversed(range(self.data_layout.count())):
            widget = self.data_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        self.display_students()
        self.display_instructors()
        self.display_courses()                  