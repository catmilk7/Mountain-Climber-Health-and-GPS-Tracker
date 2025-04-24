import requests
from website.services.token_manager import get_access_token

# Thing ID của thiết bị
THING_ID = "3284f568-841e-4717-9604-cfcdb38f1e39"
THING_ID2 = "df125c1d-2149-432a-b8b5-d2c6ad71b0b7"
LOCATION_VAR_ID = "9afa1a98-18b3-42ed-a37f-bfbfa091cacf"

# Danh sách các ID biến bạn muốn lấy giá trị
VARIABLE_IDS = {
    "temperature": "a709e627-32a5-47b8-b757-ad74872a0e93",
    "location": "a5813ce3-46c0-4e6a-93d1-bc9ecc7f571f",
    "emergency_button": "b1419324-d9bc-43f7-ab95-6d963aa4f55d"
}

def get_variable_value(token, thing_id, variable_id):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    url = f"https://api2.arduino.cc/iot/v2/things/{thing_id}/properties/{variable_id}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get('last_value')  # Đây là giá trị cần lấy
    else:
        print(f"❌ Lỗi khi gọi variable {variable_id}:")
        print(f"Phản hồi: {response.text}")
        return None

def set_variable_value(token, thing_id, property_id, value):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    url = f"https://api2.arduino.cc/iot/v2/things/{thing_id}/properties/{property_id}/publish"

    payload = {
        "value": value
    }

    response = requests.put(url, headers=headers, json=payload)

    if response.status_code in [200, 204]:
        print("✅ Gửi thành công!")
        return True
    else:
        print("❌ Lỗi khi gửi giá trị:")
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
        print("Payload:", payload)
        return False

def main():
    token = get_access_token()

    result = {}

    for name, var_id in VARIABLE_IDS.items():
        value = get_variable_value(token, THING_ID, var_id)
        result[name] = value

    print("\n📊 Kết quả đọc từ Arduino Cloud:")
    print(result)

if __name__ == "__main__":
    main()