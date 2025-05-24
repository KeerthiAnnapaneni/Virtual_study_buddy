from flask import Flask, render_template, request, jsonify, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for sessions
app.permanent_session_lifetime = timedelta(days=7)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start-session', methods=['POST'])
def start_session():
    data = request.json
    topic = data.get('topic')
    study_hours = int(data.get('studyHours'))
    break_minutes = int(data.get('breakMinutes'))
    tasks_raw = data.get('tasks', '')
    tasks = [task.strip() for task in tasks_raw.split(',') if task.strip()]

    total_minutes = study_hours * 60
    study_duration = 25
    break_duration = break_minutes
    cycle_time = study_duration + break_duration

    cycles = total_minutes // cycle_time
    leftover = total_minutes % cycle_time

    schedule = []
    for i in range(cycles):
        schedule.append({'type': 'Study', 'minutes': study_duration})
        schedule.append({'type': 'Break', 'minutes': break_duration})

    # Add leftover time as an additional session
    if leftover > 0:
        if leftover > study_duration:
            schedule.append({'type': 'Study', 'minutes': study_duration})
            schedule.append({'type': 'Break', 'minutes': leftover - study_duration})
        else:
            schedule.append({'type': 'Study', 'minutes': leftover})

    session['schedule'] = schedule
    session['current'] = 0
    session['topic'] = topic
    session['tasks'] = tasks

    return jsonify({'schedule': schedule, 'tasks': tasks})

if __name__ == '__main__':
    app.run(debug=True)

