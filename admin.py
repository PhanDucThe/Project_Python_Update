import tkinter as tk
from tkinter import ttk
import requests
from utils import read_json, getRole, get_access_token, write_json, BASE_DIR
from tkinter import messagebox
import os


def show_admin():
  admin = tk.Tk()  # Tạo cửa sổ admin
  admin.title("Admin")
  admin.geometry("1200x700")
  
  # Lấy role từ file user.json
  role = getRole()

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

      #"Quản lý Tòa Nhà"
      tk.Label(content_frame, text="Quản lý Tòa Nhà", font=("Arial", 24, "bold"), bg="white").pack(pady=10)

      #Form tìm kiếm (Phía trên)
      search_frame = tk.Frame(content_frame)
      search_frame.pack(fill="x", padx=10, pady=5)

      # Đường phân cách
      separator = ttk.Separator(search_frame, orient='horizontal')
      separator.grid(row=1, column=0, columnspan=6, sticky="ew", pady=10)

      #Danh sách các trường nhập liệu
      fields = {
          "name": "Tên Tòa Nhà", 
          "street": "Đường", 
          "ward": "Phường",
          "managerName": "Tên Quản Lý", 
          "managerPhone": "SĐT Quản Lý",
          "numberOfBasement": "Số Tầng Hầm",
          "areaFrom": "Diện Tích Từ",
          "areaTo": "Diện Tích Đến",
          "rentPriceFrom": "Giá Thuê Từ",
          "rentPriceTo": "Giá Thuê Đến"
      }

      entries = {}

      #Chia bố cục thành từng hàng có đúng 3 trường
      row_offset = 2  # Bắt đầu từ hàng thứ 2 sau phần tìm kiếm nhanh
      for idx, (field_key, label) in enumerate(fields.items()):
          row = (idx // 3) + row_offset  # Chia thành từng nhóm 3 phần tử trên mỗi hàng
          col = (idx % 3) * 2  # Mỗi trường có 2 cột: nhãn + ô nhập

          tk.Label(search_frame, text=label, font=("Arial", 12)).grid(row=row, column=col, padx=10, pady=5, sticky="w")
          entry = tk.Entry(search_frame, width=25)
          entry.grid(row=row, column=col + 1, padx=10, pady=5, sticky="ew")

          entries[field_key] = entry  # Lưu Entry để lấy giá trị sau

      # Ánh xạ giữa label hiển thị và giá trị thực tế cho quận
      districts = {
          "Quận 1": "QUAN_1",
          "Quận 2": "QUAN_2",
          "Quận 3": "QUAN_3",
          "Quận 4": "QUAN_4",
          "Quận 5": "QUAN_5",
          "Quận 7": "QUAN_7",
          "Quận Bình Thạnh": "QBT",
          "Quận Tân Bình": "QTB"
      }

      # Biến lưu trạng thái của combobox quận
      district_var = tk.StringVar()

      # Thêm combobox chọn quận
      district_row = row + 1  # Hàng tiếp theo sau các trường nhập liệu
      tk.Label(search_frame, text="Chọn Quận:", font=("Arial", 12)).grid(row=district_row, column=0, padx=10, pady=5, sticky="w")

      # Tạo danh sách các tên hiển thị
      district_labels = list(districts.keys())
      # Combobox hiển thị danh sách quận
      district_combobox = ttk.Combobox(search_frame, values=district_labels, state="readonly", width=25)
      district_combobox.grid(row=district_row, column=1, padx=10, pady=5, sticky="ew")
      
      # Thêm callback khi giá trị combobox thay đổi
      def on_district_selected(event):
          selected = district_combobox.get()
          district_code = districts.get(selected)
          print(f"Selected district: {selected}, code: {district_code}")
      
      district_combobox.bind("<<ComboboxSelected>>", on_district_selected)

      # Danh sách chọn nhân viên (đặt ở cùng hàng với combobox quận)
      if role != "STAFF":
        tk.Label(search_frame, text="Chọn Nhân Viên:", font=("Arial", 12)).grid(row=district_row, column=2, padx=10, pady=5, sticky="w")

        employees = {
            "nguyenvanb": "2",
            "nguyenvanc": "3",
            "nguyenvand": "4"
        }
        # Tạo danh sách các tên hiển thị
        employee_labels = list(employees.keys())
        # Combobox hiển thị danh sách nhân viên
        employee_combobox = ttk.Combobox(search_frame, values=employee_labels, state="readonly", width=25)
        employee_combobox.grid(row=district_row, column=3, padx=10, pady=5, sticky="ew")
        
        # Thêm callback khi giá trị combobox thay đổi
        def on_employee_selected(event):
            selected = employee_combobox.get()
            staff_id = employees.get(selected)
            print(f"Selected employee: {selected}, staffId: {staff_id}")
        
        employee_combobox.bind("<<ComboboxSelected>>", on_employee_selected)

      # Ánh xạ giữa label hiển thị và giá trị thực tế
      building_types = {
        "Tầng Trệt": "TANG_TRET",
        "Nguyên Căn": "NGUYEN_CAN",
        "Nội Thất": "NOI_THAT"
      }

      # Biến lưu trạng thái của các checkbox
      building_type_vars = {}

      # Tạo frame để chứa các checkbox
      checkbox_frame = tk.Frame(search_frame)
      checkbox_row = district_row + 1  # Hàng tiếp theo sau hàng district
      checkbox_frame.grid(row=checkbox_row, column=1, columnspan=3, padx=10, pady=5, sticky="w")
      
      # Tạo checkbox cho từng loại tòa nhà
      for idx, (label, value) in enumerate(building_types.items()):
          var = tk.BooleanVar()
          building_type_vars[label] = var

          # Tạo một hàm callback riêng cho mỗi checkbox
          def make_callback(l=label, v=var):
              def callback():
                  print(f"Checkbox {l} changed to {v.get()}")
                  # In ra danh sách các loại tòa nhà được chọn sau khi thay đổi
                  selected = [building_types[label] for label, var in building_type_vars.items() if var.get()]
                  print(f"Current selected types: {selected}")
              return callback

          cb = tk.Checkbutton(
              checkbox_frame, text=label, variable=var,
              command=make_callback()
          )
          cb.pack(side="left", padx=10)

      # Hàm lấy danh sách các giá trị thực tế được chọn
      def get_selected_building_types():
          selected_types = [
              building_types[label] for label, var in building_type_vars.items() if var.get()
          ]
          return selected_types

      #Tạo bảng hiển thị kết quả (Phía dưới)
      table_frame = tk.Frame(content_frame)
      table_frame.pack(fill="both", expand=True, padx=10, pady=5)

      columns = ("id", "name", "address", "numberOfBasement", "rentPrice",
                "managername", "managerphone", "rentArea")

      tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
      tree.pack(fill="both", expand=True)

      # Thêm thanh cuộn
      scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
      scrollbar.pack(side="right", fill="y")
      tree.configure(yscrollcommand=scrollbar.set)

      table_width = table_frame.winfo_width()
      column_width = table_width // len(columns)  # Chia đều độ rộng cho các cột

      # Đặt tiêu đề cho các cột
      column_titles = {
          "id": "ID",
          "name": "Tên Tòa Nhà",
          "address": "Địa Chỉ",
          "numberOfBasement": "Số Tầng Hầm",
          "rentPrice": "Giá Thuê",
          "managername": "Tên Quản Lý",
          "managerphone": "SĐT Quản Lý",
          "rentArea": "Diện Tích Thuê"
      }
      
      for col in columns:
        tree.heading(col, text=column_titles.get(col, col.capitalize()))
        tree.column(col, width=column_width)  # Điều chỉnh độ rộng cột tự động

      #Hàm tải dữ liệu vào bảng
      def load_data(buildings):
          tree.delete(*tree.get_children())  # Xóa dữ liệu cũ
          for building in buildings:
              tree.insert("", "end", values=(
                  building.get("id"), building.get("name"), building.get("address"),
                  building.get("numberOfBasement"), building.get("rentPrice"),
                  building.get("managerName"), building.get("managerPhone"),
                  building.get("rentArea")
              ))

      # Hàm tìm kiếm nhanh theo tên
      def search_by_name(name):
          if not name.strip():
              messagebox.showinfo("Thông báo", "Vui lòng nhập tên tòa nhà để tìm kiếm!")
              return
              
          token = get_access_token()
          if not token:
              messagebox.showerror("Lỗi", "Không tìm thấy accessToken. Vui lòng đăng nhập lại.")
              return
              
          try:
              # Hiển thị thông báo đang tìm kiếm
              messagebox.showinfo("Thông báo", "Đang tìm kiếm...")
              
              # Gửi request với Authorization header
              headers = {
                  "Content-Type": "application/json",
                  "Authorization": f"Bearer {token}"
              }
              params = {"name": name.strip()}
              response = requests.get("http://localhost:8080/admin/building-list", params=params, headers=headers)
              response.raise_for_status()  # Kiểm tra lỗi HTTP
              
              data = response.json().get("data", [])
              load_data(data)
              
              # Lưu kết quả vào file data.json
              data_file = os.path.join(BASE_DIR, "data.json")
              write_json(data, data_file)
              
              messagebox.showinfo("Thông báo", f"Tìm thấy {len(data)} kết quả!")
          except requests.RequestException as e:
              messagebox.showerror("Lỗi", f"Không thể kết nối tới API: {e}")
          except ValueError:
              messagebox.showerror("Lỗi", "Dữ liệu trả về không hợp lệ!")

      #Hàm tìm kiếm qua API với nhiều tiêu chí - Cách tiếp cận thay thế
      def search_alternative():
          # Lấy giá trị từ các trường nhập liệu
          params = {}
          for field_key, entry in entries.items():
              value = entry.get().strip()
              if value:
                  params[field_key] = value
                  
          # Thêm giá trị từ combobox nhân viên với key là staffId
          if role != "STAFF" and employee_combobox.get():
              staff_id = employees.get(employee_combobox.get())
              if staff_id:
                  params["staffId"] = staff_id
          
          # Kiểm tra token
          token = get_access_token()
          if not token:
              messagebox.showerror("Lỗi", "Không tìm thấy accessToken. Vui lòng đăng nhập lại.")
              return
          
          try:
              # Hiển thị thông báo đang tìm kiếm
              messagebox.showinfo("Thông báo", "Đang tìm kiếm...")
              
              headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
              
              # Xử lý loại tòa nhà đã chọn
              selected_types = get_selected_building_types()
              
              # Sử dụng requests.Session để có thể thêm nhiều tham số cùng tên
              session = requests.Session()
              
              # Tạo URL cơ bản với các tham số buildingSearch
              base_url = "http://localhost:8080/admin/building-list"
              
              # Chuẩn bị request với các tham số buildingSearch
              req = requests.Request('GET', base_url, params=params, headers=headers)
              prepped = session.prepare_request(req)
              
              # Thêm các tham số type vào URL
              # Spring Boot sẽ tự động chuyển đổi nhiều tham số cùng tên thành List
              url = prepped.url
              for type_value in selected_types:
                  if '?' in url:
                      url += f"&type={type_value}"
                  else:
                      url += f"?type={type_value}"
              
              # Gửi request với URL đã được điều chỉnh
              prepped.url = url
              response = session.send(prepped)
              
              response.raise_for_status()
              
              data = response.json().get("data", [])
              load_data(data)
              
              # Lưu kết quả vào file data.json
              data_file = os.path.join(BASE_DIR, "data.json")
              write_json(data, data_file)
              
              messagebox.showinfo("Thông báo", f"Tìm thấy {len(data)} kết quả!")
              
              # In ra URL và params để debug
              print(f"URL: {response.url}")
              print(f"Params: {params}")
              if selected_types:
                  print(f"Selected Types: {selected_types}")
              
          except requests.RequestException as e:
              messagebox.showerror("Lỗi", f"Không thể kết nối tới API: {e}")
              print(f"Error: {e}")
          except ValueError as e:
              messagebox.showerror("Lỗi", "Dữ liệu trả về không hợp lệ!")
              print(f"ValueError: {e}")

      # Thêm hàm tìm kiếm với cách tiếp cận khác
      def search_with_array_param():
          # Lấy giá trị từ các trường nhập liệu
          params = {}
          for field_key, entry in entries.items():
              value = entry.get().strip()
              if value:
                  # Đối với các trường số, chuyển đổi thành số
                  if field_key in ["areaFrom", "areaTo", "rentPriceFrom", "rentPriceTo", "numberOfBasement"]:
                      try:
                          params[field_key] = float(value) if "." in value else int(value)
                      except ValueError:
                          params[field_key] = value
                  else:
                      params[field_key] = value
          
          # Thêm giá trị từ combobox quận với key là district
          selected_district = district_combobox.get()
          if selected_district:
              district_code = districts.get(selected_district)
              if district_code:
                  params["district"] = district_code
                  print(f"Adding district: {district_code}")
          
          # Thêm giá trị từ combobox nhân viên với key là staffId
          if role != "STAFF":
              selected_employee = employee_combobox.get()
              if selected_employee:
                  staff_id = employees.get(selected_employee)
                  if staff_id:
                      params["staffId"] = staff_id
                      print(f"Adding staffId: {staff_id}")
          
          # Lấy danh sách các loại tòa nhà được chọn
          selected_types = get_selected_building_types()
          print(f"Selected building types: {selected_types}")
          
          # Thêm các loại tòa nhà vào params
          for type_value in selected_types:
              params.setdefault("type", []).append(type_value)
          
          # Kiểm tra token
          token = get_access_token()
          if not token:
              messagebox.showerror("Lỗi", "Không tìm thấy accessToken. Vui lòng đăng nhập lại.")
              return
          
          try:
              # Hiển thị thông báo đang tìm kiếm
              messagebox.showinfo("Thông báo", "Đang tìm kiếm...")
              
              headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
              
              # Tạo URL cơ bản
              base_url = "http://localhost:8080/admin/building-list"
              
              # Debug: In ra params trước khi gửi request
              print(f"Params before request: {params}")
              
              # Sử dụng requests với params là list các tuple
              # Tạo một list các tuple (key, value) để có thể có nhiều key cùng tên
              params_list = []
              
              # Thêm các tham số từ params vào params_list
              for key, value in params.items():
                  if isinstance(value, list):  # Nếu value là danh sách, thêm từng giá trị
                      for v in value:
                          params_list.append((key, v))
                  else:
                      params_list.append((key, value))
              
              # Debug: In ra params_list
              print(f"Params list: {params_list}")
              
              # Gửi request với params_list
              response = requests.get(base_url, params=params_list, headers=headers)
              
              # Debug: In ra URL sau khi gửi request
              print(f"Final URL: {response.url}")
              
              response.raise_for_status()
              
              data = response.json().get("data", [])
              load_data(data)
              
              # Lưu kết quả vào file data.json
              data_file = os.path.join(BASE_DIR, "data.json")
              write_json(data, data_file)
              
              messagebox.showinfo("Thông báo", f"Tìm thấy {len(data)} kết quả!")
              
          except requests.RequestException as e:
              messagebox.showerror("Lỗi", f"Không thể kết nối tới API: {e}")
              print(f"Error: {e}")
          except ValueError as e:
              messagebox.showerror("Lỗi", "Dữ liệu trả về không hợp lệ!")
              print(f"ValueError: {e}")

      # Nút tìm kiếm
      search_button = tk.Button(content_frame, text="Tìm Kiếm", font=("Arial", 12), bg="blue", fg="white", command=search_with_array_param)
      search_button.pack(pady=10)

      # Tạo frame chứa các nút
      button_frame = tk.Frame(content_frame)
      button_frame.pack(pady=10)

      # Nút "Thêm Tòa Nhà"
      add_button = tk.Button(button_frame, text="Thêm Tòa Nhà", font=("Arial", 12), bg="green", fg="white", command=lambda: print("Thêm Tòa Nhà"))
      add_button.pack(side="left", padx=10)

      # Nút "Xóa Tòa Nhà"
      delete_button = tk.Button(button_frame, text="Xóa Tòa Nhà", font=("Arial", 12), bg="red", fg="white", command=lambda: print("Xóa Tòa Nhà"))
      delete_button.pack(side="left", padx=10)     

      # Hiển thị dữ liệu ban đầu từ file JSON
      data_file = os.path.join(BASE_DIR, "data.json")
      data = read_json(data_file)
      load_data(data)

  # Tạo các nút menu
  btn1 = tk.Button(menu_frame, text="Quản lý toà nhà", font=("Arial", 14), bg="red", fg="white", command=show_building)
  btn1.pack(pady=5, fill="x") 
  
  # Hiển thị màn hình quản lý tòa nhà khi mở ứng dụng
  show_building()

  admin.mainloop()
