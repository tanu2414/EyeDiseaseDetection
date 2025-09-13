#!/usr/bin/env python3
"""
Comprehensive test script for Eye Disease Prediction Application
Tests all major components and functionality
"""

import os
import sys
import requests
import sqlite3
from pathlib import Path
import torch

def test_main_page():
    """Test if main page loads correctly"""
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            print("✅ Main page loads successfully")
            return True
        else:
            print(f"❌ Main page failed with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Main page test failed: {e}")
        return False

def test_static_files():
    """Test if static files are accessible"""
    static_files = [
        'http://localhost:5000/static/css/main.css',
        'http://localhost:5000/static/js/main.js',
        'http://localhost:5000/static/images/ccfd.png'
    ]
    
    all_passed = True
    for url in static_files:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ Static file accessible: {url.split('/')[-1]}")
            else:
                print(f"❌ Static file failed: {url.split('/')[-1]} - Status: {response.status_code}")
                all_passed = False
        except requests.exceptions.RequestException as e:
            print(f"❌ Static file error: {url.split('/')[-1]} - {e}")
            all_passed = False
    
    return all_passed

def test_dashboard():
    """Test dashboard accessibility"""
    try:
        response = requests.get('http://localhost:5000/dashboard', timeout=5)
        if response.status_code == 200:
            print("✅ Dashboard loads successfully")
            return True
        else:
            print(f"❌ Dashboard failed with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Dashboard test failed: {e}")
        return False

def test_database():
    """Test database connectivity and structure"""
    try:
        # Check if database file exists
        db_path = Path('instance/database.db')
        if not db_path.exists():
            print("❌ Database file not found")
            return False
        
        # Test database connection
        conn = sqlite3.connect('instance/database.db')
        cursor = conn.cursor()
        
        # Check if User table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user';")
        if cursor.fetchone():
            print("✅ Database and User table exist")
            conn.close()
            return True
        else:
            print("❌ User table not found in database")
            conn.close()
            return False
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_ml_model():
    """Test if ML model file exists and can be loaded"""
    try:
        model_path = Path('models/MultipleEyeDiseaseDetectModel.pth')
        if not model_path.exists():
            print("❌ ML model file not found")
            return False
        
        # Try to load model info
        model_info = torch.load(model_path, map_location=torch.device('cpu'))
        print("✅ ML model file exists and loads successfully")
        return True
        
    except Exception as e:
        print(f"❌ ML model test failed: {e}")
        return False

def test_uploads_directory():
    """Test if uploads directory exists"""
    uploads_dir = Path('uploads')
    if uploads_dir.exists() and uploads_dir.is_dir():
        print("✅ Uploads directory exists")
        return True
    else:
        print("❌ Uploads directory not found")
        return False

def test_server_response():
    """Test basic server connectivity"""
    try:
        response = requests.get('http://localhost:5000/', timeout=10)
        print(f"✅ Server responding - Status: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Server not running or not accessible")
        return False
    except Exception as e:
        print(f"❌ Server test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("🧪 Starting Eye Disease Prediction Application Tests")
    print("=" * 60)
    
    tests = [
        ("Server Response", test_server_response),
        ("Main Page", test_main_page),
        ("Static Files", test_static_files),
        ("Dashboard", test_dashboard),
        ("Database", test_database),
        ("ML Model", test_ml_model),
        ("Uploads Directory", test_uploads_directory)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 TEST SUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Application is ready to use.")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    print("Eye Disease Prediction - Application Test Suite")
    print("Make sure the Flask server is running on http://localhost:5000")
    print("Press Enter to continue or Ctrl+C to cancel...")
    
    try:
        input()
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Tests cancelled by user")
        sys.exit(1)