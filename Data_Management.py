"""
Database Management Module for School Management System

This module provides comprehensive database operations for managing students,
instructors, courses, and their relationships using SQLite. It handles all
CRUD operations, data validation, backup, and export functionality.

:author: Your Name
:version: 1.0.0
:date: 2025
"""

import sqlite3
import json
import shutil
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class DatabaseBoss:
    """
    Database manager for the School Management System.
    
    Handles all database operations including CRUD operations for students,
    instructors, courses, and registrations. Provides backup, export, and
    import functionality with proper error handling and data validation.
    
    :param db_name: Name of the SQLite database file, defaults to "school_management.db"
    :type db_name: str, optional
    
    :ivar db_name: Database file name
    :vartype db_name: str
    :ivar connection: SQLite database connection object
    :vartype connection: sqlite3.Connection
    """

    def __init__(self, db_name: str = "school_management.db") -> None:
        """
        Initialize the database manager and create database schema.
        
        Establishes connection to SQLite database, enables foreign key constraints,
        and creates necessary tables if they don't exist.
        
        :param db_name: Name of the database file to connect to
        :type db_name: str
        """
        self.db_name = db_name
        # Make connection & cursor NON-OPTIONAL to satisfy Pylance
        self.connection: sqlite3.Connection = sqlite3.connect(self.db_name)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        # Create schema on first run
        self._create_schema()

    def _create_schema(self) -> None:
        """
        Create database tables with proper schema and constraints.
        
        Creates the following tables:
        - students: Student information with validation constraints
        - instructors: Instructor information with validation constraints  
        - courses: Course information with foreign key to instructors
        - registrations: Student-course relationships with foreign keys
        
        :raises sqlite3.Error: If table creation fails
        """
        try:
            cur = self.connection.cursor()

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS students (
                    student_id TEXT PRIMARY KEY,
                    name       TEXT NOT NULL,
                    age        INTEGER NOT NULL CHECK (age >= 0),
                    email      TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS instructors (
                    instructor_id TEXT PRIMARY KEY,
                    name          TEXT NOT NULL,
                    age           INTEGER NOT NULL CHECK (age >= 0),
                    email         TEXT NOT NULL,
                    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS courses (
                    course_id     TEXT PRIMARY KEY,
                    course_name   TEXT NOT NULL,
                    instructor_id TEXT,
                    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (instructor_id) REFERENCES instructors (instructor_id)
                )
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS registrations (
                    id                INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id        TEXT NOT NULL,
                    course_id         TEXT NOT NULL,
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students (student_id) ON DELETE CASCADE,
                    FOREIGN KEY (course_id)  REFERENCES courses  (course_id)  ON DELETE CASCADE,
                    UNIQUE(student_id, course_id)
                )
                """
            )

            self.connection.commit()
            print("The tables in your database are ready")

        except sqlite3.Error as e:
            print("Sorry there is an error", e)

    def close_connection(self) -> None:
        """
        Close the database connection safely.
        
        Attempts to close the database connection, ignoring any exceptions
        that might occur during the closing process.
        """
        try:
            self.connection.close()
        except Exception:
            pass

    # ---------- Students CRUD ----------

    def createnewstudent(self, student_id: str, name: str, age: int, email: str) -> bool:
        """
        Create a new student record in the database.
        
        :param student_id: Unique identifier for the student
        :type student_id: str
        :param name: Full name of the student
        :type name: str
        :param age: Age of the student (must be non-negative)
        :type age: int
        :param email: Email address of the student
        :type email: str
        :return: True if student created successfully, False otherwise
        :rtype: bool
        :raises sqlite3.IntegrityError: If student ID already exists
        :raises sqlite3.Error: For other database-related errors
        """
        try:
            cur = self.connection.cursor()
            cur.execute(
                """
                INSERT INTO students (student_id, name, age, email)
                VALUES (?, ?, ?, ?)
                """,
                (student_id, name or "", age, email or ""),
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"Student with ID {student_id} already exists!")
            return False
        except sqlite3.Error as e:
            print("Please retry ! There is an error in creating student:", e)
            return False

    def readstudent(self, student_id: str) -> Optional[Dict]:
        """
        Retrieve a single student record by ID.
        
        :param student_id: Unique identifier of the student to retrieve
        :type student_id: str
        :return: Student data as dictionary or None if not found
        :rtype: dict or None
        :raises sqlite3.Error: For database query errors
        """
        try:
            cur = self.connection.cursor()
            cur.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
            row = cur.fetchone()
            if row:
                return dict(row)
            return None
        except sqlite3.Error as e:
            print("Please retry ! Error in  reading student:", e)
            return None

    def readallstudents(self) -> List[Dict]:
        """
        Retrieve all student records from the database.
        
        :return: List of all student records as dictionaries, ordered by name
        :rtype: list[dict]
        :raises sqlite3.Error: For database query errors
        """
        try:
            cur = self.connection.cursor()
            cur.execute("SELECT * FROM students ORDER BY name")
            return [dict(r) for r in cur.fetchall()]
        except sqlite3.Error as e:
            print("Please retry ! Error in  reading the  students:", e)
            return []

    def updatestudent(self, student_id: str, name: str, age: int, email: str) -> bool:
        """
        Update an existing student record.
        
        :param student_id: Unique identifier of the student to update
        :type student_id: str
        :param name: Updated name of the student
        :type name: str
        :param age: Updated age of the student
        :type age: int
        :param email: Updated email address of the student
        :type email: str
        :return: True if update successful, False otherwise
        :rtype: bool
        :raises sqlite3.Error: For database update errors
        """
        try:
            cur = self.connection.cursor()
            cur.execute(
                """
                UPDATE students
                SET name = ?, age = ?, email = ?
                WHERE student_id = ?
                """,
                (name or "", age, email or "", student_id),
            )
            self.connection.commit()
            return cur.rowcount > 0
        except sqlite3.Error as e:
            print("Sorry to tell you that there is an error happening  in updating student:", e)
            return False

    def deletestudentfromdb(self, sid):
        """
        Delete a student record from the database.
        
        Removes student record and all associated registrations due to CASCADE constraint.
        
        :param sid: Student ID to delete
        :type sid: str
        :return: True if deletion successful, False otherwise
        :rtype: bool
        :raises sqlite3.Error: For database deletion errors
        """
        try:
            self.cur = self.connection.cursor()
            # Registrations cascade on delete
            self.cur.execute("DELETE FROM students WHERE student_id = ?", (sid,))
            self.connection.commit()        
            return self.cur.rowcount > 0
        except sqlite3.Error:
            return False

    # ---------- Instructors CRUD ----------

    def createinstructor(self, instructor_id: str, name: str, age: int, email: str) -> bool:
        """
        Create a new instructor record in the database.
        
        :param instructor_id: Unique identifier for the instructor
        :type instructor_id: str
        :param name: Full name of the instructor
        :type name: str
        :param age: Age of the instructor (must be non-negative)
        :type age: int
        :param email: Email address of the instructor
        :type email: str
        :return: True if instructor created successfully, False otherwise
        :rtype: bool
        :raises sqlite3.IntegrityError: If instructor ID already exists
        :raises sqlite3.Error: For other database-related errors
        """
        try:
            cur = self.connection.cursor()
            cur.execute(
                """
                INSERT INTO instructors (instructor_id, name, age, email)
                VALUES (?, ?, ?, ?)
                """,
                (instructor_id, name or "", age, email or ""),
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"Instructor with ID {instructor_id} already exists!")
            return False
        except sqlite3.Error as e:
            print("Please retry ! There is an error  in creating the instructor:", e)
            return False

    def readinstructor(self, instructor_id: str) -> Optional[Dict]:
        """
        Retrieve a single instructor record by ID.
        
        :param instructor_id: Unique identifier of the instructor to retrieve
        :type instructor_id: str
        :return: Instructor data as dictionary or None if not found
        :rtype: dict or None
        :raises sqlite3.Error: For database query errors
        """
        try:
            cur = self.connection.cursor()
            cur.execute(
                "SELECT * FROM instructors WHERE instructor_id = ?",
                (instructor_id,),
            )
            row = cur.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print("Sorry to inform you that there is an error in reading instructor:", e)
            return None

    def readallinstructors(self) -> List[Dict]:
        """
        Retrieve all instructor records from the database.
        
        :return: List of all instructor records as dictionaries, ordered by name
        :rtype: list[dict]
        :raises sqlite3.Error: For database query errors
        """
        try:
            cur = self.connection.cursor()
            cur.execute("SELECT * FROM instructors ORDER BY name")
            return [dict(r) for r in cur.fetchall()]
        except sqlite3.Error as e:
            print("Pleasse retry ! Error in reading instructors:", e)
            return []

    def updateinstructor(self, instructor_id: str, name: str, age: int, email: str) -> bool:
        """
        Update an existing instructor record.
        
        :param instructor_id: Unique identifier of the instructor to update
        :type instructor_id: str
        :param name: Updated name of the instructor
        :type name: str
        :param age: Updated age of the instructor
        :type age: int
        :param email: Updated email address of the instructor
        :type email: str
        :return: True if update successful, False otherwise
        :rtype: bool
        :raises sqlite3.Error: For database update errors
        """
        try:
            cur = self.connection.cursor()
            cur.execute(
                """
                UPDATE instructors
                SET name = ?, age = ?, email = ?
                WHERE instructor_id = ?
                """,
                (name or "", age, email or "", instructor_id),
            )
            self.connection.commit()
            return cur.rowcount > 0
        except sqlite3.Error as e:
            print("Please retry ! Errorin  updating the instructor:", e)
            return False

    def deleteinstructorfromdb(self, instructor_id: str) -> bool:
        """
        Delete an instructor record from the database.
        
        Unassigns instructor from all courses before deletion to maintain data integrity.
        
        :param instructor_id: Unique identifier of instructor to delete
        :type instructor_id: str
        :return: True if deletion successful, False otherwise
        :rtype: bool
        :raises sqlite3.Error: For database deletion errors
        """
        try:
            cur = self.connection.cursor()
            # Unassign instructor from courses first (or define ON DELETE SET NULL FK)
            cur.execute(
                "UPDATE courses SET instructor_id = NULL WHERE instructor_id = ?",
                (instructor_id,),
            )
            cur.execute("DELETE FROM instructors WHERE instructor_id = ?", (instructor_id,))
            self.connection.commit()
            return cur.rowcount > 0
        except sqlite3.Error as e:
            print("Please retry ! Errorin  deleting the  instructor:", e)
            return False

    # ---------- Courses CRUD ----------

    def createnewcourse(
        self, course_id: str, course_name: str, instructor_id: Optional[str] = None
    ) -> bool:
        """
        Create a new course record in the database.
        
        :param course_id: Unique identifier for the course
        :type course_id: str
        :param course_name: Name/title of the course
        :type course_name: str
        :param instructor_id: Optional instructor ID to assign to course
        :type instructor_id: str or None
        :return: True if course created successfully, False otherwise
        :rtype: bool
        :raises sqlite3.IntegrityError: If course ID already exists
        :raises sqlite3.Error: For other database-related errors
        """
        try:
            cur = self.connection.cursor()
            cur.execute(
                """
                INSERT INTO courses (course_id, course_name, instructor_id)
                VALUES (?, ?, ?)
                """,
                (course_id, course_name or "", instructor_id),
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"Course with ID {course_id} already exists!")
            return False
        except sqlite3.Error as e:
            print("Please retry ! Error in  creating the course:", e)
            return False

    def readcourse(self, course_id: str) -> Optional[Dict]:
        """
        Retrieve a single course record with instructor information.
        
        :param course_id: Unique identifier of the course to retrieve
        :type course_id: str
        :return: Course data with instructor name or None if not found
        :rtype: dict or None
        :raises sqlite3.Error: For database query errors
        """
        try:
            cur = self.connection.cursor()
            cur.execute(
                """
                SELECT c.*, i.name AS instructor_name
                FROM courses c
                LEFT JOIN instructors i ON c.instructor_id = i.instructor_id
                WHERE c.course_id = ?
                """,
                (course_id,),
            )
            row = cur.fetchone()
            if not row:
                return None
            d = dict(row)
            d["instructor_name"] = d.get("instructor_name") or "Unassigned"
            return d
        except sqlite3.Error as e:
            print("Please retry !Error in  reading course:", e)
            return None

    def readallcourses(self) -> List[Dict]:
        """
        Retrieve all course records with instructor information.
        
        :return: List of all course records with instructor names, ordered by course name
        :rtype: list[dict]
        :raises sqlite3.Error: For database query errors
        """
        try:
            cur = self.connection.cursor()
            cur.execute(
                """
                SELECT c.*, i.name AS instructor_name
                FROM courses c
                LEFT JOIN instructors i ON c.instructor_id = i.instructor_id
                ORDER BY c.course_name
                """
            )
            rows = cur.fetchall()
            out: List[Dict] = []
            for r in rows:
                d = dict(r)
                d["instructor_name"] = d.get("instructor_name") or "Unassigned"
                out.append(d)
            return out
        except sqlite3.Error as e:
            print("Please retry !Error in reading courses:", e)
            return []

    def updatecourse(
        self, course_id: str, course_name: str, instructor_id: Optional[str] = None
    ) -> bool:
        """
        Update an existing course record.
        
        :param course_id: Unique identifier of the course to update
        :type course_id: str
        :param course_name: Updated name of the course
        :type course_name: str
        :param instructor_id: Updated instructor ID (can be None to unassign)
        :type instructor_id: str or None
        :return: True if update successful, False otherwise
        :rtype: bool
        :raises sqlite3.Error: For database update errors
        """
        try:
            cur = self.connection.cursor()
            cur.execute(
                """
                UPDATE courses
                SET course_name = ?, instructor_id = ?
                WHERE course_id = ?
                """,
                (course_name or "", instructor_id, course_id),
            )
            self.connection.commit()
            return cur.rowcount > 0
        except sqlite3.Error as e:
            print("Please retry ! Error in updating the course:", e)
            return False

    def deletecoursefromdb(self, course_id: str) -> bool:
        """
        Delete a course record from the database.
        
        Removes course record and all associated registrations due to CASCADE constraint.
        
        :param course_id: Unique identifier of course to delete
        :type course_id: str
        :return: True if deletion successful, False otherwise
        :rtype: bool
        :raises sqlite3.Error: For database deletion errors
        """
        try:
            cur = self.connection.cursor()
            # Registrations cascade on delete
            cur.execute("DELETE FROM courses WHERE course_id = ?", (course_id,))
            self.connection.commit()
            return cur.rowcount > 0
        except sqlite3.Error as e:
            print("Please retry ! Error in deleting the course:", e)
            return False

    # ---------- Registrations ----------

    def registerstudenttocourse(self, student_id: str, course_id: str) -> bool:
        """
        Register a student to a course.
        
        Creates a registration relationship between student and course.
        Prevents duplicate registrations with unique constraint.
        
        :param student_id: ID of student to register
        :type student_id: str
        :param course_id: ID of course to register for
        :type course_id: str
        :return: True if registration successful, False otherwise
        :rtype: bool
        :raises sqlite3.IntegrityError: If student already registered for course
        :raises sqlite3.Error: For other database-related errors
        """
        try:
            cur = self.connection.cursor()
            cur.execute(
                "INSERT INTO registrations (student_id, course_id) VALUES (?, ?)",
                (student_id, course_id),
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"Student {student_id} is already registered for course {course_id}!")
            return False
        except sqlite3.Error as e:
            print("Please retry ! There is an error in  registering the student:", e)
            return False

    def unregisterstudentfrmcourse(self, student_id: str, course_id: str) -> bool:
        """
        Unregister a student from a course.
        
        Removes the registration relationship between student and course.
        
        :param student_id: ID of student to unregister
        :type student_id: str
        :param course_id: ID of course to unregister from
        :type course_id: str
        :return: True if unregistration successful, False otherwise
        :rtype: bool
        :raises sqlite3.Error: For database deletion errors
        """
        try:
            cur = self.connection.cursor()
            cur.execute(
                "DELETE FROM registrations WHERE student_id = ? AND course_id = ?",
                (student_id, course_id),
            )
            self.connection.commit()
            return cur.rowcount > 0
        except sqlite3.Error as e:
            print("Please retry ! Error in  unregistering the student:", e)
            return False

    def gettingstudentcourses(self, sid):
        """
        Get all courses a student is registered for.
        
        :param sid: Student ID to look up courses for
        :type sid: str
        :return: List of course dictionaries with registration dates
        :rtype: list[dict]
        :raises sqlite3.Error: For database query errors
        """
        sql = """
        SELECT c.course_id,
            c.course_name,
            r.registration_date
        FROM registrations r
        JOIN courses c ON c.course_id = r.course_id
        WHERE r.student_id = ?
        ORDER BY c.course_id
        """
        rows = self.connection.execute(sql, (sid,)).fetchall()  
        # Return list[dict] with the exact keys your GUI uses:
        return [
            {
                "course_id": row["course_id"],
                "course_name": row["course_name"],
                "registration_date": row["registration_date"]
            }
            for row in rows
        ]

    def gettingcoursestudents(self, cid):
        """
        Get all students registered for a course.
        
        :param cid: Course ID to look up students for
        :type cid: str
        :return: List of student dictionaries with registration dates
        :rtype: list[dict]
        :raises sqlite3.Error: For database query errors
        """
        sql = """
        SELECT s.student_id,
            s.name,
            s.email,
            r.registration_date
        FROM registrations r
        JOIN students s ON s.student_id = r.student_id
        WHERE r.course_id = ?
        ORDER BY s.student_id
        """
        rows=self.connection.execute(sql, (cid,)).fetchall()        
        return [
            {
                "student_id": row["student_id"],
                "name": row["name"],
                "email": row["email"],
                "registration_date": row["registration_date"]
            }
            for row in rows
        ]

    def searchstudents(self, search_term: str) -> List[Dict]:
        """
        Search for students by ID, name, or email.
        
        :param search_term: Term to search for in student records
        :type search_term: str
        :return: List of matching student records
        :rtype: list[dict]
        :raises sqlite3.Error: For database query errors
        """
        try:
            cur = self.connection.cursor()
            like = f"%{search_term}%"
            cur.execute(
                """
                SELECT * FROM students
                WHERE student_id LIKE ? OR name LIKE ? OR email LIKE ?
                ORDER BY name
                """,
                (like, like, like),
            )
            return [dict(r) for r in cur.fetchall()]
        except sqlite3.Error as e:
            print("Please retry Error in searching students:", e)
            return []

    def searchinstructors(self, search_term: str) -> List[Dict]:
        """
        Search for instructors by ID, name, or email.
        
        :param search_term: Term to search for in instructor records
        :type search_term: str
        :return: List of matching instructor records
        :rtype: list[dict]
        :raises sqlite3.Error: For database query errors
        """
        try:
            cur = self.connection.cursor()
            like = f"%{search_term}%"
            cur.execute(
                """
                SELECT * FROM instructors
                WHERE instructor_id LIKE ? OR name LIKE ? OR email LIKE ?
                ORDER BY name
                """,
                (like, like, like),
            )
            return [dict(r) for r in cur.fetchall()]
        except sqlite3.Error as e:
            print("Please retry Error in searching  instructors:", e)
            return []

    def searchcourses(self, search_term: str) -> List[Dict]:
        """
        Search for courses by ID or name, including instructor information.
        
        :param search_term: Term to search for in course records
        :type search_term: str
        :return: List of matching course records with instructor names
        :rtype: list[dict]
        :raises sqlite3.Error: For database query errors
        """
        try:
            cur = self.connection.cursor()
            like = f"%{search_term}%"
            cur.execute(
                """
                SELECT c.*, i.name AS instructor_name
                FROM courses c
                LEFT JOIN instructors i ON c.instructor_id = i.instructor_id
                WHERE c.course_id LIKE ? OR c.course_name LIKE ?
                ORDER BY c.course_name
                """,
                (like, like),
            )
            rows = cur.fetchall()
            out: List[Dict] = []
            for r in rows:
                d = dict(r)
                d["instructor_name"] = d.get("instructor_name") or "Unassigned"
                out.append(d)
            return out
        except sqlite3.Error as e:
            print("Please retry Error in searching  courses:", e)
            return []

    # ---------- Backup / Export ----------

    def backupdb(self, backup_path: Optional[str] = None) -> bool:
        """
        Create a backup of the database file.
        
        Creates a timestamped backup copy of the database file for data protection.
        
        :param backup_path: Custom backup file path, auto-generated if None
        :type backup_path: str or None
        :return: True if backup successful, False otherwise
        :rtype: bool
        :raises Exception: For file system or database errors
        """
        try:
            if backup_path is None:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"backup_school_management_{ts}.db"
            # Ensure all writes flushed
            self.connection.commit()
            self.connection.backup(sqlite3.connect(backup_path))
            print("Database backed up to:", backup_path)
            return True
        except Exception as e:
            print("Please retry !Error in  creating the  backup:", e)
            return False

    def exporttojson(self, export_path: Optional[str] = None) -> bool:
        """
        Export all database data to JSON format.
        
        Exports students, instructors, courses, and registrations to a JSON file
        with proper formatting and timestamp.
        
        :param export_path: Custom export file path, auto-generated if None
        :type export_path: str or None
        :return: True if export successful, False otherwise
        :rtype: bool
        :raises Exception: For file system or database errors
        """
        try:
            if export_path is None:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                export_path = f"school_data_export_{ts}.json"
            data = {
                "students": self.readallstudents(),
                "instructors": self.readallinstructors(),
                "courses": self.readallcourses(),
                "registrations": self._gettingallregistrations(),
            }
            with open(export_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
            print("Data got exported to here :", export_path)
            return True
        except Exception as e:
            print("Please retry !Error in exporting the data:", e)
            return False

    def _gettingallregistrations(self) -> List[Dict]:
        """
        Get all registration records with student and course names.
        
        Private helper method for export functionality.
        
        :return: List of registration records with related information
        :rtype: list[dict]
        :raises sqlite3.Error: For database query errors
        """
        try:
            cur = self.connection.cursor()
            cur.execute(
                """
                SELECT r.id, r.student_id, r.course_id, r.registration_date,
                       s.name AS student_name, c.course_name
                FROM registrations r
                JOIN students s ON r.student_id = s.student_id
                JOIN courses  c ON r.course_id  = c.course_id
                ORDER BY r.registration_date
                """
            )
            return [dict(r) for r in cur.fetchall()]
        except sqlite3.Error as e:
            print("Please retry !Error in getting registrations:", e)
            return []

    # ---------- Stats ----------

    def get_database_stats(self) -> Dict:
        """
        Get statistical information about the database.
        
        Provides counts of records in each table for dashboard/reporting purposes.
        
        :return: Dictionary with counts of students, instructors, courses, and registrations
        :rtype: dict
        :raises sqlite3.Error: For database query errors
        """
        try:
            cur = self.connection.cursor()
            cur.execute("SELECT COUNT(*) FROM students")
            students = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM instructors")
            instructors = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM courses")
            courses = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM registrations")
            regs = cur.fetchone()[0]
            return {
                "total_students": students,
                "total_instructors": instructors,
                "total_courses": courses,
                "total_registrations": regs,
            }
        except sqlite3.Error as e:
            print("Please retry ! Error in  getting  database stats:", e)
            return {}

    def import_from_json(self, file_path: str) -> bool:
        """
        Import data from a JSON file into the database.
        
        Reads JSON export file and recreates database records for
        students, instructors, and courses.
        
        :param file_path: Path to the JSON file to import
        :type file_path: str
        :return: True if import successful, False otherwise
        :rtype: bool
        :raises Exception: For file reading or database errors
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Clear existing data (optional - you might want to ask user)
            # Import students
            for student in data.get('students', []):
                self.createnewstudent(
                    student['student_id'], 
                    student['name'], 
                    student['age'], 
                    student['email']
                )
            
            # Import instructors
            for instructor in data.get('instructors', []):
                self.createinstructor(
                    instructor['instructor_id'],
                    instructor['name'],
                    instructor['age'], 
                    instructor['email']
                )
            
            # Import courses
            for course in data.get('courses', []):
                self.createnewcourse(
                    course['course_id'],
                    course['course_name'],
                    course.get('instructor_id')
                )
            
            return True
        except Exception as e:
            print(f"Error importing data: {e}")
            return False