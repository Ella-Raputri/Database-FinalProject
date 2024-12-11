import mysql.connector

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",        
            user="root",             
            password="EllaTest2005",  
            database="ClinicSystemDB",   
            port=3306                
        )
        
        if connection.is_connected():
            # print("Success, Connected to the Database!")
            return connection
    except mysql.connector.Error as e:
        print(f"Error Failed to connect: {e}")
        return None
    

# connect_to_db()

