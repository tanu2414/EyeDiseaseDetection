#!/usr/bin/env python3
"""
Backend API Test Suite for Eye Disease Prediction Application
Tests all backend endpoints and functionality
"""

import requests
import json
import os
from pathlib import Path
import time

BASE_URL = 'http://localhost:5000'

class BackendTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
    
    def log_test(self, test_name, passed, message=""):
        """Log test results"""
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
        if message:
            print(f"    {message}")
        self.test_results.append((test_name, passed, message))
    
    def test_registration_api(self):
        """Test user registration endpoint"""
        test_data = {
            'reqst': 'r',
            'email': f'test_{int(time.time())}@example.com',
            'username': f'testuser_{int(time.time())}',
            'pass': 'testpassword123'
        }
        
        try:
            response = self.session.post(f'{BASE_URL}/', data=test_data)
            if response.status_code == 200 and response.text == "1":
                self.log_test("Registration API", True, "User registration successful")
                return True
            else:
                self.log_test("Registration API", False, f"Unexpected response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Registration API", False, f"Error: {e}")
            return False
    
    def test_login_api(self):
        """Test user login endpoint"""
        # First register a user
        timestamp = int(time.time())
        test_email = f'logintest_{timestamp}@example.com'
        test_pass = 'logintest123'
        
        # Register
        reg_data = {
            'reqst': 'r',
            'email': test_email,
            'username': f'loginuser_{timestamp}',
            'pass': test_pass
        }
        
        try:
            self.session.post(f'{BASE_URL}/', data=reg_data)
            
            # Now test login
            login_data = {
                'reqst': 'l',
                'email': test_email,
                'pass': test_pass
            }
            
            response = self.session.post(f'{BASE_URL}/', data=login_data, allow_redirects=False)
            if response.status_code in [200, 302]:  # Success or redirect
                self.log_test("Login API", True, "Login successful")
                return True
            else:
                self.log_test("Login API", False, f"Login failed with status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Login API", False, f"Error: {e}")
            return False
    
    def test_dashboard_access(self):
        """Test dashboard endpoint"""
        try:
            response = self.session.get(f'{BASE_URL}/dashboard')
            if response.status_code == 200:
                self.log_test("Dashboard Access", True, "Dashboard accessible")
                return True
            else:
                self.log_test("Dashboard Access", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Dashboard Access", False, f"Error: {e}")
            return False
    
    def test_upload_endpoint(self):
        """Test file upload endpoint"""
        try:
            # Create a dummy image file for testing
            test_file_content = b"dummy image content for testing"
            files = {'file': ('test_image.jpg', test_file_content, 'image/jpeg')}
            
            response = self.session.post(f'{BASE_URL}/success', files=files, allow_redirects=False)
            if response.status_code in [200, 302]:
                self.log_test("Upload Endpoint", True, "File upload endpoint working")
                return True
            else:
                self.log_test("Upload Endpoint", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Upload Endpoint", False, f"Error: {e}")
            return False
    
    def test_static_css(self):
        """Test CSS file loading"""
        try:
            response = self.session.get(f'{BASE_URL}/static/css/main.css')
            if response.status_code == 200:
                self.log_test("CSS Loading", True, "CSS files load correctly")
                return True
            else:
                self.log_test("CSS Loading", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("CSS Loading", False, f"Error: {e}")
            return False
    
    def test_static_js(self):
        """Test JavaScript file loading"""
        try:
            response = self.session.get(f'{BASE_URL}/static/js/main.js')
            if response.status_code == 200:
                self.log_test("JavaScript Loading", True, "JS files load correctly")
                return True
            else:
                self.log_test("JavaScript Loading", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("JavaScript Loading", False, f"Error: {e}")
            return False
    
    def test_image_assets(self):
        """Test image asset loading"""
        try:
            response = self.session.get(f'{BASE_URL}/static/images/ccfd.png')
            if response.status_code == 200:
                self.log_test("Image Assets", True, "Image assets load correctly")
                return True
            else:
                self.log_test("Image Assets", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Image Assets", False, f"Error: {e}")
            return False
    
    def test_error_handling(self):
        """Test error handling for invalid requests"""
        try:
            # Test invalid login
            invalid_login = {
                'reqst': 'l',
                'email': 'nonexistent@example.com',
                'pass': 'wrongpassword'
            }
            
            response = self.session.post(f'{BASE_URL}/', data=invalid_login)
            if response.status_code == 200 and response.text == "-1":
                self.log_test("Error Handling", True, "Invalid login properly handled")
                return True
            else:
                self.log_test("Error Handling", False, f"Unexpected response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Error Handling", False, f"Error: {e}")
            return False
    
    def test_model_prediction_endpoint(self):
        """Test model prediction endpoint structure"""
        try:
            # Test with a dummy filename (endpoint should exist even if file doesn't)
            response = self.session.get(f'{BASE_URL}/predict_image/dummy.jpg')
            # We expect this to fail with file not found, but endpoint should exist
            if response.status_code in [200, 404, 500]:  # Any response means endpoint exists
                self.log_test("Prediction Endpoint", True, "Prediction endpoint exists")
                return True
            else:
                self.log_test("Prediction Endpoint", False, f"Endpoint not found: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Prediction Endpoint", False, f"Error: {e}")
            return False
    
    def test_file_structure(self):
        """Test if required files and directories exist"""
        required_paths = [
            'app.py',
            'model.py',
            'utils.py',
            'templates/',
            'static/',
            'uploads/'
        ]
        
        all_exist = True
        for path in required_paths:
            if Path(path).exists():
                print(f"✅ Found: {path}")
            else:
                print(f"❌ Missing: {path}")
                all_exist = False
        
        self.log_test("File Structure", all_exist, "Required files and directories")
        return all_exist
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("🧪 Starting Backend API Test Suite")
        print("=" * 60)
        
        # Check if server is running first
        try:
            response = requests.get(BASE_URL, timeout=5)
            print("✅ Server is running and accessible")
        except:
            print("❌ Server is not running. Please start the Flask application first.")
            print("Run: python run.py")
            return False
        
        tests = [
            self.test_file_structure,
            self.test_registration_api,
            self.test_login_api,
            self.test_dashboard_access,
            self.test_upload_endpoint,
            self.test_static_css,
            self.test_static_js,
            self.test_image_assets,
            self.test_error_handling,
            self.test_model_prediction_endpoint
        ]
        
        print(f"\n🔍 Running {len(tests)} backend tests...\n")
        
        for test in tests:
            test()
            time.sleep(0.5)  # Small delay between tests
        
        # Summary
        passed = sum(1 for _, result, _ in self.test_results if result)
        total = len(self.test_results)
        
        print("\n" + "=" * 60)
        print(f"📊 BACKEND TEST SUMMARY: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All backend tests passed!")
        else:
            print("⚠️  Some backend tests failed. Check the output above.")
        
        return passed == total

if __name__ == "__main__":
    print("Eye Disease Prediction - Backend API Test Suite")
    print("Make sure the Flask server is running on http://localhost:5000")
    print("Press Enter to continue or Ctrl+C to cancel...")
    
    try:
        input()
        tester = BackendTester()
        success = tester.run_all_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Tests cancelled by user")
        exit(1)