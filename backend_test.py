#!/usr/bin/env python3
"""
Backend Testing Suite for Landing Page Generator
Tests the AI-powered landing page generation endpoints
"""

import requests
import json
import sys
import re
from datetime import datetime

# Get backend URL from frontend .env
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f"Error reading frontend .env: {e}")
        return None

BASE_URL = get_backend_url()
if not BASE_URL:
    print("❌ Could not get backend URL from frontend/.env")
    sys.exit(1)

API_URL = f"{BASE_URL}/api"
print(f"🔗 Testing backend at: {API_URL}")

class LandingPageTester:
    def __init__(self):
        self.generated_ids = []
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }
    
    def log_result(self, test_name, passed, message=""):
        if passed:
            print(f"✅ {test_name}")
            self.test_results['passed'] += 1
        else:
            print(f"❌ {test_name}: {message}")
            self.test_results['failed'] += 1
            self.test_results['errors'].append(f"{test_name}: {message}")
    
    def test_russian_landing_generation(self):
        """Test 1: Generate Russian landing page"""
        print("\n🧪 Test 1: Russian Landing Page Generation")
        
        payload = {
            "theme": "Онлайн школа программирования",
            "language": "Русский",
            "traffic_source": "Google Ads",
            "target_action": "Зарегистрироваться"
        }
        
        try:
            response = requests.post(f"{API_URL}/generate-landing", json=payload, timeout=60)
            
            # Check status code
            self.log_result("Russian generation - Status 200", response.status_code == 200, 
                          f"Got {response.status_code}")
            
            if response.status_code != 200:
                print(f"Response: {response.text}")
                return None
            
            data = response.json()
            
            # Check required fields
            required_fields = ['id', 'html', 'lighthouse', 'metadata']
            for field in required_fields:
                self.log_result(f"Russian generation - Has {field}", field in data,
                              f"Missing field: {field}")
            
            if 'id' in data:
                self.generated_ids.append(data['id'])
            
            # Check HTML quality
            if 'html' in data:
                html = data['html']
                self.log_result("Russian generation - HTML starts with DOCTYPE", 
                              html.strip().upper().startswith('<!DOCTYPE'),
                              "HTML doesn't start with DOCTYPE")
                
                self.log_result("Russian generation - HTML contains Russian text",
                              any(ord(char) > 127 for char in html),
                              "No Cyrillic characters found")
                
                # Check for footer elements
                footer_checks = [
                    ("Privacy Policy in Russian", "конфиденциальности" in html.lower() or "приватности" in html.lower()),
                    ("Terms in Russian", "условия" in html.lower()),
                    ("Contact info", "@" in html and "+" in html),
                    ("Professional structure", "<footer" in html.lower() or "footer" in html.lower())
                ]
                
                for check_name, condition in footer_checks:
                    self.log_result(f"Russian generation - {check_name}", condition,
                                  f"Footer check failed: {check_name}")
            
            # Check lighthouse score
            if 'lighthouse' in data:
                score = data['lighthouse']
                self.log_result("Russian generation - Lighthouse score 95+", score >= 95,
                              f"Score: {score}")
            
            # Check metadata quality
            if 'metadata' in data:
                metadata = data['metadata']
                required_meta = ['company_name', 'email', 'phone', 'address']
                
                for field in required_meta:
                    if field in metadata:
                        value = metadata[field]
                        # Check it's not placeholder data
                        placeholder_indicators = ['test', 'example', '12345', 'placeholder', 'dummy']
                        is_realistic = not any(indicator in value.lower() for indicator in placeholder_indicators)
                        self.log_result(f"Russian generation - Realistic {field}", 
                                      is_realistic and len(value) > 5,
                                      f"Looks like placeholder: {value}")
                
                # Check email format
                if 'email' in metadata:
                    email = metadata['email']
                    email_valid = '@' in email and '.' in email and not email.startswith('@')
                    self.log_result("Russian generation - Valid email format", email_valid,
                                  f"Invalid email: {email}")
                
                # Check phone format
                if 'phone' in metadata:
                    phone = metadata['phone']
                    phone_valid = '+' in phone and len(phone) > 10
                    self.log_result("Russian generation - Valid phone format", phone_valid,
                                  f"Invalid phone: {phone}")
            
            return data
            
        except requests.exceptions.Timeout:
            self.log_result("Russian generation - Request timeout", False, "Request timed out after 60s")
            return None
        except Exception as e:
            self.log_result("Russian generation - Request success", False, str(e))
            return None
    
    def test_english_landing_generation(self):
        """Test 2: Generate English landing page"""
        print("\n🧪 Test 2: English Landing Page Generation")
        
        payload = {
            "theme": "Fitness Training Online",
            "language": "English",
            "traffic_source": "Facebook Ads",
            "target_action": "Sign Up Free"
        }
        
        try:
            response = requests.post(f"{API_URL}/generate-landing", json=payload, timeout=60)
            
            self.log_result("English generation - Status 200", response.status_code == 200,
                          f"Got {response.status_code}")
            
            if response.status_code != 200:
                print(f"Response: {response.text}")
                return None
            
            data = response.json()
            
            if 'id' in data:
                self.generated_ids.append(data['id'])
            
            # Check HTML content
            if 'html' in data:
                html = data['html']
                
                # Check for English content
                english_indicators = ['fitness', 'training', 'sign up', 'free']
                has_english = any(indicator in html.lower() for indicator in english_indicators)
                self.log_result("English generation - Contains English content", has_english,
                              "No English fitness terms found")
                
                # Check for professional footer
                footer_elements = ['privacy policy', 'terms of service', 'contact']
                footer_complete = any(element in html.lower() for element in footer_elements)
                self.log_result("English generation - Complete footer", footer_complete,
                              "Footer elements missing")
            
            # Check metadata for English format
            if 'metadata' in data:
                metadata = data['metadata']
                if 'address' in metadata:
                    address = metadata['address']
                    # Check for US/UK format indicators
                    us_uk_indicators = ['usa', 'uk', 'united states', 'united kingdom', 'street', 'ave', 'road']
                    has_western_format = any(indicator in address.lower() for indicator in us_uk_indicators)
                    self.log_result("English generation - Western address format", 
                                  has_western_format or len(address) > 20,
                                  f"Address format: {address}")
            
            return data
            
        except Exception as e:
            self.log_result("English generation - Request success", False, str(e))
            return None
    
    def test_get_landing_by_id(self):
        """Test 3: Get landing page by ID"""
        print("\n🧪 Test 3: Get Landing by ID")
        
        if not self.generated_ids:
            self.log_result("Get by ID - Has generated IDs", False, "No IDs from previous tests")
            return
        
        test_id = self.generated_ids[0]
        
        try:
            response = requests.get(f"{API_URL}/landings/{test_id}")
            
            self.log_result("Get by ID - Status 200", response.status_code == 200,
                          f"Got {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Check it returns the same ID
                self.log_result("Get by ID - Correct ID returned", 
                              data.get('id') == test_id,
                              f"Expected {test_id}, got {data.get('id')}")
                
                # Check it has all required fields
                required_fields = ['id', 'theme', 'html', 'lighthouse', 'metadata']
                for field in required_fields:
                    self.log_result(f"Get by ID - Has {field}", field in data,
                                  f"Missing field: {field}")
            
        except Exception as e:
            self.log_result("Get by ID - Request success", False, str(e))
    
    def test_get_all_landings(self):
        """Test 4: Get all landing pages"""
        print("\n🧪 Test 4: Get All Landings")
        
        try:
            response = requests.get(f"{API_URL}/landings")
            
            self.log_result("Get all - Status 200", response.status_code == 200,
                          f"Got {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Check it returns an array
                self.log_result("Get all - Returns array", isinstance(data, list),
                              f"Expected array, got {type(data)}")
                
                # Check array contains our generated landings
                if isinstance(data, list):
                    returned_ids = [item.get('id') for item in data if 'id' in item]
                    
                    for generated_id in self.generated_ids:
                        found = generated_id in returned_ids
                        self.log_result(f"Get all - Contains ID {generated_id[:8]}...", found,
                                      f"Generated ID not found in list")
                    
                    self.log_result("Get all - Non-empty response", len(data) > 0,
                                  "Empty array returned")
            
        except Exception as e:
            self.log_result("Get all - Request success", False, str(e))
    
    def test_error_handling(self):
        """Test 5: Error handling"""
        print("\n🧪 Test 5: Error Handling")
        
        # Test invalid ID
        try:
            response = requests.get(f"{API_URL}/landings/invalid-id-12345")
            self.log_result("Error handling - Invalid ID returns 404", 
                          response.status_code == 404,
                          f"Got {response.status_code} instead of 404")
        except Exception as e:
            self.log_result("Error handling - Invalid ID test", False, str(e))
        
        # Test missing required fields
        try:
            response = requests.post(f"{API_URL}/generate-landing", json={})
            self.log_result("Error handling - Missing fields returns error", 
                          response.status_code >= 400,
                          f"Got {response.status_code}, expected 4xx")
        except Exception as e:
            self.log_result("Error handling - Missing fields test", False, str(e))
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Landing Page Generator Backend Tests")
        print("=" * 60)
        
        # Test basic connectivity
        try:
            response = requests.get(f"{API_URL}/", timeout=10)
            self.log_result("Backend connectivity", response.status_code == 200,
                          f"Backend not responding: {response.status_code}")
        except Exception as e:
            self.log_result("Backend connectivity", False, str(e))
            print("❌ Cannot connect to backend. Stopping tests.")
            return self.test_results
        
        # Run main tests
        self.test_russian_landing_generation()
        self.test_english_landing_generation()
        self.test_get_landing_by_id()
        self.test_get_all_landings()
        self.test_error_handling()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.test_results['passed']}")
        print(f"❌ Failed: {self.test_results['failed']}")
        
        if self.test_results['errors']:
            print("\n🔍 FAILED TESTS:")
            for error in self.test_results['errors']:
                print(f"  • {error}")
        
        success_rate = (self.test_results['passed'] / 
                       (self.test_results['passed'] + self.test_results['failed'])) * 100
        print(f"\n📈 Success Rate: {success_rate:.1f}%")
        
        return self.test_results

if __name__ == "__main__":
    tester = LandingPageTester()
    results = tester.run_all_tests()
    
    # Exit with error code if tests failed
    if results['failed'] > 0:
        sys.exit(1)
    else:
        print("\n🎉 All tests passed!")
        sys.exit(0)