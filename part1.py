import json

class Person:
    def __init__(self, name, age, email):
        if age < 0:
            print("Not a valid age.")
            age = 0

        if "@" not in email and "." not in email:
            email = "unknown"
            print("Not a valid email.") 

        self.name = name
        self.age = age
        self._email = email

    def get_email(self):
        return self._email
    
    def introduce(self):
        print(f"Hello, I am {self.name}. I am {self.age} years old.")


class Student(Person):
    def __init__(self, name, age, email, student_id):
        self.registered_courses = []
        super().__init__(name, age, email)
        self.student_id = student_id
    
    def register_course(self, course):
        if course not in self.registered_courses:
            self.registered_courses.append(course)
            course.add_student(self)
    
class Instructor(Person):
    def __init__(self, name, age, email, instructor_id):
        self.assigned_courses = []
        super().__init__(name, age, email)
        self.instructor_id = instructor_id

    def assign_course(self, course):
        if course not in self.assigned_courses:
            self.assigned_courses.append(course) 

class Course:
    def __init__(self, course_id, course_name, instructor):
        self.enrolled_students = []
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor

    def add_student(self, student):
        self.enrolled_students.append(student)
        student.register_course(self)

def save_data(students, filename = "student.json"):  #sorry I forgot completely about json so i used GPT here, i undrstood the code but had to copy this
    data = []
    for student in students:
        student_info = { "name": student.name, "age": student.age, "email": student._email, "student_id": student.student_id, "registered_courses": [course.course_name for course in student.registered_course] }
        data.append(student_info)

    with open(filename, "w") as f:
        json.dump(data, f)
    
    print("The data was saved to file: ", filename)

def load_data(filename = "student.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        print("The data loaded successfully.")
        return data
    except FileNotFoundError:
        print("This file is nowhere to be found :(")
        return []
    

if __name__ == "__main__":
    student = Student("Katia Abdallah", 21, "kma74@mail.aub.edu", "202300475")
    student.introduce()

    instructor = Instructor("Prof. Ghalayini", 27, "ig12@mail.aub.edu", "dunno")
    course = Course("EECE435L", "Software Tools Lab", instructor)

    instructor.assign_course(course)
    student.register_course(course)

    print("Course:", course.course_name, "- Instructor:", course.instructor.name)
    print("Enrolled students in this course:")
    for student in course.enrolled_students:
        print("-", student.name)

    


            

    





    


    
            



