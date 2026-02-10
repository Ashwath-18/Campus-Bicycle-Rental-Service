from flask import Flask
from routes.user_routes import user_bp

app = Flask(__name__)
app.register_blueprint(user_bp)

@app.route("/")
def home():
    return "Vehicle Service Management System Running!"

if __name__ == "__main__":
    app.run(debug=True)
