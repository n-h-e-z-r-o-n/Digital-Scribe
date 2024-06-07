

import requests
url = "https://raw.githubusercontent.com/ice-black/Digital-Scribe/main/Data_Raw/system.keys.json"
filename = './Data_Raw/system.keys.json'
response = requests.get(url)
