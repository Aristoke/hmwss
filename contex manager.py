import sqlite3


class DbConnect:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()


class Person:
    def __init__(self, full_name, age, email):
        self.full_name = full_name
        self.age = age
        self.email = email


def save(cursor, person):
    cursor.execute("INSERT INTO Person (full_name, age, email) VALUES (?, ?, ?)",
                   (person.full_name, person.age, person.email))


def get_person(cursor, person_id):
    cursor.execute("SELECT * FROM Person WHERE id=?", (person_id,))
    person_data = cursor.fetchone()
    if person_data:
        id, full_name, age, email = person_data
        return Person(full_name, age, email)
    else:
        return None


# Usage example:
db_name = "example.db"

with DbConnect(db_name) as cursor:
    # Creating Person table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS Person (
                      id INTEGER PRIMARY KEY,
                      full_name TEXT,
                      age INTEGER,
                      email TEXT)''')

    # Creating and saving a new person
    new_person = Person("John Doe", 30, "john@example.com")
    save(cursor, new_person)

    # Retrieving person by id
    retrieved_person = get_person(cursor, 1)
    if retrieved_person:
        print("Retrieved Person:")
        print("ID:", 1)
        print("Name:", retrieved_person.full_name)
        print("Age:", retrieved_person.age)
        print("Email:", retrieved_person.email)
    else:
        print("Person with ID 1 not found.")
