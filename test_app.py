"""
Automated Test Suite for Crop Yield Prediction Web Application
Verifies ML pipeline inference, database operations, agronomy advisory, and HTTP routes.
"""

import json
import sys
import unittest

# Reconfigure console output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import app as flask_app
import database
from ml.agronomy_engine import analyze_crop_prediction


class TestCropYieldApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        database.init_db()
        cls.client = flask_app.app.test_client()

    def test_database_operations(self):
        """Test database insertion, retrieval, and stats calculation."""
        initial_history = database.get_history()
        self.assertGreater(len(initial_history), 0, "Database should have seeded records")

        # Test insert
        record_id = database.save_prediction({
            "farmer_name": "Test Farmer",
            "state": "Punjab",
            "crop": "Wheat",
            "season": "Rabi",
            "soil_type": "Alluvial",
            "area_ha": 2.0,
            "rainfall_mm": 500.0,
            "temp_c": 20.0,
            "fertilizer_kg": 120.0,
            "pesticide_kg": 1.5,
            "predicted_yield_t_ha": 3.45,
            "total_production_tonnes": 6.9,
            "yield_status": "Optimal / High Yield",
            "notes": "Automated test record"
        })
        self.assertIsNotNone(record_id)

        # Verify retrieval
        updated_history = database.get_history(search_query="Test Farmer")
        self.assertGreater(len(updated_history), 0)
        self.assertEqual(updated_history[0]["farmer_name"], "Test Farmer")

        # Test stats
        stats = database.get_stats()
        self.assertIn("total_predictions", stats)
        self.assertIn("crop_stats", stats)
        self.assertGreater(stats["total_predictions"], 0)

        # Cleanup test record
        database.delete_prediction(record_id)

    def test_agronomy_engine(self):
        """Test agronomic logic and advisory generation."""
        analysis = analyze_crop_prediction(
            crop="Rice",
            season="Kharif",
            soil="Clayey",
            rainfall=1500.0,
            temp=28.0,
            fertilizer=140.0,
            predicted_yield=3.8,
            area=3.0
        )
        self.assertEqual(analysis["crop"], "Rice")
        self.assertIn("predicted_yield_t_ha", analysis)
        self.assertIn("predicted_yield_q_acre", analysis)
        self.assertIn("total_production_tonnes", analysis)
        self.assertGreater(len(analysis["advisories"]), 0)
        self.assertGreater(len(analysis["expert_tips"]), 0)

    def test_page_routes(self):
        """Test public web pages and authenticated access."""
        public_pages = ["/", "/dashboard", "/about", "/contact", "/login", "/register", "/assistant", "/how-to-use"]
        for path in public_pages:
            res = self.client.get(path)
            self.assertEqual(res.status_code, 200, f"Public route {path} failed with {res.status_code}")

        # Test unauthenticated access to /predict redirects to /login
        unauth_predict = self.client.get("/predict")
        self.assertEqual(unauth_predict.status_code, 302, "Unauthenticated /predict should redirect")
        self.assertIn("/login", unauth_predict.headers.get("Location", ""))

        # Test authenticated access to /predict
        with self.client.session_transaction() as sess:
            sess["user_id"] = 1
            sess["user_name"] = "Balaji"
        auth_predict = self.client.get("/predict")
        self.assertEqual(auth_predict.status_code, 200, "Authenticated /predict should return 200")

    def test_api_predict_and_export(self):
        """Test /api/predict inference endpoint and CSV export."""
        payload = {
            "farmer_name": "Balaji Test",
            "state": "Punjab",
            "crop": "Wheat",
            "season": "Rabi",
            "soil_type": "Alluvial",
            "area_ha": 2.5,
            "rainfall_mm": 520,
            "temp_c": 19.5,
            "fertilizer_kg": 130,
            "pesticide_kg": 1.4,
            "notes": "Test field simulation"
        }
        res = self.client.post("/api/predict", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get("success"))
        self.assertIn("predicted_yield_t_ha", data)
        self.assertGreater(data["predicted_yield_t_ha"], 0)
        self.assertIn("analysis", data)

        # Test CSV export
        csv_res = self.client.get("/api/export-csv")
        self.assertEqual(csv_res.status_code, 200)
        self.assertIn("text/csv", csv_res.content_type)
        csv_text = csv_res.data.decode("utf-8")
        self.assertIn("predicted_yield_t_ha", csv_text)

    def test_case_1_normal_values(self):
        """Test 1: Enter normal values (Rainfall = 800, Temperature = 27). Does prediction appear?"""
        payload = {
            "rainfall": 800,
            "temperature": 27,
            "area": 2.5,
            "crop": "Rice"
        }
        res = self.client.post("/predict", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get("success"))
        self.assertIn("prediction", data)
        self.assertGreater(data["prediction"], 0)
        print(f"\n   [Test 1 Passed] Normal values (Rainfall 800mm, Temp 27°C) -> Predicted Yield: {data['prediction']} tonnes/ha")

    def test_case_2_empty_values(self):
        """Test 2: Enter empty values. Does the website show: 'Please enter all required information.'?"""
        payload = {
            "rainfall": "",
            "temperature": "",
            "area": ""
        }
        res = self.client.post("/predict", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertFalse(data.get("success"))
        self.assertEqual(data.get("error"), "Please enter all required information.")
        print("\n   [Test 2 Passed] Empty values rejected with: 'Please enter all required information.'")

    def test_case_3_invalid_negative_values(self):
        """Test 3: Enter invalid values (Rainfall = -500). Does the website reject it?"""
        payload = {
            "rainfall": -500,
            "temperature": 28,
            "area": 2.5
        }
        res = self.client.post("/predict", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertFalse(data.get("success"))
        self.assertIn("Rainfall cannot be negative", data.get("error"))
        print(f"\n   [Test 3 Passed] Invalid values rejected with: '{data.get('error')}'")

    def test_case_4_frontend_backend_api_connection(self):
        """Test 4: Verify Frontend <-> Backend API connection endpoint (POST /predict)."""
        payload = {
            "rainfall": 850,
            "temperature": 28,
            "area": 2.5
        }
        res = self.client.post("/predict", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get("success"))
        self.assertIn("prediction", data)
        self.assertEqual(data.get("unit"), "tonnes/hectare")
        print(f"\n   [Test 4 Passed] POST /predict returned prediction: {data['prediction']} {data['unit']}")

    def test_user_registration_and_login(self):
        """Test user registration, login verification, and logout."""
        email = "testfarmer@agriculture.gov.in"
        password = "securefarmerpassword123"

        # 1. Register new user
        reg_res = self.client.post("/register", data={
            "name": "Kisan Balaji",
            "email": email,
            "password": password,
            "confirm_password": password,
            "phone": "9876543210",
            "state": "Punjab",
            "farm_size": "3.5"
        }, follow_redirects=True)
        self.assertEqual(reg_res.status_code, 200)

        # Verify user in database
        user = database.get_user_by_email(email)
        self.assertIsNotNone(user)
        self.assertEqual(user["name"], "Kisan Balaji")
        print("\n   [Auth Test Passed] User registration successful.")

        # 2. Test logout
        logout_res = self.client.get("/logout", follow_redirects=True)
        self.assertEqual(logout_res.status_code, 200)

        # 3. Test login with correct password
        login_res = self.client.post("/login", data={
            "email": email,
            "password": password
        }, follow_redirects=True)
        self.assertEqual(login_res.status_code, 200)
        print("   [Auth Test Passed] User login verification successful.")

        # 4. Test login with incorrect password
        bad_login = self.client.post("/login", data={
            "email": email,
            "password": "wrongpassword"
        }, follow_redirects=True)
        self.assertIn(b"Invalid email or password", bad_login.data)
        print("   [Auth Test Passed] Invalid credentials correctly rejected.")

    def test_kisan_ai_chat(self):
        """Test Kisan AI Assistant NLP endpoint."""
        queries = [
            ("When to sow wheat in Punjab?", "Wheat"),
            ("Why are rice leaves turning yellow?", "Zinc"),
            ("How to control bollworm in cotton?", "Bollworm"),
            ("Government schemes for farmers", "PM-KISAN")
        ]

        for q, expected_term in queries:
            res = self.client.post("/api/chat", data=json.dumps({"message": q}), content_type="application/json")
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertTrue(data.get("success"))
            self.assertIn(expected_term.lower(), data["reply"].lower())
            self.assertGreater(len(data.get("suggestions", [])), 0)
            print(f"   [Kisan AI Test Passed] '{q}' -> Response matched term: {expected_term}")

    def test_all_states_and_new_crops_prediction(self):
        """Test yield inference across diverse Indian states and newly added crops."""
        test_cases = [
            ("Jammu and Kashmir", "Apple", "Rabi", "Sandy Loam", 2.0, 900, 16.0, 150, 2.5),
            ("Assam", "Tea", "Whole Year", "Laterite", 3.5, 2100, 24.0, 130, 2.0),
            ("Maharashtra", "Onion", "Rabi", "Black", 1.8, 550, 22.0, 140, 2.0),
            ("Tamil Nadu", "Banana", "Whole Year", "Clayey", 2.5, 1400, 29.0, 240, 2.5),
            ("Kerala", "Coconut", "Whole Year", "Laterite", 4.0, 2300, 28.0, 140, 1.8),
            ("Sikkim", "Cardamom", "Whole Year", "Laterite", 1.2, 2200, 20.0, 70, 1.2),
            ("Rajasthan", "Barley", "Rabi", "Sandy Loam", 3.0, 350, 18.0, 75, 1.0),
            ("West Bengal", "Jute", "Kharif", "Alluvial", 2.0, 1600, 30.0, 90, 1.8),
        ]

        for state, crop, season, soil, area, rain, temp, fert, pest in test_cases:
            payload = {
                "farmer_name": f"Farmer from {state}",
                "state": state,
                "crop": crop,
                "season": season,
                "soil_type": soil,
                "area_ha": area,
                "rainfall_mm": rain,
                "temp_c": temp,
                "fertilizer_kg": fert,
                "pesticide_kg": pest,
                "notes": f"Pan-India test case for {state} - {crop}"
            }
            res = self.client.post("/api/predict", data=json.dumps(payload), content_type="application/json")
            self.assertEqual(res.status_code, 200, f"Failed prediction for {crop} in {state}")
            data = res.get_json()
            self.assertTrue(data.get("success"))
            self.assertGreater(data["predicted_yield_t_ha"], 0)
            print(f"   [State/Crop Test Passed] {state} • {crop} -> {data['predicted_yield_t_ha']} t/ha")


if __name__ == "__main__":
    print("🌾 Running Crop Yield Application Test Suite (Including Auth & Kisan AI)...")
    unittest.main()
