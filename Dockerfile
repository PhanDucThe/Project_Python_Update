# Sử dụng Python 3.11 làm base imageFROM python:3.11-slim
# Thiết lập thư mục làm việc
WORKDIR /app
# Cài đặt các dependencies cho GUIRUN apt-get update && apt-get install -y \
    python3-tk \    python3-pil.imagetk \
    && rm -rf /var/lib/apt/lists/*
# Sao chép requirements.txt (nếu có)COPY requirements.txt* ./
# Cài đặt các thư viện Python cần thiết
RUN pip install --no-cache-dir -r requirements.txt || \    pip install --no-cache-dir requests pillow
# Sao chép toàn bộ mã nguồn vào container
COPY . .
# Thiết lập biến môi trường cho displayENV DISPLAY=host.docker.internal:0.0

# Lệnh mặc định khi chạy container












FROM baseImage
