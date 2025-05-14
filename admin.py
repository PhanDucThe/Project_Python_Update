import tkinter as tk
from tkinter import ttk
import requests
from utils import read_json, getRole, get_access_token, write_json, BASE_DIR
from tkinter import messagebox
import os
from createbuilding import show_create_building_form  # Import hàm từ file mới
from editbuilding import show_edit_building_form  # Import hàm từ file mới

def show_admin(role=None):
  # Nếu role không được truyền vào, lấy từ file user.json
  if role is None:
    role = getRole()
  
  print(f"Current role: {role}")  # Debug: In ra role để kiểm tra
  
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
          
      # Tiêu đề
      title_label = tk.Label(content_frame, text="Quản Lý Tòa Nhà", font=("Arial", 18, "bold"))
      title_label.pack(pady=20)
      
      # Form tìm kiếm (Phía trên)
      search_frame = tk.Frame(content_frame)
      search_frame.pack(fill="x", padx=10, pady=5)

      # Đường phân cách
      separator = ttk.Separator(search_frame, orient='horizontal')
      separator.grid(row=1, column=0, columnspan=6, sticky="ew", pady=10)

      # Danh sách các trường nhập liệu
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

      # Chia bố cục thành từng hàng có đúng 3 trường
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

      # Tạo bảng hiển thị kết quả (Phía dưới)
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

      # Hàm tải dữ liệu vào bảng
      def load_data(buildings):
          tree.delete(*tree.get_children())  # Xóa dữ liệu cũ
          for building in buildings:
              tree.insert("", "end", values=(
                  building.get("id"), building.get("name"), building.get("address"),
                  building.get("numberOfBasement"), building.get("rentPrice"),
                  building.get("managerName"), building.get("managerPhone"),
                  building.get("rentArea")
              ))

      # Hàm tìm kiếm với các tham số
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
              
              # Gửi request GET đến API
              response = requests.get(base_url, params=params, headers=headers)
              response.raise_for_status()
              
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
          except Exception as e:
              messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

      # Nút tìm kiếm
      search_button = tk.Button(content_frame, text="Tìm Kiếm", font=("Arial", 12), bg="blue", fg="white", command=search_with_array_param)
      search_button.pack(pady=10)

      # Hiển thị dữ liệu ban đầu từ file JSON
      data_file = os.path.join(BASE_DIR, "data.json")
      data = read_json(data_file)
      load_data(data)

      # Tạo frame chứa các nút thêm, sửa, xóa (đặt sau nút tìm kiếm)
      if role == "MANAGER":
          button_frame = tk.Frame(content_frame)
          button_frame.pack(pady=10)
          
          # Nút "Thêm Tòa Nhà"
          add_button = tk.Button(button_frame, text="Thêm Tòa Nhà", font=("Arial", 12), bg="green", fg="white", command=lambda: show_create_building_form(admin, content_frame))
          add_button.pack(side="left", padx=10)
          
          # Nút "Chỉnh Sửa Tòa Nhà"
          edit_button = tk.Button(button_frame, text="Chỉnh Sửa Tòa Nhà", font=("Arial", 12), bg="blue", fg="white", command=lambda: edit_selected_building())
          edit_button.pack(side="left", padx=10)
          
          # Nút "Xóa Tòa Nhà"
          delete_button = tk.Button(button_frame, text="Xóa Tòa Nhà", font=("Arial", 12), bg="red", fg="white", command=lambda: delete_selected_building())
          delete_button.pack(side="left", padx=10)

      # Hàm xử lý khi click vào nút "Chỉnh Sửa Tòa Nhà"
      def edit_selected_building():
          # Lấy item được chọn từ tree
          selected_items = tree.selection()
          
          if not selected_items:
              messagebox.showwarning("Cảnh báo", "Vui lòng chọn một tòa nhà để chỉnh sửa!")
              return
              
          # Lấy ID của tòa nhà được chọn
          selected_id = tree.item(selected_items[0])['values'][0]  # Giả sử ID ở cột đầu tiên
          
          # Gọi hàm hiển thị form chỉnh sửa tòa nhà
          show_edit_building_form(admin, content_frame, selected_id)

      # Hàm xử lý khi click vào nút "Xóa Tòa Nhà"
      def delete_selected_building():
          # Lấy item được chọn từ tree
          selected_items = tree.selection()
          
          if not selected_items:
              messagebox.showwarning("Cảnh báo", "Vui lòng chọn một tòa nhà để xóa!")
              return
          
          # Lấy ID của tòa nhà được chọn
          selected_id = tree.item(selected_items[0])['values'][0]  # Giả sử ID ở cột đầu tiên
          building_name = tree.item(selected_items[0])['values'][1]  # Giả sử tên tòa nhà ở cột thứ hai
          
          # Hiển thị hộp thoại xác nhận
          confirm = messagebox.askyesno(
              "Xác nhận xóa", 
              f"Bạn có chắc chắn muốn xóa tòa nhà '{building_name}' (ID: {selected_id}) không?"
          )
          
          if confirm:
              # Người dùng đã xác nhận, tiến hành xóa
              delete_building_by_id(selected_id)

      # Hàm gửi request xóa tòa nhà đến API
      def delete_building_by_id(building_id):
          try:
              # Lấy token xác thực
              token = get_access_token()
              
              if not token:
                  messagebox.showerror("Lỗi", "Không thể xác thực. Vui lòng đăng nhập lại!")
                  return
              
              # Chuẩn bị headers với token xác thực
              headers = {
                  "Content-Type": "application/json",
                  "Authorization": f"Bearer {token}"
              }
              
              # Tạo URL với tham số buildingIds
              url = f"http://localhost:8080/admin/building-del/?buildingIds={building_id}"
              
              # Debug: In ra URL trước khi gửi request
              print(f"Delete URL: {url}")
              
              # Gửi request DELETE đến API
              response = requests.delete(url, headers=headers)
              
              # Kiểm tra kết quả
              if response.status_code == 200 or response.status_code == 204:
                  # Hiển thị thông báo thành công
                  messagebox.showinfo("Thành công", "Xóa tòa nhà thành công!")
                  
                  # Cập nhật danh sách tòa nhà
                  from createbuilding import refresh_building_list
                  refresh_building_list(content_frame, token)
              else:
                  # Hiển thị thông báo lỗi
                  try:
                      error_data = response.json()
                      error_message = error_data.get("message", "Lỗi không xác định")
                      messagebox.showerror("Lỗi", f"Không thể xóa tòa nhà: {error_message}")
                  except:
                      messagebox.showerror("Lỗi", f"Không thể xóa tòa nhà. Mã lỗi: {response.status_code}")
              
          except requests.RequestException as e:
              messagebox.showerror("Lỗi kết nối", f"Không thể kết nối đến máy chủ: {str(e)}")
          except Exception as e:
              messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

  # Tạo các nút menu
  btn1 = tk.Button(menu_frame, text="Quản lý toà nhà", font=("Arial", 14), bg="red", fg="white", command=show_building)
  btn1.pack(pady=5, fill="x") 
  
  # Hiển thị màn hình quản lý tòa nhà khi mở ứng dụng
  show_building()

  admin.mainloop()
