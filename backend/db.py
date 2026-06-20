import mysql.connector
import os

db = None
cursor = None

try:
    db = mysql.connector.connect(
         host="mysql-1ce8f6d7-anusridhanabal007-112d.a.aivencloud.com",
        user="avnadmin",
        password = os.getenv("DB_PASSWORD"),
        database="defaultdb",
        port=10936,
        ssl_disabled=False
    )

    cursor = db.cursor()
    print("Database Connected Successfully")

except Exception as e:
    print("Database Connection Failed:", e)