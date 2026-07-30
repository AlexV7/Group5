import csv
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
TASKS_FILE = 'tasks.csv'
STUDY_FILE = 'study_history.csv'

# --- Helper Functions (Replacing TaskModel & CSV Methods) ---

def load_tasks():
    """Reads tasks from tasks.csv (Equivalent to TaskModel loadFromFile)"""
    tasks = []
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    # row[0] = title, row[1] = isCompleted ('True'/'False')
                    tasks.append({
                        'title': row[0],
                        'is_completed': row[1].strip().lower() == 'true'
                    })
    return tasks

def save_task(title, is_completed=False):
    """Appends a new task to tasks.csv (Equivalent to Task.toCSV)"""
    with open(TASKS_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([title, is_completed])

# --- Routes (Replacing Controllers) ---

@app.route('/')
def home():
    """Home View (Equivalent to HomeController)"""
    return render_template('index.html')

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    """Task Management View & Actions (Equivalent to TaskController)"""
    if request.method == 'POST':
        task_title = request.form.get('title')
        if task_title:
            save_task(task_title, False)
        return redirect(url_for('tasks'))

    all_tasks = load_tasks()
    return render_template('tasks.html', tasks=all_tasks)

@app.route('/timer')
def timer():
    """Pomodoro Timer View (Equivalent to TimerController)"""
    return render_template('timer.html')

@app.route('/study-log')
def study_log():
    """Study History View (Equivalent to StudyLogController)"""
    return render_template('logs.html')

if __name__ == '__main__':
    app.run(debug=True)
