from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)


# Connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn


# Load Student Details API with pagination
@app.route('/api/students', methods=['GET'])
def get_students():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 5, type=int)

    offset = (page - 1) * page_size

    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students LIMIT ? OFFSET ?', (page_size, offset)).fetchall()
    conn.close()

    total_students = len(students)

    return jsonify({
        'students': [dict(row) for row in students],
        'total_students': total_students,
        'page': page,
        'page_size': page_size
    })


# Server-side Filtering API
@app.route('/api/filter/students', methods=['POST'])
def filter_students():
    filters = request.json
    query = 'SELECT * FROM students WHERE 1=1'
    query_params = []

    if 'name' in filters:
        query += ' AND name LIKE ?'
        query_params.append(f"%{filters['name']}%")

    if 'min_marks' in filters:
        query += ' AND total_marks >= ?'
        query_params.append(filters['min_marks'])

    if 'max_marks' in filters:
        query += ' AND total_marks <= ?'
        query_params.append(filters['max_marks'])

    conn = get_db_connection()
    filtered_students = conn.execute(query, query_params).fetchall()
    conn.close()

    return jsonify({'students': [dict(row) for row in filtered_students]})


# Frontend to display student details
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
