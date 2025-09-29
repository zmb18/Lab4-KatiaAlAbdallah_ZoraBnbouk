"""
Person Base Class Module

This module defines the Person base class that serves as the foundation
for Student and Instructor classes in the School Management System.

:author: Your Name
:version: 1.0.0
:date: 2025
"""


class Person:
    """
    Base class representing a person in the school management system.
    
    This class provides common attributes and functionality shared between
    students and instructors, including personal information management
    and basic introduction capabilities.
    
    :param name: Full name of the person
    :type name: str
    :param age: Age of the person in years
    :type age: int
    :param email: Email address of the person
    :type email: str
    
    :ivar name: Person's full name
    :vartype name: str
    :ivar age: Person's age in years  
    :vartype age: int
    :ivar _email: Person's email address (protected attribute)
    :vartype _email: str
    """
    
    def __init__(self, name, age, email):
        """
        Initialize a Person instance with basic information.
        
        :param name: Full name of the person
        :type name: str
        :param age: Age of the person in years
        :type age: int
        :param email: Email address of the person
        :type email: str
        """
        self.name = name
        self.age = age
        self._email = email

    def introduce(self):
        """
        Generate a basic introduction string for the person.
        
        :return: A formatted introduction message
        :rtype: str
        :example: "Hello, my name is John Doe."
        """
        return f"Hello, my name is {self.name} ."