from flask import Flask, render_template, request, flash, redirect, url_for, get_flashed_messages
import csv

app = Flask(__name__)
app.secret_key = 'random string'

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/login', methods=['GET'])
def show_login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    with open('registered.csv', 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            if len(line) == 3 and line[0] == username and line[2] == password:
                flash('You were successfully logged in', category='success')
                return redirect(url_for('login'))
                # return render_template('success.html', message='Login successful')
        
    # If no match is found, return an error message
        flash('Enter a valid username and password', category='error')
        return redirect(url_for('login'))
    # return render_template('failure.html', error=error)

@app.route('/register', methods=['GET'])
def show_register():
    return render_template('register.html')
    
@app.route('/register', methods=['POST'])
def register():
    # Get the username from the form
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if the username already exists in the CSV file

    with open('registered.csv', 'r') as file:
        reader = csv.reader(file)
        existing_usernames = [line[0] for line in reader if len(line) != 0]
        
        if username in existing_usernames:
            flash('Username or email already exists', category='error')
            return redirect(url_for('register'))
        
        # If the username does not exist, write the new username to the CSV file

        with open('registered.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow((username, email, password))
            flash('Registration successful', category='success')
            return redirect(url_for('register'))
        


if __name__ == '__main__':
    app.run(debug=True)
