from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Gowtham0813",
        database="task_manager"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks')
def view_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return render_template('view_tasks.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        priority = request.form['priority']
        deadline = request.form['deadline']
        status = request.form['status']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, priority, deadline, status) VALUES (%s, %s, %s, %s)",
            (title, priority, deadline, status)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('view_tasks'))
    return render_template('add_task.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST']) 
def edit_task(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id=%s", (id,)) 
    task = cursor.fetchone()

    if request.method == 'POST':
        title = request.form['title']
        priority = request.form['priority']
        deadline = request.form['deadline']
        status = request.form['status']

        cursor.execute(
            "UPDATE tasks SET title=%s, priority=%s, deadline=%s, status=%s WHERE id=%s",
            (title, priority, deadline, status, id) 
        )
        conn.commit()
        conn.close()
        return redirect(url_for('view_tasks'))

    conn.close()
    return render_template('edit_task.html', task=task)

@app.route('/delete/<int:id>', methods=['GET', 'POST']) 
def delete_task(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id=%s", (id,))
    task = cursor.fetchone()

    if request.method == 'POST':
        cursor.execute("DELETE FROM tasks WHERE id=%s", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('view_tasks'))

    conn.close()
    return render_template('delete_task.html', task=task)

# SORT BY PRIORITY
@app.route('/sort/priority')
def sort_by_priority():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY priority ASC")
    tasks = cursor.fetchall()
    conn.close()
    return render_template('sort_by_priority.html', tasks=tasks)

# SORT BY DEADLINE
@app.route('/sort/deadline')
def sort_by_deadline():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY deadline ASC")
    tasks = cursor.fetchall()
    conn.close()
    return render_template('sort_by_deadline.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)
