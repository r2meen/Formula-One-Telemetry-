import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="f1_telemetry"
)

print("Connected successfully!")

connection.close()
print("Connection closed.")