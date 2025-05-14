import tkinter as tk
from PIL import Image, ImageTk
import requests
from utils import write_json
import admin
from tkinter import messagebox
from utils import fetch_api

def show_login(main_root):
  login_window = tk.Toplevel(main_root)  # Tạo cửa sổ đăng nhập
  login_window.title("Đăng nhập")
  login_window.geometry("1200x700")

  # Lấy kích thước màn hình
  screen_width = login_window.winfo_screenwidth()
  screen_height = login_window.winfo_screenheight()

  # Kích thước cửa sổ đăng nhập
  window_width = 1200
  window_height = 700

  # Tính toán vị trí chính giữa
  x_position = (screen_width - window_width) // 2
  y_position = (screen_height - window_height) // 2

  # Đặt vị trí cửa sổ
  login_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")



  # Chia cửa sổ thành 2 phần
  left_frame = tk.Frame(login_window, width=600, height=700, bg="white")
  left_frame.pack(side="left", fill="both", expand=True)

  right_frame = tk.Frame(login_window, width=600, height=700, bg="lightgray")
  right_frame.pack(side="right", fill="both", expand=True)

  # Hiển thị ảnh
  try:
    image = Image.open("C:/Users/Admin/Downloads/logo-python.png")  # Đường dẫn ảnh
    image = image.resize((600, 700))  # Điều chỉnh kích thước
    img_logo = ImageTk.PhotoImage(image)
        
    img_label = tk.Label(left_frame, image=img_logo)
    img_label.pack(fill="both", expand=True)

    img_label.image = img_logo  # Giữ tham chiếu tránh bị xóa
  except Exception as e:
    print(f"Lỗi tải ảnh: {e}")

  # Form đăng nhập
  tk.Label(right_frame, text="Đăng nhập", font=("Arial", 24, "bold"), bg="lightgray").pack(pady=20)

  tk.Label(right_frame, text="Tên đăng nhập:", font=("Arial", 14), bg="lightgray").pack(pady=5)
  username_entry = tk.Entry(right_frame, font=("Arial", 14))
  username_entry.pack(pady=5, ipadx=5, ipady=5)

  tk.Label(right_frame, text="Mật khẩu:", font=("Arial", 14), bg="lightgray").pack(pady=5)
  password_entry = tk.Entry(right_frame, show="*", font=("Arial", 14))
  password_entry.pack(pady=5, ipadx=5, ipady=5)

  # Tạo một frame cho nút đăng nhập và quay lại.
  button_frame = tk.Frame(right_frame, bg="lightgray")
  button_frame.pack(pady=20)

  def close_login():
    login_window.destroy()  # Đóng cửa sổ đăng nhập
    main_root.deiconify()  # Hiển thị lại cửa sổ chính

  def login_action():
    # Thực hiện hành động đăng nhập ở đây
    username = username_entry.get()
    password = password_entry.get()
    api_url = "http://localhost:8080/auth/log-in"  # Thay bằng URL API thực tế
    headers = {"Content-Type": "application/json"}  # Thêm header Content-Type
    
    try:
      # Gửi yêu cầu POST đến API với thông tin đăng nhập và header
      response = requests.post(api_url, json={"username": username, "password": password}, headers=headers)
      
      # Xử lý phản hồi từ API
      data = response.json()
      if data.get("status") == 200:
        # Lấy thông tin từ phản hồi
        messagebox.showinfo("Thành công", "Đăng nhập thành công!")
        user_data = data.get("data", {})
        
        # Import os và lấy đường dẫn tuyệt đối
        import os
        from utils import BASE_DIR
        
        # Lưu thông tin vào file user.json hiện có với đường dẫn tuyệt đối
        user_file = os.path.join(BASE_DIR, "user.json")
        write_json(user_data, user_file)
        
        login_window.withdraw()  # Ẩn cửa sổ đăng nhập
        
        # Lấy dữ liệu tòa nhà và lưu vào file data.json hiện có
        api_url = "http://localhost:8080/admin/building-list"
        buildings_data = fetch_api(api_url)
        
        # Lấy role từ user_data và truyền vào hàm show_admin
        role = user_data.get("role")
        admin.show_admin(role)  # Truyền role vào hàm show_admin
        return {"status": "success", "role": user_data.get("role")}
      else:
        messagebox.showerror("Thất bại", "Tài khoản hoặc mật khẩu không đúng!")
        return {"status": "failure", "message": data.get("message", "Đăng nhập thất bại")}
    except Exception as e:
      messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")
      return {"status": "failure", "message": str(e)}
    # Có thể thêm mã xác thực ở đây
    # Sau khi đăng nhập thành công, có thể đóng cửa sổ đăng nhập và hiển thị cửa sổ chính

  # Nút đăng nhập
  login_btn = tk.Button(button_frame, text="Đăng nhập", font=("Arial", 14, "bold"), bg="blue", fg="white",
                          command=login_action)
  login_btn.pack(side="left", padx=10, ipadx=10, ipady=5)

  # Nút quay lại
  back_btn = tk.Button(button_frame, text="Quay lại", font=("Arial", 14, "bold"), bg="red", fg="white",
                         command=close_login)  # Có thể đổi thành một hành động khác
  back_btn.pack(side="left", padx=10, ipadx=10, ipady=5)
