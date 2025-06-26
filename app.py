# Using Python as Backend file for establishing connection between MySQL and website.

# app.py

from flask import Flask, render_template, request
import mysql.connector

# Initialize the Flask application
app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',         # <-- The password for 'root' in XAMPP is often empty
    'database': 'HealthMonitor'
}

# --- Function to establish a database connection ---
def get_db_connection():
    """Establishes and returns a new connection to the database."""
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Successfully connected to MySQL Database, version: {db_info}")
            return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL database: {err}")
    return None

# --- Main Route to test the connection ---
@app.route('/')
def index():
    """
    A simple route to check if the backend is running and can connect to the database.
    """
    connection = get_db_connection()
    if connection:
        # If connection is successful, close it and return a success message
        connection.close()
        return "<h1>Backend is up and running!</h1><p>Successfully connected to the 'HealthMonitor' database.</p>"
    else:
        # If connection fails, return an error message
        return "<h1>Backend is down!</h1><p>Failed to connect to the 'HealthMonitor' database. Check XAMPP and your credentials.</p>"

# --- A simple route to demonstrate fetching data ---
@app.route('/health_data')
def get_health_data():
    """
    Fetches some data from a sample table in the database.
    """
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True) # dictionary=True for easy access by column name
        
        try:
            # First, check if the table exists and create it if it doesn't
            # This is a good practice for the first run
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    blood_pressure VARCHAR(50),
                    heart_rate INT,
                    entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            connection.commit() # Commit the table creation
            
            # Now, fetch some data
            cursor.execute("SELECT * FROM patients ORDER BY entry_date DESC LIMIT 10")
            records = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            # Format the data for display on the website
            if records:
                html_output = "<h2>Recent Patient Records</h2><ul>"
                for record in records:
                    html_output += f"<li>ID: {record['id']}, Name: {record['name']}, BP: {record['blood_pressure']}, Heart Rate: {record['heart_rate']}</li>"
                html_output += "</ul>"
                return html_output
            else:
                return "<p>No patient data found. The 'patients' table is empty.</p>"
                
        except mysql.connector.Error as err:
            return f"An error occurred while fetching data: {err}"
            
    return "<h1>Database Connection Failed!</h1><p>Could not fetch data.</p>"


# --- Run the Flask application ---
if __name__ == '__main__':
    # 'debug=True' is great for development as it auto-reloads the server on code changes
    app.run(debug=True)