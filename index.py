
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import login

def show_index():
    root = tk.Tk()
    root.title("Trang chủ")
    root.geometry("1200x700")

    # Lấy kích thước màn hình
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Kích thước cửa sổ đăng nhập
    window_width = 1200
    window_height = 700

    # Tính toán vị trí chính giữa
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    # Đặt vị trí cửa sổ
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Tạo Frame cho phần header.
    header_frame = tk.Frame(root, height=100)
    header_frame.pack(fill="x", padx=10, pady=10)

    # open_login
    def open_login():
        root.withdraw()  # Ẩn cửa sổ chính
        login.show_login(root)  # Gọi hàm show_login từ file login.py

    # Phần 1 Logo 
    try:
        image = Image.open("C:/Users/Admin/Downloads/logo-python.png")
        image = image.resize((80, 80))  # Điều chỉnh kích thước nếu cần
        logo_image = ImageTk.PhotoImage(image)  # Sử dụng ImageTk.PhotoImage

        # Tạo label hiển thị ảnh
        logo_label = Label(header_frame, image=logo_image)
        logo_label.pack(side="left", padx=10, pady=10)
        logo_label.image = logo_image  # Lưu giữ ảnh tránh bị xóa bởi garbage collector
    except Exception as e:
        print(f"Không thể tải logo: {e}")
        # Hiển thị text thay thế nếu không tải được logo
        logo_label = Label(header_frame, text="LOGO", font=("Arial", 20, "bold"))
        logo_label.pack(side="left", padx=10, pady=10)

    # Phần 2 Menu điều hướng.
    menu_frame = tk.Frame(header_frame)
    menu_frame.pack(side="left", expand=True)
    menu_items = ["Trang chủ", "Giới thiệu", "Sản phẩm", "Tin tức", "Liên hệ"]
    for item in menu_items:
        btn = tk.Button(menu_frame, text=item, relief="flat", fg='blue', font=("Arial", 12))
        btn.pack(side="left", padx=5)

    # Phần 3 tạo đăng nhập vào đăng ký,
    auth_frame = tk.Frame(header_frame)
    auth_frame.pack(side="right", padx=10)

    login_btn = tk.Button(auth_frame, text="Đăng nhập", bg="blue", fg="white", font=("Arial", 12), command=open_login)
    login_btn.pack(side="left", padx=5)

    register_btn = tk.Button(auth_frame, text="Đăng ký", bg="green", fg="white", font=("Arial", 12))
    register_btn.pack(side="left", padx=5)

    # Thêm nội dung chính của trang
    main_content = tk.Frame(root)
    main_content.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Tiêu đề trang chủ
    title_label = tk.Label(main_content, text="Chào mừng đến với Hệ thống Quản lý Tòa nhà", 
                           font=("Arial", 24, "bold"))
    title_label.pack(pady=20)
    
    # Mô tả ngắn
    description = tk.Label(main_content, text="Hệ thống giúp quản lý thông tin tòa nhà, nhân viên và khách hàng một cách hiệu quả.",
                          font=("Arial", 14), wraplength=800)
    description.pack(pady=10)

    return root

# Nếu file này được chạy trực tiếp
if __name__ == "__main__":
    root = show_index()
root.mainloop()
