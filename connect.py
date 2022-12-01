import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_pos"
)

def query(query:str)->list:
    mycursor = conn.cursor()
    mycursor.execute(query)
    result =  mycursor.fetchall()
    return result

def statement(query:str):
    mycursor = conn.cursor()
    mycursor.execute(query)
    conn.commit()
    print(mycursor.rowcount, "record succescfully.")
