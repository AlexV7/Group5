from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tasks')
def tasks():
    return render_template('tasks.html')

@app.route('/timer')
def timer():
    return render_template('timer.html')

@app.route('/study-log')
def study_log():
    return render_template('logs.html')

if __name__ == '__main__':
    app.run(debug=True)
