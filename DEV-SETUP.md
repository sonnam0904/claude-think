# Development Setup Guide - Localhost Dify Testing

## 🚀 Quick Start

### Option 1: Using Helper Script (Recommended)

```bash
./run-dev.sh
```

Script sẽ tự động:
- Tạo virtual environment nếu chưa có
- Cài đặt dependencies
- Kiểm tra configuration
- Chạy plugin

### Option 2: Manual Setup

#### 1. Setup Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Configure Environment

Tạo file `.env`:

```bash
INSTALL_METHOD=remote
REMOTE_INSTALL_URL=localhost:5003
REMOTE_INSTALL_KEY=your-debug-key-here
```

**Lấy Debug Key từ localhost Dify:**

1. Mở trình duyệt và truy cập: `http://localhost/plugins` (hoặc URL của localhost Dify)
2. Vào phần **Plugin Management**
3. Tìm **Remote Debug Key** hoặc **Development Key**
4. Copy key và paste vào `.env` file

**Lưu ý:** 
- Nếu Dify chạy trên port khác, thay đổi `REMOTE_INSTALL_URL`
- Format thường là: `localhost:PORT` hoặc `127.0.0.1:PORT`

#### 4. Run Plugin

```bash
python -m main
```

## 📋 Configuration

### .env File Structure

```bash
# Required for remote debugging
INSTALL_METHOD=remote
REMOTE_INSTALL_URL=localhost:5003
REMOTE_INSTALL_KEY=your-actual-debug-key

# Optional: Plugin configuration
THINK_MAX_THOUGHTS=100
THINK_LOG_LEVEL=INFO
THINK_LOG_THOUGHTS=false
THINK_CLEANUP_HOURS=24
```

### Common Localhost Dify URLs

- **Default**: `localhost:5003`
- **Custom port**: `localhost:YOUR_PORT`
- **With protocol**: `http://localhost:5003` (usually not needed)

## 🔍 Verification

### Check Plugin is Running

Khi plugin chạy thành công, bạn sẽ thấy:

```
INFO - Initializing Claude Think Tool plugin...
INFO - Claude Think Tool plugin started successfully
INFO - Waiting for tool invocations...
```

### Check in Dify

1. Mở Dify Plugin Management page
2. Plugin "Claude Think Tool" sẽ xuất hiện trong danh sách
3. Status sẽ hiển thị "Connected" hoặc "Active"

### Test in Node Agent

1. Tạo hoặc mở một Node Agent workflow
2. Vào phần Tools
3. Tìm "think" tool trong danh sách
4. Tool sẽ có description: "Use this tool to think about something..."

## 🐛 Troubleshooting

### Issue: "Could not connect to Dify"

**Solutions:**
- Kiểm tra Dify đang chạy: `curl http://localhost:5003/health` (hoặc port tương ứng)
- Kiểm tra `REMOTE_INSTALL_URL` trong `.env` đúng chưa
- Kiểm tra firewall không block port
- Thử với `127.0.0.1` thay vì `localhost`

### Issue: "Invalid debug key"

**Solutions:**
- Lấy lại debug key từ Dify Plugin Management
- Đảm bảo không có spaces trong key
- Kiểm tra key chưa expired

### Issue: "Module not found: dify_plugin"

**Solutions:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Python version too old"

**Solutions:**
- Plugin yêu cầu Python 3.12+, nhưng có thể chạy với 3.10+
- Nếu có lỗi, cài Python 3.12:
  ```bash
  # Ubuntu/Debian
  sudo apt install python3.12 python3.12-venv
  
  # macOS
  brew install python@3.12
  ```

### Issue: Plugin không xuất hiện trong Dify

**Solutions:**
- Kiểm tra logs của plugin có lỗi không
- Restart plugin
- Kiểm tra `plugin.yaml` có đúng format không
- Kiểm tra Dify version tương thích

## 📝 Testing Workflow

### 1. Start Plugin

```bash
./run-dev.sh
# hoặc
python -m main
```

### 2. Verify in Dify

- Plugin xuất hiện trong Plugin Management
- Status: Connected

### 3. Create Test Workflow

1. Tạo Node Agent trong Dify
2. Add "think" tool vào workflow
3. Test với simple thought:
   ```
   think(thought="This is a test thought")
   ```

### 4. Test Multi-Step

```
think(thought="Step 1: Analyze request")
think(thought="Step 2: Check requirements")
think(thought="Step 3: Plan action")
```

### 5. Check Logs

Plugin logs sẽ hiển thị:
- Tool invocations
- Context updates
- Errors (nếu có)

## 🔧 Development Tips

### Enable Debug Logging

Trong `.env`:
```bash
THINK_LOG_LEVEL=DEBUG
THINK_LOG_THOUGHTS=true  # Log thought content for debugging
```

### Monitor Context

Plugin logs sẽ hiển thị:
- Session IDs
- Step numbers
- Context sizes
- Cleanup operations

### Hot Reload

Plugin không support hot reload. Để test changes:
1. Stop plugin (Ctrl+C)
2. Make code changes
3. Restart plugin

## 📚 Next Steps

- Xem [USER-GUIDE.md](./USER-GUIDE.md) để biết cách sử dụng tool
- Xem [EXAMPLES.md](./EXAMPLES.md) cho usage examples
- Xem [API-DOCS.md](./API-DOCS.md) cho API reference

---

**Last Updated**: [Current Date]

