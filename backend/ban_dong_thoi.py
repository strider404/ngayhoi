import sys
import httpx
from concurrent.futures import ThreadPoolExecutor

if len(sys.argv) < 2:
    print("Sử dụng: python ban_dong_thoi.py <ma_phien>")
    sys.exit(1)

URL = "http://localhost:8000/api/dang-ky"
PHIEN = sys.argv[1]

def gui(i):
    r = httpx.post(URL, json={"ma_sv": f"TN{i:03d}", "ma_phien": PHIEN})
    return r.status_code

with ThreadPoolExecutor(max_workers=40) as ex:
    ma = list(ex.map(gui, range(40)))

print(f"{PHIEN} 201: {ma.count(201)} · 409: {ma.count(409)}")

