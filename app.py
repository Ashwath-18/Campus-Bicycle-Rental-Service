from flask import Flask, render_template, request, jsonify, redirect, url_for
from config import Config
from database.db_connection import get_db_connection
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)


# ================= TEST DB =================
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


# ================= HOME =================
@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT type, COUNT(*) as count
        FROM Bicycles
        WHERE status='Available'
        GROUP BY type
    """)
    results = cursor.fetchall()

    normal = 0
    ev = 0

    for row in results:
        if row['type'] == 'Normal':
            normal = row['count']
        elif row['type'] == 'EV':
            ev = row['count']

    cursor.close()
    conn.close()

    return render_template('index.html', normal=normal, ev=ev)


# ================= RETURN MODULE =================
@app.route('/return', methods=['GET', 'POST'])
def return_bike():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Stations")
    stations = cursor.fetchall()

    if request.method == 'POST':
        roll_no = request.form['roll_no']
        return_station_id = request.form['station_id']

        cursor.execute("""
            SELECT Rentals.*, Students.name
            FROM Rentals
            JOIN Students ON Rentals.roll_no = Students.roll_no
            WHERE Rentals.roll_no = %s AND Rentals.return_time IS NULL
        """, (roll_no,))
        rental = cursor.fetchone()

        if not rental:
            cursor.close()
            conn.close()
            return "No active rental found for this student."

        bicycle_id = rental['bicycle_id']
        student_name = rental['name']
        return_time = datetime.now().replace(second=0, microsecond=0)

        cursor.execute("""
            UPDATE Rentals
            SET return_time = %s,
                return_station_id = %s
            WHERE rental_id = %s
        """, (return_time, return_station_id, rental['rental_id']))

        cursor.execute("""
            UPDATE Bicycles
            SET status = 'Available',
                station_id = %s
            WHERE bicycle_id = %s
        """, (return_station_id, bicycle_id))

        conn.commit()

        cursor.execute("SELECT block_name FROM Stations WHERE station_id = %s", (return_station_id,))
        station = cursor.fetchone()

        cursor.close()
        conn.close()

        return render_template(
            "return_success.html",
            name=student_name,
            bicycle_id=bicycle_id,
            station_name=station['block_name'],
            date=return_time.strftime("%Y-%m-%d"),
            time=return_time.strftime("%H:%M")
        )

    cursor.close()
    conn.close()

    return render_template("return.html", stations=stations)


# ================= GRAB MODULE =================
@app.route('/grab', methods=['GET', 'POST'])
def grab_bicycle():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Stations")
    stations = cursor.fetchall()

    # ================= POST =================
    if request.method == 'POST':
        roll_no = request.form['roll_no'].strip().upper()
        bicycle_type = request.form['bicycle_type']
        station_id = request.form['station_id']

        try:
            # Check student
            cursor.execute("SELECT * FROM Students WHERE roll_no = %s", (roll_no,))
            student = cursor.fetchone()

            if not student:
                return "Student not found."

            # Check active rental
            cursor.execute("""
                SELECT * FROM Rentals
                WHERE roll_no = %s AND return_time IS NULL
            """, (roll_no,))
            if cursor.fetchone():
                return "You already have an active rental."

            # Find available bike
            cursor.execute("""
                SELECT * FROM Bicycles
                WHERE type=%s AND status='Available' AND station_id=%s
                LIMIT 1
            """, (bicycle_type, station_id))

            bicycle = cursor.fetchone()

            if not bicycle:
                return "No bicycles available at selected station."

            grab_time = datetime.now().replace(second=0, microsecond=0)

            # Insert rental
            cursor.execute("""
                INSERT INTO Rentals (roll_no, bicycle_id, grab_time, grab_station_id)
                VALUES (%s, %s, %s, %s)
            """, (roll_no, bicycle['bicycle_id'], grab_time, station_id))

            # Update bike status
            cursor.execute("""
                UPDATE Bicycles
                SET status='In Use'
                WHERE bicycle_id=%s
            """, (bicycle['bicycle_id'],))

            conn.commit()

            cursor.close()
            conn.close()

            return redirect(url_for('grab_bicycle'))

        except Exception as e:
            conn.rollback()
            cursor.close()
            conn.close()
            return f"Error: {e}"

    # ================= GET =================
    # By default → show TOTAL campus availability
    availability = {"Normal": 0, "EV": 0}

    cursor.execute("""
        SELECT type, COUNT(*) as count
        FROM Bicycles
        WHERE status='Available'
        GROUP BY type
    """)
    results = cursor.fetchall()

    for row in results:
        availability[row['type']] = row['count']

    cursor.close()
    conn.close()

    return render_template(
        'grab.html',
        stations=stations,
        availability=availability
    )


# ================= AJAX (Station-wise Availability) =================
@app.route('/get-availability/<int:station_id>')
def get_availability(station_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    availability = {"Normal": 0, "EV": 0}

    cursor.execute("""
        SELECT type, COUNT(*) as count
        FROM Bicycles
        WHERE station_id=%s AND status='Available'
        GROUP BY type
    """, (station_id,))

    results = cursor.fetchall()

    for row in results:
        availability[row['type']] = row['count']

    cursor.close()
    conn.close()

    return jsonify(availability)


if __name__ == '__main__':
    app.run(debug=True)