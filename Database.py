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

username = ' 105 OR 1=1' #'hezron26'
password = '105 OR 1=1'
mycursor.execute("select * from users_type2 where Email=%s and Password=%s", ("m@gmail", encryp('12maureen12')))
myresult = mycursor.fetchall()

print(myresult)



#mycursor.execute("INSERT INTO menta_application_schema.users_type2 (First_Name, Second_Name, Last_Name, Email, Username, Password) VALUES (%s, %s, %s, %s, %s, %s)", ('Maureen', 'Wamboi', 'Lucy ', 'm@gmail', 'mauerrn', encryp('12maureen12')))
#mydb.commit()
#
