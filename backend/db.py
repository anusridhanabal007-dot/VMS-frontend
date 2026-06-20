import mysql.connector

db = None
cursor = None

try:
    db = mysql.connector.connect(
        host="localhost",
        user="vmsuser",
        password="vms123",
        database="VMS"
    )

    cursor = db.cursor()
    print("Database Connected Successfully")

except Exception as e:
    print("Database Connection Skipped:", e)