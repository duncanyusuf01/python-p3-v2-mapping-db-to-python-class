import sqlite3

class Department:
    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    @classmethod
    def create_table(cls):
        """Creates the departments table if it doesn't exist"""
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                location TEXT
            )
        ''')
        conn.commit()
        conn.close()

    @classmethod
    def drop_table(cls):
        """Drops the departments table if it exists"""
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS departments')
        conn.commit()
        conn.close()

    def save(self):
        """Saves the Department instance to the database and assigns an id"""
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute('''
                INSERT INTO departments (name, location)
                VALUES (?, ?)
            ''', (self.name, self.location))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE departments
                SET name = ?, location = ?
                WHERE id = ?
            ''', (self.name, self.location, self.id))
        conn.commit()
        conn.close()

    @classmethod
    def create(cls, name, location):
        """Creates a new Department and saves it to the database"""
        department = cls(name, location)
        department.save()
        return department

    def update(self):
        """Updates the database row to match the current instance"""
        if self.id is not None:
            conn = sqlite3.connect('company.db')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE departments
                SET name = ?, location = ?
                WHERE id = ?
            ''', (self.name, self.location, self.id))
            conn.commit()
            conn.close()

    def delete(self):
        """Deletes the database row corresponding to the current instance"""
        if self.id is not None:
            conn = sqlite3.connect('company.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM departments WHERE id = ?', (self.id,))
            conn.commit()
            conn.close()
            self.id = None

    @classmethod
    def instance_from_db(cls, row):
        """Creates a Department instance from a database row"""
        if row is None:
            return None
        return cls(id=row[0], name=row[1], location=row[2])

    @classmethod
    def get_all(cls):
        """Returns a list of all Department instances"""
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM departments')
        rows = cursor.fetchall()
        conn.close()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Finds a Department by ID"""
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM departments WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        return cls.instance_from_db(row)

    @classmethod
    def find_by_name(cls, name):
        """Finds a Department by name"""
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM departments WHERE name = ?', (name,))
        row = cursor.fetchone()
        conn.close()
        return cls.instance_from_db(row)