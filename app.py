from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "dev-secret-key"  # para flash messages
DB_PATH = Path("todo.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                category TEXT,
                done INTEGER NOT NULL DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        conn.commit()


@app.route("/", methods=["GET"])
def index():
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "all")  # all | done | pending

    sql = "SELECT * FROM tasks WHERE 1=1"
    params = []

    if q:
        sql += " AND (title LIKE ? OR description LIKE ? OR category LIKE ?)"
        like = f"%{q}%"
        params += [like, like, like]

    if status == "done":
        sql += " AND done = 1"
    elif status == "pending":
        sql += " AND done = 0"

    sql += " ORDER BY done ASC, created_at DESC"

    with get_conn() as conn:
        tasks = conn.execute(sql, params).fetchall()

    return render_template("index.html", tasks=tasks, q=q, status=status)


@app.route("/new", methods=["GET", "POST"])
def new_task():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "").strip()

        if not title:
            flash("Título é obrigatório.", "error")
            return render_template("form.html")

        with get_conn() as conn:
            conn.execute(
                "INSERT INTO tasks (title, description, category) VALUES (?, ?, ?)",
                (title, description, category),
            )
            conn.commit()

        flash("Tarefa criada com sucesso!", "success")
        return redirect(url_for("index"))

    return render_template("form.html")


@app.post("/toggle/<int:task_id>")
def toggle_task(task_id: int):
    with get_conn() as conn:
        row = conn.execute("SELECT done FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not row:
            flash("Tarefa não encontrada.", "error")
            return redirect(url_for("index"))

        new_done = 0 if row["done"] == 1 else 1
        conn.execute("UPDATE tasks SET done = ? WHERE id = ?", (new_done, task_id))
        conn.commit()

    flash("Status atualizado.", "success")
    return redirect(url_for("index"))


@app.post("/delete/<int:task_id>")
def delete_task(task_id: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()

    flash("Tarefa removida.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)