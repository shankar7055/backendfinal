#!/usr/bin/env python3
"""
Comprehensive connection test - Verifies all functions are correctly connected
"""

import requests
import json
import sys

BASE_URL = "http://localhost:5002"
TIMEOUT = 5

def test_endpoint(method, endpoint, data=None, description=""):
    """Test a single endpoint"""
    try:
        url = f"{BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url, timeout=TIMEOUT)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=TIMEOUT)
        
        if response.status_code == 200:
            result = response.json() if response.content else {}
            return {
                "status": "✅ PASS",
                "code": response.status_code,
                "has_data": len(str(result)) > 0,
                "data_preview": str(result)[:100] if result else "Empty response"
            }
        else:
            return {
                "status": f"❌ FAIL (Code: {response.status_code})",
                "code": response.status_code,
                "error": response.text[:100]
            }
    except requests.exceptions.ConnectionError:
        return {
            "status": "❌ CONNECTION ERROR",
            "error": "Server not running or wrong port"
        }
    except Exception as e:
        return {
            "status": "❌ ERROR",
            "error": str(e)[:100]
        }

def test_all_connections():
    """Test all API endpoints and connections"""
    
    print("=" * 70)
    print("COMPREHENSIVE CONNECTION TEST")
    print("=" * 70)
    print(f"Testing server at: {BASE_URL}")
    print()
    
    # Test server is running
    print("1. Testing Server Connection...")
    server_test = test_endpoint("GET", "/")
    print(f"   {server_test['status']}")
    if server_test['status'] != "✅ PASS":
        print("   ⚠️  Server is not running! Start it with: python3 Backend_api1.py")
        return False
    print()
    
    # Test all GET endpoints
    print("2. Testing GET Endpoints...")
    print("-" * 70)
    
    get_endpoints = [
        ("/customers", "Get all customers"),
        ("/inventory", "Get inventory"),
        ("/financials", "Get financial summary"),
        ("/purchases", "Get all purchases"),
        ("/competitors", "Get competitor data"),
        ("/loyalty/active-customers", "Get loyalty rewards"),
        ("/store-design/current", "Get store design"),
    ]
    
    get_results = {}
    for endpoint, desc in get_endpoints:
        result = test_endpoint("GET", endpoint)
        get_results[endpoint] = result
        status_icon = "✅" if "PASS" in result['status'] else "❌"
        print(f"   {status_icon} {endpoint:35} {result['status']}")
        if "PASS" in result['status'] and result.get('has_data'):
            print(f"      Data: {result.get('data_preview', '')[:60]}...")
    
    print()
    
    # Test POST endpoints
    print("3. Testing POST Endpoints...")
    print("-" * 70)
    
    post_endpoints = [
        ("/ai/query", {"query": "Show me financial reports"}, "AI Query - Financial"),
        ("/ai/query", {"query": "What products need restocking?"}, "AI Query - Inventory"),
        ("/ai/query", {"query": "Recommend loyalty rewards"}, "AI Query - Loyalty"),
        ("/ai/query", {"query": "Generate a modern store design"}, "AI Query - Design"),
        ("/ai/query", {"query": "Check website problems"}, "AI Query - Website"),
    ]
    
    post_results = {}
    for endpoint, data, desc in post_endpoints:
        result = test_endpoint("POST", endpoint, data)
        post_results[f"{endpoint}_{desc}"] = result
        status_icon = "✅" if "PASS" in result['status'] else "❌"
        print(f"   {status_icon} {desc:35} {result['status']}")
        if "PASS" in result['status']:
            response_preview = result.get('data_preview', '')[:60]
            print(f"      Response: {response_preview}...")
    
    print()
    
    # Test dynamic endpoints
    print("4. Testing Dynamic Endpoints...")
    print("-" * 70)
    
    dynamic_tests = [
        ("/purchases/C001", "Get purchases for customer C001"),
        ("/invoice/PUR000", "Get invoice for purchase PUR000"),
    ]
    
    dynamic_results = {}
    for endpoint, desc in dynamic_tests:
        result = test_endpoint("GET", endpoint)
        dynamic_results[endpoint] = result
        status_icon = "✅" if "PASS" in result['status'] else "❌"
        print(f"   {status_icon} {desc:35} {result['status']}")
    
    print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    all_results = {**get_results, **post_results, **dynamic_results}
    total = len(all_results)
    passed = sum(1 for r in all_results.values() if "PASS" in r['status'])
    failed = total - passed
    
    print(f"Total Tests: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print()
    
    if failed > 0:
        print("Failed Endpoints:")
        for endpoint, result in all_results.items():
            if "PASS" not in result['status']:
                print(f"   ❌ {endpoint}: {result.get('error', result['status'])}")
        print()
    
    # Connection health
    print("Connection Health:")
    if passed == total:
        print("   🎉 EXCELLENT - All connections working perfectly!")
    elif passed >= total * 0.8:
        print("   ✅ GOOD - Most connections working")
    elif passed >= total * 0.5:
        print("   ⚠️  FAIR - Some connections need attention")
    else:
        print("   ❌ POOR - Many connections failing")
    
    return passed == total

def test_data_flow():
    """Test data flow between endpoints"""
    print()
    print("=" * 70)
    print("DATA FLOW TEST")
    print("=" * 70)
    
    try:
        # Test: Get customers, then get their purchases
        print("1. Testing Customer → Purchase Flow...")
        customers = requests.get(f"{BASE_URL}/customers", timeout=TIMEOUT).json()
        if customers and len(customers) > 0:
            customer_id = customers[0].get('customer_id', 'C001')
            purchases = requests.get(f"{BASE_URL}/purchases/{customer_id}", timeout=TIMEOUT)
            if purchases.status_code == 200:
                print(f"   ✅ Customer {customer_id} → Purchases: Connected")
            else:
                print(f"   ❌ Customer {customer_id} → Purchases: Failed")
        else:
            print("   ⚠️  No customers found")
        
        # Test: Get financials
        print("2. Testing Financial Calculations...")
        financials = requests.get(f"{BASE_URL}/financials", timeout=TIMEOUT).json()
        if financials and 'total_revenue' in financials:
            print(f"   ✅ Financials calculated: Revenue=${financials['total_revenue']:.2f}")
        else:
            print("   ❌ Financials calculation failed")
        
        # Test: AI Query flow
        print("3. Testing AI Query Flow...")
        ai_response = requests.post(
            f"{BASE_URL}/ai/query",
            json={"query": "Show me financial reports"},
            timeout=TIMEOUT
        )
        if ai_response.status_code == 200:
            response_data = ai_response.json()
            if 'response' in response_data:
                print(f"   ✅ AI Query → Response: Connected")
                print(f"      Response type: {type(response_data['response']).__name__}")
            else:
                print("   ⚠️  AI Query returned unexpected format")
        else:
            print(f"   ❌ AI Query failed: {ai_response.status_code}")
        
    except Exception as e:
        print(f"   ❌ Data flow test error: {e}")

if __name__ == "__main__":
    print()
    success = test_all_connections()
    test_data_flow()
    print()
    print("=" * 70)
    if success:
        print("✅ ALL CONNECTIONS VERIFIED - Everything is working!")
    else:
        print("⚠️  SOME CONNECTIONS NEED ATTENTION - Check failed endpoints above")
    print("=" * 70)
    print()
    
    sys.exit(0 if success else 1)

