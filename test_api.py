#!/usr/bin/env python3
"""
API Test Suite for Eye Disease Prediction Application
Tests all REST API endpoints and functionality
"""

import requests
import json
import os
from pathlib import Path
import time

BASE_URL = 'http://localhost:5000'

class APITester:
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
    
    def test_health_check(self):
        """Test health check endpoint"""
        try:
            response = self.session.get(f'{BASE_URL}/api/health')
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    self.log_test("Health Check", True, "API is healthy")
                    return True
                else:
                    self.log_test("Health Check", False, f"Unexpected status: {data.get('status')}")
                    return False
            else:
                self.log_test("Health Check", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check", False, f"Error: {e}")
            return False
    
    def test_api_documentation(self):
        """Test API documentation endpoint"""
        try:
            response = self.session.get(f'{BASE_URL}/')
            if response.status_code == 200:
                data = response.json()
                if 'endpoints' in data and 'name' in data:
                    self.log_test("API Documentation", True, "Documentation available")
                    return True
                else:
                    self.log_test("API Documentation", False, "Missing documentation fields")
                    return False
            else:
                self.log_test("API Documentation", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("API Documentation", False, f"Error: {e}")
            return False
    
    def test_user_registration(self):
        """Test user registration endpoint"""
        test_data = {
            'email': f'test_{int(time.time())}@example.com',
            'username': f'testuser_{int(time.time())}',
            'password': 'testpassword123'
        }
        
        try:
            response = self.session.post(
                f'{BASE_URL}/api/register',
                json=test_data,
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == 201:
                data = response.json()
                if 'message' in data:
                    self.log_test("User Registration", True, "User registered successfully")
                    return True
                else:
                    self.log_test("User Registration", False, f"Unexpected response: {data}")
                    return False
            else:
                self.log_test("User Registration", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("User Registration", False, f"Error: {e}")
            return False
    
    def test_user_login(self):
        """Test user login endpoint"""
        # First register a user
        timestamp = int(time.time())
        test_email = f'logintest_{timestamp}@example.com'
        test_pass = 'logintest123'
        
        reg_data = {
            'email': test_email,
            'username': f'loginuser_{timestamp}',
            'password': test_pass
        }
        
        try:
            # Register
            self.session.post(
                f'{BASE_URL}/api/register',
                json=reg_data,
                headers={'Content-Type': 'application/json'}
            )
            
            # Now test login
            login_data = {
                'email': test_email,
                'password': test_pass
            }
            
            response = self.session.post(
                f'{BASE_URL}/api/login',
                json=login_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'user' in data and data['user']['email'] == test_email:
                    self.log_test("User Login", True, "Login successful")
                    return True
                else:
                    self.log_test("User Login", False, f"Unexpected response: {data}")
                    return False
            else:
                self.log_test("User Login", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("User Login", False, f"Error: {e}")
            return False
    
    def test_invalid_login(self):
        """Test invalid login credentials"""
        try:
            login_data = {
                'email': 'nonexistent@example.com',
                'password': 'wrongpassword'
            }
            
            response = self.session.post(
                f'{BASE_URL}/api/login',
                json=login_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 401:
                data = response.json()
                if 'error' in data:
                    self.log_test("Invalid Login", True, "Invalid credentials properly rejected")
                    return True
                else:
                    self.log_test("Invalid Login", False, f"Unexpected response: {data}")
                    return False
            else:
                self.log_test("Invalid Login", False, f"Expected 401, got: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Invalid Login", False, f"Error: {e}")
            return False
    
    def test_file_upload(self):
        """Test file upload endpoint"""
        try:
            # Create a dummy image file for testing
            test_file_content = b"dummy image content for testing"
            files = {'file': ('test_image.jpg', test_file_content, 'image/jpeg')}
            
            response = self.session.post(f'{BASE_URL}/api/upload', files=files)
            
            if response.status_code == 200:
                data = response.json()
                if 'filename' in data and 'prediction' in data:
                    self.log_test("File Upload", True, "File upload and prediction working")
                    return True
                else:
                    self.log_test("File Upload", False, f"Missing fields in response: {data}")
                    return False
            else:
                self.log_test("File Upload", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("File Upload", False, f"Error: {e}")
            return False
    
    def test_missing_file_upload(self):
        """Test upload endpoint without file"""
        try:
            response = self.session.post(f'{BASE_URL}/api/upload')
            
            if response.status_code == 400:
                data = response.json()
                if 'error' in data:
                    self.log_test("Missing File Upload", True, "Missing file properly handled")
                    return True
                else:
                    self.log_test("Missing File Upload", False, f"Unexpected response: {data}")
                    return False
            else:
                self.log_test("Missing File Upload", False, f"Expected 400, got: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Missing File Upload", False, f"Error: {e}")
            return False
    
    def test_file_structure(self):
        """Test if required files and directories exist"""
        required_paths = [
            'app.py',
            'model.py',
            'utils.py',
            'uploads/',
            'models/'
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
        """Run all API tests"""
        print("🧪 Starting Eye Disease Prediction API Test Suite")
        print("=" * 60)
        
        # Check if server is running first
        try:
            response = requests.get(BASE_URL, timeout=5)
            print("✅ API server is running and accessible")
        except:
            print("❌ API server is not running. Please start the Flask application first.")
            print("Run: python run.py")
            return False
        
        tests = [
            self.test_file_structure,
            self.test_health_check,
            self.test_api_documentation,
            self.test_user_registration,
            self.test_user_login,
            self.test_invalid_login,
            self.test_file_upload,
            self.test_missing_file_upload
        ]
        
        print(f"\n🔍 Running {len(tests)} API tests...\n")
        
        for test in tests:
            test()
            time.sleep(0.5)  # Small delay between tests
        
        # Summary
        passed = sum(1 for _, result, _ in self.test_results if result)
        total = len(self.test_results)
        
        print("\n" + "=" * 60)
        print(f"📊 API TEST SUMMARY: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All API tests passed!")
        else:
            print("⚠️  Some API tests failed. Check the output above.")
        
        return passed == total

if __name__ == "__main__":
    print("Eye Disease Prediction - API Test Suite")
    print("Make sure the Flask server is running on http://localhost:5000")
    print("Press Enter to continue or Ctrl+C to cancel...")
    
    try:
        input()
        tester = APITester()
        success = tester.run_all_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Tests cancelled by user")
        exit(1)