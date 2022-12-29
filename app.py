# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import mysql.connector

app = Flask(__name__)


#app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'vaccinebook'


def connect_db():
      # Replace 'username', 'password', and 'database' with your MySQL credentials
  connection = mysql.connector.connect(user='root', password='', database='vaccinebook')
  return connection

mysql = MySQL(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('index.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/adminlogin')
def adminlogin():
    return render_template('adminlogin.html')

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or  not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO accounts(id,username, password, email, ) VALUES (NULL,% s, % s, % s)', (username, password, email,))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)
@app.route('/adminlocations', methods=['GET', 'POST'])
def admin_locations():
    
  connection = connect_db()
  cursor = connection.cursor()
  if request.method == 'POST':
    if request.form['action'] == 'add':
      center = request.form['center']
      # Add the center to the database
      cursor.execute('INSERT INTO centers (name) VALUES (%s)', (center,))
      connection.commit()
      flash('Vaccination center added')
    elif request.form['action'] == 'remove':
      center = request.form['center']
      # Remove the center from the database
      cursor.execute('DELETE FROM centers WHERE name = %s', (center,))
      connection.commit()
      flash('Vaccination center removed')
  # Get the list of centers from the database
  cursor.execute('SELECT name FROM centers')
  centers = cursor.fetchall()
  cursor.close()
  connection.close()
  return render_template('admin_locations.html', centers=centers)


if __name__ == '__main__':
    app.run()
