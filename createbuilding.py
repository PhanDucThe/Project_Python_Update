import tkinter as tk
from tkinter import ttk, messagebox
import os
import requests
import json
from utils import write_json, BASE_DIR, get_access_token

def show_create_building_form(admin, content_frame):
    """
    Hiển thị form thêm mới tòa nhà
    
    Parameters:
    - admin: cửa sổ chính của ứng dụng
    - content_frame: frame nội dung hiện tại cần ẩn đi
    """
    # Ẩn nội dung hiện tại
    content_frame.pack_forget()
    
    # Tạo frame mới cho form thêm tòa nhà
    add_building_frame = tk.Frame(admin, width=950, height=700, bg="white")
    add_building_frame.pack(side="right", fill="both", expand=True)
    
    # Tiêu đề
    tk.Label(add_building_frame, text="Thêm Mới Tòa Nhà", font=("Arial", 24, "bold"), bg="white").pack(pady=10)
    
    # Tạo frame chứa form
    form_frame = tk.Frame(add_building_frame, bg="white")
    form_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Tạo canvas và scrollbar để có thể cuộn khi form dài
    canvas = tk.Canvas(form_frame, bg="white")
    scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
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
    
    # Tạo danh sách các tên hiển thị
    district_labels = list(districts.keys())
    
    # Combobox hiển thị danh sách quận
    district_combobox = ttk.Combobox(scrollable_frame, values=district_labels, state="readonly", width=47)
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
    
    # Xóa phần checkbox loại tòa nhà
    
    # Frame chứa các nút
    button_frame = tk.Frame(add_building_frame, bg="white")
    button_frame.pack(pady=20)
    
    # Hàm lưu tòa nhà mới
    def save_new_building():
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
            else:
                building_data["numberOfBasement"] = 0
                
            if building_data.get("floorArea"):
                building_data["floorArea"] = float(building_data["floorArea"])
            else:
                building_data["floorArea"] = 0
                
            if building_data.get("rentPrice"):
                building_data["rentPrice"] = float(building_data["rentPrice"])
            else:
                building_data["rentPrice"] = 0
                
            # Thêm trường brokerageFee mặc định là 0
            building_data["brokerageFee"] = 0
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
            "note": ""
        }
        
        for field, default_value in additional_fields.items():
            if field not in building_data:
                building_data[field] = default_value
        
        # Gửi dữ liệu lên API để tạo tòa nhà mới
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
            
            # Gửi request POST đến API
            response = requests.post(
                "http://localhost:8080/admin/building-create",
                headers=headers,
                data=json.dumps(building_data)
            )
            
            # Kiểm tra kết quả
            if response.status_code == 201 or response.status_code == 200:
                # Hiển thị thông báo thành công
                messagebox.showinfo("Thành công", "Thêm mới tòa nhà thành công!")
                
                # Quay lại trang admin
                add_building_frame.destroy()
                content_frame.pack(side="right", fill="both", expand=True)
                
                # Gọi API để cập nhật danh sách tòa nhà
                refresh_building_list(content_frame, token)
            else:
                # Hiển thị thông báo lỗi
                error_data = response.json()
                error_message = error_data.get("message", "Lỗi không xác định")
                messagebox.showerror("Lỗi", f"Không thể thêm tòa nhà: {error_message}")
                
        except requests.RequestException as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối đến máy chủ: {str(e)}")
        except ValueError as e:
            messagebox.showerror("Lỗi dữ liệu", f"Dữ liệu không hợp lệ: {str(e)}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")
    
    # Hàm hủy và quay lại trang admin
    def cancel_add_building():
        add_building_frame.destroy()
        content_frame.pack(side="right", fill="both", expand=True)
    
    # Nút "Thêm Mới"
    add_btn = tk.Button(button_frame, text="Thêm Mới", font=("Arial", 12), bg="green", fg="white", command=save_new_building)
    add_btn.pack(side="left", padx=10)
    
    # Nút "Hủy"
    cancel_btn = tk.Button(button_frame, text="Hủy", font=("Arial", 12), bg="red", fg="white", command=cancel_add_building)
    cancel_btn.pack(side="left", padx=10)

# Hàm cập nhật danh sách tòa nhà
def refresh_building_list(content_frame, token):
    try:
        # Tìm tree widget trong content_frame
        tree = None
        for widget in content_frame.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Treeview):
                        tree = child
                        break
        
        if not tree:
            print("Không tìm thấy Treeview widget để cập nhật")
            return
        
        # Gửi request GET đến API để lấy danh sách tòa nhà
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.get(
            "http://localhost:8080/admin/building-list",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json().get("data", [])
            
            # Xóa dữ liệu cũ
            tree.delete(*tree.get_children())
            
            # Thêm dữ liệu mới
            for building in data:
                tree.insert("", "end", values=(
                    building.get("id"), building.get("name"), building.get("address"),
                    building.get("numberOfBasement"), building.get("rentPrice"),
                    building.get("managerName"), building.get("managerPhone"),
                    building.get("rentArea")
                ))
            
            # Lưu kết quả vào file data.json
            import os
            from utils import BASE_DIR, write_json
            data_file = os.path.join(BASE_DIR, "data.json")
            write_json(data, data_file)
            
            print(f"Đã cập nhật danh sách tòa nhà: {len(data)} tòa nhà")
        else:
            print(f"Lỗi khi lấy danh sách tòa nhà: {response.status_code}")
    
    except Exception as e:
        print(f"Lỗi khi cập nhật danh sách tòa nhà: {str(e)}")




