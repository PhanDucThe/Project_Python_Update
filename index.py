import tkinter as tk
from tkinter import Label, ttk
from PIL import Image, ImageTk
import os

# Lấy đường dẫn thư mục hiện tại
current_dir = os.path.dirname(os.path.abspath(__file__))

# Sử dụng os.path.join để tạo đường dẫn đầy đủ
logo_path = os.path.join(current_dir, "logo-python.png")
building_path = os.path.join(current_dir, "building.jpg")

def show_index():
    root = tk.Tk()
    root.title("Hệ thống Quản lý Tòa nhà")
    root.geometry("1200x700")
    
    # Thiết lập theme cho ttk
    style = ttk.Style()
    style.theme_use('clam')  # Sử dụng theme clam cho giao diện hiện đại
    style.configure('TButton', font=('Arial', 12), background='#4096FF', foreground='white')
    style.configure('TLabel', font=('Arial', 11))
    style.configure('Header.TLabel', font=('Arial', 14, 'bold'), foreground='#001F54')
    style.configure('Title.TLabel', font=('Arial', 28, 'bold'), foreground='#001F54')
    style.configure('Subtitle.TLabel', font=('Arial', 14), foreground='#707070')
    style.configure('Feature.TFrame', background='#F8F9FA', relief='ridge', borderwidth=1)
    
    # Lấy kích thước màn hình và căn giữa cửa sổ
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 1200
    window_height = 700
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    # Tạo Frame cho phần header với màu nền
    header_frame = tk.Frame(root, height=100, bg="#F8F9FA")
    header_frame.pack(fill="x", padx=0, pady=0)
    
    # Tạo đường viền dưới header
    separator = ttk.Separator(root, orient='horizontal')
    separator.pack(fill='x', pady=0)
    
    # Phần Logo
    try:
        image = Image.open(logo_path)
        image = image.resize((60, 60))
        logo_image = ImageTk.PhotoImage(image)
        
        logo_label = Label(header_frame, image=logo_image, bg="#F8F9FA")
        logo_label.pack(side="left", padx=20, pady=10)
        logo_label.image = logo_image
        
        # Thêm tên ứng dụng bên cạnh logo
        app_name = Label(header_frame, text="BUILDING MANAGEMENT", font=("Arial", 18, "bold"), fg="#001F54", bg="#F8F9FA")
        app_name.pack(side="left", padx=5)
    except Exception as e:
        print(f"Lỗi khi tải logo: {e}")
        app_name = Label(header_frame, text="BUILDING MANAGEMENT", font=("Arial", 18, "bold"), fg="#001F54", bg="#F8F9FA")
        app_name.pack(side="left", padx=20)
    
    # Tạo Frame cho nội dung chính với màu nền
    current_content_frame = tk.Frame(root, bg="white")
    current_content_frame.pack(fill="both", expand=True, padx=0, pady=0)

    # Các hàm hiển thị nội dung
    def show_homepage_content():
        for widget in current_content_frame.winfo_children():
            widget.destroy()
        
        # Container chính với padding
        main_container = tk.Frame(current_content_frame, bg="white")
        main_container.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Banner section - Tiêu đề trước, ảnh sau
        banner_frame = tk.Frame(main_container, bg="white")
        banner_frame.pack(fill="x", pady=10)
        
        # Tiêu đề trang chủ
        title_label = ttk.Label(banner_frame, text="Chào mừng đến với Hệ thống Quản lý Tòa nhà",
                              style="Title.TLabel")
        title_label.pack(pady=(10, 5))
        
        subtitle_label = ttk.Label(banner_frame, text="Giải pháp toàn diện cho việc quản lý bất động sản của bạn",
                                 style="Subtitle.TLabel")
        subtitle_label.pack(pady=5)
        
        # Nút CTA lớn
        cta_button = tk.Button(banner_frame, text="BẮT ĐẦU NGAY", bg="#4096FF", fg="white",
                              font=("Arial", 14, "bold"), padx=30, pady=10, relief="flat",
                              cursor="hand2", state="disabled")
        cta_button.pack(pady=20)
        
        # Tạo một đường phân cách nhẹ
        separator = ttk.Separator(main_container, orient='horizontal')
        separator.pack(fill='x', pady=10)
        
        # Hình ảnh chính - đặt trong container riêng
        image_section = tk.Frame(main_container, bg="white")
        image_section.pack(fill="x", pady=20)
        
        try:
            main_image = Image.open(building_path)
            main_image = main_image.resize((800, 400), Image.LANCZOS)
            main_photo = ImageTk.PhotoImage(main_image)
            
            # Tạo frame chứa ảnh với viền và bóng
            image_container = tk.Frame(image_section, bd=1, relief="solid", bg="white")
            image_container.pack(pady=10)
            
            image_label = tk.Label(image_container, image=main_photo, bd=0)
            image_label.image = main_photo
            image_label.pack()
            
            # Thêm chú thích dưới ảnh
            caption = ttk.Label(image_section, text="Tòa nhà hiện đại với đầy đủ tiện nghi", 
                              style="Subtitle.TLabel", font=("Arial", 12, "italic"))
            caption.pack(pady=5)
        except Exception as e:
            print(f"Lỗi khi tải ảnh chính: {e}")
            ttk.Label(image_section, text="[Ảnh minh họa tòa nhà]", font=("Arial", 18)).pack(pady=20)
        
        # Tạo một đường phân cách khác
        separator2 = ttk.Separator(main_container, orient='horizontal')
        separator2.pack(fill='x', pady=10)
        
        # Phần giới thiệu về dự án
        intro_section = tk.Frame(main_container, bg="white")
        intro_section.pack(fill="x", pady=20)
        
        intro_title = ttk.Label(intro_section, text="Về Dự Án Của Chúng Tôi", 
                              style="Header.TLabel", font=("Arial", 20, "bold"))
        intro_title.pack(pady=10)
        
        intro_text = """
        Hệ thống Quản lý Tòa nhà là giải pháp toàn diện giúp quản lý hiệu quả các tòa nhà, 
        chung cư và bất động sản thương mại. Với giao diện thân thiện và tính năng đa dạng, 
        chúng tôi cung cấp công cụ hỗ trợ đắc lực cho các nhà quản lý, chủ đầu tư và ban quản lý.
        
        Hệ thống được phát triển dựa trên nhu cầu thực tế của thị trường, mang đến trải nghiệm 
        quản lý chuyên nghiệp và hiệu quả nhất.
        """
        
        intro_label = ttk.Label(intro_section, text=intro_text, 
                              style="TLabel", wraplength=800, justify="center")
        intro_label.pack(pady=10)
        
        # Phần tính năng nổi bật
        features_container = tk.Frame(main_container, bg="white")
        features_container.pack(fill="x", pady=20)
        
        ttk.Label(features_container, text="Tính năng nổi bật", 
                 style="Header.TLabel", font=("Arial", 20, "bold")).pack(pady=10)
        
        # Grid layout cho các tính năng
        features_grid = tk.Frame(features_container, bg="white")
        features_grid.pack(pady=20)
        
        features = [
            {"icon": "🏢", "title": "Quản lý tòa nhà", "desc": "Quản lý thông tin chi tiết về tòa nhà, căn hộ và tiện ích"},
            {"icon": "📊", "title": "Báo cáo thống kê", "desc": "Xem báo cáo và thống kê về tình trạng thuê, doanh thu"},
            {"icon": "👥", "title": "Quản lý người thuê", "desc": "Theo dõi thông tin người thuê và hợp đồng"},
            {"icon": "🔒", "title": "Bảo mật cao", "desc": "Hệ thống phân quyền và bảo mật dữ liệu chuyên nghiệp"}
        ]
        
        # Tạo grid 2x2 cho các tính năng
        for i, feature in enumerate(features):
            col = i % 2
            row = i // 2
            
            feature_frame = tk.Frame(features_grid, bg="#F8F9FA", bd=1, relief="solid", width=350, height=150)
            feature_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            feature_frame.pack_propagate(False)
            
            icon_label = tk.Label(feature_frame, text=feature["icon"], font=("Arial", 30), bg="#F8F9FA")
            icon_label.pack(pady=(15, 5))
            
            title_label = tk.Label(feature_frame, text=feature["title"], font=("Arial", 14, "bold"), bg="#F8F9FA", fg="#001F54")
            title_label.pack(pady=5)
            
            desc_label = tk.Label(feature_frame, text=feature["desc"], font=("Arial", 11), bg="#F8F9FA", fg="#707070", wraplength=300)
            desc_label.pack(pady=5)
        
        # Phần lời kêu gọi hành động (CTA)
        cta_section = tk.Frame(main_container, bg="#E6F7FF", height=150)
        cta_section.pack(fill="x", pady=30)
        cta_section.pack_propagate(False)
        
        cta_text = ttk.Label(cta_section, text="Sẵn sàng trải nghiệm hệ thống quản lý hiện đại?", 
                            style="Header.TLabel", font=("Arial", 18, "bold"))
        cta_text.pack(pady=(30, 10))
        
        cta_button2 = tk.Button(cta_section, text="ĐĂNG KÝ NGAY", bg="#52C41A", fg="white",
                               font=("Arial", 14, "bold"), padx=30, pady=10, relief="flat",
                               cursor="hand2", state="disabled")
        cta_button2.pack(pady=10)

    def show_about_us_content():
        for widget in current_content_frame.winfo_children():
            widget.destroy()
        ttk.Label(current_content_frame, text="Giới thiệu về chúng tôi", font=("Arial", 28, "bold"), foreground="navy").pack(pady=30)
        about_text_full = ("Chúng tôi là một đội ngũ phát triển tận tâm, chuyên tạo ra các giải pháp phần mềm "
                           "để tối ưu hóa quy trình quản lý bất động sản. Với nhiều năm kinh nghiệm trong lĩnh vực "
                           "phát triển ứng dụng desktop và tích hợp API, chúng tôi tự hào mang đến cho khách hàng "
                           "một hệ thống quản lý tòa nhà mạnh mẽ, an toàn và dễ sử dụng.\n\n"
                           "Mục tiêu của chúng tôi là đơn giản hóa các tác vụ quản lý phức tạp, "
                           "giúp các chủ sở hữu, quản lý tòa nhà và nhân viên có thể tập trung "
                           "vào các hoạt động kinh doanh cốt lõi. Chúng tôi luôn lắng nghe phản hồi "
                           "từ người dùng để liên tục cải thiện và phát triển sản phẩm, đảm bảo rằng "
                           "hệ thống của chúng tôi luôn đáp ứng được nhu cầu ngày càng cao của thị trường.")
        ttk.Label(current_content_frame, text=about_text_full, wraplength=800, justify="left", font=("Arial", 12)).pack(pady=10, padx=50)

    def show_products_content():
        for widget in current_content_frame.winfo_children():
            widget.destroy()
        ttk.Label(current_content_frame, text="Sản phẩm và Dịch vụ", font=("Arial", 28, "bold"), foreground="navy").pack(pady=30)
        ttk.Label(current_content_frame, text="Chúng tôi cung cấp một loạt các sản phẩm và dịch vụ để hỗ trợ quản lý tòa nhà của bạn:",
                  font=("Arial", 14)).pack(pady=10)

        product_frame = ttk.Frame(current_content_frame)
        product_frame.pack(pady=20, padx=50, fill="x")

        products = [
            ("Hệ thống Quản lý Tòa nhà Desktop", "Ứng dụng trên máy tính với đầy đủ tính năng quản lý cơ bản."),
            ("Module Quản lý Hợp đồng", "Dễ dàng theo dõi và quản lý các hợp đồng thuê, gia hạn và thanh toán."),
            ("Module Báo cáo & Thống kê", "Tạo báo cáo chi tiết về doanh thu, tình trạng thuê và các chỉ số khác."),
            ("Hỗ trợ Khách hàng 24/7", "Đội ngũ hỗ trợ chuyên nghiệp sẵn sàng giải đáp mọi thắc mắc của bạn.")
        ]

        for title, desc in products:
            item_frame = ttk.Frame(product_frame, relief="solid", borderwidth=1, padding="10 10 10 10")
            item_frame.pack(fill="x", pady=10)
            ttk.Label(item_frame, text=title, font=("Arial", 16, "bold"), foreground="darkblue").pack(anchor="w")
            ttk.Label(item_frame, text=desc, wraplength=700, font=("Arial", 11)).pack(anchor="w", pady=5)

    def show_news_content():
        for widget in current_content_frame.winfo_children():
            widget.destroy()
        ttk.Label(current_content_frame, text="Tin tức và Sự kiện", font=("Arial", 28, "bold"), foreground="navy").pack(pady=30)
        ttk.Label(current_content_frame, text="Cập nhật những tin tức mới nhất về ngành quản lý bất động sản và các cải tiến của chúng tôi.",
                  font=("Arial", 14)).pack(pady=10)

        news_items = [
            ("Nâng cấp giao diện người dùng", "Chúng tôi đã phát hành bản cập nhật mới với giao diện thân thiện hơn và hiệu suất được cải thiện. Chi tiết...", "2024-05-15"),
            ("Workshop quản lý tòa nhà hiệu quả", "Tham gia buổi workshop trực tuyến của chúng tôi để tìm hiểu các mẹo quản lý tòa nhà chuyên nghiệp. Đăng ký ngay...", "2024-04-28"),
            ("Tích hợp API thanh toán mới", "Hệ thống giờ đây hỗ trợ tích hợp với các cổng thanh toán phổ biến, giúp quá trình thu phí dễ dàng hơn. Tìm hiểu thêm...", "2024-04-01")
        ]

        news_frame = ttk.Frame(current_content_frame, padding="10 10 10 10")
        news_frame.pack(pady=20, padx=50, fill="x")

        for title, desc, date in news_items:
            news_item_frame = ttk.Frame(news_frame, relief="solid", borderwidth=1, padding="10 10 10 10")
            news_item_frame.pack(fill="x", pady=10)
            ttk.Label(news_item_frame, text=title, font=("Arial", 16, "bold"), foreground="chocolate").pack(anchor="w")
            ttk.Label(news_item_frame, text=f"Ngày: {date}", font=("Arial", 10, "italic")).pack(anchor="w")
            ttk.Label(news_item_frame, text=desc, wraplength=700, font=("Arial", 11)).pack(anchor="w", pady=5)

    def show_contact_content():
        for widget in current_content_frame.winfo_children():
            widget.destroy()
        ttk.Label(current_content_frame, text="Liên hệ chúng tôi", font=("Arial", 28, "bold"), foreground="navy").pack(pady=30)
        ttk.Label(current_content_frame, text="Chúng tôi luôn sẵn lòng lắng nghe và hỗ trợ bạn.",
                  font=("Arial", 14)).pack(pady=10)

        contact_info_frame = ttk.Frame(current_content_frame, padding="15 15 15 15", relief="solid")
        contact_info_frame.pack(pady=20, padx=100, fill="x")

        ttk.Label(contact_info_frame, text="Địa chỉ:", font=("Arial", 12, "bold")).pack(anchor="w", pady=2)
        ttk.Label(contact_info_frame, text="123 Đường ABC, Quận XYZ, Thành phố Hồ Chí Minh", font=("Arial", 11)).pack(anchor="w")

        ttk.Label(contact_info_frame, text="Điện thoại:", font=("Arial", 12, "bold")).pack(anchor="w", pady=2)
        ttk.Label(contact_info_frame, text="+84 987 654 321", font=("Arial", 11)).pack(anchor="w")

        ttk.Label(contact_info_frame, text="Email:", font=("Arial", 12, "bold")).pack(anchor="w", pady=2)
        ttk.Label(contact_info_frame, text="info@quanlytoanha.com", font=("Arial", 11)).pack(anchor="w")

        ttk.Label(contact_info_frame, text="Thời gian làm việc:", font=("Arial", 12, "bold")).pack(anchor="w", pady=2)
        ttk.Label(contact_info_frame, text="Thứ Hai - Thứ Sáu: 8:00 AM - 5:00 PM", font=("Arial", 11)).pack(anchor="w")

    # Phần Menu điều hướng
    menu_frame = tk.Frame(header_frame, bg="#F8F9FA")
    menu_frame.pack(side="left", expand=True)
    
    menu_items = [
        ("Trang chủ", show_homepage_content),
        ("Giới thiệu", show_about_us_content),
        ("Sản phẩm", show_products_content),
        ("Tin tức", show_news_content),
        ("Liên hệ", show_contact_content)
    ]
    for item_text, command_func in menu_items:
        btn = tk.Button(menu_frame, text=item_text, relief="flat", bg="#F8F9FA", fg='#001F54', 
                        font=("Arial", 13, "bold"), command=command_func, bd=0,
                        activebackground="#E6F0FF", activeforeground="#0066CC",
                        padx=18, pady=7, cursor="hand2")
        btn.pack(side="left", padx=12)

    # Phần đăng nhập và đăng ký (nút đăng nhập sẽ mở giao diện login)
    auth_frame = tk.Frame(header_frame, bg="#F8F9FA")
    auth_frame.pack(side="right", padx=30)

    def open_login():
        root.withdraw()
        import login
        login.show_login(root)

    def open_register():
        root.withdraw()
        import resgiter
        resgiter.RegisterForm(root)

    login_btn = tk.Button(auth_frame, text="Đăng nhập", bg="#4096FF", fg="white", 
                         font=("Arial", 12, "bold"), padx=18, pady=7, relief="flat", cursor="hand2", command=open_login)
    login_btn.pack(side="left", padx=10)
    register_btn = tk.Button(auth_frame, text="Đăng ký", bg="#52C41A", fg="white", 
                            font=("Arial", 12, "bold"), padx=18, pady=7, relief="flat", cursor="hand2", command=open_register)
    register_btn.pack(side="left", padx=5)

    # Hiển thị nội dung trang chủ mặc định khi khởi động
    show_homepage_content()

    # Thêm footer
    footer_frame = tk.Frame(root, height=60, bg="#001F54")
    footer_frame.pack(fill="x", side="bottom")
    
    footer_content = tk.Frame(footer_frame, bg="#001F54")
    footer_content.pack(fill="both", expand=True, padx=20, pady=10)
    
    copyright_label = tk.Label(
        footer_content, 
        text="© 2024 Hệ thống Quản lý Tòa nhà. Mọi quyền được bảo lưu.",
        font=("Arial", 11, "italic"), bg="#001F54", fg="white")
    copyright_label.pack(side="left", pady=10)
    
    # Thêm các liên kết mạng xã hội ở bên phải footer
    social_frame = tk.Frame(footer_content, bg="#001F54")
    social_frame.pack(side="right")
    
    social_text = tk.Label(social_frame, text="Kết nối với chúng tôi:", 
                          font=("Arial", 11, "italic"), bg="#001F54", fg="white")
    social_text.pack(side="left", padx=5)
    
    for social, color in zip(["Facebook", "Twitter", "LinkedIn"], ["#1877F3", "#1DA1F2", "#0A66C2"]):
        social_btn = tk.Label(social_frame, text=social, font=("Arial", 11, "bold"), 
                             bg="#001F54", fg=color, cursor="hand2")
        social_btn.pack(side="left", padx=10)
    
    return root

# Nếu file này được chạy trực tiếp
if __name__ == "__main__":
    root = show_index()
    root.mainloop()
