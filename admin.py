import tkinter as tk
from tkinter import ttk
from utils import read_json, getRole, write_json, BASE_DIR
from tkinter import messagebox
import os
from createbuilding import show_create_building_form, refresh_building_list  # Import hàm từ file mới
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
      
      # --- Bố trí lại form tìm kiếm cho đẹp ---
      search_frame = tk.LabelFrame(content_frame, text="Tìm kiếm tòa nhà", font=("Arial", 12, "bold"), padx=15, pady=10)
      search_frame.pack(fill="x", padx=20, pady=10)

      fields = [
          ("name", "Tên Tòa Nhà"),
          ("street", "Đường"),
          ("ward", "Phường"),
          ("managerName", "Tên Quản Lý"),
          ("managerPhone", "SĐT Quản Lý"),
          ("numberOfBasement", "Số Tầng Hầm"),
          ("rentPriceFrom", "Giá Thuê Từ"),
          ("rentPriceTo", "Giá Thuê Đến")
      ]
      entries = {}
      num_cols = 3
      for idx, (field_key, label) in enumerate(fields):
          row = idx // num_cols
          col = (idx % num_cols) * 2
          tk.Label(search_frame, text=label, font=("Arial", 11)).grid(row=row, column=col, padx=(0,5), pady=7, sticky="e")
          entry = tk.Entry(search_frame, width=22, font=("Arial", 11))
          entry.grid(row=row, column=col+1, padx=(0,15), pady=7, sticky="w")
          entries[field_key] = entry

      # Hàng tiếp theo cho combobox quận
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
      district_labels = list(districts.keys())
      last_row = (len(fields)-1) // num_cols + 1
      tk.Label(search_frame, text="Quận", font=("Arial", 11)).grid(row=last_row, column=0, padx=(0,5), pady=7, sticky="e")
      district_combobox = ttk.Combobox(search_frame, values=district_labels, state="readonly", width=20, font=("Arial", 11))
      district_combobox.grid(row=last_row, column=1, padx=(0,15), pady=7, sticky="w")
      def on_district_selected(event):
          selected = district_combobox.get()
          print(f"Selected district: {selected}")
      district_combobox.bind("<<ComboboxSelected>>", on_district_selected)

      # Đường phân cách
      separator = ttk.Separator(search_frame, orient='horizontal')
      separator.grid(row=last_row+1, column=0, columnspan=6, sticky="ew", pady=10)

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
          params = {}
          for field_key, entry in entries.items():
              value = entry.get().strip()
              if value:
                  if field_key in ["rentPriceFrom", "rentPriceTo", "numberOfBasement"]:
                      try:
                          params[field_key] = float(value) if "." in value else int(value)
                      except ValueError:
                          messagebox.showwarning("Giá trị không hợp lệ", f"Trường '{field_key}' phải là số!")
                          return
                  else:
                      params[field_key] = value
          selected_district = district_combobox.get()
          if selected_district:
              params["district"] = selected_district
          try:
              data_file = os.path.join(BASE_DIR, "data.json")
              all_data = read_json(data_file)
              results = []
              for building in all_data:
                  match = True
                  for key, value in params.items():
                      # So sánh số cho các trường số
                      if key == "numberOfBasement":
                          try:
                              if int(building.get(key, 0)) != int(value):
                                  match = False
                                  break
                          except Exception:
                              match = False
                              break
                      elif key == "rentPriceFrom":
                          try:
                              if float(building.get("rentPrice", 0)) < float(value):
                                  match = False
                                  break
                          except Exception:
                              match = False
                              break
                      elif key == "rentPriceTo":
                          try:
                              if float(building.get("rentPrice", 0)) > float(value):
                                  match = False
                                  break
                          except Exception:
                              match = False
                              break
                      elif key == "district":
                          # So sánh tên quận (không phân biệt hoa thường, loại bỏ khoảng trắng thừa)
                          if str(value).strip().lower() not in str(building.get("district", "")).strip().lower():
                              match = False
                              break
                      else:
                          # So sánh chuỗi (không phân biệt hoa thường, tìm kiếm gần đúng)
                          if str(value).lower() not in str(building.get(key, "")).lower():
                              match = False
                              break
                  if match:
                      results.append(building)
              load_data(results)
              messagebox.showinfo("Kết quả", f"Tìm thấy {len(results)} kết quả!")
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
          if role != "MANAGER":
              messagebox.showwarning("Cảnh báo", "Bạn không có quyền chỉnh sửa tòa nhà!")
              return
          selected_items = tree.selection()
          if not selected_items:
              messagebox.showwarning("Cảnh báo", "Vui lòng chọn một tòa nhà để chỉnh sửa!")
              return
          selected_id = tree.item(selected_items[0])['values'][0]
          show_edit_building_form(admin, content_frame, selected_id)

      # Hàm xử lý khi click vào nút "Xóa Tòa Nhà"
      def delete_selected_building():
          if role != "MANAGER":
              messagebox.showwarning("Cảnh báo", "Bạn không có quyền xóa tòa nhà!")
              return
          selected_items = tree.selection()
          if not selected_items:
              messagebox.showwarning("Cảnh báo", "Vui lòng chọn một tòa nhà để xóa!")
              return
          selected_id = tree.item(selected_items[0])['values'][0]
          building_name = tree.item(selected_items[0])['values'][1]
          confirm = messagebox.askyesno(
              "Xác nhận xóa", 
              f"Bạn có chắc chắn muốn xóa tòa nhà '{building_name}' (ID: {selected_id}) không?"
          )
          if confirm:
              delete_building_by_id(selected_id)

      # Hàm xóa tòa nhà khỏi file data.json
      def delete_building_by_id(building_id):
          if role != "MANAGER":
              messagebox.showwarning("Cảnh báo", "Bạn không có quyền xóa!")
              return
          try:
              data_file = os.path.join(BASE_DIR, "data.json")
              all_data = read_json(data_file)
              new_data = [b for b in all_data if str(b.get("id")) != str(building_id)]
              write_json(new_data, data_file)
              messagebox.showinfo("Thành công", "Xóa tòa nhà thành công!")
              refresh_building_list(content_frame)
          except Exception as e:
              messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

  # Tạo các nút menu
  btn1 = tk.Button(menu_frame, text="Quản lý toà nhà", font=("Arial", 14), bg="red", fg="white", command=show_building)
  btn1.pack(pady=5, fill="x") 

  # Thêm các chức năng Option khác
  def show_user_management():
      for widget in content_frame.winfo_children():
          widget.destroy()
      tk.Label(content_frame, text="Quản Lý Người Dùng", font=("Arial", 18, "bold")).pack(pady=20)
      # Hiển thị danh sách user từ user.json
      user_file = os.path.join(BASE_DIR, "user.json")
      users = read_json(user_file)
      columns = ("userId", "userName", "role")
      tree = ttk.Treeview(content_frame, columns=columns, show="headings", height=10)
      tree.pack(fill="both", expand=True, padx=20, pady=10)
      tree.heading("userId", text="ID")
      tree.heading("userName", text="Tên Đăng Nhập")
      tree.heading("role", text="Phân Quyền")
      for user in users:
          tree.insert("", "end", values=(user.get("userId"), user.get("userName"), user.get("role")))
      # Có thể thêm các nút Thêm/Sửa/Xóa user nếu là MANAGER
      if role == "MANAGER":
          user_btn_frame = tk.Frame(content_frame)
          user_btn_frame.pack(pady=10)
          tk.Button(user_btn_frame, text="Thêm User", font=("Arial", 12), bg="green", fg="white").pack(side="left", padx=10)
          tk.Button(user_btn_frame, text="Sửa User", font=("Arial", 12), bg="blue", fg="white").pack(side="left", padx=10)
          tk.Button(user_btn_frame, text="Xóa User", font=("Arial", 12), bg="red", fg="white").pack(side="left", padx=10)

  def show_app_info():
      for widget in content_frame.winfo_children():
          widget.destroy()
      tk.Label(content_frame, text="Thông Tin Ứng Dụng", font=("Arial", 18, "bold")).pack(pady=20)
      info = "Ứng dụng Quản lý Tòa nhà\nPhiên bản: 1.0\nTác giả: Nhóm phát triển\nHoạt động hoàn toàn offline với file JSON."
      tk.Label(content_frame, text=info, font=("Arial", 14), justify="left").pack(pady=10)

  def show_help():
      for widget in content_frame.winfo_children():
          widget.destroy()
      tk.Label(content_frame, text="Trợ Giúp & Hướng Dẫn", font=("Arial", 18, "bold")).pack(pady=20)
      help_text = "- Đăng nhập đúng tài khoản để sử dụng.\n- STAFF chỉ được xem dữ liệu.\n- MANAGER có thể thêm/sửa/xóa.\n- Dữ liệu lưu tại các file JSON trong thư mục ứng dụng.\n- Mọi thao tác đều thực hiện trực tiếp trên máy."
      tk.Label(content_frame, text=help_text, font=("Arial", 14), justify="left").pack(pady=10)

  # Nút Option cho các chức năng khác
  btn2 = tk.Button(menu_frame, text="Quản lý người dùng", font=("Arial", 14), bg="#007bff", fg="white", command=show_user_management)
  btn2.pack(pady=5, fill="x")
  btn3 = tk.Button(menu_frame, text="Thông tin ứng dụng", font=("Arial", 14), bg="#28a745", fg="white", command=show_app_info)
  btn3.pack(pady=5, fill="x")
  btn4 = tk.Button(menu_frame, text="Trợ giúp", font=("Arial", 14), bg="#ffc107", fg="black", command=show_help)
  btn4.pack(pady=5, fill="x")

  # Nút Logout
  def logout():
      # Xóa user_current.json nếu có
      user_current_file = os.path.join(BASE_DIR, "user_current.json")
      try:
          if os.path.exists(user_current_file):
              os.remove(user_current_file)
      except Exception as e:
          print(f"Lỗi khi xóa user_current.json: {e}")
      admin.destroy()
      # Import lại index.py để quay về màn hình đăng nhập
      import subprocess, sys
      python = sys.executable
      subprocess.Popen([python, os.path.join(BASE_DIR, "index.py")])

  btn_logout = tk.Button(menu_frame, text="Đăng xuất", font=("Arial", 14, "bold"), bg="#dc3545", fg="white", command=logout)
  btn_logout.pack(pady=30, fill="x")

  # Hiển thị màn hình quản lý tòa nhà khi mở ứng dụng
  show_building()

  admin.mainloop()
