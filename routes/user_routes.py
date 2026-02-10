from flask import Blueprint, render_template, request, redirect
from config import get_db_connection

user_bp = Blueprint('user', __name__)

@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO users (name, email, phone, password)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (name, email, phone, password))
        conn.commit()

        cursor.close()
        conn.close()

        return "User Registered Successfully!"

    return render_template("register.html")
