import requests

# Thay các giá trị này bằng thông tin thật từ Arduino IoT Cloud của bạn
CLIENT_ID = "0pnRNDz6wMx7DB7FbeGyWClgun0MlyW9"
CLIENT_SECRET = "YL5AEhBy2lTVg8J9BLqMAOCVi0tV62giIYHZC5TS3lvGp84G3OsY5LkJZfVAzvrN"
AUDIENCE = "https://api2.arduino.cc/iot"
GRANT_TYPE = "client_credentials"

def get_access_token():
    url = "https://api2.arduino.cc/iot/v1/clients/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": GRANT_TYPE,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "audience": AUDIENCE
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"❌ Không lấy được access token:\n{response.text}")