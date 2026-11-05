import os
import sqlite3

# CSDL tạm cho test
TEST_DB = "test_con_cho.db"
os.environ["DB_PATH"] = TEST_DB

import pytest
from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

@pytest.fixture(autouse=True)
def clean_db():
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

def test_con_cho_khi_chua_co_ai():
    r = client.get("/api/con-cho?ma_phien=P01")
    assert r.status_code == 200
    assert r.json() == {"con_cho": 30}

def test_con_cho_khi_da_co_nguoi_dang_ky():
    client.post("/api/dang-ky", json={"ma_sv": "SV001", "ma_phien": "P01"})
    client.post("/api/dang-ky", json={"ma_sv": "SV002", "ma_phien": "P01"})
    
    r = client.get("/api/con-cho?ma_phien=P01")
    assert r.status_code == 200
    assert r.json() == {"con_cho": 28}

