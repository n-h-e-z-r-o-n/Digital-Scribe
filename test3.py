host_name = "localhost"
user_name = "root"
password_key = "12hezron12"
database_name = "hostel"
import mysql.connector

mydb = mysql.connector.connect(
host=host_name,
user=user_name,
password=password_key,
database=database_name
)
mycursor = mydb.cursor()

with open(r"C:\Users\HEZRON WEKESA\Downloads\AngelaUON_Data-20240605T114805Z-001 (1)\AngelaUON_Data\sba_makadara_appointment_old.sql", 'r') as file:
    sql_script = file.read()

print(sql_script)
mycursor.execute(sql_script)
mydb.commit()

