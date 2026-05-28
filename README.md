# PBL5 - FastAPI Backend Service

Dịch vụ backend (REST API) viết bằng **FastAPI** phục vụ cho hệ thống **Nhận diện gương mặt mở cửa phòng tự động** dành cho nhà trọ / chung cư cho thuê. Module này đóng vai trò là tầng phụ trợ (quản lý dữ liệu, lưu trữ, xác thực) cho module AI nhận diện gương mặt chạy độc lập.

---

## 1. Bối cảnh nghiệp vụ (Business Context)

Hệ thống tổng thể của dự án PBL5 giải quyết bài toán **mở cửa phòng cho người thuê nhà thông qua nhận diện gương mặt**, gồm 2 module chính:

1. **Module AI Nhận diện gương mặt** (nằm ở repo khác): chịu trách nhiệm chụp ảnh khuôn mặt từ camera, trích xuất vector đặc trưng (Feature Vector) và so sánh để xác định danh tính của người đang đứng trước cửa.
2. **Module FastAPI Backend** (repo này): cung cấp các API phụ trợ cho module AI cũng như cho ứng dụng quản lý (web/mobile) của chủ nhà, bao gồm:
   - Quản lý hồ sơ người thuê (CRUD user, ảnh khuôn mặt, vector đặc trưng).
   - Xác thực đăng nhập của chủ nhà / người thuê vào ứng dụng quản lý.
   - Lưu trữ **lịch sử quét mặt** mỗi khi có người đứng trước cửa (kèm ảnh chụp, thời điểm và kết quả xác thực).
   - Tiếp nhận **yêu cầu của người thuê** (chẳng hạn xin được nhận diện lại, cập nhật mẫu khuôn mặt mới).

Vai trò các bên trong nghiệp vụ:

| Đối tượng | Mô tả |
|-----------|------|
| **Chủ nhà (admin)** | Đăng nhập, tạo/sửa/xóa hồ sơ người thuê, gán phòng, xem lịch sử quét mặt, xử lý request từ người thuê. |
| **Người thuê (user)** | Đăng nhập, tự cập nhật thông tin cá nhân của mình, gửi yêu cầu lên chủ nhà. |
| **Module AI (camera)** | Gọi API để lấy danh sách user + vector đặc trưng để so khớp; ghi log lịch sử mỗi lần quét. |

Luồng tương tác điển hình giữa Camera/AI và Backend:

```
┌──────────────┐                   ┌────────────────┐                ┌────────────┐
│ Camera + AI  │                   │ FastAPI Backend│                │  MongoDB   │
└──────┬───────┘                   └────────┬───────┘                └─────┬──────┘
       │                                    │                              │
       │ 1. GET /user/  (lấy danh sách      │                              │
       │     user + FeatureVector)          │                              │
       │ ─────────────────────────────────▶ │ ────  find({})  ───────────▶ │
       │ ◀───── User[] (kèm vector) ─────── │ ◀──── cursor ─────────────── │
       │                                    │                              │
       │ 2. Quét mặt người đứng trước cửa,  │                              │
       │    so khớp với vector đã có        │                              │
       │                                    │                              │
       │ 3. POST /history/                  │                              │
       │   (timestamps, imageURi,           │                              │
       │    isVerify, userId|"UNKNOWN")     │                              │
       │ ─────────────────────────────────▶ │ ──── insert_one ──────────▶ │
       │                                    │                              │
       │ 4. (Tuỳ nghiệp vụ) Mở cửa nếu      │                              │
       │    isVerify hợp lệ                 │                              │
```

Song song, **chủ nhà** thao tác qua app quản lý:
1. `POST /user/` tạo hồ sơ người thuê mới.
2. `POST /user/save_image` upload nhiều ảnh khuôn mặt (base64) → Cloudinary trả URL → lưu vào trường `image`.
3. Module AI dùng các ảnh này để sinh `FeatureVector` rồi ghi ngược lại trường `FeatureVector` của user.

---

## 2. Các chức năng chính (Features)

### 2.1. Xác thực (Authentication)
- Đăng nhập bằng `username` / `password`.
- Mật khẩu được hash (SHA-256 / MD5) trước khi lưu vào DB; khi đăng nhập, hệ thống verify giữa plaintext và hash.
- Khi xác thực thành công, trả về toàn bộ thông tin user (đã loại bỏ `FeatureVector` để giảm payload).
- **Stateless — không có JWT / session**: backend không phát hành token, không lưu trạng thái đăng nhập. Mỗi lần cần xác minh, client phải gọi lại `/auth/login`. Các Pydantic model `Token` / `TokenData` có sẵn trong `models/user.py` đang dành chỗ cho việc mở rộng sau này nhưng **hiện chưa được dùng** ở bất kỳ endpoint nào.
- Khi sai `username` / `password`, response vẫn trả HTTP **200**, nhưng trong body có `code: 400` và `error: true` — client cần đọc field `code`/`error` thay vì chỉ dựa vào HTTP status.

### 2.2. Quản lý người dùng (User Management)
- Lấy danh sách toàn bộ user.
- Lấy chi tiết một user theo `_id`.
- Tạo mới user (chủ nhà tạo cho người thuê). Khi tạo, hai trường `image` và `FeatureVector` để rỗng — sẽ được nạp ở bước upload ảnh và bước trích xuất vector của module AI.
- Cập nhật thông tin user (full update — chủ nhà), giữ nguyên `image` và `FeatureVector`.
- Người thuê **tự cập nhật thông tin cá nhân** (`fullname`, `gender`, `address`, `mobile`, `identityNumber`) — không thay đổi `username`, `password`, `role`, `image`, `FeatureVector`.
- Xóa user theo `_id`.
- **Upload ảnh khuôn mặt**: client gửi danh sách ảnh dưới dạng **base64** (không kèm prefix data-URI; server tự ghép `data:image/jpeg;base64,` trước khi gọi Cloudinary). Server upload lên **Cloudinary** (folder riêng theo `pbl5/{user_id}`) và lưu các URL trả về vào trường `image` của user. Lưu ý: thao tác này **thay thế toàn bộ** danh sách ảnh hiện có chứ không cộng dồn — muốn giữ ảnh cũ, client phải gửi kèm chúng trong cùng request.

### 2.3. Lịch sử quét mặt (Scan History)
- Module AI / camera ghi nhận mỗi lần có người đứng trước cửa: lưu thời điểm, ảnh đã chụp, kết quả xác thực (đúng/sai/ai), và `userId` đã nhận diện được.
- Khi `userId = "UNKNOWN"` ⇒ là người lạ (không có trong hệ thống), hiển thị `fullname = "Người lạ"`, `room = "Chưa thuê phòng"`.
- Khi `userId` là `ObjectId` hợp lệ ⇒ join với collection `user` để hiển thị `fullname` và `room` (số phòng) của người đó.
- Có API lấy toàn bộ lịch sử (đã sort **tăng dần** theo `timestamps` — bản ghi cũ nhất ở đầu danh sách) và lấy lịch sử theo `userId` cụ thể.

### 2.4. Yêu cầu của người thuê (User Requests)
- Người thuê có thể gửi request lên cho chủ nhà (ví dụ: yêu cầu cập nhật lại mẫu khuôn mặt).
- Khi đọc danh sách request, server thực hiện join với collection `user` để bổ sung `fullname` và `room`, giúp giao diện hiển thị dễ đọc.

---

## 3. Kiến trúc & Công nghệ (Technical)

### 3.1. Stack
- **Ngôn ngữ**: Python 3
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) `0.78.0` + ASGI server **Uvicorn** `0.17.6`.
- **Cơ sở dữ liệu**: **MongoDB** (cluster), truy cập **bất đồng bộ** qua **Motor** `3.0.0` (async driver, dựa trên `pymongo` `4.1.1`).
- **Lưu trữ ảnh**: **Cloudinary** (`cloudinary==1.29.0`) — upload trực tiếp từ chuỗi base64.
- **Hashing**: `passlib` với scheme `sha256_crypt` (mặc định) và fallback `md5_crypt`.
- **Validation & serialization**: `pydantic` `1.9.0`.
- **TLS**: `certifi` cho TLS CA bundle khi kết nối tới MongoDB Atlas.

### 3.2. Cấu trúc thư mục

```
PBL5-API/
├── main.py                  # Entry point: khởi tạo app FastAPI, CORS, mount router
├── config.json              # Cluster URL của MongoDB + credential Cloudinary (KHÔNG commit secret)
├── requirements.txt
├── routes/
│   └── api.py               # Tổng hợp & include các router con
├── endpoints/               # Tầng controller (handler HTTP)
│   ├── auth.py              # /auth — login
│   ├── user.py              # /user — CRUD user + upload ảnh
│   ├── history.py           # /history — lịch sử quét mặt
│   └── userRequest.py       # /userRequest — yêu cầu của người thuê
├── database/                # Tầng repository (truy cập MongoDB)
│   ├── driver.py            # Singleton kết nối MongoDB (Motor)
│   ├── auth.py              # Hash & verify password, authenticate
│   ├── user.py              # CRUD user, upload Cloudinary
│   ├── history.py           # Đọc/ghi lịch sử, aggregate join user
│   └── userRequest.py       # Đọc/ghi user request
├── models/                  # Pydantic schemas
│   ├── user.py              # User, UserUpsert, UserInfor, UserImage, UserLogin, Token
│   ├── history.py           # History, HistoryUpsert
│   ├── userRequest.py       # UserRequest, UserRequestUpsert
│   ├── PyObjectId.py        # Custom ObjectId validator cho Pydantic
│   └── ResponseModel.py     # Hàm tạo response chuẩn hóa
├── testCreateUser.py        # Script test tạo user
└── testSaveImage.py         # Script test upload ảnh base64
```

### 3.3. Mô hình dữ liệu (MongoDB collections)

Database name: **`pbl5`**

#### Collection `user`
| Trường           | Kiểu           | Mô tả |
|------------------|----------------|------|
| `_id`            | ObjectId       | Khóa chính |
| `username`       | string         | Tên đăng nhập (unique theo nghiệp vụ) |
| `password`       | string         | Hash của mật khẩu |
| `fullname`       | string         | Họ tên |
| `gender`         | string         | Giới tính |
| `address`        | string         | Địa chỉ thường trú |
| `mobile`         | string         | Số điện thoại |
| `identityNumber` | string         | Số CMND/CCCD |
| `floor`          | int            | Tầng |
| `room`           | string         | Phòng |
| `role`           | string         | `admin` (chủ nhà) hoặc `user` (người thuê) |
| `image`          | List[string]   | Danh sách URL ảnh khuôn mặt trên Cloudinary |
| `FeatureVector`  | List[List]     | Danh sách vector đặc trưng do module AI sinh ra |

#### Collection `history`
| Trường       | Kiểu     | Mô tả |
|--------------|----------|------|
| `_id`        | ObjectId | Khóa chính |
| `timestamps` | string   | Thời điểm xảy ra sự kiện quét mặt |
| `imageURi`   | string   | URI ảnh được camera chụp lại |
| `isVerify`   | string   | Kết quả xác thực (đúng / sai / unknown) |
| `userId`     | string   | `ObjectId` của user nhận diện được, hoặc `"UNKNOWN"` nếu là người lạ |

#### Collection `userRequest`
| Trường       | Kiểu     | Mô tả |
|--------------|----------|------|
| `_id`        | ObjectId | Khóa chính |
| `userId`     | string   | `ObjectId` của user gửi request |
| `timestamps` | string   | Thời điểm gửi request |

### 3.4. Response chuẩn hóa

Mọi endpoint đều trả về đối tượng có dạng:

```json
{
  "data":    <payload>,
  "code":    200,
  "message": "Mô tả kết quả",
  "error":   false
}
```

---

## 4. API Endpoints

Base URL mặc định: `http://127.0.0.1:8000`

### 4.1. Auth — `/auth`
| Method | Path     | Mô tả                                | Body                                 |
|--------|----------|--------------------------------------|--------------------------------------|
| POST   | `/login` | Đăng nhập, trả về thông tin user     | `{ "username": "...", "password": "..." }` |

### 4.2. User — `/user`
| Method | Path           | Mô tả                                                            | Tham số / Body |
|--------|----------------|------------------------------------------------------------------|----------------|
| GET    | `/`            | Lấy danh sách tất cả user                                        | —              |
| GET    | `/{id}`        | Lấy chi tiết một user theo `_id`                                 | path `id`      |
| POST   | `/`            | Tạo mới user (ảnh và vector để rỗng)                             | `UserUpsert`   |
| POST   | `/save_image`  | Upload danh sách ảnh (base64) lên Cloudinary, lưu URL vào user   | `UserImage`    |
| PUT    | `/`            | Chủ nhà cập nhật thông tin một user (giữ nguyên ảnh & vector)    | query `id` + `UserUpsert` |
| DELETE | `/`            | Xóa user theo `_id`                                              | query `id`     |
| PUT    | `/user-infor`  | Người thuê tự cập nhật profile của mình                          | query `id` + `UserInfor` |

### 4.3. History — `/history`
| Method | Path     | Mô tả                                                                   | Body            |
|--------|----------|-------------------------------------------------------------------------|-----------------|
| GET    | `/`      | Lấy toàn bộ lịch sử quét mặt (join `user` để bổ sung `fullname`, `room`) | —               |
| GET    | `/{id}`  | Lấy lịch sử theo `userId`                                               | path `id`       |
| POST   | `/`      | Ghi một bản ghi lịch sử mới (do module AI gọi mỗi lần camera quét)      | `HistoryUpsert` |

### 4.4. UserRequest — `/userRequest`
| Method | Path | Mô tả                                                                   | Body                |
|--------|------|-------------------------------------------------------------------------|---------------------|
| GET    | `/`  | Lấy danh sách request (đã join với `user` để có `fullname`, `room`)     | —                   |
| POST   | `/`  | Tạo mới một request từ người thuê                                       | `UserRequestUpsert` |

---

## 5. Cài đặt & Chạy

### 5.1. Yêu cầu
- Python 3.8+
- Một MongoDB cluster (khuyến nghị MongoDB Atlas) — cần URI dạng `mongodb+srv://...`
- Một tài khoản **Cloudinary** (có `cloud_name`, `api_key`, `api_secret`)

### 5.2. Cấu hình
Điền giá trị thực vào file `config.json` ở thư mục gốc:

```json
{
    "cluster":     "mongodb+srv://<user>:<pass>@<host>/?retryWrites=true&w=majority",
    "cloud_name":  "<your-cloudinary-cloud-name>",
    "api_key":     "<your-cloudinary-api-key>",
    "api_secret":  "<your-cloudinary-api-secret>"
}
```

> ⚠️ Lưu ý: `config.json` chứa thông tin nhạy cảm. Trên môi trường production nên dùng biến môi trường hoặc secret manager và thêm `config.json` vào `.gitignore`.

### 5.3. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 5.4. Khởi động server

```bash
# Bắt buộc chạy từ thư mục gốc của project (cùng cấp với config.json)
python main.py
# hoặc
python3 main.py
```

> ⚠️ `config.json` được load bằng **đường dẫn tương đối** (`./config.json`) ở `database/driver.py` và `endpoints/user.py`. Vì vậy phải start server từ thư mục gốc của project, nếu không quá trình import module sẽ ném `FileNotFoundError`.

Mặc định server chạy ở `http://127.0.0.1:8000` với chế độ `reload=True` (hot reload trong môi trường dev). Truy cập tài liệu Swagger tự động sinh tại:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc:      `http://127.0.0.1:8000/redoc`

### 5.5. Test nhanh
Có sẵn 2 script ví dụ để kiểm thử:
- `testCreateUser.py` — gọi `POST /user` để tạo một user mẫu.
- `testSaveImage.py` — đọc nhiều file ảnh từ thư mục local, encode base64 và gọi `POST /user/save_image` để upload lên Cloudinary.

---

## 6. Ghi chú thiết kế

- **Bất đồng bộ toàn diện**: tất cả các handler dùng `async def` và truy cập MongoDB qua Motor, phù hợp với mô hình I/O-bound (đọc/ghi DB, upload Cloudinary).
- **Connection pooling**: lớp `Database` (`database/driver.py`) cache client kết nối ở lần gọi đầu, các lần sau dùng lại.
- **Tách lớp rõ ràng**: `endpoints/` (HTTP layer) → `database/` (repository layer) → `models/` (schema). Giúp dễ test và dễ mở rộng.
- **CORS mở (`*`)**: phù hợp giai đoạn phát triển; production nên giới hạn domain cụ thể. Lưu ý cấu hình hiện tại có `allow_origins=["*"]` cùng với `allow_credentials=True` — kết hợp này bị trình duyệt từ chối theo CORS spec; nếu cần gửi credential, phải thay `"*"` bằng danh sách domain cụ thể.
- **Bảo mật mật khẩu**: passlib với `sha256_crypt` (kèm `md5_crypt` để verify legacy nếu có). Nên cân nhắc nâng cấp lên `bcrypt`/`argon2` cho hệ thống thực tế.
- **FeatureVector**: được sinh từ module AI riêng và ghi thẳng vào trường `FeatureVector` của user; backend này không tính toán vector.

## 7. Hạn chế hiện tại & Hướng cải tiến

- **Chưa có cơ chế token / phân quyền**: bất kỳ ai biết URL đều có thể gọi các endpoint CRUD user, đọc lịch sử, xóa user. Nên bổ sung middleware xác thực (JWT bearer) và phân quyền theo `role` (`admin` vs `user`).
- **Không có rate-limit / audit log** cho các endpoint nhạy cảm (login, delete user).
- **`timestamps` lưu dạng `string`** thay vì `datetime`: thuận tiện khi truyền JSON nhưng khó cho các thao tác filter theo khoảng thời gian / sort native trên MongoDB. Nên đổi sang `datetime` (BSON `Date`).
- **`userRequest` chưa xử lý case `userId` không tồn tại / `UNKNOWN`**: pipeline aggregate giả định luôn join được với collection `user`; nếu user đã bị xóa, request đọc sẽ lỗi.
- **`config.json` được load tại import-time** bằng đường dẫn tương đối — không phù hợp khi đóng gói/container hóa. Nên chuyển sang biến môi trường (Pydantic `BaseSettings` / `python-dotenv`).
- **Bí mật (`config.json`) hiện không nằm trong `.gitignore`** — cần thêm vào hoặc tách secret ra biến môi trường.
- **`update_user` yêu cầu gửi lại password mỗi lần**, password sẽ bị hash lại — client cần lưu ý không vô tình gửi password rỗng/cũ sai cách.
- **Một vài message trả về bị sao chép nhầm** (ví dụ `DELETE /user` trả về "Product deleted successfully.", `GET /history/{id}` trả về "UserRequest retrieved successfully.") — chỉ là cosmetic, nhưng nên dọn lại cho nhất quán.
