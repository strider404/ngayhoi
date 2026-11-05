import os
import sqlite3
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Cổng đăng ký Ngày hội việc làm")

# Cấu hình CORSMiddleware: chỉ cho phép địa chỉ giao diện Vite
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUC_CHUA = 30

def get_db_connection():
    db_path = os.getenv("DB_PATH", "ngayhoi.db")
    return sqlite3.connect(db_path)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dang_ky (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ma_sv TEXT NOT NULL,
            ma_phien TEXT NOT NULL,
            UNIQUE(ma_sv, ma_phien)
        )
    """)
    conn.commit()
    conn.close()

# Khởi tạo bảng cơ sở dữ liệu khi khởi động
init_db()

class DangKyRequest(BaseModel):
    ma_sv: str
    ma_phien: str

@app.post("/api/dang-ky", status_code=status.HTTP_201_CREATED)
def dang_ky(data: DangKyRequest):
    ma_sv = data.ma_sv.strip()
    ma_phien = data.ma_phien.strip()

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Bước 1: Kiểm tra xem sinh viên đã đăng ký phiên này chưa
        cursor.execute(
            "SELECT 1 FROM dang_ky WHERE ma_sv = ? AND ma_phien = ?",
            (ma_sv, ma_phien)
        )
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="DA_DANG_KY"
            )


        # Bước 2: Gộp đếm và ghi vào một câu lệnh SQL duy nhất để tránh Race Condition
        cursor.execute(
            f"""
            INSERT INTO dang_ky (ma_sv, ma_phien)
            SELECT ?, ?
            WHERE (SELECT COUNT(*) FROM dang_ky WHERE ma_phien = ?) < {SUC_CHUA}
            """,
            (ma_sv, ma_phien, ma_phien)
        )

        if cursor.rowcount == 0:
            # Không có dòng nào được thêm -> phiên đã đủ 30 chỗ
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="HET_CHO"
            )

        conn.commit()
        return {"ok": True}
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="DA_DANG_KY"
        )
    finally:
        conn.close()

@app.get("/api/con-cho")
def lay_con_cho(ma_phien: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM dang_ky WHERE ma_phien = ?", (ma_phien.strip(),))
        da_dang_ky = cursor.fetchone()[0]
        con_cho = max(0, SUC_CHUA - da_dang_ky)
        return {"con_cho": con_cho}
    finally:
        conn.close()
