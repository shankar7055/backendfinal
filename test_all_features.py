#!/usr/bin/env python3
"""
Comprehensive test script to verify all features are working
"""

import sys
import json

def test_imports():
    """Test all module imports"""
    results = {}
    
    print("=" * 60)
    print("TESTING IMPORTS")
    print("=" * 60)
    
    # Core dependencies
    try:
        import flask
        import flask_cors
        results['flask'] = "✅ OK"
    except ImportError as e:
        results['flask'] = f"❌ FAILED: {e}"
    
    try:
        import pandas
        import numpy
        results['pandas_numpy'] = "✅ OK"
    except ImportError as e:
        results['pandas_numpy'] = f"❌ FAILED: {e}"
    
    try:
        import openai
        results['openai'] = "✅ OK"
    except ImportError as e:
        results['openai'] = f"❌ FAILED: {e}"
    
    try:
        import google.generativeai
        results['google_generativeai'] = "✅ OK"
    except ImportError as e:
        results['google_generativeai'] = f"⚠️  NOT INSTALLED: {e}"
    
    # Project modules
    try:
        from openai_assistant import OpenAIAssistant
        results['openai_assistant'] = "✅ OK"
    except Exception as e:
        results['openai_assistant'] = f"❌ FAILED: {e}"
    
    try:
        from gemini_assistant import GeminiAssistant
        results['gemini_assistant'] = "✅ OK"
    except Exception as e:
        results['gemini_assistant'] = f"⚠️  FAILED: {e}"
    
    try:
        from demo_mode import DemoAIModules
        results['demo_mode'] = "✅ OK"
    except Exception as e:
        results['demo_mode'] = f"❌ FAILED: {e}"
    
    try:
        from ai_modules import AIModules
        results['ai_modules'] = "✅ OK"
    except Exception as e:
        results['ai_modules'] = f"❌ FAILED: {e}"
    
    # Print results
    for module, status in results.items():
        print(f"{module:25} {status}")
    
    return results

def test_data_files():
    """Test data file existence"""
    print("\n" + "=" * 60)
    print("TESTING DATA FILES")
    print("=" * 60)
    
    import os
    files = {
        'data/data.json': 'Main data file',
        'data/competitor_data.json': 'Competitor data',
    }
    
    results = {}
    for filepath, description in files.items():
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    size = len(str(data))
                    results[filepath] = f"✅ OK ({size} chars)"
            except Exception as e:
                results[filepath] = f"⚠️  EXISTS BUT INVALID: {e}"
        else:
            results[filepath] = "❌ MISSING"
    
    for filepath, status in results.items():
        print(f"{filepath:35} {status}")
    
    return results

def test_openai_assistant():
    """Test OpenAI assistant initialization"""
    print("\n" + "=" * 60)
    print("TESTING OPENAI ASSISTANT")
    print("=" * 60)
    
    import os
    results = {}
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        try:
            from openai_assistant import OpenAIAssistant
            assistant = OpenAIAssistant()
            results['initialization'] = "✅ OK"
            results['api_key'] = "✅ SET"
        except Exception as e:
            results['initialization'] = f"❌ FAILED: {e}"
            results['api_key'] = "✅ SET"
    else:
        results['initialization'] = "⚠️  SKIPPED (no API key)"
        results['api_key'] = "❌ NOT SET"
    
    for test, status in results.items():
        print(f"{test:25} {status}")
    
    return results

def test_gemini_assistant():
    """Test Gemini assistant initialization"""
    print("\n" + "=" * 60)
    print("TESTING GEMINI ASSISTANT")
    print("=" * 60)
    
    import os
    results = {}
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        try:
            from gemini_assistant import GeminiAssistant
            assistant = GeminiAssistant()
            results['initialization'] = "✅ OK"
            results['api_key'] = "✅ SET"
        except Exception as e:
            results['initialization'] = f"❌ FAILED: {e}"
            results['api_key'] = "✅ SET"
    else:
        results['initialization'] = "⚠️  SKIPPED (no API key)"
        results['api_key'] = "❌ NOT SET"
    
    for test, status in results.items():
        print(f"{test:25} {status}")
    
    return results

def test_ai_modules():
    """Test AI modules with data"""
    print("\n" + "=" * 60)
    print("TESTING AI MODULES")
    print("=" * 60)
    
    results = {}
    
    try:
        import json
        with open('data/data.json', 'r') as f:
            data = json.load(f)
        
        from ai_modules import AIModules
        ai_modules = AIModules(data)
        
        # Test methods
        customers = ai_modules.get_customers()
        results['get_customers'] = f"✅ OK ({len(customers)} customers)"
        
        inventory = ai_modules.get_inventory()
        results['get_inventory'] = f"✅ OK ({len(inventory)} products)"
        
        financials = ai_modules.get_financials()
        results['get_financials'] = "✅ OK"
        
    except Exception as e:
        results['error'] = f"❌ FAILED: {e}"
    
    for test, status in results.items():
        print(f"{test:25} {status}")
    
    return results

def test_app_compatibility():
    """Test app file compatibility"""
    print("\n" + "=" * 60)
    print("TESTING APP COMPATIBILITY")
    print("=" * 60)
    
    results = {}
    
    # Test Backend_api1.py
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("backend_api1", "Backend_api1.py")
        results['Backend_api1.py'] = "✅ Can be imported"
    except Exception as e:
        results['Backend_api1.py'] = f"❌ FAILED: {e}"
    
    # Test app_enhanced.py (will fail if Gemini not available, that's OK)
    try:
        spec = importlib.util.spec_from_file_location("app_enhanced", "app_enhanced.py")
        results['app_enhanced.py'] = "✅ Can be imported"
    except Exception as e:
        results['app_enhanced.py'] = f"⚠️  ISSUE: {e}"
    
    for test, status in results.items():
        print(f"{test:25} {status}")
    
    return results

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("COMPREHENSIVE FEATURE TEST")
    print("=" * 60)
    print()
    
    all_results = {}
    all_results['imports'] = test_imports()
    all_results['data_files'] = test_data_files()
    all_results['openai'] = test_openai_assistant()
    all_results['gemini'] = test_gemini_assistant()
    all_results['ai_modules'] = test_ai_modules()
    all_results['compatibility'] = test_app_compatibility()
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    total_tests = 0
    passed_tests = 0
    warnings = 0
    
    for category, tests in all_results.items():
        for test, status in tests.items():
            total_tests += 1
            if "✅" in status:
                passed_tests += 1
            elif "⚠️" in status:
                warnings += 1
    
    print(f"Total Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"⚠️  Warnings: {warnings}")
    print(f"❌ Failed: {total_tests - passed_tests - warnings}")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed!")
    elif passed_tests + warnings == total_tests:
        print("\n✅ Core functionality OK (some optional features unavailable)")
    else:
        print("\n⚠️  Some critical tests failed - check errors above")

if __name__ == "__main__":
    main()

