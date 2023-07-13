from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient

from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "kartik"  # Change this to a secure key
client = MongoClient('mongodb+srv://kartikpoojary8:kartik@kartik.p9a2qyy.mongodb.net/?retryWrites=true&w=majority')
db = client['student_management_system']
students = db['students']

# Rest of the code...



@app.route('/')
def index():
    if 'username' in session:
        return redirect('/dashboard')
    else:
        return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_student = students.find_one({'username': username})
        if existing_student:
            return render_template('register.html', error='Username already taken')

        existing_student = students.find_one({'email': request.form['email']})
        if existing_student:
            return render_template('register.html', error='Email already registered')

        student = {
            'username': username,
            'password': password,
            'email': request.form['email'],
            'marks': {},
            'activities': [],
            'attendance': {}
        }
        students.insert_one(student)
        session['username'] = username
        return redirect('/dashboard')
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        student = students.find_one({'username': username, 'password': password})
        if student:
            session['username'] = username
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        student = students.find_one({'username': username})
        return render_template('dashboard.html', student=student)
    else:
        return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
