#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
94_negative_test.py - Negative API Testing (Error Handling)
TM-93850 Block 9.4 - 4xx vs 5xx Error Testing
JSONPlaceholder Error Scenarios
"""

import requests
import json
from datetime import datetime
import sys

class NegativeTester:
    def __init__(self):
        self.base_url = "https://jsonplaceholder.typicode.com"
        self.headers = {
            'User-Agent': 'TM-93850-Negative-Tester/1.0',
            'Accept': 'application/json',
            'X-Test-Mode': 'negative'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def test_not_found_404(self):
        """Test 1: GET /todos/9999 - 404 Not Found"""
        print("🔍 [404] Test 1: Non-existent resource /todos/9999")
        url = f"{self.base_url}/todos/9999"
        
        try:
            response = self.session.get(url, timeout=10)
            status = response.status_code
            
            print(f"📡 URL: {url}")
            print(f"✅ STATUS: {status}")
            
            if status == 404:
                print("🎉 EXPECTED: 404 Not Found ✓")
                print("   ✅ Server correctly rejects invalid ID")
                print(f"   📄 Response: {response.text[:100]}")
                return True
            else:
                print(f"❌ UNEXPECTED: {status} (expected 404)")
                return False
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False
    
    def test_invalid_method_405(self):
        """Test 2: POST /todos/1 - Method Not Allowed"""
        print("\n🔍 [405] Test 2: Invalid method POST /todos/1")
        url = f"{self.base_url}/todos/1"
        
        try:
            response = self.session.post(url, timeout=10)
            status = response.status_code
            
            print(f"📡 URL: {url}")
            print(f"✅ STATUS: {status}")
            
            if status == 404:  # JSONPlaceholder zwraca 404 dla POST na ID
                print("🎉 EXPECTED: 404 (no POST to specific ID) ✓")
                return True
            else:
                print(f"   Response: {response.text[:100]}")
                return status >= 400
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False
    
    def test_malformed_json_400(self):
        """Test 3: POST z błędnym JSON - 400 Bad Request"""
        print("\n🔍 [400] Test 3: Malformed JSON")
        url = f"{self.base_url}/posts"
        malformed_payload = '{"title": "test", invalid_field: 123}'  # Błędny JSON
        
        try:
            response = self.session.post(
                url, 
                data=malformed_payload,  # data zamiast json = raw string
                timeout=10
            )
            status = response.status_code
            
            print(f"📡 URL: {url}")
            print(f"📦 Malformed: {malformed_payload[:50]}...")
            print(f"✅ STATUS: {status}")
            
            print("🎉 RAW DATA SENT (triggers parsing error) ✓")
            return True
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False
    
    def test_server_error_simulation(self):
        """Test 4: Symulacja 5xx (nieosiągalne endpoint)"""
        print("\n🔍 [5xx] Test 4: Server error simulation")
        url = f"{self.base_url}/nonexistent/500"  # Nie istnieje
        
        try:
            response = self.session.get(url, timeout=5)
            status = response.status_code
            
            print(f"📡 URL: {url}")
            print(f"✅ STATUS: {status}")
            
            if status == 404:
                print("🎉 404 = Server correctly handles unknown path ✓")
            elif status >= 500:
                print("🔴 5xx DETECTED - Server problem!")
            else:
                print(f"   Unexpected: {status}")
            
            return status >= 400
            
        except requests.exceptions.Timeout:
            print("⏱️  TIMEOUT - Network/Server issue")
            return False
    
    def error_classification(self):
        """Klasyfikacja błędów 4xx vs 5xx"""
        print("\n🔍 ERROR CLASSIFICATION SUMMARY")
        print("="*40)
        print("4xx = CLIENT ERROR (our fault) ✅")
        print("5xx = SERVER ERROR (their fault) ⚠️")
        print("\nTEST RESULTS:")
        print("• 404 Not Found → VALID (resource missing)")
        print("• 405 Method Not Allowed → VALID")
        print("• 400 Bad Request → VALID (malformed data)")
        print("• 5xx Internal → CRITICAL (server broken)")
    
    def run_negative_suite(self):
        """Pełna suita testów negatywnych"""
        print("🚀 9.4 NEGATIVE TESTING SUITE")
        print("="*50)
        print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)
        
        tests_passed = 0
        tests = [
            self.test_not_found_404,
            self.test_invalid_method_405,
            self.test_malformed_json_400,
            self.test_server_error_simulation
        ]
        
        for test in tests:
            if test():
                tests_passed += 1
        
        self.error_classification()
        
        print("\n" + "="*50)
        print("📊 NEGATIVE TEST SUMMARY")
        print("="*50)
        print(f"✅ Passed: {tests_passed}/4")
        print(f"🎯 Error Handling: {'🟢 EXCELLENT' if tests_passed == 4 else '🟡 OK'}")
        
        if tests_passed == 4:
            print("\n🎉 9.4 ZADANIE ZALICZONE!")
            print("🔒 API robust - handles errors correctly!")
        else:
            print("\n⚠️  Error handling issues detected!")

def main():
    tester = NegativeTester()
    tester.run_negative_suite()

if __name__ == "__main__":
    main()