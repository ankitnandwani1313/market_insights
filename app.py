from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from psycopg2 import sql, Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
db_config = {
    'host': 'localhost',
    'database': 'users',
    'user': 'XXXXXXXXXX',
    'password': 'XXXXXXXXX'
}
@app.route('/market_insights_info')
def market_insights_info():
    return render_template('market_insights_info.html')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email_id = request.form['email_id']
        password = request.form['password']
        address = request.form['address']

        try:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            # Insert the new user into the database
            cursor.execute('''
                INSERT INTO users.users_details (first_name, last_name, username, email_id, password, address)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (first_name, last_name, username, email_id, password, address))
            conn.commit()

            cursor.close()
            conn.close()

            flash('Sign up successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except Error as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('signup'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            # Fetch user from database based on username
            cursor.execute('SELECT * FROM users.users_details WHERE username = %s', (username,))
            user = cursor.fetchone()

            cursor.close()
            conn.close()

            if user and user[5] == password:  # Assuming password is in the 6th column
                flash('Login successful!', 'success')
                return redirect(url_for('success'))
            else:
                flash('Invalid username or password', 'danger')

        except Error as e:
            flash(f'Error: {str(e)}', 'danger')

        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)
