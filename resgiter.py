import tkinter as tk
from tkinter import ttk, messagebox
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_FILE = os.path.join(BASE_DIR, "user.json")

class RegisterForm:
    def __init__(self, parent):
        self.parent = parent  # parent là cửa sổ index (Tk)
        self.window = tk.Toplevel(parent)
        self.window.title("Đăng ký tài khoản")
        self.window.geometry("700x500")
        self.window.configure(bg="#f8f9fa")
        self.create_widgets()
        self.window.protocol("WM_DELETE_WINDOW", self.back_to_index)  # Đảm bảo đóng bằng X cũng quay lại index

    def create_widgets(self):
        # Main container chia 2 cột: trái là logo, phải là form
        main_frame = tk.Frame(self.window, bg="#f8f9fa")
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Cột trái: logo
        left_frame = tk.Frame(main_frame, bg="#f8f9fa", width=300)
        left_frame.pack(side="left", fill="both", expand=False)
        left_frame.pack_propagate(False)
        try:
            from PIL import Image, ImageTk
            logo_path = os.path.join(BASE_DIR, "logo-python.png")
            image = Image.open(logo_path)
            image = image.resize((120, 120))
            logo_img = ImageTk.PhotoImage(image)
            logo_label = tk.Label(left_frame, image=logo_img, bg="#f8f9fa")
            logo_label.image = logo_img
            logo_label.pack(pady=(60, 20))
        except Exception:
            tk.Label(left_frame, text="LOGO", font=("Arial", 28, "bold"), fg="#007bff", bg="#f8f9fa").pack(pady=(80, 20))
        tk.Label(left_frame, text="BUILDING\nMANAGEMENT", font=("Arial", 16, "bold"), fg="#001F54", bg="#f8f9fa", justify="center").pack()

        # Cột phải: form đăng ký
        right_frame = tk.Frame(main_frame, bg="#f8f9fa")
        right_frame.pack(side="right", fill="both", expand=True)
        tk.Label(right_frame, text="ĐĂNG KÝ TÀI KHOẢN", font=("Arial", 22, "bold"), fg="#007bff", bg="#f8f9fa").pack(pady=(32, 10))
        form_frame = tk.LabelFrame(right_frame, text="Thông tin đăng ký", font=("Arial", 14, "bold"), fg="#007bff", bg="#f8f9fa", padx=24, pady=24)
        form_frame.pack(fill="both", expand=True, padx=32, pady=10)

        # Tên đăng nhập
        tk.Label(form_frame, text="Tên đăng nhập", font=("Arial", 12, "bold"), bg="#f8f9fa").grid(row=0, column=0, sticky="e", padx=12, pady=12)
        self.username_entry = tk.Entry(form_frame, width=28, font=("Arial", 12))
        self.username_entry.grid(row=0, column=1, padx=12, pady=12)

        # Mật khẩu (ẩn)
        tk.Label(form_frame, text="Mật khẩu", font=("Arial", 12, "bold"), bg="#f8f9fa").grid(row=1, column=0, sticky="e", padx=12, pady=12)
        self.password_entry = tk.Entry(form_frame, show="*", width=28, font=("Arial", 12))
        self.password_entry.grid(row=1, column=1, padx=12, pady=12)

        # Xác nhận mật khẩu (ẩn)
        tk.Label(form_frame, text="Xác nhận mật khẩu", font=("Arial", 12, "bold"), bg="#f8f9fa").grid(row=2, column=0, sticky="e", padx=12, pady=12)
        self.confirm_entry = tk.Entry(form_frame, show="*", width=28, font=("Arial", 12))
        self.confirm_entry.grid(row=2, column=1, padx=12, pady=12)

        # Checkbox hiển thị mật khẩu
        self.show_password_var = tk.BooleanVar(value=False)
        show_pw_cb = tk.Checkbutton(form_frame, text="Hiển thị mật khẩu", variable=self.show_password_var, bg="#f8f9fa", font=("Arial", 11), command=self.toggle_password)
        show_pw_cb.grid(row=3, column=1, sticky="w", padx=12, pady=(0, 8))

        # Dời các trường còn lại xuống 1 dòng
        # Họ tên
        tk.Label(form_frame, text="Họ tên", font=("Arial", 12, "bold"), bg="#f8f9fa").grid(row=4, column=0, sticky="e", padx=12, pady=12)
        self.fullname_entry = tk.Entry(form_frame, width=28, font=("Arial", 12))
        self.fullname_entry.grid(row=4, column=1, padx=12, pady=12)

        # Số điện thoại
        tk.Label(form_frame, text="Số điện thoại", font=("Arial", 12, "bold"), bg="#f8f9fa").grid(row=5, column=0, sticky="e", padx=12, pady=12)
        self.phone_entry = tk.Entry(form_frame, width=28, font=("Arial", 12))
        self.phone_entry.grid(row=5, column=1, padx=12, pady=12)

        # Nút đăng ký
        btn_frame = tk.Frame(right_frame, bg="#f8f9fa")
        btn_frame.pack(pady=12)
        register_btn = tk.Button(btn_frame, text="Đăng ký", font=("Arial", 14, "bold"), bg="#28a745", fg="white", activebackground="#218838", activeforeground="white", width=16, height=1, relief="raised", bd=2, command=self.register)
        register_btn.pack(side="left", padx=8)
        # Nút quay lại
        back_btn = tk.Button(btn_frame, text="Quay lại", font=("Arial", 14, "bold"), bg="#ffc107", fg="#001F54", activebackground="#ffe082", activeforeground="#001F54", width=12, height=1, relief="raised", bd=2, command=self.back_to_index)
        back_btn.pack(side="left", padx=8)

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()
        fullname = self.fullname_entry.get().strip()
        phone = self.phone_entry.get().strip()
        # Không còn lấy role từ entry, luôn mặc định là STAFF
        role = "STAFF"

        # Kiểm tra hợp lệ
        if not username or not password or not confirm or not fullname or not phone:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin!")
            return
        if len(username) < 4:
            messagebox.showwarning("Tên đăng nhập yếu", "Tên đăng nhập phải từ 4 ký tự trở lên!")
            return
        if len(password) < 4:
            messagebox.showwarning("Mật khẩu yếu", "Mật khẩu phải từ 4 ký tự trở lên!")
            return
        if password != confirm:
            messagebox.showwarning("Mật khẩu không khớp", "Xác nhận mật khẩu không đúng!")
            return
        if not phone.isdigit() or len(phone) < 8:
            messagebox.showwarning("Số điện thoại không hợp lệ", "Số điện thoại phải là số và từ 8 ký tự trở lên!")
            return

        # Đọc user.json
        try:
            with open(USER_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)
        except Exception:
            users = []
        # Kiểm tra trùng tên đăng nhập
        for user in users:
            if user.get("userName") == username:
                messagebox.showerror("Trùng tên đăng nhập", "Tên đăng nhập đã tồn tại!")
                return
        # Tạo userId tự động
        max_id = max([int(u.get("userId", 0)) for u in users], default=0)
        new_user = {
            "userId": str(max_id + 1),
            "userName": username,
            "password": password,
            "fullName": fullname,
            "phone": phone,
            "role": role
        }
        users.append(new_user)
        with open(USER_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=4)
        # Đăng ký thành công
        messagebox.showinfo("Thành công", "Đăng ký tài khoản thành công!")
        self.back_to_index()

    def toggle_password(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
            self.confirm_entry.config(show="")
        else:
            self.password_entry.config(show="*")
            self.confirm_entry.config(show="*")

    def back_to_index(self):
        # Hiện lại cửa sổ index (Tk) và đóng cửa sổ đăng ký (Toplevel)
        self.parent.deiconify()
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ẩn index khi test riêng file này
    app = RegisterForm(root)
    root.mainloop()
