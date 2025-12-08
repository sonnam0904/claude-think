# Fix: Lỗi khi Import Plugin từ File

## ❌ Vấn đề

- ✅ **Remote debug**: Plugin hoạt động bình thường
- ❌ **Import từ file**: Lỗi `ImportError: LLMResultChunkWithStructuredOutput`

## 🔍 Nguyên nhân

Khi import từ file, Dify sẽ:
1. Giải nén package
2. Cài đặt dependencies từ `requirements.txt` trong package
3. Có thể dùng SDK version khác với version trong môi trường debug

## ✅ Giải pháp đã áp dụng

### 1. Pin Exact SDK Version

Đã cập nhật `requirements.txt`:

```diff
- dify-plugin>=0.0.1b44
+ dify-plugin==0.0.1b44
```

**Lý do**: Đảm bảo Dify cài đặt đúng version SDK đã test.

### 2. Thêm Minimum Dify Version

Đã thêm vào `manifest.yaml`:

```yaml
meta:
  minimum_dify_version: 1.7.1
```

**Lý do**: Đảm bảo plugin chỉ cài đặt trên Dify version tương thích.

## 🔄 Các bước Tiếp theo

1. **Rebuild package**:

```bash
cd /home/sonnn/Work/dify-plugin
dify plugin package ./claude-think
```

2. **Xóa plugin cũ trong Dify** (nếu đã cài)

3. **Import lại plugin từ file mới**

4. **Test lại**

## 📝 Lưu ý

- Luôn pin exact version của SDK trong production
- Test cả remote debug và import từ file
- Kiểm tra `minimum_dify_version` phù hợp với Dify instance

## 🔗 Xem thêm

- `requirements.txt` - Dependencies với exact versions
- `manifest.yaml` - Plugin metadata và version requirements

