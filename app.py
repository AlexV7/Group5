import csv
import datetime
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

TASKS_FILE = 'tasks.csv'
STUDY_FILE = 'study_history.csv'


# ==============================================================================
# 1. HOME CONTROLLER (Ported directly from HomeController.java)
# ==============================================================================

@app.route('/')
def home():
    """Renders the main Home view."""
    return render_template('index.html')


@app.route('/tasks', methods=['GET', 'POST'])
def goToTasks():
    """
    Equivalent to goToTasks(ActionEvent event) in HomeController.java.
    Loads task data and processes new task creation.
    """
    if request.method == 'POST':
        task_title = request.form.get('title')
        if task_title:
            save_task(task_title, False)
        return redirect(url_for('goToTasks'))

    all_tasks = load_tasks()
    return render_template('tasks.html', tasks=all_tasks)


@app.route('/timer')
def goToTimer():
    """
    Equivalent to goToTimer(ActionEvent event) in HomeController.java.
    Loads active tasks for the timer dropdown.
    """
    all_tasks = load_tasks()
    active_tasks = [t for t in all_tasks if not t['is_completed']]
    return render_template('timer.html', tasks=active_tasks)


@app.route('/study-log')
def goToStudyLog():
    """
    Equivalent to goToStudyLog(ActionEvent event) in HomeController.java.
    Loads recorded study sessions.
    """
    sessions = load_study_sessions()
    return render_template('logs.html', sessions=sessions)


# ==============================================================================
# 2. HELPER FUNCTIONS & MODELS (Ported from Task.java & StudySession.java)
# ==============================================================================

def load_tasks():
    """Reads tasks from tasks.csv (Equivalent to TaskModel / Task.java)."""
    tasks = []
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    tasks.append({
                        'title': row[0],
                        'is_completed': row[1].strip().lower() == 'true'
                    })
    return tasks


def save_task(title, is_completed=False):
    """Appends a task to tasks.csv (Equivalent to Task.toCSV())."""
    with open(TASKS_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([title, is_completed])


def load_study_sessions():
    """Reads session history from study_history.csv."""
    sessions = []
    if os.path.exists(STUDY_FILE):
        with open(STUDY_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 5:
                    sessions.append({
                        'date': row[0],
                        'duration': row[1],
                        'task_name': row[2],
                        'completed': row[3],
                        'type': row[4]
                    })
    return sessions


# ==============================================================================
# 3. TIMER API ENDPOINT (Ported from TimerController.java)
# ==============================================================================

@app.route('/log-session', methods=['POST'])
def log_session():
    """Saves completed focus sessions to study_history.csv."""
    data = request.get_json()
    if data:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        duration = data.get('duration', 25)
        task_name = data.get('task_name', 'Unspecified Focus')
        session_type = data.get('type', 'Pomodoro')

        with open(STUDY_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, duration, task_name, True, session_type])

        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'error'}), 400


if __name__ == '__main__':
    app.run(debug=True)
