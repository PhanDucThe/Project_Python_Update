import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

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
    edit_building_frame = tk.Frame(admin, width=950, height=700, bg="#f8f9fa")
    edit_building_frame.pack(side="right", fill="both", expand=True)

    # Tiêu đề lớn, căn giữa
    tk.Label(edit_building_frame, text=f"Chỉnh Sửa Tòa Nhà (ID: {building_id})", font=("Arial", 26, "bold"), fg="#2c3e50", bg="#f8f9fa").pack(pady=(18, 8))

    # Tạo LabelFrame chứa form
    form_labelframe = tk.LabelFrame(edit_building_frame, text="Thông tin tòa nhà", font=("Arial", 14, "bold"), bg="#f8f9fa", fg="#007bff", bd=2, relief="groove", padx=18, pady=18)
    form_labelframe.pack(fill="both", expand=True, padx=30, pady=10)

    # Tạo canvas và scrollbar để cuộn khi form dài
    canvas = tk.Canvas(form_labelframe, bg="#f8f9fa", highlightthickness=0)
    scrollbar = ttk.Scrollbar(form_labelframe, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f8f9fa")
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
    row_idx = 0

    # Tên tòa nhà
    tk.Label(scrollable_frame, text="Tên Tòa Nhà", font=("Arial", 12, "bold"), bg="#f8f9fa").grid(row=row_idx, column=0, padx=12, pady=8, sticky="e")
    name_entry = tk.Entry(scrollable_frame, width=38, font=("Arial", 12))
    name_entry.grid(row=row_idx, column=1, padx=12, pady=8, sticky="w")
    entries["name"] = name_entry
    row_idx += 1

    # Quận (combobox)
    tk.Label(scrollable_frame, text="Quận", font=("Arial", 12, "bold"), bg="#f8f9fa").grid(row=row_idx, column=0, padx=12, pady=8, sticky="e")
    district_combobox = ttk.Combobox(scrollable_frame, values=list(districts.keys()), state="readonly", width=36, font=("Arial", 12))
    district_combobox.grid(row=row_idx, column=1, padx=12, pady=8, sticky="w")
    entries["district"] = district_combobox
    row_idx += 1

    # Các trường còn lại
    for field_key, label in fields.items():
        if field_key == "name":
            continue
        tk.Label(scrollable_frame, text=label, font=("Arial", 12, "bold"), bg="#f8f9fa").grid(row=row_idx, column=0, padx=12, pady=8, sticky="e")
        if field_key == "rentPriceDescription":
            entry = tk.Text(scrollable_frame, width=38, height=3, font=("Arial", 12))
            entry.grid(row=row_idx, column=1, padx=12, pady=8, sticky="w")
        else:
            entry = tk.Entry(scrollable_frame, width=38, font=("Arial", 12))
            entry.grid(row=row_idx, column=1, padx=12, pady=8, sticky="w")
        entries[field_key] = entry
        row_idx += 1

    # Frame chứa các nút
    button_frame = tk.Frame(edit_building_frame, bg="#f8f9fa")
    button_frame.pack(pady=18)
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Hàm lấy dữ liệu tòa nhà từ file JSON
    def fetch_building_data():
        data_file = os.path.join(BASE_DIR, "data.json")
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []
        building_data = None
        for b in data:
            if str(b.get("id")) == str(building_id):
                building_data = b
                break
        if not building_data:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin tòa nhà!")
            return None
        # Điền dữ liệu vào các trường
        for field_key, entry in entries.items():
            if field_key == "district":
                district_value = building_data.get(field_key)
                district_label = districts_reverse.get(district_value, "")
                if district_label:
                    entry.set(district_label)
            elif field_key == "rentPriceDescription":
                entry.delete("1.0", tk.END)
                entry.insert("1.0", building_data.get(field_key, ""))
            else:
                entry.delete(0, tk.END)
                entry.insert(0, str(building_data.get(field_key, "")))
        return building_data

    # Hàm lưu tòa nhà đã chỉnh sửa (ghi vào file JSON)
    def save_edited_building():
        building_data = {}
        for field_key, entry in entries.items():
            if field_key == "rentPriceDescription":
                value = entry.get("1.0", tk.END).strip()
            elif field_key == "district":
                selected_district = entry.get()
                value = districts.get(selected_district) if selected_district else ""
            else:
                value = entry.get().strip()
            building_data[field_key] = value
        building_data["id"] = building_id
        building_data["type"] = ["NGUYEN_CAN"]
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
        except ValueError:
            messagebox.showwarning("Cảnh báo", "Các trường số phải nhập đúng định dạng số!")
            return
        building_data["address"] = f"{building_data['street']}, {building_data['ward']}, {building_data['district']}"
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
        # Ghi lại vào file data.json
        data_file = os.path.join(BASE_DIR, "data.json")
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []
        found = False
        for idx, b in enumerate(data):
            if str(b.get("id")) == str(building_id):
                data[idx] = {**b, **building_data}
                found = True
                break
        if not found:
            messagebox.showerror("Lỗi", "Không tìm thấy tòa nhà để cập nhật!")
            return
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Thành công", "Cập nhật tòa nhà thành công!")
        edit_building_frame.destroy()
        content_frame.pack(side="right", fill="both", expand=True)
        from createbuilding import refresh_building_list
        refresh_building_list(content_frame)
    
    # Hàm hủy và quay lại trang admin
    def cancel_edit_building():
        edit_building_frame.destroy()
        content_frame.pack(side="right", fill="both", expand=True)
    
    # Nút "Lưu Thay Đổi"
    save_btn = tk.Button(button_frame, text="Lưu Thay Đổi", font=("Arial", 13, "bold"), bg="#28a745", fg="white", activebackground="#218838", activeforeground="white", width=12, height=1, relief="raised", bd=2, command=save_edited_building)
    save_btn.pack(side="left", padx=18)
    
    # Nút "Hủy"
    cancel_btn = tk.Button(button_frame, text="Hủy", font=("Arial", 13, "bold"), bg="#dc3545", fg="white", activebackground="#c82333", activeforeground="white", width=12, height=1, relief="raised", bd=2, command=cancel_edit_building)
    cancel_btn.pack(side="left", padx=18)
    
    # Lấy dữ liệu tòa nhà và điền vào form
    fetch_building_data()