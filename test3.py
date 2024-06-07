import requests
def download_app_icon():
    url = "https://raw.githubusercontent.com/ice-black/Digital-Scribe/main/Data_Raw/system.keys.json"
    filename = 'system.keys.json'
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

download_app_icon()