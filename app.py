
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("tasks.db")

with get_db() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    """)

@app.route("/")
def home():
    with get_db() as conn:
        tasks = conn.execute(
            "SELECT * FROM tasks ORDER BY id DESC"
        ).fetchall()

    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task", "").strip()

    if task:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO tasks (task) VALUES (?)",
                (task,)
            )

    return redirect("/")

@app.route("/delete/<int:task_id>")
def delete(task_id):
    with get_db() as conn:
        conn.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)