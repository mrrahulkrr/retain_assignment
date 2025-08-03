# Original messy code (before refactoring)
from flask import Flask, request, jsonify
import sqlite3
import hashlib

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('users.db')
    return conn

@app.route('/')
def health():
    return "OK"

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    result = []
    for user in users:
        result.append({
            'id': user[0],
            'name': user[1],
            'email': user[2],
            'password': user[3]  # Security issue: exposing passwords
        })
    return jsonify(result)

@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    conn = get_db()
    cursor = conn.cursor()
    # SQL injection vulnerability
    cursor.execute(f"SELECT * FROM users WHERE id = {id}")
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({
            'id': user[0],
            'name': user[1],
            'email': user[2],
            'password': user[3]  # Security issue
        })
    return "User not found", 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    # No validation
    name = data['name']
    email = data['email']
    password = data['password']
    
    # Weak password hashing
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    
    conn = get_db()
    cursor = conn.cursor()
    # SQL injection vulnerability
    cursor.execute(f"INSERT INTO users (name, email, password) VALUES ('{name}', '{email}', '{hashed_password}')")
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'User created'})

@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    # SQL injection vulnerability
    cursor.execute(f"UPDATE users SET name = '{data['name']}', email = '{data['email']}' WHERE id = {id}")
    conn.commit()
    conn.close()
    return jsonify({'message': 'User updated'})

@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    conn = get_db()
    cursor = conn.cursor()
    # SQL injection vulnerability
    cursor.execute(f"DELETE FROM users WHERE id = {id}")
    conn.commit()
    conn.close()
    return jsonify({'message': 'User deleted'})

@app.route('/search')
def search_users():
    name = request.args.get('name')
    conn = get_db()
    cursor = conn.cursor()
    # SQL injection vulnerability
    cursor.execute(f"SELECT * FROM users WHERE name LIKE '%{name}%'")
    users = cursor.fetchall()
    conn.close()
    result = []
    for user in users:
        result.append({
            'id': user[0],
            'name': user[1],
            'email': user[2]
        })
    return jsonify(result)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    
    # Weak password hashing
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    
    conn = get_db()
    cursor = conn.cursor()
    # SQL injection vulnerability
    cursor.execute(f"SELECT * FROM users WHERE email = '{email}' AND password = '{hashed_password}'")
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({'message': 'Login successful', 'user_id': user[0]})
    return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)
