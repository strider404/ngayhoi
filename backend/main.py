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
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO dang_ky (ma_sv, ma_phien) VALUES (?, ?)",
            (data.ma_sv.strip(), data.ma_phien.strip())
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
