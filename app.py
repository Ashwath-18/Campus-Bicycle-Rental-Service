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

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ✅ Always fetch stations first (for dropdown)
    cursor.execute("SELECT * FROM Stations")
    stations = cursor.fetchall()

    if request.method == 'POST':
        roll_no = request.form['roll_no']
        return_station_id = request.form['station_id']

        # 1️⃣ Find active rental
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

        # 2️⃣ Update Rentals table
        cursor.execute("""
            UPDATE Rentals
            SET return_time = %s,
                return_station_id = %s
            WHERE rental_id = %s
        """, (return_time, return_station_id, rental['rental_id']))

        # 3️⃣ Update Bicycle status + move to return station
        cursor.execute("""
            UPDATE Bicycles
            SET status = 'Available',
                station_id = %s
            WHERE bicycle_id = %s
        """, (return_station_id, bicycle_id))

        conn.commit()

        formatted_date = return_time.strftime("%Y-%m-%d")
        formatted_time = return_time.strftime("%H:%M")

        # 🔹 Get return station name
        cursor.execute("SELECT block_name FROM Stations WHERE station_id = %s", (return_station_id,))
        station = cursor.fetchone()
        return_station_name = station['block_name']

        return render_template(
            "return_success.html",
            name=student_name,
            bicycle_id=bicycle_id,
            station_name=return_station_name,
            date=formatted_date,
            time=formatted_time
        )

    # 🔹 GET request
    cursor.close()
    conn.close()

    return render_template("return.html", stations=stations)


@app.route('/grab', methods=['GET', 'POST'])
def grab_bicycle():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 🔹 Always fetch stations first (for dropdown)
    cursor.execute("SELECT * FROM Stations")
    stations = cursor.fetchall()

    if request.method == 'POST':
        roll_no = request.form['roll_no']
        bicycle_type = request.form['bicycle_type']
        station_id = request.form['station_id']

        try:
            # 1️⃣ Get student
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

            # 3️⃣ Find available bicycle in selected station
            cursor.execute("""
                SELECT * FROM Bicycles
                WHERE type = %s 
                AND status = 'Available'
                AND station_id = %s
                LIMIT 1
            """, (bicycle_type, station_id))

            bicycle = cursor.fetchone()

            if not bicycle:
                return "No bicycles available at selected station."

            grab_time = datetime.now().replace(second=0, microsecond=0)

            # 4️⃣ Insert rental
            cursor.execute("""
                INSERT INTO Rentals (roll_no, bicycle_id, grab_time, grab_station_id)
                VALUES (%s, %s, %s, %s)
            """, (roll_no, bicycle['bicycle_id'], grab_time, station_id))

            # 5️⃣ Update bicycle status
            cursor.execute("""
                UPDATE Bicycles
                SET status = 'In Use'
                WHERE bicycle_id = %s
            """, (bicycle['bicycle_id'],))

            conn.commit()

            # 6️⃣ Get station name
            cursor.execute("SELECT block_name FROM Stations WHERE station_id = %s", (station_id,))
            station = cursor.fetchone()
            station_name = station['block_name']

            formatted_date = grab_time.strftime("%Y-%m-%d")
            formatted_time = grab_time.strftime("%H:%M")

            return render_template(
                "grab_success.html",
                name=student['name'],
                bicycle_id=bicycle['bicycle_id'],
                station_name=station_name,
                date=formatted_date,
                time=formatted_time
            )

        except Exception as e:
            conn.rollback()
            return f"Error: {e}"

        finally:
            cursor.close()
            conn.close()

    # 🔹 For GET request
    cursor.close()
    conn.close()

    return render_template('grab.html', stations=stations)

if __name__ == '__main__':
    app.run(debug=True)