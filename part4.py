import sqlite3

def table():
    db = sqlite3.connect("school.db")
    cur = db.cursor()

    cur.execute()
    db.commit()
    db.close()

def student(name, age, email):
    db = sqlite3.connect("school.db")
    cur = db.cursor()
    db.commit()
    db.close()
    print("inserted student")