import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="vmsuser",
    password="vms123",
    database="VMS"
)

cursor = db.cursor()

print("Database Connected Successfully")