import os
import sqlite3

# CSDL tạm cho test
TEST_DB = "test_ngayhoi.db"
os.environ["DB_PATH"] = TEST_DB

import pytest
from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

@pytest.fixture(autouse=True)
def so_trong():
    conn = main.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dang_ky (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ma_sv TEXT NOT NULL,
            ma_phien TEXT NOT NULL,
            UNIQUE(ma_sv, ma_phien)
        )
    """)
    cursor.execute("DELETE FROM dang_ky")
    conn.commit()
    conn.close()

def lap_day(ma_phien, n, bat_dau_tu=0):
    for i in range(bat_dau_tu, bat_dau_tu + n):
        r = client.post("/api/dang-ky", json={"ma_sv": f"SV{i:03d}", "ma_phien": ma_phien})
        assert r.status_code == 201

# Dòng 1: P01 trống -> SV001 đăng ký P01 -> 201
def test_p01_trong_dang_ky_thanh_cong():
    r = client.post("/api/dang-ky", json={"ma_sv": "SV001", "ma_phien": "P01"})
    assert r.status_code == 201
    assert r.json() == {"ok": True}

# Dòng 2: P01 có 29 -> SV mới đăng ký P01 -> 201
def test_nguoi_thu_30_dang_ky_thanh_cong():
    lap_day("P01", 29)
    r = client.post("/api/dang-ky", json={"ma_sv": "SV029", "ma_phien": "P01"})
    assert r.status_code == 201
    assert r.json() == {"ok": True}

# Dòng 3: P01 có 30 -> SV mới đăng ký P01 -> 409 HET_CHO
def test_nguoi_thu_31_bi_tu_choi():
    lap_day("P01", 30)
    r = client.post("/api/dang-ky", json={"ma_sv": "SV030", "ma_phien": "P01"})
    assert r.status_code == 409
    assert r.json()["detail"] == "HET_CHO"

# Dòng 4: P01 có 30, gồm SV000 -> SV000 đăng ký lại P01 -> 409 DA_DANG_KY
def test_dang_ky_lai_khi_da_day():
    lap_day("P01", 30)
    r = client.post("/api/dang-ky", json={"ma_sv": "SV000", "ma_phien": "P01"})
    assert r.status_code == 409
    assert r.json()["detail"] == "DA_DANG_KY"

# Dòng 5: P01 có 30 -> SV031 đăng ký P02 -> 201
def test_phien_khac_van_dang_ky_duoc():
    lap_day("P01", 30)
    r = client.post("/api/dang-ky", json={"ma_sv": "SV031", "ma_phien": "P02"})
    assert r.status_code == 201
    assert r.json() == {"ok": True}

