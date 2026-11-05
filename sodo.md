# Sơ đồ kiến trúc luồng dữ liệu Cổng đăng ký Ngày hội việc làm

## 1. Sơ đồ tuần tự tương tác (Sequence Diagram)

```mermaid
sequenceDiagram
    autonumber
    actor U as Người dùng (Sinh viên)
    participant UI as Giao diện Frontend (React / Vite)<br/>http://localhost:5173
    participant API as Máy chủ Backend (FastAPI)<br/>http://localhost:8000
    participant DB as Cơ sở dữ liệu SQLite<br/>ngayhoi.db (Table: dang_ky)

    %% Trường hợp 1: Đăng ký lần đầu thành công
    rect rgb(235, 248, 235)
    Note over U,DB: TRƯỜNG HỢP 1: Đăng ký lần đầu (Thành công - 201)
    U->>UI: Nhập `ma_sv` ("22020001"), `ma_phien` ("P01") & bấm "Đăng ký"
    activate UI
    UI->>UI: Cập nhật state: "Đang gửi..." (Loading)
    UI->>API: POST /api/dang-ky<br/>Body: {"ma_sv": "22020001", "ma_phien": "P01"}
    activate API
    API->>API: Kiểm tra CORS (nguồn http://localhost:5173) & Pydantic Validate
    API->>DB: INSERT INTO dang_ky (ma_sv, ma_phien) VALUES ('22020001', 'P01')
    activate DB
    DB-->>API: Ghi thành công
    deactivate DB
    API-->>UI: HTTP Status 201 Created<br/>Body: {"ok": true}
    deactivate API
    UI->>U: Hiển thị thông báo: Thành công (201 Created)
    deactivate UI
    end

    %% Trường hợp 2: Đăng ký trùng lặp
    rect rgb(254, 243, 199)
    Note over U,DB: TRƯỜNG HỢP 2: Gửi trùng lặp cùng ma_sv & ma_phien (Trùng lặp - 409)
    U->>UI: Bấm đăng ký lại cùng `ma_sv` ("22020001"), `ma_phien` ("P01")
    activate UI
    UI->>UI: Cập nhật state: "Đang gửi..." (Loading)
    UI->>API: POST /api/dang-ky<br/>Body: {"ma_sv": "22020001", "ma_phien": "P01"}
    activate API
    API->>DB: INSERT INTO dang_ky (ma_sv, ma_phien) VALUES ('22020001', 'P01')
    activate DB
    DB-->>API: Lỗi vi phạm UNIQUE(ma_sv, ma_phien)<br/>sqlite3.IntegrityError
    deactivate DB
    API-->>UI: HTTP Status 409 Conflict<br/>Body: {"detail": "DA_DANG_KY"}
    deactivate API
    UI->>U: Hiển thị cảnh báo: Báo lỗi trùng (409 Conflict - DA_DANG_KY)
    deactivate UI
    end
```

---

## 2. Sơ đồ kiến trúc tổng thể (Architecture & Flow)

```mermaid
flowchart LR
    subgraph Client["Frontend: Vite + React (localhost:5173)"]
        UIForm["Form Nhập Liệu<br/>(ma_sv, ma_phien)"]
        UIState["Quản lý 3 trạng thái:<br/>1. Đang gửi (loading)<br/>2. Thành công (201)<br/>3. Báo trùng (409)"]
        UIForm --> UIState
    end

    subgraph Server["Backend: FastAPI (localhost:8000)"]
        CORS["CORSMiddleware<br/>allow_origins=['http://localhost:5173']"]
        Route["POST /api/dang-ky"]
        Model["Pydantic DangKyRequest<br/>(ma_sv: str, ma_phien: str)"]
        Logic["Xử lý Transaction & Bắt Ngoại Lệ"]
        
        CORS --> Route
        Route --> Model
        Model --> Logic
    end

    subgraph Database["Database: SQLite (ngayhoi.db)"]
        Table[("Table: dang_ky<br/>- id (PK)<br/>- ma_sv<br/>- ma_phien<br/>UNIQUE(ma_sv, ma_phien)")]
    end

    UIState -- "fetch(http://localhost:8000/api/dang-ky)" --> CORS
    Logic -- "Thành công: 201 Created" --> UIState
    Logic -- "Trùng lặp: 409 Conflict" --> UIState
    Logic <--> |INSERT / Check UNIQUE| Table
```

---

## 3. Chi tiết thiết kế các thành phần

| Thành phần | Công nghệ | Vai trò & Đặc tả kỹ thuật |
| :--- | :--- | :--- |
| **Giao diện (Frontend)** | Vite + React | - Chạy tại `http://localhost:5173`.<br/>- Có form nhập `ma_sv` và `ma_phien`.<br/>- Hiển thị trực quan 3 trạng thái: Đang gửi (Loading), Thành công (201 Created), Trùng lặp (409 Conflict). |
| **Máy chủ (Backend)** | FastAPI + Uvicorn | - Chạy tại `http://localhost:8000`.<br/>- Endpoint tiếp nhận: `POST /api/dang-ky`.<br/>- `CORSMiddleware` cấu hình chuẩn xác chỉ mở cho `["http://localhost:5173"]`.<br/>- Trả về mã 201 (`{"ok": true}`) hoặc 409 (`{"detail": "DA_DANG_KY"}`). |
| **Cơ sở dữ liệu (Database)** | SQLite (`ngayhoi.db`) | - Bảng `dang_ky` với ràng buộc `UNIQUE(ma_sv, ma_phien)` nhằm đảm bảo sinh viên không thể đăng ký trùng 1 phiên. |

