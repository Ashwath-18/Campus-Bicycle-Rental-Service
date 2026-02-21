from flask import Flask, render_template, request
from config import Config
from database.db_connection import get_db_connection
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/test-db')
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        cursor.close()
        conn.close()
        return f"Connected to database: {db_name}"
    except Exception as e:
        return f"Error: {e}"

@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) as count FROM Bicycles WHERE type='Normal' AND status='Available'")
    normal_count = cursor.fetchone()['count']

    cursor.execute("SELECT COUNT(*) as count FROM Bicycles WHERE type='EV' AND status='Available'")
    ev_count = cursor.fetchone()['count']

    cursor.close()
    conn.close()

    return render_template('index.html', normal=normal_count, ev=ev_count)



@app.route('/return', methods=['GET', 'POST'])
def return_bike():

    if request.method == 'POST':
        roll_no = request.form['roll_no']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 1️⃣ Find active rental
        cursor.execute("""
            SELECT Rentals.*, Students.name
            FROM Rentals
            JOIN Students ON Rentals.roll_no = Students.roll_no
            WHERE Rentals.roll_no = %s AND Rentals.return_time IS NULL
        """, (roll_no,))

        rental = cursor.fetchone()

        if not rental:
            return "No active rental found for this student."

        bicycle_id = rental['bicycle_id']
        student_name = rental['name']
        return_time = datetime.now().replace(second=0, microsecond=0)

        # 2️⃣ Update Rentals table
        cursor.execute("""
            UPDATE Rentals
            SET return_time = %s
            WHERE rental_id = %s
        """, (return_time, rental['rental_id']))

        # 3️⃣ Update Bicycle status
        cursor.execute("""
            UPDATE Bicycles
            SET status = 'Available'
            WHERE bicycle_id = %s
        """, (bicycle_id,))

        conn.commit()
        cursor.close()
        conn.close()

        formatted_date = return_time.strftime("%Y-%m-%d")
        formatted_time = return_time.strftime("%H:%M")

        return render_template(
            "return_success.html",
            name=student_name,
            bicycle_id=bicycle_id,
            date=formatted_date,
            time=formatted_time
        )

    return render_template("return.html")

@app.route('/grab', methods=['GET', 'POST'])
def grab_bicycle():
    if request.method == 'POST':
        roll_no = request.form['roll_no']
        bicycle_type = request.form['bicycle_type']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # 1️⃣ Get student details
            cursor.execute("SELECT * FROM Students WHERE roll_no = %s", (roll_no,))
            student = cursor.fetchone()

            if not student:
                return "Student not found."

            # 2️⃣ Check active rental
            cursor.execute("""
                SELECT * FROM Rentals
                WHERE roll_no = %s AND return_time IS NULL
            """, (roll_no,))
            active_rental = cursor.fetchone()

            if active_rental:
                return "You already have an active rental."

            # 3️⃣ Find available bicycle
            cursor.execute("""
                SELECT * FROM Bicycles
                WHERE type = %s AND status = 'Available'
                LIMIT 1
            """, (bicycle_type,))
            bicycle = cursor.fetchone()

            if not bicycle:
                return "No bicycles available."

            grab_time = datetime.now().replace(second=0, microsecond=0)

            # 4️⃣ Insert rental
            cursor.execute("""
                INSERT INTO Rentals (roll_no, bicycle_id, grab_time)
                VALUES (%s, %s, %s)
            """, (roll_no, bicycle['bicycle_id'], grab_time))

            # 5️⃣ Update bicycle status
            cursor.execute("""
                UPDATE Bicycles
                SET status = 'In Use'
                WHERE bicycle_id = %s
            """, (bicycle['bicycle_id'],))

            conn.commit()

            formatted_date = grab_time.strftime("%Y-%m-%d")
            formatted_time = grab_time.strftime("%H:%M")

            return render_template(
                "grab_success.html",
                name=student['name'],
                bicycle_id=bicycle['bicycle_id'],
                date=formatted_date,
                time=formatted_time
            )

        except Exception as e:
            conn.rollback()
            return f"Error: {e}"

        finally:
            cursor.close()
            conn.close()

    return render_template('grab.html')

if __name__ == '__main__':
    app.run(debug=True)