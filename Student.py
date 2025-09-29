"""
Student Class Module

This module defines the Student class which inherits from Person and
represents students in the School Management System with course
registration capabilities.

:author: Your Name
:version: 1.0.0
:date: 2025
"""

from Person import Person


class Student(Person):
    """
    Student class representing a student in the school management system.
    
    Inherits from Person base class and adds student-specific functionality
    including unique student ID and course registration management.
    
    :param id: Unique identifier for the student
    :type id: str
    :param name: Full name of the student
    :type name: str
    :param age: Age of the student in years
    :type age: int
    :param email: Email address of the student
    :type email: str
    
    :ivar id: Unique student identifier
    :vartype id: str
    :ivar registered_courses: List of courses the student is registered for
    :vartype registered_courses: list
    """
    
    def __init__(self, id, name, age, email):
        """
        Initialize a Student instance with personal information and student ID.
        
        Calls parent constructor to set basic person attributes and
        initializes student-specific attributes.
        
        :param id: Unique identifier for the student
        :type id: str
        :param name: Full name of the student
        :type name: str
        :param age: Age of the student in years
        :type age: int
        :param email: Email address of the student
        :type email: str
        """
        super().__init__(name, age, email)
        self.id = id
        self.registered_courses = []

    def register_course(self, course):
        """
        Register the student for a course.
        
        Adds the specified course to the student's list of registered courses.
        This method handles the in-memory course registration for the student object.
        
        :param course: Course object to register for
        :type course: Course
        :note: This method works with Course objects in memory.
               Database registration is handled separately in the GUI layer.
        """
        self.registered_courses.append(course)