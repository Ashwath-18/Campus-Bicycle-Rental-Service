from flask import Flask, render_template

app = Flask(__name__)

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
