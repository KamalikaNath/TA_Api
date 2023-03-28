from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import sqlite3

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)

DATABASE = 'ta.db'

conn = sqlite3.connect('ta.db')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS TA')
c.execute('CREATE TABLE TA (id INTEGER PRIMARY KEY, native_english_speaker BOOLEAN, course_instructor VARCHAR(50), course VARCHAR(50), semester BOOLEAN, class_size INT, performance_score VARCHAR(10))')

c.execute('INSERT INTO TA (id, native_english_speaker, course_instructor, course, semester, class_size, '
          'performance_score) VALUES (?,?, ?, ?, ?, ?, ?)', (1, 1, 23, 3, 1, 19, 3))
conn.commit()
conn.close()


def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'admin' or password != 'admin':
        return jsonify({'message': 'Invalid username or password'}), 401
    access_token = create_access_token(identity=username)
    return jsonify({'access_token': access_token})


@app.route('/api/ta', methods=['POST'])
@jwt_required()
def add_ta():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO TA (id ,native_english_speaker, course_instructor, course, semester, class_size, '
        'performance_score) '
        'VALUES (?, ?, ?, ?, ?, ?, ?)',
        (
            data['id'], data['native_english_speaker'], data['course_instructor'], data['course'], data['semester'],
            data['class_size'],
            data['performance_score']))
    db.commit()
    cursor.close()
    return jsonify({'message': 'added successfully'}), 201


@app.route('/api/ta/<int:id>', methods=['GET'])
@jwt_required()
def get_ta(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM TA WHERE id = ?', (id,))
    ta = cursor.fetchone()
    cursor.close()
    if ta:
        return jsonify(dict(ta))
    else:
        return jsonify({'message': ' not found'}), 404


@app.route('/api/ta/<int:id>', methods=['PUT'])
@jwt_required()
def update_ta(id):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'UPDATE TA SET  native_english_speaker=?, course_instructor=?, course=?, semester=?, class_size=?, '
        'performance_score=? WHERE id=?',
        (
            data['native_english_speaker'], data['course_instructor'], data['course'], data['semester'],
            data['class_size'],
            data['performance_score'], id))
    db.commit()
    cursor.close()
    return jsonify({'message': 'TA updated successfully'})


@app.route('/api/ta/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_ta(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM TA WHERE id = ?', (id,))
    db.commit()
    cursor.close()
    return jsonify({'message': 'TA deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)
