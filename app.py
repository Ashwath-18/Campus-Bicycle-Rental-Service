from flask import Flask, render_template
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

@app.route('/grab')
def grab():
    return render_template('grab.html')

@app.route('/return')
def return_bike():
    return render_template('return.html')

if __name__ == '__main__':
    app.run(debug=True)
