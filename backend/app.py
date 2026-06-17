from flask import Flask, request, jsonify
from db import db, cursor
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

    data = request.json

    name = data['name']
    mobile = data['mobile']
    email = data['email']
    company = data['company']

    sql = """
    INSERT INTO visitor_vms
    (visitor_name, visitor_mobile,
     visitor_mail, visitor_company)
    VALUES (%s,%s,%s,%s)
    """

    cursor.execute(
        sql,
        (name, mobile, email, company)
    )

    db.commit()

    return jsonify({
        "message": "Visitor Registered Successfully"
    })
@app.route('/visitors', methods=['GET'])
def get_visitors():

    cursor.execute("SELECT * FROM visitor_vms")
    rows = cursor.fetchall()

    visitors = []

    for row in rows:
        visitors.append({
            "visitor_id": row[0],
            "name": row[1],
            "mobile": row[2],
            "email": row[3],
            "company": row[4]
        })

    return jsonify(visitors)
if __name__ == '__main__':
    app.run(debug=True)
