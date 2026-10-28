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

    def setUp(self):
        self.client = flask_app.app.test_client()

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

    def test_weather_integration(self):
        """Test Automated State & GPS Weather Integration endpoint."""
        # 1. Test by State & Season (Punjab Rabi)
        res = self.client.post("/api/weather", data=json.dumps({
            "state": "Punjab",
            "season": "Rabi"
        }), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get("success"))
        self.assertEqual(data.get("state"), "Punjab")
        self.assertIn("temperature_c", data)
        self.assertIn("rainfall_mm", data)
        self.assertGreater(data["temperature_c"], 0)
        self.assertGreater(data["rainfall_mm"], 0)
        print(f"\n   [Weather Test Passed] Punjab (Rabi) -> {data['temperature_c']}°C, {data['rainfall_mm']} mm rain")

        # 2. Test by State & Season (Maharashtra Kharif)
        res_mh = self.client.post("/api/weather", data=json.dumps({
            "state": "Maharashtra",
            "season": "Kharif"
        }), content_type="application/json")
        self.assertEqual(res_mh.status_code, 200)
        data_mh = res_mh.get_json()
        self.assertTrue(data_mh.get("success"))
        self.assertEqual(data_mh.get("state"), "Maharashtra")
        print(f"   [Weather Test Passed] Maharashtra (Kharif) -> {data_mh['temperature_c']}°C, {data_mh['rainfall_mm']} mm rain")

        # 3. Test by GPS Coordinates (Bengaluru lat 12.97, lon 77.59)
        res_gps = self.client.post("/api/weather", data=json.dumps({
            "lat": 12.97,
            "lon": 77.59
        }), content_type="application/json")
        self.assertEqual(res_gps.status_code, 200)
        data_gps = res_gps.get_json()
        self.assertTrue(data_gps.get("success"))
        self.assertEqual(data_gps.get("nearest_state"), "Karnataka")
        print(f"   [Weather Test Passed] GPS (12.97, 77.59) -> Nearest State: {data_gps['nearest_state']}")

    def test_admin_and_farmer_dashboards_and_permissions(self):
        """Test Admin Dashboard, Farmer Dashboard, and User Permission Management."""
        # 1. Test Admin Login with default seeded credentials
        login_res = self.client.post("/login", data={
            "email": "admin@cropyield.ai",
            "password": "admin123"
        }, follow_redirects=False)
        self.assertEqual(login_res.status_code, 302)
        self.assertIn("/admin/dashboard", login_res.headers.get("Location", ""))

        # 2. Test Admin Dashboard Access
        with self.client.session_transaction() as sess:
            sess["user_id"] = 1
            sess["user_name"] = "Master Administrator"
            sess["user_role"] = "admin"
            sess["user_status"] = "approved"

        admin_res = self.client.get("/admin/dashboard")
        self.assertEqual(admin_res.status_code, 200)
        self.assertIn(b"System Administration & Permissions", admin_res.data)
        print("\n   [Admin Test Passed] Admin login and dashboard access verified.")

        # 3. Test Farmer restricted from Admin Dashboard
        with self.client.session_transaction() as sess:
            sess["user_id"] = 2
            sess["user_name"] = "Test Farmer"
            sess["user_role"] = "farmer"
            sess["user_status"] = "approved"

        unauth_admin_res = self.client.get("/admin/dashboard")
        self.assertEqual(unauth_admin_res.status_code, 302)
        self.assertIn("/farmer/dashboard", unauth_admin_res.headers.get("Location", ""))
        print("   [RBAC Test Passed] Non-admin user correctly blocked from Admin Dashboard.")

        # 4. Create a test farmer user with 'pending' status to test Admin Permission Granting
        test_farmer_id = database.create_user(
            name="Ravi Verification Test",
            email="ravi_verify@farmer.in",
            password_hash="fakehash123",
            phone="9876500000",
            state="Haryana",
            farm_size_ha=3.0,
            role="farmer",
            status="pending"
        )
        created_farmer = database.get_user_by_id(test_farmer_id)
        self.assertEqual(created_farmer["status"], "pending")

        # 5. Admin grants permission: Set status to 'approved'
        with self.client.session_transaction() as sess:
            sess["user_id"] = 1
            sess["user_role"] = "admin"

        perm_res = self.client.post(
            f"/admin/user/{test_farmer_id}/permission",
            data=json.dumps({"status": "approved", "role": "farmer"}),
            content_type="application/json"
        )
        self.assertEqual(perm_res.status_code, 200)
        updated_farmer = database.get_user_by_id(test_farmer_id)
        self.assertEqual(updated_farmer["status"], "approved")
        print("   [Permission Test Passed] Admin successfully granted permission (status -> approved).")

        # 6. Test Farmer Dashboard Access & Personal Profile Updates
        with self.client.session_transaction() as sess:
            sess["user_id"] = test_farmer_id
            sess["user_name"] = "Ravi Verification Test"
            sess["user_role"] = "farmer"
            sess["user_status"] = "approved"

        farmer_dash_res = self.client.get("/farmer/dashboard")
        self.assertEqual(farmer_dash_res.status_code, 200)
        self.assertIn(b"Ravi Verification Test", farmer_dash_res.data)

        # Farmer updates profile
        update_res = self.client.post("/farmer/update-profile", data={
            "name": "Ravi Kumar Farmer",
            "phone": "9998887776",
            "state": "Haryana",
            "farm_size": "4.5"
        }, follow_redirects=True)
        self.assertEqual(update_res.status_code, 200)
        farmer_profile = database.get_user_by_id(test_farmer_id)
        self.assertEqual(farmer_profile["name"], "Ravi Kumar Farmer")
        self.assertEqual(farmer_profile["farm_size_ha"], 4.5)
        print("   [Farmer Dashboard Test Passed] Farmer profile update verified.")

        # 7. Admin deletes test user
        with self.client.session_transaction() as sess:
            sess["user_id"] = 1
            sess["user_role"] = "admin"

        del_res = self.client.post(f"/admin/user/{test_farmer_id}/delete")
        self.assertEqual(del_res.status_code, 302)
        self.assertIsNone(database.get_user_by_id(test_farmer_id))
        print("   [User Deletion Test Passed] Admin user removal verified.")

    def test_crop_recommendation_on_low_yield(self):
        """Test intelligent alternative crop recommendation when predicted yield is low."""
        # 1. Test low yield scenario in Rajasthan (Semi-arid conditions with low rainfall)
        payload = {
            "crop": "Rice",
            "state": "Rajasthan",
            "season": "Rabi",
            "soil_type": "Sandy Loam",
            "area_ha": 2.0,
            "rainfall_mm": 250,
            "temp_c": 18.0,
            "fertilizer_kg": 80,
            "pesticide_kg": 1.0
        }
        res = self.client.post("/api/predict", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get("success"))

        analysis = data.get("analysis", {})
        sug = analysis.get("suggested_alternative_crop")
        self.assertIsNotNone(sug, "Alternative crop should be suggested for low yield in Rajasthan")
        self.assertIn("crop", sug)
        self.assertIn("expected_yield_t_ha", sug)
        self.assertIn("reason", sug)
        self.assertGreater(sug["expected_yield_t_ha"], 0)
        print(f"\n   [Crop Suggestion Test Passed] Low yield Rice in Rajasthan -> Recommended '{sug['crop']}' ({sug['expected_yield_t_ha']} t/ha)")

        # 2. Test low yield scenario in Punjab (unsuitable spice in northern plains)
        payload_punjab = {
            "crop": "Cardamom",
            "state": "Punjab",
            "season": "Rabi",
            "soil_type": "Alluvial",
            "area_ha": 2.0,
            "rainfall_mm": 450,
            "temp_c": 18.0,
            "fertilizer_kg": 120,
            "pesticide_kg": 1.5
        }
        res_pb = self.client.post("/api/predict", data=json.dumps(payload_punjab), content_type="application/json")
        self.assertEqual(res_pb.status_code, 200)
        data_pb = res_pb.get_json()
        sug_pb = data_pb.get("analysis", {}).get("suggested_alternative_crop")
        self.assertIsNotNone(sug_pb)
        self.assertGreater(sug_pb["expected_yield_t_ha"], data_pb["predicted_yield_t_ha"])
        print(f"   [Crop Suggestion Test Passed] Low yield Cardamom in Punjab -> Recommended '{sug_pb['crop']}' ({sug_pb['expected_yield_t_ha']} t/ha)")

    def test_automatic_50_predictions_limit(self):
        """Test that database automatically retains only the latest 50 predictions and prunes remaining."""
        conn = database.get_connection()
        cursor = conn.cursor()

        # Add 10 dummy predictions
        for i in range(10):
            database.save_prediction({
                "farmer_name": f"Cap Test Farmer {i}",
                "state": "Punjab",
                "crop": "Wheat",
                "season": "Rabi",
                "soil_type": "Alluvial",
                "area_ha": 2.0,
                "rainfall_mm": 500,
                "temp_c": 20.0,
                "fertilizer_kg": 120,
                "pesticide_kg": 1.5,
                "predicted_yield_t_ha": 3.5,
                "total_production_tonnes": 7.0,
                "yield_status": "Optimal / High Yield"
            })

        count = cursor.execute("SELECT COUNT(*) FROM predictions").fetchone()[0]
        self.assertLessEqual(count, 50, f"Predictions table count should not exceed 50, got {count}")
        self.assertEqual(count, 50, "Predictions table should be capped exactly at 50")
        conn.close()
        print(f"   [50-Limit Test Passed] Automatic history cap verified: Database strictly maintains {count} records.")

    def test_district_integration(self):
        """Test State-District mapping, microclimate weather lookup, and district persistence."""
        from ml.district_data import get_districts_for_state, STATE_DISTRICTS

        # 1. Verify district data repository has major states & UTs
        self.assertIn("Punjab", STATE_DISTRICTS)
        self.assertIn("Maharashtra", STATE_DISTRICTS)
        self.assertIn("Tamil Nadu", STATE_DISTRICTS)

        punjab_districts = get_districts_for_state("Punjab")
        self.assertIn("Ludhiana", punjab_districts)
        self.assertIn("Amritsar", punjab_districts)

        # 2. Test /api/districts endpoint
        res = self.client.get("/api/districts?state=Maharashtra")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get("success"))
        self.assertIn("Nashik", data.get("districts", []))

        # 3. Test /api/weather with district microclimate
        weather_res = self.client.post("/api/weather", data=json.dumps({
            "state": "Maharashtra",
            "district": "Nashik",
            "season": "Rabi"
        }), content_type="application/json")
        self.assertEqual(weather_res.status_code, 200)
        weather_data = weather_res.get_json()
        self.assertTrue(weather_data.get("success"))
        self.assertEqual(weather_data.get("district"), "Nashik")
        self.assertGreater(weather_data.get("temperature_c"), 0)

        # 4. Test prediction submission with district
        pred_payload = {
            "farmer_name": "District Test Farmer",
            "state": "Maharashtra",
            "district": "Nashik",
            "crop": "Onion",
            "season": "Rabi",
            "soil_type": "Black",
            "area_ha": 2.0,
            "rainfall_mm": 550,
            "temp_c": 22.0,
            "fertilizer_kg": 140,
            "pesticide_kg": 2.0,
            "notes": "Nashik onion belt test"
        }
        pred_res = self.client.post("/api/predict", data=json.dumps(pred_payload), content_type="application/json")
        self.assertEqual(pred_res.status_code, 200)
        pred_json = pred_res.get_json()
        self.assertTrue(pred_json.get("success"))
        self.assertEqual(pred_json.get("district"), "Nashik")

        # 5. Verify district stored in database and searchable
        records = database.get_history(search_query="Nashik")
        self.assertGreater(len(records), 0)
        self.assertEqual(records[0]["district"], "Nashik")

        # 6. Verify CSV export includes district column
        csv_res = self.client.get("/api/export-csv")
        self.assertEqual(csv_res.status_code, 200)
        csv_text = csv_res.data.decode("utf-8")
        self.assertIn("district", csv_text)
        self.assertIn("Nashik", csv_text)

        print(f"   [District Integration Test Passed] Verified District API, Weather Microclimate, DB Storage & CSV.")

    def test_pesticide_limit_25(self):
        """Test that pesticide usage accepts values up to 25.0 kg/ha and rejects > 25.0 kg/ha."""
        # 1. Test pesticide = 25.0 (accepted)
        payload_valid = {
            "farmer_name": "Pesticide Test Farmer",
            "state": "Punjab",
            "crop": "Wheat",
            "season": "Rabi",
            "soil_type": "Alluvial",
            "area_ha": 2.0,
            "rainfall_mm": 500,
            "temp_c": 20.0,
            "fertilizer_kg": 120,
            "pesticide_kg": 25.0,
            "notes": "Test max pesticide 25"
        }
        res_valid = self.client.post("/api/predict", data=json.dumps(payload_valid), content_type="application/json")
        self.assertEqual(res_valid.status_code, 200)
        data_valid = res_valid.get_json()
        self.assertTrue(data_valid.get("success"))
        self.assertGreater(data_valid.get("predicted_yield_t_ha", 0), 0)

        # 2. Test pesticide = 25.5 (rejected)
        payload_invalid = dict(payload_valid)
        payload_invalid["pesticide_kg"] = 25.5
        res_invalid = self.client.post("/api/predict", data=json.dumps(payload_invalid), content_type="application/json")
        self.assertEqual(res_invalid.status_code, 400)
        data_invalid = res_invalid.get_json()
        self.assertFalse(data_invalid.get("success"))
        self.assertIn("cannot exceed 25", data_invalid.get("error", ""))

        print("   [Pesticide 25 Limit Test Passed] Successfully accepts up to 25.0 kg/ha and rejects > 25.0 kg/ha.")

    def test_financial_roi_calculation(self):
        """Test Financial Profit & Revenue ROI Calculator on prediction endpoint."""
        payload = {
            "farmer_name": "Finance Test Farmer",
            "state": "Punjab",
            "crop": "Wheat",
            "season": "Rabi",
            "soil_type": "Alluvial",
            "area_ha": 2.0,
            "rainfall_mm": 520,
            "temp_c": 19.5,
            "fertilizer_kg": 130,
            "pesticide_kg": 1.4,
        }
        res = self.client.post("/api/predict", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get("success"))
        self.assertIn("financials", data)
        fin = data["financials"]
        self.assertEqual(fin["crop"], "Wheat")
        self.assertIn("gross_revenue_mandi", fin)
        self.assertIn("total_cost", fin)
        self.assertIn("net_profit", fin)
        self.assertIn("profit_per_acre", fin)
        self.assertIn("roi_percent", fin)
        self.assertIn("profit_rating", fin)
        self.assertGreater(fin["gross_revenue_mandi"], 0)
        self.assertGreater(fin["total_cost"], 0)
        print(f"   [Financial Profit Engine Test Passed] Revenue: {fin['formatted_gross_revenue']} | Profit: {fin['formatted_net_profit']} ({fin['formatted_profit_per_acre']}, ROI: {fin['roi_percent']}%)")

    def test_spray_weather_advisory(self):
        """Test 7-Day Weather Forecast & Spray Advisory endpoint."""
        res = self.client.get("/api/spray-forecast?state=Punjab&district=Ludhiana")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get("success"))
        self.assertIn("forecast_days", data)
        self.assertEqual(len(data["forecast_days"]), 7)
        self.assertIn("spray_advisory", data)
        adv = data["spray_advisory"]
        self.assertIn("can_spray", adv)
        self.assertIn("status", adv)
        self.assertIn("headline", adv)
        self.assertIn("best_window", adv)
        print(f"   [Spray Advisory Test Passed] Location: {data['location']} | Status: {adv['status']} | Window: {adv['best_window']}")

    def test_plant_doctor_leaf_diagnosis(self):
        """Test Plant Doctor: Leaf Disease Photo Diagnosis endpoint."""
        import io
        dummy_image = io.BytesIO(b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.' \",#\x1c\x1c(7),01444\x1f'9=82<.342\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xbf\x00\xff\xd9")
        data = {
            "image": (dummy_image, "tomato_early_blight_leaf.jpg"),
            "crop": "Tomato"
        }
        res = self.client.post("/api/diagnose-leaf", data=data, content_type="multipart/form-data")
        self.assertEqual(res.status_code, 200)
        res_json = res.get_json()
        self.assertTrue(res_json.get("success"))
        self.assertIn("diagnosis", res_json)
        diag = res_json["diagnosis"]
        self.assertIn("disease_name", diag)
        self.assertIn("organic_remedy", diag)
        self.assertIn("chemical_remedy", diag)
        self.assertIn("confidence_percent", diag)
        print(f"   [Plant Doctor Test Passed] Diagnosed: {diag['disease_name']} ({diag['confidence_percent']}%) | Organic: {diag['organic_remedy'][:40]}...")

    def test_market_intelligence_rates(self):
        """Test Mandi market rates & Government MSP catalog endpoint."""
        res = self.client.get("/api/market-rates")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get("success"))
        self.assertEqual(data.get("total_crops"), 32)
        self.assertIn("Wheat", data["rates"])
        self.assertIn("Rice", data["rates"])
        self.assertIn("Cotton", data["rates"])

        # Test single crop lookup
        crop_res = self.client.get("/api/market-rates?crop=Rice")
        self.assertEqual(crop_res.status_code, 200)
        crop_data = crop_res.get_json()
        self.assertTrue(crop_data.get("success"))
        self.assertEqual(crop_data["crop"], "Rice")
        self.assertGreater(crop_data["rate"]["msp_per_quintal"], 0)
        print(f"   [Market Rates Test Passed] All 32 crops available with official MSP & Mandi benchmarks.")

    def test_language_switch_endpoint(self):
        """Test English / Hindi language switching route."""
        # Switch to Hindi
        res_hi = self.client.get("/set-language/hi?format=json")
        self.assertEqual(res_hi.status_code, 200)
        data_hi = res_hi.get_json()
        self.assertEqual(data_hi.get("lang"), "hi")

        # Switch to English
        res_en = self.client.get("/set-language/en?format=json")
        self.assertEqual(res_en.status_code, 200)
        data_en = res_en.get_json()
        self.assertEqual(data_en.get("lang"), "en")
        print(f"   [Language Switch Test Passed] Successfully toggles session between English ('en') and Hindi ('hi').")


if __name__ == "__main__":
    print("🌾 Running Crop Yield Application Test Suite (Including Dashboards & Permissions)...")
    unittest.main()


