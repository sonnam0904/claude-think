# Quick Start - Chạy Plugin với Localhost Dify

## 🚀 Cách Nhanh Nhất

```bash
./run-dev.sh
```

Script sẽ tự động setup và chạy plugin.

## 📝 Các Bước Chi Tiết

### 1. Lấy Debug Key từ Localhost Dify

1. Mở trình duyệt: `http://localhost/plugins` (hoặc URL localhost Dify của bạn)
2. Vào **Plugin Management**
3. Tìm **Remote Debug Key** hoặc **Development Key**
4. Copy key

### 2. Cập nhật .env File

Mở file `.env` và cập nhật:

```bash
REMOTE_INSTALL_KEY=paste-your-actual-key-here
REMOTE_INSTALL_URL=localhost:5003  # Hoặc port của bạn
```

### 3. Chạy Plugin

```bash
# Option 1: Dùng script
./run-dev.sh

# Option 2: Manual
source venv/bin/activate
python -m main
```

## ✅ Kiểm Tra Plugin Đã Chạy

### Trong Terminal

Bạn sẽ thấy:
```
INFO - Initializing Claude Think Tool plugin...
INFO - Claude Think Tool plugin started successfully
INFO - Waiting for tool invocations...
```

### Trong Dify

1. Vào Plugin Management
2. Plugin "Claude Think Tool" sẽ xuất hiện
3. Status: **Connected** hoặc **Active**

## 🧪 Test Tool

1. Tạo Node Agent workflow
2. Thêm "think" tool
3. Test với:
   ```
   think(thought="This is a test thought")
   ```

## 🐛 Troubleshooting

### Plugin không kết nối được

- Kiểm tra Dify đang chạy: `curl http://localhost:5003/health`
- Kiểm tra debug key đúng chưa
- Kiểm tra port trong `.env` đúng chưa

### Import errors

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Xem logs chi tiết

Thêm vào `.env`:
```bash
THINK_LOG_LEVEL=DEBUG
```

---

Xem [DEV-SETUP.md](./DEV-SETUP.md) cho hướng dẫn chi tiết hơn.

