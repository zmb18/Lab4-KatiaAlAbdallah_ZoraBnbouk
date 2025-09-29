"""
Instructor Class Module

This module defines the Instructor class which inherits from Person and
represents instructors in the School Management System with course
assignment capabilities.

:author: Your Name
:version: 1.0.0
:date: 2025
"""

from Person import Person


class Instructor(Person):
    """
    Instructor class representing an instructor in the school management system.
    
    Inherits from Person base class and adds instructor-specific functionality
    including unique instructor ID and course assignment management.
    
    :param instructor_id: Unique identifier for the instructor
    :type instructor_id: str
    :param name: Full name of the instructor
    :type name: str
    :param age: Age of the instructor in years
    :type age: int
    :param email: Email address of the instructor
    :type email: str
    
    :ivar instructor_id: Unique instructor identifier
    :vartype instructor_id: str
    :ivar assigned_courses: List of courses assigned to the instructor
    :vartype assigned_courses: list
    """
    
    def __init__(self, instructor_id, name, age, email):
        """
        Initialize an Instructor instance with personal information and instructor ID.
        
        Calls parent constructor to set basic person attributes and
        initializes instructor-specific attributes.
        
        :param instructor_id: Unique identifier for the instructor
        :type instructor_id: str
        :param name: Full name of the instructor
        :type name: str
        :param age: Age of the instructor in years
        :type age: int
        :param email: Email address of the instructor
        :type email: str
        """
        super().__init__(name, age, email)  
        self.instructor_id = instructor_id
        self.assigned_courses = []
       
    def assign_course(self, course):
        """
        Assign a course to the instructor.
        
        Adds the specified course to the instructor's list of assigned courses.
        This method handles the in-memory course assignment for the instructor object.
        
        :param course: Course object to assign to the instructor
        :type course: Course
        :note: This method works with Course objects in memory.
               Database assignments are handled separately in the GUI layer.
        """
        self.assigned_courses.append(course)