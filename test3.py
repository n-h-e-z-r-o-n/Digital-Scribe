import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate(r"C:\Users\HEZRON WEKESA\Downloads\mentalhealth-badb3-firebase-adminsdk-ivmin-7a32a3b7ec.json")
firebase_admin.initialize_app(cred)