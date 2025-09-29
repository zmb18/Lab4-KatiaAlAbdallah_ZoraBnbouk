"""
Course Class Module

This module defines the Course class which represents courses in the
School Management System with student enrollment management capabilities.

:author: Your Name
:version: 1.0.0
:date: 2025
"""


class Course:
    """
    Course class representing a course in the school management system.
    
    Manages course information including unique identifier, name, assigned instructor,
    and enrolled students. Provides functionality for student enrollment management.
    
    :param course_id: Unique identifier for the course
    :type course_id: str
    :param course_name: Name/title of the course
    :type course_name: str
    :param instructor: Instructor assigned to teach the course
    :type instructor: Instructor or None
    
    :ivar course_id: Unique course identifier
    :vartype course_id: str
    :ivar course_name: Name of the course
    :vartype course_name: str
    :ivar instructor: Assigned instructor object
    :vartype instructor: Instructor or None
    :ivar enrolled_students: List of students enrolled in the course
    :vartype enrolled_students: list
    """
    
    def __init__(self, course_id, course_name, instructor):
        """
        Initialize a Course instance with basic course information.
        
        :param course_id: Unique identifier for the course
        :type course_id: str
        :param course_name: Name/title of the course
        :type course_name: str
        :param instructor: Instructor assigned to teach the course, can be None
        :type instructor: Instructor or None
        """
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = []

    def add_student(self, student):
        """
        Add a student to the course enrollment list.
        
        Enrolls the specified student in this course by adding them to the
        enrolled_students list. This method handles in-memory enrollment
        for the course object.
        
        :param student: Student object to enroll in the course
        :type student: Student
        :note: This method works with Student objects in memory.
               Database enrollment is handled separately in the GUI layer.
        """
        self.enrolled_students.append(student)