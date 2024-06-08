import requests, datetime, base64
from requests.auth import HTTPBasicAuth

def mpesa_pay():
                consumer_key = "j03STGaUVRui7xJahkgHOcRGkGcGNpf4"  # Consumer Key from safaricom
                consumer_secret = "XnnIXhtJ8H8zeRHC"  # Consumer Secret from safaricom
                api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

                r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
                response = r.json()
                access_token = response['access_token']
                requests_amount = 1  # Mount to request
                phone = "254748439248"  # Recipient phone number
                saa = datetime.datetime.now()
                timestamp_format = saa.strftime("%Y%m%d%H%M%S")

                businessshortcode = "174379"
                passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"  # pass_key from safaricom
                pd_decode = businessshortcode + passkey + timestamp_format
                ret = base64.b64encode(pd_decode.encode())
                pd = ret.decode('utf-8')

                api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
                headers = {"Authorization": "Bearer %s" % access_token}

                request = {
                    "BusinessShortCode": businessshortcode,  # # Paybill or Buygoods - account number
                    "Password": pd,  # password used for encrypting the request sent
                    "Timestamp": timestamp_format,
                    # Timestamp of the transaction, normaly in the formart of YEAR+MONTH+DATE+HOUR+MINUTE+SECOND (YYYYMMDDHHMMSS)
                    "TransactionType": "CustomerPayBillOnline",
                    # used to identify the transaction when sending the request to M-Pesa (CustomerPayBillOnline, CustomerBuyGoodsOnline)
                    "Amount": requests_amount,  # Money that customer pays to the Shorcode. Only whole numbers are supported
                    "PartyA": phone,  # The phone number sending money
                    "PartyB": businessshortcode,  # businessshortcode, # The organization receiving the funds
                    "PhoneNumber": phone,  # Mobile Number to receive the STK Pin Prompt
                    "CallBackURL": "https://6a1e-102-68-77-69.eu.ngrok.io/MPESA_TEST/MpesaTest.php",
                    # "https://41.139.244.238:80/callback", # valid secure URL that is used to receive notifications from M-Pesa API. It is the endpoint to which the results will be sent by M-Pesa API.
                    "AccountReference": "28774056",
                    "TransactionDesc": 'Payment of X'
                    # information/comment that can be sent along with the request from your system.
                }
                response = requests.post(api_url, json=request, headers=headers)
                print(response.content)
mpesa_pay()