import base64

import mysql.connector
import hashlib

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12hezron12",
    database="menta_application_schema"
)
mycursor = mydb.cursor()

def encryp(string):
    salt = "5gzbella"
    string = string + salt  # Adding salt to the password
    hashed = hashlib.md5(string.encode()) # Encoding the password
    return hashed.hexdigest()  # return the Hash



file = open('./13.jpeg', 'rb').read()
file = base64.b64encode(file)
mycursor.execute('UPDATE menta_application_schema.users_type2 SET profile_Image = %s WHERE idPatient = %s', [file, 1235])
mydb.commit()


#mycursor.execute("INSERT INTO menta_application_schema.users_type2 (First_Name, Second_Name, Last_Name, Email, Username, Password) VALUES (%s, %s, %s, %s, %s, %s)", ('Maureen', 'Wamboi', 'Lucy ', 'm@gmail', 'mauerrn', encryp('12maureen12')))
#mydb.commit()
#
