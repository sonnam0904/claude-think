# Hướng dẫn Tạo Chữ ký cho Dify Plugin

## 📋 Tổng quan

Dify CLI cung cấp các công cụ tích hợp để tạo chữ ký cho plugin. Quy trình bao gồm:
1. Tạo cặp khóa (private/public key)
2. Ký plugin package
3. Cấu hình Dify để chấp nhận public key

## 🔑 Bước 1: Tạo Cặp Khóa

### Sử dụng Dify CLI

```bash
# Tạo cặp khóa với tên tùy chỉnh
dify signature generate -f plugin_keys

# Hoặc để tên mặc định
dify signature generate
```

Lệnh này sẽ tạo 2 files:
- `plugin_keys_private.pem` - Private key (GIỮ BÍ MẬT!)
- `plugin_keys_public.pem` - Public key (có thể chia sẻ)

### Kiểm tra khóa đã tạo

```bash
ls -lh plugin_keys_*.pem

# Xem public key (có thể chia sẻ)
cat plugin_keys_public.pem
```

## 📦 Bước 2: Ký Plugin Package

### Trước khi ký

Đảm bảo bạn đã:
1. ✅ Đóng gói plugin: `dify plugin package ./claude-think`
2. ✅ File `.difypkg` đã được tạo

### Ký plugin

```bash
# Ký plugin với private key
dify signature sign ../claude-think.difypkg -p plugin_keys_private.pem

# Hoặc với authorized category (mặc định là "langgenius")
dify signature sign ../claude-think.difypkg \
  -p plugin_keys_private.pem \
  -c "your_category"
```

### Kiểm tra plugin đã được ký

```bash
# Xác minh chữ ký
dify signature verify ../claude-think.difypkg -p plugin_keys_public.pem
```

## 🔧 Bước 3: Cấu hình Dify để Chấp nhận Public Key

### Tùy chọn A: Cấu hình qua Environment Variables

Thêm vào file `.env` của Dify (thư mục `docker/`):

```env
# Plugin Signature Configuration
FORCE_VERIFYING_SIGNATURE=true
PLUGIN_VERIFICATION_PUBLIC_KEY_PATH=/path/to/plugin_keys_public.pem
```

Hoặc inline public key content:

```env
PLUGIN_VERIFICATION_PUBLIC_KEY_CONTENT="-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...
-----END PUBLIC KEY-----"
```

### Tùy chọn B: Cấu hình qua Docker Compose

Nếu Dify chạy bằng Docker, thêm vào `docker-compose.yml`:

```yaml
services:
  api:
    environment:
      - FORCE_VERIFYING_SIGNATURE=true
      - PLUGIN_VERIFICATION_PUBLIC_KEY_PATH=/app/keys/plugin_keys_public.pem
    volumes:
      - ./keys:/app/keys  # Mount thư mục chứa public key
```

### Tùy chọn C: Cấu hình trong Dify UI

1. Vào **Settings** → **Plugin Settings**
2. Tìm phần **Plugin Signature Verification**
3. Upload hoặc paste public key content

## ✅ Bước 4: Khởi động lại và Cài đặt

1. **Khởi động lại Dify**:
   ```bash
   cd docker
   docker compose down
   docker compose up -d
   ```

2. **Cài đặt plugin đã ký**:
   - Vào Plugin Management
   - Click "Install Plugin" → "Via Local File"
   - Upload file `claude-think.difypkg` đã được ký
   - Dify sẽ tự động kiểm tra chữ ký

## 📝 Quy trình Tự động hóa

Tạo script `package_and_sign.sh` để tự động hóa toàn bộ quy trình:

```bash
#!/bin/bash
set -e

PLUGIN_DIR="."
PRIVATE_KEY="plugin_keys_private.pem"
OUTPUT_DIR="../"

echo "📦 Đóng gói plugin..."
cd "$PLUGIN_DIR"
dify plugin package . --output "$OUTPUT_DIR/claude-think.difypkg"

echo "🔐 Ký plugin..."
cd "$OUTPUT_DIR"
dify signature sign claude-think.difypkg -p "$PRIVATE_KEY"

echo "✅ Xác minh chữ ký..."
dify signature verify claude-think.difypkg -p plugin_keys_public.pem

echo ""
echo "✅ Plugin đã được đóng gói và ký thành công!"
echo "📦 Package: claude-think.difypkg"
echo "🔐 Chữ ký đã được tích hợp vào package"
```

## 🔐 Bảo mật

### ⚠️ Quan trọng

1. **Private Key (`.pem` file chứa "private")**:
   - ⚠️ **KHÔNG BAO GIỜ** chia sẻ private key
   - ⚠️ **KHÔNG** commit private key vào Git
   - ✅ Thêm `*_private.pem` vào `.gitignore`
   - ✅ Lưu trữ ở nơi an toàn (keychain, vault, etc.)

2. **Public Key (`.pem` file chứa "public")**:
   - ✅ Có thể chia sẻ an toàn
   - ✅ Cần cung cấp cho Dify admin
   - ✅ Có thể commit vào repository (nếu muốn)

### Thêm vào .gitignore

```bash
# Plugin signing keys
*_private.pem
*.private
private_key*
```

## 🎯 Workflow Khuyến nghị

### Development/Testing

1. Tạo cặp khóa một lần cho development:
   ```bash
   dify signature generate -f dev_keys
   ```

2. Ký mỗi version mới:
   ```bash
   dify signature sign ../claude-think.difypkg -p dev_keys_private.pem
   ```

3. Cấu hình Dify với public key để test

### Production

1. Tạo cặp khóa production riêng
2. Giữ private key cực kỳ an toàn
3. Chia sẻ public key với Dify admin
4. Ký từng release với private key production

## 🔍 Troubleshooting

### Lỗi: "bad signature"

1. Kiểm tra private key đúng không:
   ```bash
   ls -lh plugin_keys_private.pem
   ```

2. Kiểm tra plugin đã được ký chưa:
   ```bash
   dify signature verify ../claude-think.difypkg -p plugin_keys_public.pem
   ```

3. Đảm bảo public key trong Dify khớp với private key đã dùng để ký

### Lỗi: "verification failed"

1. Kiểm tra đường dẫn public key trong Dify config
2. Đảm bảo format public key đúng (PEM format)
3. Khởi động lại Dify sau khi thay đổi config

## 📚 Tài liệu Tham khảo

- [Dify Plugin Signature Documentation](https://docs.dify.ai/plugin-dev-en/0312-third-party-signature-verification)
- Dify CLI: `dify signature --help`

## ✨ Ví dụ Hoàn chỉnh

```bash
# 1. Tạo cặp khóa
dify signature generate -f myplugin

# 2. Đóng gói plugin
cd claude-think
dify plugin package .

# 3. Ký plugin
cd ..
dify signature sign claude-think.difypkg -p myplugin_private.pem

# 4. Xác minh
dify signature verify claude-think.difypkg -p myplugin_public.pem

# 5. Cấu hình Dify với myplugin_public.pem
# 6. Cài đặt plugin trong Dify
```
