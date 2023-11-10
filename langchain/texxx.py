
import shelve

session = shelve.open("session.db")

print(type(session))
if session['logged_in']:
    print(" -------------------- ")
    x = session.get('logged_in', 'N/A')
    print("== ", x)
    session['logged_in'] = False
else:
    print(" else -------------------- ")
    x = session.get('logged_in', 'N/A')
    user_name = session.get('user_name', 'N/A')
    user_age = session.get('user_age', 'N/A')
    print("== ", x)
    print(user_name)
    print(user_age)
    print(" else end-------------------- ")


user_name = "Hezron"
user_age = 30


# Store data in the session
session['user_name'] = user_name
session['user_age'] = user_age
session['logged_in'] = True


user_name = session.get('user_name', 'N/A')
user_age = session.get('user_age', 'N/A')
x = session.get('logged_in', 'N/A')

print("== :", x)
print(user_name)
print(user_age)

# Close the session when the application is closed
#session.clear()
session.close()
