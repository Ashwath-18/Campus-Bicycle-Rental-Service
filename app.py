from flask import Flask, render_template, request, jsonify, redirect , url_for
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

    # Fetch stations for dropdown
    cursor.execute("SELECT * FROM Stations")
    stations = cursor.fetchall()

    if request.method == 'POST':
        roll_no = request.form['roll_no']
        return_station_id = request.form['station_id']

        # Get active rental for this student
        cursor.execute("""
            SELECT Rentals.*, Students.name, Bicycles.type
            FROM Rentals
            JOIN Students ON Rentals.roll_no = Students.roll_no
            JOIN Bicycles ON Rentals.bicycle_id = Bicycles.bicycle_id
            WHERE Rentals.roll_no = %s AND Rentals.return_time IS NULL
        """, (roll_no,))
        rental = cursor.fetchone()

        # First check if student exists
        cursor.execute("SELECT * FROM Students WHERE roll_no = %s", (roll_no,))
        student = cursor.fetchone()

        if not student:
            cursor.close()
            conn.close()
            return render_template(
                "invalid_entry.html",
                roll_no=roll_no
            )

        # Then check active rental
        cursor.execute("""
            SELECT Rentals.*, Students.name, Bicycles.type
            FROM Rentals
            JOIN Students ON Rentals.roll_no = Students.roll_no
            JOIN Bicycles ON Rentals.bicycle_id = Bicycles.bicycle_id
            WHERE Rentals.roll_no = %s AND Rentals.return_time IS NULL
        """, (roll_no,))
        rental = cursor.fetchone()

        if not rental:
            cursor.close()
            conn.close()
            return render_template(
                "no_active_rental.html",
                roll_no=roll_no
        )

        bicycle_type = rental['type']

        # If EV, redirect to battery selection page
        if bicycle_type == "EV":
            cursor.close()
            conn.close()
            return redirect(url_for('return_battery',
                                    roll_no=roll_no,
                                    station_id=return_station_id))

        # NORMAL bicycle return
        bicycle_id = rental['bicycle_id']
        student_name = rental['name']
        return_time = datetime.now().replace(second=0, microsecond=0)

        # Update Rentals table
        cursor.execute("""
            UPDATE Rentals
            SET return_time = %s,
                return_station_id = %s
            WHERE rental_id = %s
        """, (return_time, return_station_id, rental['rental_id']))

        # Update Bicycles table
        cursor.execute("""
            UPDATE Bicycles
            SET status = 'Available',
                station_id = %s
            WHERE bicycle_id = %s
        """, (return_station_id, bicycle_id))

        conn.commit()

        # Get station name
        cursor.execute("SELECT block_name FROM Stations WHERE station_id = %s", (return_station_id,))
        station = cursor.fetchone()

        cursor.close()
        conn.close()

        # Render return success page
        return render_template(
            "return_success.html",
            name=student_name,
            bicycle_id=bicycle_id,
            bicycle_type=bicycle_type,
            station_name=station['block_name'],
            date=return_time.strftime("%Y-%m-%d"),
            time=return_time.strftime("%H:%M")
        )

    cursor.close()
    conn.close()
    return render_template("return.html", stations=stations)

# ================= RETURN BATTERY MODULE =================
@app.route('/return_battery', methods=['GET', 'POST'])
def return_battery():
    if request.method == 'POST':
        roll_no = request.form['roll_no']
        return_station_id = request.form['station_id']
        battery_percentage = request.form['battery_percentage']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Get active rental
        cursor.execute("""
            SELECT Rentals.*, Students.name, Bicycles.type
            FROM Rentals
            JOIN Students ON Rentals.roll_no = Students.roll_no
            JOIN Bicycles ON Rentals.bicycle_id = Bicycles.bicycle_id
            WHERE Rentals.roll_no = %s AND Rentals.return_time IS NULL
        """, (roll_no,))
        rental = cursor.fetchone()

        if not rental:
            cursor.close()
            conn.close()
            return "No active rental found."

        bicycle_id = rental['bicycle_id']
        student_name = rental['name']
        return_time = datetime.now().replace(second=0, microsecond=0)

        # Update Rentals table
        cursor.execute("""
            UPDATE Rentals
            SET return_time = %s,
                return_station_id = %s
            WHERE rental_id = %s
        """, (return_time, return_station_id, rental['rental_id']))

        # Update Bicycles table including battery percentage
        cursor.execute("""
            UPDATE Bicycles
            SET status = 'Available',
                station_id = %s,
                battery_percentage = %s
            WHERE bicycle_id = %s
        """, (return_station_id, battery_percentage, bicycle_id))

        conn.commit()

        # Get station name
        cursor.execute("SELECT block_name FROM Stations WHERE station_id = %s", (return_station_id,))
        station = cursor.fetchone()

        cursor.close()
        conn.close()

        # Render return success page
        return render_template(
            "return_success.html",
            name=student_name,
            bicycle_id=bicycle_id,
            bicycle_type='EV',
            battery_percentage=battery_percentage,
            station_name=station['block_name'],
            date=return_time.strftime("%Y-%m-%d"),
            time=return_time.strftime("%H:%M")
        )

    # GET request → show battery selection page
    roll_no = request.args.get('roll_no')
    return_station_id = request.args.get('station_id')
    return render_template("return_battery.html",
                           roll_no=roll_no,
                           station_id=return_station_id)


# ================= GRAB MODULE =================
@app.route('/grab', methods=['GET', 'POST'])
def grab_bicycle():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Load stations (for dropdown)
    cursor.execute("SELECT * FROM Stations")
    stations = cursor.fetchall()

    # ================= POST =================
    if request.method == 'POST':
        roll_no = request.form['roll_no'].strip().upper()
        bicycle_type = request.form['bicycle_type']
        station_id = request.form['station_id']

        try:
            # 1️⃣ Check student
            cursor.execute("SELECT * FROM Students WHERE roll_no = %s", (roll_no,))
            student = cursor.fetchone()

            if not student:
                cursor.close()
                conn.close()

                return render_template(
                    "invalid_entry.html",
                    roll_no=roll_no
                )

            # 2️⃣ Check active rental
            cursor.execute("""
                SELECT * FROM Rentals
                WHERE roll_no = %s AND return_time IS NULL
            """, (roll_no,))

            active_rental = cursor.fetchone()
            if active_rental:
            # Get extra details of active rental
                cursor.execute("""
                    SELECT Bicycles.type, Stations.block_name
                    FROM Rentals
                    JOIN Bicycles ON Rentals.bicycle_id = Bicycles.bicycle_id
                    JOIN Stations ON Rentals.grab_station_id = Stations.station_id
                    WHERE Rentals.roll_no = %s AND Rentals.return_time IS NULL
                """, (roll_no,))

                rental_info = cursor.fetchone()

                cursor.close()
                conn.close()

                return render_template(
                    "grab_error.html",
                    roll_no=roll_no,
                    bicycle_type=rental_info['type'],
                    station_name=rental_info['block_name']
                )

            # 3️⃣ Find available bike
            cursor.execute("""
                SELECT * FROM Bicycles
                WHERE type=%s 
                AND status='Available'
                AND station_id=%s
                AND (type='Normal' OR battery_percentage >= 5)
                LIMIT 1
            """, (bicycle_type, station_id))

            bicycle = cursor.fetchone()

            if not bicycle:
                cursor.close()
                conn.close()

                if bicycle_type == "Normal":
                    message = "Normal bicycles are currently not available at this station."
                else:
                    message = "EV bicycles are currently not available at this station."

                return render_template(
                    "grab_unavailable.html",
                    message=message,
                    station_id=station_id
                )

            grab_time = datetime.now().replace(second=0, microsecond=0)

            # 4️⃣ Insert rental
            cursor.execute("""
                INSERT INTO Rentals (roll_no, bicycle_id, grab_time, grab_station_id)
                VALUES (%s, %s, %s, %s)
            """, (roll_no, bicycle['bicycle_id'], grab_time, station_id))

            # 5️⃣ Update bike status
            cursor.execute("""
                UPDATE Bicycles
                SET status='In Use'
                WHERE bicycle_id=%s
            """, (bicycle['bicycle_id'],))

            conn.commit()

            # 6️⃣ Get station name for popup
            cursor.execute("SELECT block_name FROM Stations WHERE station_id=%s", (station_id,))
            station = cursor.fetchone()
            station_name = station['block_name']

            formatted_date = grab_time.strftime("%Y-%m-%d")
            formatted_time = grab_time.strftime("%H:%M")

            cursor.close()
            conn.close()

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
            cursor.close()
            conn.close()
            return f"Error: {e}"

    # ================= GET =================
    availability = {"Normal": 0, "EV": 0}

    cursor.execute("""
        SELECT type, COUNT(*) as count
        FROM Bicycles
        WHERE status='Available'
        AND (type='Normal' OR battery_percentage >= 5)
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
        AND (type='Normal' OR battery_percentage >= 5) 
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