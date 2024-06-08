import requests

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer vtSAX2TA9W8Xpp1uectPSXp2KDld'
}

payload = {
    "BusinessShortCode": 174379,
    "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjQwNjA4MTM0NDI2",
    "Timestamp": "20240608134426",
    "TransactionType": "CustomerPayBillOnline",
    "Amount": 1,
    "PartyA": 254714415034,
    "PartyB": 174379,
    "PhoneNumber": 254708374149,
    "CallBackURL": "https://mydomain.com/path",
    "AccountReference": "CompanyXLTD",
    "TransactionDesc": "Payment of X"
  }

response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, data = payload)
print(response.text.encode('utf8'))