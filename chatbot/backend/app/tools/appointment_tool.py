import os
import sqlite3


class AppointmentTool:
    def __init__(self, db_path="appointments.db"):
        self.db_path = db_path
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                service TEXT,
                date_time TEXT,
                status TEXT DEFAULT 'pending'
            )
        """
        )
        conn.commit()
        conn.close()

    def add_appointment(self, user_id, service, date_time):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO appointments (user_id, service, date_time)
            VALUES (?, ?, ?)
        """,
            (user_id, service, date_time),
        )
        conn.commit()
        conn.close()
        return "Appointment added successfully."

    def cancel_appointment(self, appointment_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE appointments SET status = 'cancelled' WHERE id = ?
        """,
            (appointment_id,),
        )
        conn.commit()
        conn.close()
        return (
            "Appointment cancelled successfully."
            if cursor.rowcount > 0
            else "Appointment not found."
        )

    def reschedule_appointment(self, appointment_id, new_date_time):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE appointments SET date_time = ? WHERE id = ?
        """,
            (new_date_time, appointment_id),
        )
        conn.commit()
        conn.close()
        return (
            "Appointment rescheduled successfully."
            if cursor.rowcount > 0
            else "Appointment not found."
        )

    def get_appointments(self, user_id=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if user_id:
            cursor.execute(
                "SELECT * FROM appointments WHERE user_id = ?", (user_id,)
            )
        else:
            cursor.execute("SELECT * FROM appointments")
        results = cursor.fetchall()
        conn.close()
        return results