# Using Python as Backend file for establishing connection between MySQL and website.

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import datetime

app = Flask(__name__)

db_info = {
    'host': "localhost",
    'username': "root",
    'password': "",
    'database': "HealthMonitor"
}

def db_connect():
    try:
        conn = mysql.connector.connect(**db_info)
        return "<h1>Connection successful to " + db_info['database'] + "</h1>"
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # This section will handle the logic of request
        user_age = request.form.get('age')
        user_height = request.form.get('height')
        user_weight = request.form.get('weight')

        received_data=f"Received data: Age={user_age}, Weight={user_weight}, Height={user_height}"

        return render_template('index.html', received_data=received_data)
    else:
        # render index.html
        return render_template('index.html')


@app.route('/greet')
def greet():
    return "Hello, World! This is the Health Monitor System."


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)