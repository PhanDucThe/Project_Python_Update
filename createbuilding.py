import tkinter as tk
from tkinter import ttk, messagebox
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
    add_building_frame = tk.Frame(admin, width=950, height=700, bg="#f8f9fa")
    add_building_frame.pack(side="right", fill="both", expand=True)

    # Tiêu đề lớn, căn giữa
    tk.Label(add_building_frame, text="Thêm Mới Tòa Nhà", font=("Arial", 26, "bold"), fg="#2c3e50", bg="#f8f9fa").pack(pady=(18, 8))

    # Tạo LabelFrame chứa form
    form_labelframe = tk.LabelFrame(add_building_frame, text="Thông tin tòa nhà", font=("Arial", 14, "bold"), bg="#f8f9fa", fg="#007bff", bd=2, relief="groove", padx=18, pady=18)
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
    district_combobox = ttk.Combobox(scrollable_frame, values=district_labels, state="readonly", width=36, font=("Arial", 12))
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

    # Nút chức năng
    button_frame = tk.Frame(add_building_frame, bg="#f8f9fa")
    button_frame.pack(pady=18)
    def save_new_building():
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
        building_data["type"] = ["NGUYEN_CAN"]
        required_fields = ["name", "district", "ward", "street", "managerName", "managerPhone"]
        for field in required_fields:
            if not building_data.get(field):
                field_label = "Quận" if field == "district" else fields.get(field, field)
                messagebox.showwarning("Cảnh báo", f"Vui lòng nhập {field_label}!")
                return
        try:
            building_data["numberOfBasement"] = int(building_data.get("numberOfBasement", 0) or 0)
            building_data["floorArea"] = float(building_data.get("floorArea", 0) or 0)
            building_data["rentPrice"] = float(building_data.get("rentPrice", 0) or 0)
            building_data["brokerageFee"] = 0
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
            "note": ""
        }
        for field, default_value in additional_fields.items():
            if field not in building_data:
                building_data[field] = default_value
        data_file = os.path.join(BASE_DIR, "data.json")
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []
        max_id = max([b.get("id", 0) for b in data], default=0)
        building_data["id"] = max_id + 1
        data.append(building_data)
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Thành công", "Thêm mới tòa nhà thành công!")
        add_building_frame.destroy()
        content_frame.pack(side="right", fill="both", expand=True)
        refresh_building_list(content_frame)
    def cancel_add_building():
        add_building_frame.destroy()
        content_frame.pack(side="right", fill="both", expand=True)
    add_btn = tk.Button(button_frame, text="Thêm Mới", font=("Arial", 13, "bold"), bg="#28a745", fg="white", activebackground="#218838", activeforeground="white", width=12, height=1, relief="raised", bd=2, command=save_new_building)
    add_btn.pack(side="left", padx=18)
    cancel_btn = tk.Button(button_frame, text="Hủy", font=("Arial", 13, "bold"), bg="#dc3545", fg="white", activebackground="#c82333", activeforeground="white", width=12, height=1, relief="raised", bd=2, command=cancel_add_building)
    cancel_btn.pack(side="left", padx=18)

# Hàm cập nhật danh sách tòa nhà (chỉ đọc file data.json)
def refresh_building_list(content_frame, token=None):
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
        
        # Đọc dữ liệu từ file data.json
        data_file = os.path.join(BASE_DIR, "data.json")
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []
        
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
    
    except Exception as e:
        print(f"Lỗi khi cập nhật danh sách tòa nhà: {str(e)}")

# Hàm sửa tòa nhà
def edit_building(building_id, new_data):
    data_file = os.path.join(BASE_DIR, "data.json")
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = []
    for b in data:
        if str(b.get("id")) == str(building_id):
            b.update(new_data)
            break
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Hàm xoá tòa nhà
def delete_building(building_id):
    data_file = os.path.join(BASE_DIR, "data.json")
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = []
    data = [b for b in data if str(b.get("id")) != str(building_id)]
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)




