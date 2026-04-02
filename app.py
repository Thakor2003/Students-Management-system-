from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def dashboard():
    conn = get_db()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template('dashboard.html', count=len(students))

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']

        conn = get_db()
        conn.execute("INSERT INTO students (name,email,course) VALUES (?,?,?)",
                     (name, email, course))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_student.html')

@app.route('/students')
def students():
    conn = get_db()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template('view_students.html', students=students)

@app.route('/delete/<int:id>')
def delete_student(id):
    conn = get_db()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/students')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = get_db()
    student = conn.execute("SELECT * FROM students WHERE id=?", (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']

        conn.execute("UPDATE students SET name=?, email=?, course=? WHERE id=?",
                     (name, email, course, id))
        conn.commit()
        conn.close()
        return redirect('/students')

    conn.close()
    return render_template('edit_student.html', student=student)

if __name__ == "__main__":
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        course TEXT
    )''')
    conn.close()

    app.run(host="0.0.0.0", port=5000, debug=True)
