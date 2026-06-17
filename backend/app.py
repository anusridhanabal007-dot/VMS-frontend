from flask import Flask, request, jsonify
from db import db, cursor
app = Flask(__name__)
@app.route('/login', methods=['POST'])
def login():

    data = request.json

    username = data['username']
    password = data['password']

    sql = """
    SELECT user_id, user_name, user_role
    FROM users_vms
    WHERE user_name=%s
    AND user_password=%s
    """

    cursor.execute(sql, (username, password))

    user = cursor.fetchone()

    if user:
        return jsonify({
            "success": True,
            "user_id": user[0],
            "username": user[1],
            "role": user[2]
        })

    return jsonify({
        "success": False,
        "message": "Invalid Credentials"
    }), 401
visitors = []
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
