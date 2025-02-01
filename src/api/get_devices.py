import os
import requests

URL = "https://api.scalefusion.com/api/v2/devices.json"
API_KEY = os.getenv("API_KEY") # Задано через змінну середовища

def get_devices():
    headers = {
        "Accept": "application/json",
        "Authorization": f"Token {API_KEY}"
    }

    response = requests.get(URL, headers=headers)

    if response.status_code == 200:
        devices_data = response.json()
        return devices_data
    else:
        print(f"Error {response.status_code}: {response.text}")

