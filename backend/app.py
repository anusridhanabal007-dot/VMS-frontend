from flask import Flask, request, jsonify
app = Flask(__name__)
admin_user = {"username": "admin", "password": "admin123"}
visitors = []
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({'success': False, 'message': 'JSON payload required'}), 400

    username = data.get('username')
    password = data.get('password')
    if username == admin_user['username'] and password == admin_user['password']:
        return jsonify({'success': True, 'message': 'Login successful'})

    return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
@app.route('/register-visitor', methods=['POST'])
def register_visitor():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({'success': False, 'message': 'JSON payload required'}), 400
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    purpose = data.get('purpose')
    if not all([name, email, phone, purpose]):
        return jsonify({'success': False, 'message': 'Missing visitor fields'}), 400
    visitor = {
        'id': len(visitors) + 1,
        'name': name,
        'email': email,
        'phone': phone,
        'purpose': purpose,
    }
    visitors.append(visitor)
    return jsonify({'success': True, 'visitor': visitor}), 201
@app.route('/visitors', methods=['GET'])
def list_visitors():
    return jsonify({'success': True, 'visitors': visitors})

if __name__ == '__main__':
    app.run(debug=True)
