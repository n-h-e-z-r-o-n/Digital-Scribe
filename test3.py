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