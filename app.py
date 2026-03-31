from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    course TEXT
                )''')
    conn.commit()
    conn.close()

create_table()

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form["username"]=="admin" and request.form["password"]=="1234":
            session["user"]="admin"
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    conn=get_db()
    count=conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    conn.close()
    return render_template("dashboard.html",count=count)

@app.route("/add", methods=["GET","POST"])
def add_student():
    if "user" not in session:
        return redirect("/")
    if request.method=="POST":
        conn=get_db()
        conn.execute("INSERT INTO students (name,email,course) VALUES (?,?,?)",
                     (request.form["name"],request.form["email"],request.form["course"]))
        conn.commit()
        conn.close()
        return redirect("/students")
    return render_template("add_student.html")

@app.route("/students")
def students():
    if "user" not in session:
        return redirect("/")
    conn=get_db()
    data=conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template("view_students.html",students=data)

@app.route("/delete/<int:id>")
def delete(id):
    conn=get_db()
    conn.execute("DELETE FROM students WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return redirect("/students")

@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):
    conn=get_db()
    if request.method=="POST":
        conn.execute("UPDATE students SET name=?,email=?,course=? WHERE id=?",
                     (request.form["name"],request.form["email"],request.form["course"],id))
        conn.commit()
        conn.close()
        return redirect("/students")
    student=conn.execute("SELECT * FROM students WHERE id=?",(id,)).fetchone()
    conn.close()
    return render_template("edit_student.html",student=student)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)
