import requests
import json
import os
import shutil

BASE_URL = "http://localhost:8000/api/v1"
HEALTH_URL = "http://localhost:8000/api/health"

TEST_USER = {
    "username": "e2e_test_user_2",
    "email": "e2e_test_2@example.com",
    "password": "Password123!",
    "password_confirm": "Password123!",
    "first_name": "E2E",
    "last_name": "User"
}

def run_e2e_tests():
    print("========================================")
    print("DHATREE AI - END TO END FUNCTIONAL TEST")
    print("========================================\n")
    
    session = requests.Session()
    
    # 1. Health Check
    print("1. Checking Backend Health...")
    try:
        res = session.get(f"{HEALTH_URL}/liveness/")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        print("[PASS] Backend is ALIVE")
    except Exception as e:
        print(f"[FAIL] Backend health check failed: {e}")
        return

    # 2. Register & Login
    print("\n2. Testing Authentication...")
    try:
        # Register (might fail if already exists, that's okay)
        reg_res = session.post(f"{BASE_URL}/auth/register/", json=TEST_USER)
        if reg_res.status_code == 400:
            print("Registration Note:", reg_res.text)
        if reg_res.status_code in [201, 400]:
            # Now login
            login_res = session.post(f"{BASE_URL}/auth/login/", json={
                "identifier": TEST_USER["email"],
                "password": TEST_USER["password"]
            })
            assert login_res.status_code == 200, f"Login failed: {login_res.text}"
            token = login_res.json()["data"]["tokens"]["access"]
            session.headers.update({"Authorization": f"Bearer {token}"})
            print("[PASS] Authentication successful (Token received)")
        else:
            raise Exception(f"Registration unexpected status: {reg_res.text}")
    except Exception as e:
        print(f"[FAIL] Authentication test failed: {e}")
        return

    # 3. Create a Farm
    print("\n3. Testing Farm Management...")
    farm_id = None
    try:
        farm_data = {
            "farm_name": "E2E Test Farm 2",
            "area": 10.5,
            "soil_type": "loamy",
            "latitude": 20.296,
            "longitude": 85.824
        }
        res = session.post(f"{BASE_URL}/farms/", json=farm_data)
        assert res.status_code in [201, 200], f"Expected 201/200, got {res.status_code}: {res.text}"
        farm_id = res.json()["data"]["id"] if "id" in res.json()["data"] else res.json()["data"][0]["id"]
        print(f"[PASS] Farm created/fetched successfully (ID: {farm_id})")
    except Exception as e:
        print(f"[FAIL] Farm test failed: {e}")
        # Need a real UUID if failed, but we can't easily guess. Let's hope it works.

    # 4. Crop Recommendation
    print("\n4. Testing Crop Recommendation...")
    try:
        crop_payload = {
            "nitrogen": 90,
            "phosphorus": 42,
            "potassium": 43,
            "temperature": 20.8,
            "humidity": 82.0,
            "ph": 6.5,
            "rainfall": 202.9,
            "farm": farm_id
        }
        res = session.post(f"{BASE_URL}/crop-recommendation/predictions/", json=crop_payload)
        assert res.status_code in [200, 201], f"Expected 200/201, got {res.status_code}: {res.text}"
        print(f"[PASS] Crop recommendation successful: {res.json()['data']['recommended_crop']}")
    except Exception as e:
        print(f"[FAIL] Crop recommendation failed: {e}")

    # 5. Fertilizer Recommendation
    print("\n5. Testing Fertilizer Recommendation...")
    try:
        fert_payload = {
            "nitrogen": 37,
            "phosphorus": 0,
            "potassium": 0,
            "temperature": 26,
            "humidity": 52,
            "moisture": 38,
            "ph_level": 6.5,
            "rainfall": 202.9,
            "soil_type": "sandy",
            "crop_type": "maize",
            "farm": farm_id
        }
        res = session.post(f"{BASE_URL}/fertilizer-recommendation/predictions/", json=fert_payload)
        assert res.status_code in [200, 201], f"Expected 200/201, got {res.status_code}: {res.text}"
        print(f"[PASS] Fertilizer recommendation successful: {res.json()}")
    except Exception as e:
        print(f"[FAIL] Fertilizer recommendation failed: {e}")

    # 6. Disease Detection
    print("\n6. Testing Disease Detection...")
    try:
        img_path = "scratch_dummy_leaf.jpg"
        if not os.path.exists(img_path):
            raise Exception("Cannot find scratch_dummy_leaf.jpg for testing.")
        
        with open(img_path, "rb") as f:
            files = {"image": ("scratch_dummy_leaf.jpg", f, "image/jpeg")}
            data = {"farm": farm_id}
            res = session.post(f"{BASE_URL}/disease-detection/predictions/", files=files, data=data)
            assert res.status_code in [200, 201], f"Expected 200/201, got {res.status_code}: {res.text}"
            print(f"[PASS] Disease detection successful: {res.json()}")
    except Exception as e:
        print(f"[FAIL] Disease detection failed: {e}")

    # 7. AI Assistant
    print("\n7. Testing AI Assistant (Gemini)...")
    try:
        chat_payload = {"message": "How do I water my corn?"}
        res = session.post(f"{BASE_URL}/assistant/chat/", json=chat_payload)
        assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
        data = res.json().get('data', {})
        response_text = data.get('response', data.get('content', str(data)))
        print(f"[PASS] Assistant response successful: {response_text[:50]}...")
    except Exception as e:
        print(f"[FAIL] AI Assistant failed: {e}")

    print("\n========================================")
    print("ALL TESTS COMPLETED.")
    print("========================================")

if __name__ == "__main__":
    run_e2e_tests()
