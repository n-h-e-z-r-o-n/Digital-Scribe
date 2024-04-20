#!C:\Users\HEZRON WEKESA\AppData\Local\Programs\Python\Python310\python.exe
print("Content-Type: text/html")
print()
print('<html>')
print('<body>')

import cgi
import cgitb
cgitb.enable()
form = cgi.FieldStorage()
#receive  values from user form and trim white spaces
guest_name = form.getvalue('guest_email')
guest_phone_number = form.getvalue('guest_password')

print(guest_name, "\n", guest_phone_number)



print('<h1 style="text-align: center; display: flex; flex-direction: column; justify-content: center;"> You Have Been Added Successfuly in The Booking List</h1>')

print('</body>')

print('</html>')