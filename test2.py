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
auth = firebase.auth() #Authentication
db = firebase.database()

def login():
        email = 'hezron.w12@gmail.com'
        passw = "12wekesa12"
        try:
           auth.sign_in_with_email_and_password(email, passw)

           userInfo = auth.current_user
           idToken = userInfo['idToken']
           displayName = userInfo['displayName']
           expiresIn = userInfo['expiresIn']
           email = userInfo['email']

           print(auth.current_user, '\n\n')
           print(idToken)

        except Exception as e:

                print(e)
def signup():
        email = 'hezron.w12@gmail.com'
        passw = "12wekesa12"
        try:
           user = auth.create_user_with_email_and_password(email, passw)
        except Exception as e:

                print(e)

def forgot_pass():
        email = 'hezron.w12@gmail.com'
        auth.send_password_reset_email(email)

m = db.get()
print(m)



