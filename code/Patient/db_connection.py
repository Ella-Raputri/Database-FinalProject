import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="BinusSQL2005",  # Update with your MySQL password
        database="ClinicSystemDB"
    )
