from flask import Flask, request, jsonify
from db import db, cursor
from werkzeug.utils import secure_filename
import os
import qrcode
app = Flask(__name__)
PHOTO_FOLDER = "uploads/photos"
ID_FOLDER = "uploads/idproofs"

os.makedirs(PHOTO_FOLDER, exist_ok=True)
os.makedirs(ID_FOLDER, exist_ok=True)
os.makedirs("qr_code", exist_ok=True)
@app.route('/login', methods=['POST'])
def login():
    if cursor is None:
        return jsonify({
            "success": False,
            "message": "Database not available"
            })
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
    if cursor is None:
        return jsonify({
            "success": False,
            "message": "Database not available"
            })
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
    "success": True,
    "message": "Visitor Registered Successfully",
    "notification": "Visitor registration notification sent"
    })
@app.route('/upload-files', methods=['POST'])
def upload_files():

    photo = request.files.get('photo')
    idproof = request.files.get('idproof')

    if not photo or not idproof:
        return jsonify({
            "success": False,
            "message": "Please upload both files"
        }), 400

    photo_name = secure_filename(photo.filename)
    id_name = secure_filename(idproof.filename)

    photo.save(os.path.join(PHOTO_FOLDER, photo_name))
    idproof.save(os.path.join(ID_FOLDER, id_name))

    return jsonify({
        "success": True,
        "message": "Files uploaded successfully"
    })
@app.route('/dashboard', methods=['GET'])
def dashboard():
    if cursor is None:
        return jsonify({
            "success": False,
            "message": "Database not available"
            })
    cursor.execute("SELECT COUNT(*) FROM Visitor_vms")
    total_visitors = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) 
        FROM Visitor_vms
        WHERE DATE(created_at) = CURDATE()
    """)
    today_visitors = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM Visitor_vms
        WHERE visitor_status = 'pending'
    """)
    pending_approvals = cursor.fetchone()[0]

    return jsonify({
        "total_visitors": total_visitors,
        "today_visitors": today_visitors,
        "pending_approvals": pending_approvals
    })
@app.route('/visitors', methods=['GET'])
def get_visitors():
    if cursor is None:
        return jsonify({
            "success": False,
            "message": "Database not available"
            })
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
@app.route('/reports/daily')
def daily_report():
    return jsonify({
        "report": "Daily Report"
    })
@app.route('/reports/weekly')
def weekly_report():
    return jsonify({
        "report": "Weekly Report"
    })

@app.route('/reports/monthly')
def monthly_report():
    return jsonify({
        "report": "Monthly Report"
    })

@app.route('/generate-pass')
def generate_pass():

    data = """Visitor Name: Anusri Dhanabal
    Host Employee: Admin
    Date: 2026-06-19"""

    img = qrcode.make(data)

    img.save("qr_code/visitor_pass.png")

    return jsonify({
        "success": True,
        "message": "Visitor Pass Generated"
    })
@app.route('/send-notification')
def send_notification():

    return jsonify({
        "success": True,
        "message": "Notification Sent Successfully"
    })
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
