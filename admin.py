import tkinter as tk
from tkinter import ttk
import requests
from utils import read_json, getRole
from utils import get_access_token
from tkinter import messagebox

role = getRole()

def show_admin():
  admin = tk.Tk()  # Tạo cửa sổ admin
  admin.title("Admin")
  admin.geometry("1200x700")

  #Menu cố định bên trái
  menu_frame = tk.Frame(admin, width=300, height=700, bg="lightgray")
  menu_frame.pack(side="left", fill="y")

  # Content thay đổi bên phải
  content_frame = tk.Frame(admin, width=950, height=700, bg="white")
  content_frame.pack(side="right", fill="both", expand=True)

  #Tiêu đề menu
  tk.Label(menu_frame, text="MENU", font=("Arial", 16, "bold"), bg="lightgray").pack(pady=10)

  def show_building():
      """Hàm cập nhật nội dung khi chọn menu"""
      # Xóa toàn bộ nội dung cũ nhưng giữ menu cố định
      for widget in content_frame.winfo_children():
          widget.destroy()

      # 📌 Tiêu đề "Quản lý Tòa Nhà"
      tk.Label(content_frame, text="Quản lý Tòa Nhà", font=("Arial", 24, "bold"), bg="white").pack(pady=10)

      # 📌 Form tìm kiếm (Phía trên)
      search_frame = tk.Frame(content_frame)
      search_frame.pack(fill="x", padx=10, pady=5)


      # 📌 Danh sách các trường nhập liệu
      fields = [
          "Tên Tòa Nhà", "Đường", "Phường",
          "Quận", "Tên Quản Lý", "SĐT Quản Lý",
          "Giá Thuê", "Diện Tích Thuê", "Số Tầng Thuê",
          "Số Tầng Hầm"
      ]

      entries = {}

      # 📌 Chia bố cục thành từng hàng có đúng 3 trường
      for idx, label in enumerate(fields):
          row = idx // 3   # Chia thành từng nhóm 3 phần tử trên mỗi hàng
          col = (idx % 3) * 2  # Mỗi trường có 2 cột: nhãn + ô nhập

          tk.Label(search_frame, text=label, font=("Arial", 12)).grid(row=row, column=col, padx=10, pady=5, sticky="w")
          entry = tk.Entry(search_frame, width=25)
          entry.grid(row=row, column=col + 1, padx=10, pady=5, sticky="ew")

          entries[label] = entry  # Lưu Entry để lấy giá trị sau

      # 📌 Danh sách chọn quận

      tk.Label(search_frame, text="Chọn Quận:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
      districts = ["Quận 1", "Quận 2", "Quận 3", "Quận 4", "Quận 5"]
      district_var = tk.StringVar()
      district_combobox = ttk.Combobox(search_frame, textvariable=district_var, values=districts, state="readonly", width=30)
      district_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="ew")



      # 📌 Danh sách chọn nhân viên
      if role != "STAFF":
        tk.Label(search_frame, text="Chọn Nhân Viên:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")

        employees = ["Nguyễn Văn A", "Trần Thị B", "Lê Văn C"]
        employee_var = tk.StringVar()
        employee_combobox = ttk.Combobox(search_frame, textvariable=employee_var, values=employees, state="readonly", width=25)
        employee_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="ew")




      # 📌 Các checkbox - Loại Tòa Nhà
      tk.Label(search_frame, text="Loại Tòa Nhà", font=("Arial", 12)).grid(row=5, column=0, padx=10, pady=5, sticky="w")

      ground_floor_var = tk.BooleanVar()
      tk.Checkbutton(search_frame, text="Tầng Trệt", variable=ground_floor_var).grid(row=5, column=1, padx=10, pady=5, sticky="w")

      full_building_var = tk.BooleanVar()
      tk.Checkbutton(search_frame, text="Nguyên Căn", variable=full_building_var).grid(row=5, column=2, padx=10, pady=5, sticky="w")

      furnished_var = tk.BooleanVar()
      tk.Checkbutton(search_frame, text="Nội Thất", variable=furnished_var).grid(row=5, column=3, padx=10, pady=5, sticky="w")

      # 📌 Đảm bảo các cột **tự mở rộng theo cửa sổ**
      for i in range(6):  # Tổng cộng có 6 cột
          search_frame.columnconfigure(i, weight=1)




      # 📌 Tạo bảng hiển thị kết quả (Phía dưới)
      table_frame = tk.Frame(content_frame)
      table_frame.pack(fill="both", expand=True, padx=10, pady=5)


      columns = ("id", "name", "address", "numberOfBasement", "rentPrice",
                "managername", "managerphone", "rentArea")

      tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
      tree.pack(fill="both", expand=True)

      table_width = table_frame.winfo_width()
      column_width = table_width // len(columns)  # Chia đều độ rộng cho các cột

      for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=column_width)  # Điều chỉnh độ rộng cột tự động


      # 📌 Hàm tải dữ liệu vào bảng
      def load_data(buildings):
          tree.delete(*tree.get_children())  # Xóa dữ liệu cũ
          for building in buildings:
              tree.insert("", "end", values=(
                  building.get("id"), building.get("name"), building.get("address"),
                  building.get("numberOfBasement"), building.get("rentPrice"),
                  building.get("managerName"), building.get("managerPhone"),
                  building.get("rentArea")
              ))

      # 📌 Hàm tìm kiếm qua API
      def search():
          params = {key: entry.get().strip() for key, entry in fields.items() if entry.get().strip()}
          token = get_access_token("user.json")

          if not token:
              messagebox.showerror("Lỗi", "Không tìm thấy accessToken. Vui lòng đăng nhập lại.")
              return
          
          try:
              headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
              response = requests.get("http://localhost:8080/admin/building-list", params=params, headers=headers)
              response.raise_for_status()
              data = response.json().get("data", [])
              load_data(data)
          except requests.RequestException as e:
              messagebox.showerror("Lỗi", f"Không thể kết nối tới API: {e}")
          except ValueError:
              messagebox.showerror("Lỗi", "Dữ liệu trả về không hợp lệ!")

      # Nút tìm kiếm
      tk.Button(content_frame, text="Tìm Kiếm", font=("Arial", 12), bg="blue", fg="white", command=search).pack(pady=10)

      # Hiển thị dữ liệu ban đầu từ file JSON
      data = read_json("data.json")
      load_data(data)

  # Tạo các nút menu
  btn1 = tk.Button(menu_frame, text="Quản lý toà nhà", font=("Arial", 14), bg="red", fg="white", command=show_building)
  btn1.pack(pady=5, fill="x") 
  

  admin.mainloop()