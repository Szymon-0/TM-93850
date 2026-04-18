#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
91_api_setup.py - API Endpoint Discovery & Health Check
TM-93850 Block 9.1 - REST API Testing
JSONPlaceholder Test Suite
"""

import requests
import json
from datetime import datetime

class APITester:
    def __init__(self):
        # JSONPlaceholder - profesjonalny testowy API
        self.base_url = "https://jsonplaceholder.typicode.com"
        self.headers = {
            'User-Agent': 'TM-93850-API-Tester/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def test_get_todos(self):
        """Test 1: GET /todos/1 - Basic endpoint discovery"""
        print("🔍 [GET] Test 1: /todos/1 (Single Todo)")
        url = f"{self.base_url}/todos/1"
        
        try:
            response = self.session.get(url, timeout=10)
            print(f"   📡 URL: {url}")
            print(f"   ✅ STATUS: {response.status_code}")
            print(f"   📏 Size: {len(response.content)} bytes")
            print(f"   ⏱️  Time: {response.elapsed.total_seconds():.2f}s")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   📋 Title: {data.get('title', 'OK')[:50]}...")
                print(f"   ✅ COMPLETED: {data.get('completed')}")
                return True
            else:
                print(f"   ❌ ERROR: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ CONNECTION ERROR: {e}")
            return False
    
    def test_get_users(self):
        """Test 2: GET /users - Multiple resources"""
        print("\n🔍 [GET] Test 2: /users (List)")
        url = f"{self.base_url}/users"
        
        try:
            response = self.session.get(url, timeout=10)
            print(f"   📡 URL: {url}")
            print(f"   ✅ STATUS: {response.status_code}")
            print(f"   📊 Users: {len(response.json())}")
            return True
            
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            return False
    
    def test_post_todo(self):
        """Test 3: POST /todos - Create resource"""
        print("\n🔍 [POST] Test 3: Create new Todo")
        url = f"{self.base_url}/todos"
        payload = {
            "title": "TM-93850 Security Test",
            "userId": 1,
            "completed": False
        }
        
        try:
            response = self.session.post(url, json=payload, timeout=10)
            print(f"   📡 URL: {url}")
            print(f"   ✅ STATUS: {response.status_code}")
            print(f"   📤 Created ID: {response.json().get('id')}")
            return response.status_code in [200, 201]
            
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            return False
    
    def test_auth_header(self):
        """Test 4: Custom Authorization Header"""
        print("\n🔍 [GET] Test 4: Auth Header (Bearer Token)")
        url = f"{self.base_url}/posts/1"
        headers = {
            'Authorization': 'Bearer tm93850_test_token_12345',
            'X-API-Key': 'sk-93850-security-audit'
        }
        
        try:
            response = self.session.get(url, headers=headers, timeout=10)
            print(f"   📡 URL: {url}")
            print(f"   🔑 Auth Headers: Bearer + API Key")
            print(f"   ✅ STATUS: {response.status_code}")
            return True
            
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            return False
    
    def full_health_check(self):
        """Kompletny health check API"""
        print("🚀 9.1 API SETUP - Endpoint Discovery")
        print("="*50)
        print(f"📡 Target: {self.base_url}")
        print(f"🕐 Started: {datetime.now().strftime('%H:%M:%S')}")
        print("="*50)
        
        tests = [
            ("GET /todos/1", self.test_get_todos),
            ("GET /users", self.test_get_users),
            ("POST /todos", self.test_post_todo),
            ("GET /posts/1 + Auth", self.test_auth_header)
        ]
        
        passed = 0
        for name, test_func in tests:
            if test_func():
                passed += 1
        
        print("\n" + "="*50)
        print("📊 TEST SUMMARY")
        print("="*50)
        print(f"✅ PASSED: {passed}/4")
        print(f"🎯 SUCCESS RATE: {(passed/4)*100:.0f}%")
        print(f"📡 API HEALTH: {'🟢 OK' if passed == 4 else '🟡 DEGRADED'}")
        
        if passed == 4:
            print("\n🎉 API READY FOR SECURITY TESTING!")
        else:
            print("\n⚠️  API PROBLEMY - Sprawdź connectivity!")

def main():
    tester = APITester()
    tester.full_health_check()

if __name__ == "__main__":
    main()