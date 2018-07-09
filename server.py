from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
import datetime
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z.+_-]+$')
app = Flask(__name__)
app.secret_key = 'shhh'
mysql = connectToMySQL('emails')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def add():
    #print(mysql.query_db("SELECT * FROM emails"))
    error = 0
    if len(request.form['email']) < 1:
        flash("Email cannot be blank")
        error = 1
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid email address")
        error = 1
    if error > 0:
        return redirect('/')
    query = "INSERT INTO emails (email, created_at) VALUES (%(email)s, NOW());"
    data = {
        'email': request.form['email'],
        'created': datetime.datetime.now()
    }
    mysql.query_db(query, data)
    flash("Thank you for registering!")
    return redirect('/success')

@app.route('/success')
def success():
    results = mysql.query_db("SELECT email, created_at FROM emails")
    print(results)
    return render_template('success.html', results = results)

if __name__ == "__main__":
    app.run(debug=True)