#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
93_schema_test.py - JSON Schema Contract Validation
TM-93850 Block 9.3 - API Schema Testing
JSONPlaceholder /posts/1 Schema Validation
"""

import requests
import json
import jsonschema
from datetime import datetime
import sys

class SchemaValidator:
    def __init__(self):
        self.base_url = "https://jsonplaceholder.typicode.com"
        self.post_url = f"{self.base_url}/posts/1"
        self.headers = {
            'User-Agent': 'TM-93850-Schema-Validator/1.0',
            'Accept': 'application/json'
        }
        
        # JSON SCHEMA dla /posts/1 (kontrakt API)
        self.post_schema = {
            "type": "object",
            "properties": {
                "userId": {"type": "integer", "minimum": 1},
                "id": {"type": "integer", "minimum": 1},
                "title": {"type": "string", "minLength": 1},
                "body": {"type": "string", "minLength": 1}
            },
            "required": ["userId", "id", "title", "body"],
            "additionalProperties": False
        }
    
    def fetch_post(self):
        """Pobranie /posts/1"""
        print("🔍 [GET] Fetching https://jsonplaceholder.typicode.com/posts/1")
        
        try:
            response = requests.get(
                self.post_url,
                headers=self.headers,
                timeout=10
            )
            
            print(f"✅ STATUS: {response.status_code}")
            print(f"📏 Size: {len(response.content)} bytes")
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ HTTP {response.status_code}")
                return None
                
        except requests.RequestException as e:
            print(f"❌ Network error: {e}")
            return None
    
    def validate_schema(self, post_data):
        """Walidacja JSON Schema"""
        print("\n🔍 [SCHEMA] Validating contract...")
        print("📋 Expected Schema:")
        print(json.dumps(self.post_schema, indent=2)[:200] + "...")
        
        try:
            jsonschema.validate(instance=post_data, schema=self.post_schema)
            print("✅ SCHEMA VALIDATION PASSED ✓")
            print("   ✅ userId: integer ✓")
            print("   ✅ id: integer ✓") 
            print("   ✅ title: string ✓")
            print("   ✅ body: string ✓")
            print("   ✅ No extra fields ✓")
            return True
            
        except jsonschema.exceptions.ValidationError as err:
            print("❌ SCHEMA VALIDATION FAILED!")
            print(f"   ❌ Error: {err.message}")
            print(f"   ❌ Path: {err.path}")
            return False
        except Exception as e:
            print(f"❌ Schema error: {e}")
            return False
    
    def type_check_demo(self, post_data):
        """Demonstracja typów danych"""
        print("\n🔍 [TYPES] Data Type Verification")
        
        checks = {
            "userId": (post_data.get("userId"), "integer"),
            "id": (post_data.get("id"), "integer"),
            "title": (post_data.get("title"), "string"),
            "body": (post_data.get("body"), "string")
        }
        
        all_pass = True
        for field, (value, expected) in checks.items():
            actual_type = type(value).__name__
            status = "✅" if actual_type == expected else "❌"
            if status == "❌":
                all_pass = False
            print(f"   {field}: {value} → {actual_type} (expected: {expected}) {status}")
        
        print(f"\n📊 TYPE CHECK: {'🟢 ALL PASS' if all_pass else '🔴 TYPE MISMATCH!'}")
        return all_pass
    
    def run_schema_test(self):
        """Pełny test schema validation"""
        print("🚀 9.3 JSON SCHEMA VALIDATION")
        print("="*50)
        print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)
        
        # 1. Fetch data
        post_data = self.fetch_post()
        if not post_data:
            print("\n❌ Cannot fetch data - test failed")
            sys.exit(1)
        
        print(f"\n📄 Raw data: {json.dumps(post_data, indent=2)[:200]}...")
        
        # 2. Schema validation
        schema_pass = self.validate_schema(post_data)
        
        # 3. Type checking
        types_pass = self.type_check_demo(post_data)
        
        # Summary
        print("\n" + "="*50)
        print("📊 FINAL RESULTS")
        print("="*50)
        print(f"✅ HTTP Status: 200 ✓")
        print(f"✅ Schema Valid: {'✓' if schema_pass else '✗'}")
        print(f"✅ Types Valid: {'✓' if types_pass else '✗'}")
        print(f"🎯 CONTRACT COMPLIANCE: {'🟢 PASS' if schema_pass and types_pass else '🔴 FAIL'}")
        
        if schema_pass and types_pass:
            print("\n🎉 9.3 ZADANIE ZALICZONE!")
            print("📱 MOBILE APP SAFE - No contract breaks!")
        else:
            print("\n⚠️  CONTRACT VIOLATION DETECTED!")
            print("💥 Mobile app CRASH risk!")

def main():
    # Check dependencies
    try:
        import jsonschema
        import requests
        print("✅ jsonschema + requests OK")
    except ImportError as e:
        print(f"❌ pip install jsonschema requests")
        sys.exit(1)
    
    validator = SchemaValidator()
    validator.run_schema_test()

if __name__ == "__main__":
    main()