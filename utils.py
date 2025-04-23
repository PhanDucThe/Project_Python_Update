import json
import requests

def read_json(filepath="data.json"):
    """
    Đọc dữ liệu từ file JSON.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {filepath} không tồn tại.")
        return {}
    except json.JSONDecodeError:
        print(f"File {filepath} không đúng định dạng JSON.")
        return {}
    
def write_json(data, filepath):
    """
    Ghi dữ liệu vào file JSON.
    """
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def get_access_token(filepath="user.json"):
    """
    Lấy accessToken từ file user.json.
    """
    try:
        data = read_json(filepath)
        return data.get("accessToken")
    except FileNotFoundError:
        print("File user.json không tồn tại.")
        return None
    

def getRole(filepath="user.json"):
    """
    Lấy giá trị role từ file JSON.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("role")  # Lấy giá trị role từ file JSON
    except FileNotFoundError:
        print(f"File {filepath} không tồn tại.")
        return None
    except json.JSONDecodeError:
        print(f"File {filepath} không đúng định dạng JSON.")
        return None
    
def fetch_api(api_url):
    """
    Gửi request với accessToken để lấy dữ liệu bảo vệ và lưu vào file data.json.
    """
    token = get_access_token()
    if not token:
        print("Không tìm thấy accessToken. Vui lòng đăng nhập lại.")
        return

    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        full_data = response.json()  # Dữ liệu trả về từ API
        buildings = full_data.get("data", [])  # Lấy danh sách tòa nhà từ key "data"
        write_json(buildings, "data.json")  # Lưu danh sách tòa nhà vào file data.json
        return buildings
    except requests.RequestException as e:
        print(f"Lỗi khi gọi API: {e}")
        return None

