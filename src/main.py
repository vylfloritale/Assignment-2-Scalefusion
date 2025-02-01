from api.get_devices import get_devices
from api.to_drive import upload_to_drive

try:
    # Отримання даних про пристрої
    devices = get_devices()
    
    # Якщо дані отримано успішно, вони передаються для запису на Google Drive
    if devices:
        upload_to_drive()
    else:
        print("No devices to process.")
    
except Exception as e:
    print(f"Error: {e}")
