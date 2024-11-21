import mysql.connector

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",        # Replace with your host
            user="root",             # Replace with your username
            password="Ella84712005#",  # Replace with your password
            database="ClinicSystemDB",   # gk usah diubah
            port=3306                # Default MySQL port
        )
        
        if connection.is_connected():
            print("Success, Connected to the Database!")
            return connection
    except mysql.connector.Error as e:
        print(f"Error Failed to connect: {e}")
        return None
    

# connect_to_db()

