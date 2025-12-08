# Hướng dẫn Tắt Plugin Verification trong Dify

## ⚠️ Lỗi gặp phải

```
PluginDaemonBadRequestError: plugin verification has been enabled, and the plugin you want to install has a bad signature
```

## 🔧 Giải pháp: Tắt Plugin Verification (Cho Local/Development)

### Bước 1: Tìm file cấu hình Dify

Nếu bạn đang chạy Dify bằng Docker:

```bash
# Tìm thư mục docker của Dify
cd /path/to/dify/docker
```

Hoặc nếu bạn có quyền truy cập vào thư mục cài đặt Dify:
- Thư mục thường là: `docker/` hoặc `dify/docker/`

### Bước 2: Sửa file `.env`

1. Mở file `.env` trong thư mục `docker/`:
   ```bash
   nano docker/.env
   # hoặc
   vi docker/.env
   ```

2. Thêm dòng sau vào cuối file:
   ```env
   FORCE_VERIFYING_SIGNATURE=false
   ```

3. Lưu file (nếu dùng nano: `Ctrl+X`, sau đó `Y`, rồi `Enter`)

### Bước 3: Khởi động lại Dify

```bash
cd docker
docker compose down
docker compose up -d
```

### Bước 4: Kiểm tra

Đợi vài giây để Dify khởi động lại, sau đó thử cài đặt plugin lại.

## 📝 Lưu ý Bảo mật

⚠️ **Quan trọng**: Tắt plugin verification cho phép cài đặt các plugin chưa được ký. Chỉ nên:
- Sử dụng trong môi trường **development/test**
- Hoặc khi bạn **tin tưởng hoàn toàn** nguồn plugin

## 🔐 Giải pháp Thay thế: Tạo Chữ ký cho Plugin (Cho Production)

Nếu bạn muốn giữ verification bật, bạn cần:
1. Tạo cặp khóa (private/public key)
2. Ký plugin bằng private key
3. Cấu hình Dify để chấp nhận public key

Xem thêm: [Third-Party Signature Verification](https://docs.dify.ai/plugin-dev-en/0312-third-party-signature-verification)

