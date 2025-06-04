import os
import tkinter as tk
from PIL import Image, ImageTk
import admin
from tkinter import messagebox
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "logo-python.png")
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
    image = Image.open(logo_path)  # Đường dẫn ảnh
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

  # Checkbox hiển thị mật khẩu
  show_password_var = tk.BooleanVar(value=False)
  def toggle_password():
    if show_password_var.get():
      password_entry.config(show="")
    else:
      password_entry.config(show="*")
  show_pw_cb = tk.Checkbutton(right_frame, text="Hiển thị mật khẩu", variable=show_password_var, bg="lightgray", font=("Arial", 12), command=toggle_password)
  show_pw_cb.pack(pady=(0, 10), anchor="w", padx=30)

  # Tạo một frame cho nút đăng nhập và quay lại.
  button_frame = tk.Frame(right_frame, bg="lightgray")
  button_frame.pack(pady=20)

  def close_login():
    login_window.destroy()  # Đóng cửa sổ đăng nhập
    main_root.deiconify()  # Hiển thị lại cửa sổ chính

  def login_action():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    user_file = os.path.join(current_dir, "user.json")
    try:
        with open(user_file, "r", encoding="utf-8") as f:
            users = json.load(f)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không đọc được file user.json: {e}")
        return
    user = next((u for u in users if u["userName"] == username and u["password"] == password), None)
    if user:
        messagebox.showinfo("Thành công", "Đăng nhập thành công!")
        with open(os.path.join(current_dir, "user_current.json"), "w", encoding="utf-8") as f:
            json.dump(user, f, ensure_ascii=False, indent=4)
        login_window.destroy()
        main_root.destroy()  # Tắt hoàn toàn trang index
        admin.show_admin(user["role"])
    else:
        messagebox.showerror("Thất bại", "Tài khoản hoặc mật khẩu không đúng!")

  # Nút đăng nhập
  login_btn = tk.Button(button_frame, text="Đăng nhập", font=("Arial", 14, "bold"), bg="blue", fg="white",
                          command=login_action)
  login_btn.pack(side="left", padx=10, ipadx=10, ipady=5)

  # Nút quay lại
  back_btn = tk.Button(button_frame, text="Quay lại", font=("Arial", 14, "bold"), bg="red", fg="white",
                         command=close_login)  # Có thể đổi thành một hành động khác
  back_btn.pack(side="left", padx=10, ipadx=10, ipady=5)
