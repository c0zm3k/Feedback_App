import sqlite3
import hashlib
import secrets
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_path="feedback_system.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create admin table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create teachers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT,
                subject TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create students table (per-teacher student roster)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teacher_id INTEGER NOT NULL,
                student_id TEXT NOT NULL,
                student_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(teacher_id, student_id),
                FOREIGN KEY (teacher_id) REFERENCES teachers (id)
            )
        ''')

        # Create feedback table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teacher_id INTEGER NOT NULL,
                student_name TEXT NOT NULL,
                feedback_text TEXT NOT NULL,
                submission_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (teacher_id) REFERENCES teachers (id)
            )
        ''')

        # Schema migration: add student_id column to feedback if missing
        cursor.execute("PRAGMA table_info(feedback)")
        feedback_columns = [row[1] for row in cursor.fetchall()]
        if 'student_id' not in feedback_columns:
            cursor.execute("ALTER TABLE feedback ADD COLUMN student_id TEXT")
        
        # Insert default admin if not exists
        cursor.execute("SELECT * FROM admins WHERE username = 'admin'")
        if not cursor.fetchone():
            admin_password = "admin123"
            admin_hash = hashlib.sha256(admin_password.encode()).hexdigest()
            cursor.execute("INSERT INTO admins (username, password_hash) VALUES (?, ?)", 
                         ('admin', admin_hash))
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash a password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_admin_login(self, username, password):
        """Verify admin login credentials"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute("SELECT * FROM admins WHERE username = ? AND password_hash = ?", 
                      (username, password_hash))
        
        admin = cursor.fetchone()
        conn.close()
        
        return admin is not None
    
    def verify_teacher_login(self, username, password):
        """Verify teacher login credentials"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute("SELECT * FROM teachers WHERE username = ? AND password_hash = ?", 
                      (username, password_hash))
        
        teacher = cursor.fetchone()
        conn.close()
        
        return teacher
    
    # -----------------------------
    # Student roster (per teacher)
    # -----------------------------
    def add_student(self, teacher_id: int, student_id: str, student_name: str) -> bool:
        """Add a student to a teacher's roster. Returns True on success, False if duplicate."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO students (teacher_id, student_id, student_name)
                VALUES (?, ?, ?)
                """,
                (teacher_id, student_id.strip(), student_name.strip()),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def get_students_for_teacher(self, teacher_id: int):
        """Return list of (id, teacher_id, student_id, student_name, created_at) for a teacher."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, teacher_id, student_id, student_name, created_at
            FROM students
            WHERE teacher_id = ?
            ORDER BY created_at DESC
            """,
            (teacher_id,),
        )
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_student_by_student_id(self, teacher_id: int, student_id: str):
        """Return a single student row for given teacher and student_id, or None."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, teacher_id, student_id, student_name, created_at
            FROM students
            WHERE teacher_id = ? AND student_id = ?
            """,
            (teacher_id, student_id.strip()),
        )
        row = cursor.fetchone()
        conn.close()
        return row

    def delete_student(self, teacher_id: int, student_id: str) -> bool:
        """Delete a student from a teacher's roster. Returns True if a row was deleted."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM students WHERE teacher_id = ? AND student_id = ?",
            (teacher_id, student_id.strip()),
        )
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted

    def generate_unique_student_id(self, teacher_id: int) -> str:
        """Generate a unique student ID for a given teacher.
        New format: SID{alpha}{seq:03d} (e.g., SIDA001 for teacher 1, SIDB001 for teacher 2).
        The alphabetic component is derived from the teacher_id using an Excel-like column scheme
        (1 -> A, 2 -> B, ..., 26 -> Z, 27 -> AA, etc.). Sequence number is per-teacher.
        Backward compatible with legacy format SID{seq:03d} when computing the next sequence.
        """
        def teacher_id_to_alpha(n: int) -> str:
            # Convert 1-based integer to Excel-like column letters
            letters = []
            while n > 0:
                n, rem = divmod(n - 1, 26)
                letters.append(chr(ord('A') + rem))
            return ''.join(reversed(letters))

        alpha = teacher_id_to_alpha(int(teacher_id))
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Start sequence at max existing sequence + 1 for stability across deletions
        cursor.execute(
            "SELECT student_id FROM students WHERE teacher_id = ?",
            (teacher_id,),
        )
        existing_ids = [row[0] for row in cursor.fetchall() if row and row[0]]
        existing_nums = []
        for sid in existing_ids:
            if not isinstance(sid, str):
                continue
            # Prefer new format: SID{alpha}{digits}
            if sid.startswith("SID" + alpha):
                tail = sid[3 + len(alpha):]
                if tail.isdigit():
                    existing_nums.append(int(tail))
                    continue
            # Fallback: legacy format SID{digits}
            if sid.startswith("SID") and sid[3:].isdigit():
                existing_nums.append(int(sid[3:]))
        seq = (max(existing_nums) + 1) if existing_nums else 1
        # Loop until we find an unused id (handles rare collisions)
        while True:
            candidate = f"SID{alpha}{int(seq):03d}"
            cursor.execute(
                "SELECT 1 FROM students WHERE teacher_id = ? AND student_id = ?",
                (teacher_id, candidate),
            )
            if cursor.fetchone() is None:
                conn.close()
                return candidate
            seq += 1

    def add_student_auto(self, teacher_id: int, student_name: str):
        """Add a student by auto-generating a unique student ID.
        Returns (True, student_id) on success, else (False, None).
        """
        generated_id = self.generate_unique_student_id(teacher_id)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO students (teacher_id, student_id, student_name)
                VALUES (?, ?, ?)
                """,
                (teacher_id, generated_id, student_name.strip()),
            )
            conn.commit()
            return True, generated_id
        except sqlite3.IntegrityError:
            return False, None
        finally:
            conn.close()

    def add_teacher(self, username, password, full_name, email, subject):
        """Add a new teacher"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            password_hash = self.hash_password(password)
            cursor.execute("""
                INSERT INTO teachers (username, password_hash, full_name, email, subject)
                VALUES (?, ?, ?, ?, ?)
            """, (username, password_hash, full_name, email, subject))
            
            conn.commit()
            success = True
        except sqlite3.IntegrityError:
            success = False
        finally:
            conn.close()
        
        return success
    
    def get_all_teachers(self):
        """Get all teachers"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, username, full_name, email, subject, created_at FROM teachers")
        teachers = cursor.fetchall()
        
        conn.close()
        return teachers
    
    def get_teacher_by_id(self, teacher_id):
        """Get teacher details by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, username, full_name, email, subject FROM teachers WHERE id = ?", 
                      (teacher_id,))
        teacher = cursor.fetchone()
        
        conn.close()
        return teacher
    
    def submit_feedback(self, teacher_id: int, student_id: str, feedback_text: str) -> bool:
        """Submit feedback for a teacher by a valid student_id. Returns True on success.
        Ensures both student_id and student_name are stored.
        """
        # Validate student belongs to teacher
        student = self.get_student_by_student_id(teacher_id, student_id)
        if not student:
            return False

        student_name = student[3]
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO feedback (teacher_id, student_name, feedback_text, student_id)
            VALUES (?, ?, ?, ?)
            """,
            (teacher_id, student_name, feedback_text, student_id.strip()),
        )
        conn.commit()
        conn.close()
        return True
    
    def get_feedback_for_teacher(self, teacher_id):
        """Get all feedback for a specific teacher"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, student_name, feedback_text, submission_time
            FROM feedback 
            WHERE teacher_id = ?
            ORDER BY submission_time DESC
        """, (teacher_id,))
        
        feedback_list = cursor.fetchall()
        conn.close()
        return feedback_list
    
    def get_all_feedback(self):
        """Get all feedback with teacher names"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT f.id, t.full_name, f.student_name, f.feedback_text, f.submission_time
            FROM feedback f
            JOIN teachers t ON f.teacher_id = t.id
            ORDER BY f.submission_time DESC
        """)
        
        feedback_list = cursor.fetchall()
        conn.close()
        return feedback_list
    
    def delete_teacher(self, teacher_id):
        """Delete a teacher and all their feedback"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Delete feedback first (due to foreign key constraint)
            cursor.execute("DELETE FROM feedback WHERE teacher_id = ?", (teacher_id,))
            # Delete teacher
            cursor.execute("DELETE FROM teachers WHERE id = ?", (teacher_id,))
            
            conn.commit()
            success = True
        except Exception as e:
            success = False
        finally:
            conn.close()
        
        return success

    def has_student_submitted_today(self, teacher_id: int, student_id: str) -> bool:
        """Check if a student has already submitted feedback today for this teacher."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 1
            FROM feedback
            WHERE teacher_id = ? AND student_id = ?
              AND DATE(submission_time) = DATE('now','localtime')
            LIMIT 1
            """,
            (teacher_id, student_id.strip()),
        )
        exists = cursor.fetchone() is not None
        conn.close()
        return exists
