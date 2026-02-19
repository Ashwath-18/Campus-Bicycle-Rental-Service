from flask import Flask, render_template, request
from config import Config
from database.db_connection import get_db_connection


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
    return render_template('index.html')



@app.route('/return')
def return_bike():
    return render_template('return.html')

@app.route('/grab', methods=['GET', 'POST'])
def grab_bicycle():
    if request.method == 'POST':
        roll_no = request.form['roll_no']
        bicycle_type = request.form['bicycle_type']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT * FROM Rentals
                WHERE roll_no = %s AND return_time IS NULL
            """, (roll_no,))
            active_rental = cursor.fetchone()

            if active_rental:
                return "You already have an active rental."

            cursor.execute("""
                SELECT * FROM Bicycles
                WHERE type = %s AND status = 'Available'
                LIMIT 1
            """, (bicycle_type,))
            bicycle = cursor.fetchone()

            if not bicycle:
                return "No bicycles available."

            cursor.execute("""
                INSERT INTO Rentals (roll_no, bicycle_id, grab_time)
                VALUES (%s, %s, NOW())
            """, (roll_no, bicycle['bicycle_id']))

            cursor.execute("""
                UPDATE Bicycles
                SET status = 'In Use'
                WHERE bicycle_id = %s
            """, (bicycle['bicycle_id'],))

            conn.commit()
            return f"Bicycle {bicycle['bicycle_id']} Grabbed Successfully!"

        except Exception as e:
            conn.rollback()
            return f"Error: {e}"

        finally:
            cursor.close()
            conn.close()

    return render_template('grab.html')

if __name__ == '__main__':
    app.run(debug=True)
