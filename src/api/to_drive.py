import os
import gspread # type: ignore
from google.oauth2.service_account import Credentials
from api.get_devices import get_devices

# Облікові дані для доступу до Google Sheets
credentials = Credentials.from_service_account_file("credentials.json",  scopes=["https://www.googleapis.com/auth/spreadsheets"])

# Авторизація у Google Sheets
client = gspread.authorize(credentials)

# Відриття потрібної таблиці за її ID
SHEET = client.open_by_key(os.getenv("SHEET_ID")).sheet1 # Значення "SHEET_ID" задано через змінну середовища

# Функція для отримання всіх ключів з JSON
# Розбиває ключі на шляхи, щоб можна було звертатися до вкладених значень
def extract_keys(data, parent_key=''):
    keys = []
    
    if isinstance(data, dict):
        # Якщо data - це словник, перебираються його елементи
        for key, value in data.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            keys.extend(extract_keys(value, new_key))

    elif isinstance(data, list):
        # Якщо data - це список, перебираються його елементи
        for i, item in enumerate(data):
            keys.extend(extract_keys(item, f"{parent_key}[{i}]"))
            
    else:
        # Якщо data - це просто значення, додається поточний ключ
        keys.append(parent_key)
    
    return keys

def upload_to_drive():
    # Отримується інформація про пристрій з API
    device_info = get_devices()["devices"][0]["device"]
    
    # Витягаються всі ключі
    headers = extract_keys(device_info)

    # Перевірка, чи є заголовки в таблиці
    existing_values = SHEET.get_all_values()
    if not existing_values or not existing_values[0]:  # Якщо таблиця порожня або заголовків немає
        # Додаються заголовки, якщо їх немає
        SHEET.insert_row(headers, 1)

    # Створюється рядок для вставки в таблицю
    insert_row = []
    for key in headers:
        last_key = key.split('.')[-1]  # Береться останній ключ для доступу до значення
        insert_row.append(device_info.get(last_key, ''))  # Повертається значення або порожній рядок, якщо значення немає
    
    # Додається новий рядок у таблицю
    SHEET.insert_rows([insert_row], 2)
    
    print("The row has been added.")
