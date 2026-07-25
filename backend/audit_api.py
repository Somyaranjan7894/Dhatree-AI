import json
import uuid

import requests

BASE_URL = "http://localhost:8000/api/v1"
TEST_USER = f"test_{uuid.uuid4().hex[:6]}@example.com"
TEST_PASS = "TestPassword123!"

session = requests.Session()


def print_result(name, res):
    if res.status_code in [200, 201]:
        print(f"[OK] {name} passed (HTTP {res.status_code})")
    else:
        print(f"[FAIL] {name} failed (HTTP {res.status_code})")
        print(res.text)


def run_audit():
    print("--- API Audit ---")

    # 1. Register User
    res = session.post(
        f"{BASE_URL}/auth/register/",
        json={
            "email": TEST_USER,
            "username": TEST_USER.split("@")[0],
            "password": TEST_PASS,
            "password_confirm": TEST_PASS,
            "first_name": "Test",
            "last_name": "User",
        },
    )
    print_result("Register User", res)

    # 2. Login
    res = session.post(
        f"{BASE_URL}/auth/login/", json={"identifier": TEST_USER, "password": TEST_PASS}
    )
    print_result("Login User", res)
    if res.status_code != 200:
        print(res.text)
        return

    data = res.json()
    token = data.get("data", {}).get("tokens", {}).get("access") or data.get("access")
    print(f"Token extracted: {token[:10] if token else 'None'}...")
    session.headers.update({"Authorization": f"Bearer {token}"})

    # 3. Get Me
    res = session.get(f"{BASE_URL}/users/me/")
    print_result("Get Profile", res)

    # 4. Create Farm
    res = session.post(
        f"{BASE_URL}/farms/",
        json={
            "farm_name": "Audit Farm",
            "location": "Audit Location",
            "area": 10.5,
            "soil_type": "Loamy",
        },
    )
    print_result("Create Farm", res)
    farm_id = res.json().get("data", {}).get("id") if res.status_code == 201 else None

    # 4b. Register Crop
    if farm_id:
        crops_res = session.get(f"{BASE_URL}/crops/")
        items = crops_res.json().get("data", {}).get("items", [])
        if crops_res.status_code == 200 and len(items) > 0:
            crop_id = items[0]["id"]
            res = session.post(
                f"{BASE_URL}/farms/{farm_id}/crops/",
                json={
                    "farm": farm_id,
                    "crop": crop_id,
                    "sowing_date": "2026-07-20",
                    "expected_harvest_date": "2026-11-20",
                    "area_allocated": 5.0,
                },
            )
            print_result("Register Crop", res)
        else:
            print("[SKIP] Register Crop (No crops available in master DB)")
    else:
        print("[SKIP] Register Crop (Farm creation failed)")

    # 5. Dashboard
    res = session.get(f"{BASE_URL}/dashboard/overview/")
    print_result("Dashboard Overview", res)

    # 6. AI Assistant Test (Simple greeting)
    res = session.post(
        f"{BASE_URL}/assistant/chat/",
        json={"message": "Hello, this is a test.", "context": {}},
    )
    print_result("AI Assistant Chat", res)


if __name__ == "__main__":
    run_audit()
