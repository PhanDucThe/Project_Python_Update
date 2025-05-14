import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os
from utils import read_json, write_json, get_access_token, BASE_DIR

def show_edit_building_form(admin, content_frame, building_id):
    """
    Hiển thị form chỉnh sửa tòa nhà
    
    Parameters:
    - admin: cửa sổ chính của ứng dụng
    - content_frame: frame nội dung hiện tại cần ẩn đi
    - building_id: ID của tòa nhà cần chỉnh sửa
    """
    # Ẩn nội dung hiện tại
    content_frame.pack_forget()
    
    # Tạo frame mới cho form chỉnh sửa tòa nhà
    edit_building_frame = tk.Frame(admin, width=950, height=700, bg="white")
    edit_building_frame.pack(side="right", fill="both", expand=True)
    
    # Tiêu đề
    tk.Label(edit_building_frame, text=f"Chỉnh Sửa Tòa Nhà (ID: {building_id})", font=("Arial", 24, "bold"), bg="white").pack(pady=10)
    
    # Tạo frame có thanh cuộn
    main_frame = tk.Frame(edit_building_frame, bg="white")
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Tạo canvas và scrollbar
    canvas = tk.Canvas(main_frame, bg="white")
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    
    # Tạo frame bên trong canvas để chứa các widget
    scrollable_frame = tk.Frame(canvas, bg="white")
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
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
    
    # Đảo ngược mapping để lấy label từ value
    districts_reverse = {v: k for k, v in districts.items()}
    
    # Danh sách các trường nhập liệu (trừ quận vì sẽ dùng combobox)
    fields = {
        "name": "Tên Tòa Nhà", 
        "ward": "Phường",
        "street": "Đường", 
        "numberOfBasement": "Số Tầng Hầm",
        "floorArea": "Diện Tích Sàn",
        "rentArea": "Diện Tích Thuê",
        "rentPrice": "Giá Thuê",
        "rentPriceDescription": "Mô Tả Giá",
        "managerName": "Tên Quản Lý", 
        "managerPhone": "SĐT Quản Lý"
    }
    
    entries = {}
    
    # Tạo các trường nhập liệu
    row_idx = 0
    
    # Thêm trường Tên Tòa Nhà trước
    tk.Label(scrollable_frame, text="Tên Tòa Nhà", font=("Arial", 12), bg="white").grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
    name_entry = tk.Entry(scrollable_frame, width=50)
    name_entry.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
    entries["name"] = name_entry
    row_idx += 1
    
    # Thêm combobox cho quận
    tk.Label(scrollable_frame, text="Quận", font=("Arial", 12), bg="white").grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
    district_combobox = ttk.Combobox(scrollable_frame, values=list(districts.keys()), state="readonly", width=48)
    district_combobox.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
    entries["district"] = district_combobox
    row_idx += 1
    
    # Thêm các trường còn lại
    for field_key, label in fields.items():
        if field_key == "name":  # Đã thêm ở trên
            continue
            
        tk.Label(scrollable_frame, text=label, font=("Arial", 12), bg="white").grid(row=row_idx, column=0, padx=10, pady=5, sticky="w")
        
        # Nếu là trường mô tả giá, sử dụng Text thay vì Entry để nhập nhiều dòng
        if field_key == "rentPriceDescription":
            entry = tk.Text(scrollable_frame, width=50, height=3)
            entry.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
        else:
            entry = tk.Entry(scrollable_frame, width=50)
            entry.grid(row=row_idx, column=1, padx=10, pady=5, sticky="ew")
        
        entries[field_key] = entry
        row_idx += 1
    
    # Frame chứa các nút
    button_frame = tk.Frame(edit_building_frame, bg="white")
    button_frame.pack(pady=20)
    
    # Hàm lấy dữ liệu tòa nhà từ API
    def fetch_building_data():
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
            
            # Gửi request GET đến API
            response = requests.get(
                f"http://localhost:8080/admin/building-byid/{building_id}",
                headers=headers
            )
            
            # Kiểm tra kết quả
            if response.status_code == 200:
                building_data = response.json().get("data", {})
                
                # Điền dữ liệu vào các trường
                for field_key, entry in entries.items():
                    if field_key == "district":
                        # Đối với combobox quận, cần tìm label tương ứng
                        district_value = building_data.get(field_key)
                        district_label = districts_reverse.get(district_value, "")
                        if district_label:
                            entry.set(district_label)
                    elif field_key == "rentPriceDescription":
                        # Đối với Text widget, cần sử dụng insert
                        entry.delete("1.0", tk.END)
                        entry.insert("1.0", building_data.get(field_key, ""))
                    else:
                        # Đối với Entry widget
                        entry.delete(0, tk.END)
                        entry.insert(0, building_data.get(field_key, ""))
                
                return building_data
            else:
                # Hiển thị thông báo lỗi
                error_data = response.json()
                error_message = error_data.get("message", "Lỗi không xác định")
                messagebox.showerror("Lỗi", f"Không thể lấy thông tin tòa nhà: {error_message}")
                return None
                
        except requests.RequestException as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối đến máy chủ: {str(e)}")
            return None
        except ValueError as e:
            messagebox.showerror("Lỗi dữ liệu", f"Dữ liệu không hợp lệ: {str(e)}")
            return None
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")
            return None
    
    # Hàm lưu tòa nhà đã chỉnh sửa
    def save_edited_building():
        # Lấy giá trị từ các trường nhập liệu
        building_data = {}
        for field_key, entry in entries.items():
            if field_key == "rentPriceDescription":
                # Đối với Text widget, cần sử dụng get với tham số
                value = entry.get("1.0", tk.END).strip()
            elif field_key == "district":
                # Đối với Combobox, lấy giá trị hiển thị
                selected_district = entry.get()
                if selected_district:
                    # Chuyển đổi sang giá trị thực tế
                    value = districts.get(selected_district)
                else:
                    value = ""
            else:
                value = entry.get().strip()
            building_data[field_key] = value
        
        # Thêm ID của tòa nhà
        building_data["id"] = building_id
        
        # Thêm loại tòa nhà mặc định là "NGUYEN_CAN"
        building_data["type"] = ["NGUYEN_CAN"]
        
        # Debug: In ra dữ liệu trước khi gửi
        print("Building data to send:", building_data)
        
        # Kiểm tra các trường bắt buộc
        required_fields = ["name", "district", "ward", "street", "managerName", "managerPhone"]
        for field in required_fields:
            if not building_data.get(field):
                field_label = "Quận" if field == "district" else fields.get(field, field)
                messagebox.showwarning("Cảnh báo", f"Vui lòng nhập {field_label}!")
                return
        
        # Chuyển đổi các trường số
        try:
            if building_data.get("numberOfBasement"):
                building_data["numberOfBasement"] = int(building_data["numberOfBasement"])
            if building_data.get("floorArea"):
                building_data["floorArea"] = float(building_data["floorArea"])
            if building_data.get("rentPrice"):
                building_data["rentPrice"] = float(building_data["rentPrice"])
        except ValueError:
            messagebox.showwarning("Cảnh báo", "Các trường số phải nhập đúng định dạng số!")
            return
        
        # Tạo địa chỉ đầy đủ
        building_data["address"] = f"{building_data['street']}, {building_data['ward']}, {building_data['district']}"
        
        # Thêm các trường còn thiếu theo yêu cầu API
        additional_fields = {
            "structure": "",
            "direction": "",
            "level": "",
            "serviceFee": "",
            "carFee": "",
            "motoFee": "",
            "overTimeFee": "",
            "electricityFee": "",
            "deposit": "",
            "payment": "",
            "rentTime": "",
            "decorationTime": "",
            "note": "",
            "brokerageFee": 0
        }
        
        for field, default_value in additional_fields.items():
            if field not in building_data:
                building_data[field] = default_value
        
        # Gửi dữ liệu lên API để cập nhật tòa nhà
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
            
            # Debug: In ra dữ liệu JSON trước khi gửi
            print("JSON data to send:", json.dumps(building_data, indent=2))
            
            # Gửi request PUT đến API
            response = requests.put(
                "http://localhost:8080/admin/building-edit",
                headers=headers,
                data=json.dumps(building_data)
            )
            
            # Kiểm tra kết quả
            if response.status_code == 200 or response.status_code == 204:
                # Hiển thị thông báo thành công
                messagebox.showinfo("Thành công", "Cập nhật tòa nhà thành công!")
                
                # Quay lại trang admin
                edit_building_frame.destroy()
                content_frame.pack(side="right", fill="both", expand=True)
                
                # Gọi API để cập nhật danh sách tòa nhà
                from createbuilding import refresh_building_list
                refresh_building_list(content_frame, token)
            else:
                # Hiển thị thông báo lỗi
                error_data = response.json()
                error_message = error_data.get("message", "Lỗi không xác định")
                messagebox.showerror("Lỗi", f"Không thể cập nhật tòa nhà: {error_message}")
                
        except requests.RequestException as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối đến máy chủ: {str(e)}")
        except ValueError as e:
            messagebox.showerror("Lỗi dữ liệu", f"Dữ liệu không hợp lệ: {str(e)}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")
    
    # Hàm hủy và quay lại trang admin
    def cancel_edit_building():
        edit_building_frame.destroy()
        content_frame.pack(side="right", fill="both", expand=True)
    
    # Nút "Lưu Thay Đổi"
    save_btn = tk.Button(button_frame, text="Lưu Thay Đổi", font=("Arial", 12), bg="green", fg="white", command=save_edited_building)
    save_btn.pack(side="left", padx=10)
    
    # Nút "Hủy"
    cancel_btn = tk.Button(button_frame, text="Hủy", font=("Arial", 12), bg="red", fg="white", command=cancel_edit_building)
    cancel_btn.pack(side="left", padx=10)
    
    # Lấy dữ liệu tòa nhà và điền vào form
    fetch_building_data()