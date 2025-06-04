import json
import os

# Lấy đường dẫn tuyệt đối đến thư mục chứa file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def read_json(filepath="data.json"):
    """
    Đọc dữ liệu từ file JSON.
    """
    # Chuyển đổi thành đường dẫn tuyệt đối nếu chưa phải
    if not os.path.isabs(filepath):
        filepath = os.path.join(BASE_DIR, filepath)
        
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
    # Chuyển đổi thành đường dẫn tuyệt đối nếu chưa phải
    if not os.path.isabs(filepath):
        filepath = os.path.join(BASE_DIR, filepath)
        
    try:
        # Đảm bảo thư mục chứa file tồn tại
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        # Ghi dữ liệu vào file
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Đã lưu dữ liệu vào file {filepath}")
    except Exception as e:
        print(f"Lỗi khi ghi file {filepath}: {e}")

def getRole(filepath="user_current.json"):
    """
    Lấy giá trị role từ file user_current.json (user đang đăng nhập).
    """
    # Chuyển đổi thành đường dẫn tuyệt đối nếu chưa phải
    if not os.path.isabs(filepath):
        filepath = os.path.join(BASE_DIR, filepath)
        
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            role = data.get("role")
            print(f"Role from file: {role}")  # Debug: In ra role đọc từ file
            return role  # Lấy giá trị role từ file JSON
    except FileNotFoundError:
        print(f"File {filepath} không tồn tại.")
        return None
    except json.JSONDecodeError:
        print(f"File {filepath} không đúng định dạng JSON.")
        return None

