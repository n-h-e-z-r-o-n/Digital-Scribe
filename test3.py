import pyrebase
config = {
        'apiKey': "AIzaSyAL6KeL8SGTc7GvHtWQLhVXQ3A_pfs0fgA",
        'authDomain': "mentalhealth-badb3.firebaseapp.com",
        'databaseURL': "https://trialauth-7eeal-7eeal.firebaseio.com",
        'projectId': "mentalhealth-badb3",
        'storageBucket': "mentalhealth-badb3.appspot.com",
        'messagingSenderId': "668556041575",
        'appId': "1:668556041575:web:8170d74edf2fdbcf8f23c2",
        'measurementId': "G-168YG4NVDE"
}
firebase = pyrebase.initialize_app(config)

db = firebase.database()

data = {"name": "Mortimer 'Morty' Smith"}
db.child("users").push(data)



host_name = "localhost"
user_name = "root"
password_key = "12hezron12"
database_name = "hostel"
import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
host=host_name,
user=user_name,
password=password_key,
database=database_name
)
mycursor = mydb.cursor()

# Uplload data to database

with open(r"C:\Users\HEZRON WEKESA\Downloads\AngelaUON_Data-20240605T114805Z-001 (1)\AngelaUON_Data\sba_makadara_appointment_old.sql", 'r') as file:
    sql_script = file.read()
data = sql_script.split("),")
print(data[0])
count = 1
for command in data:
    print(count)
    mycursor.execute(f"INSERT INTO hostel.s_appointment_old VALUES {command});")
    mydb.commit()
    count +=1

# write to an Excel file


# Define the SQL query to fetch the table data
query = "SELECT * FROM hostel.s_appointment_old;"

# Execute the query
mycursor.execute(query)

# Fetch all rows from the executed query
rows = mycursor.fetchall()

# Get column names from the cursor
columns = [i[0] for i in mycursor.description]

# Create a DataFrame from the fetched data
df = pd.DataFrame(rows, columns=columns)

# Write the DataFrame to an Excel file
df.to_excel('output.xlsx', index=False)

# Close the cursor and connection
mycursor.close()
