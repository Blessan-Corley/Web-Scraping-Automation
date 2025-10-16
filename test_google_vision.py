"""
Test Google Vision API Integration
Run this first to verify everything works
"""

import sys
import logging
from google_vision_captcha import GoogleVisionCaptchaSolver

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_api_key():
    """Test if Google Vision API key works"""
    print("\n" + "="*70)
    print(" 🧪 TESTING GOOGLE VISION API")
    print("="*70)
    
    api_key = "AIzaSyBiAno0bQ9PtrhUNvJ-lVeD8EyBEBFyrcs"
    
    print(f"\n📋 API Key: {api_key[:20]}...")
    print("\nTesting API connection...")
    
    try:
        solver = GoogleVisionCaptchaSolver(api_key)
        
        if solver.test_api_key():
            print("\n" + "="*70)
            print(" ✅ SUCCESS! Google Vision API is working!")
            print("="*70)
            print("\n📊 What this means:")
            print("   ✓ API key is valid")
            print("   ✓ Cloud Vision API is enabled")
            print("   ✓ You have quota available")
            print("\n🎯 Next Steps:")
            print("   1. Run: python test_single.py")
            print("   2. If that works, run: python automation.py")
            return True
        else:
            print("\n" + "="*70)
            print(" ❌ FAILED! API key not working")
            print("="*70)
            print("\n🔍 Troubleshooting:")
            print("   1. Check if Cloud Vision API is enabled:")
            print("      → https://console.cloud.google.com/apis/library/vision.googleapis.com")
            print("\n   2. Verify billing is enabled (free tier works):")
            print("      → https://console.cloud.google.com/billing")
            print("\n   3. Check API key restrictions:")
            print("      → https://console.cloud.google.com/apis/credentials")
            print("      → Make sure 'Cloud Vision API' is allowed")
            print("\n   4. Wait 5 minutes after enabling API (propagation time)")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_with_sample_captcha():
    """Test with an actual CAPTCHA image if available"""
    print("\n" + "="*70)
    print(" 🖼️  TESTING WITH ACTUAL CAPTCHA")
    print("="*70)
    
    import os
    
    # Check if there's a captcha image to test
    captcha_files = ['captcha_temp.png', 'captcha_test.png', 'captcha_original.png']
    
    found_captcha = None
    for file in captcha_files:
        if os.path.exists(file):
            found_captcha = file
            break
    
    if not found_captcha:
        print("\n⚠️  No CAPTCHA image found to test")
        print("   (This is okay - we'll test during actual run)")
        return
    
    print(f"\n📸 Found CAPTCHA: {found_captcha}")
    print("   Testing OCR...")
    
    try:
        api_key = "AIzaSyBiAno0bQ9PtrhUNvJ-lVeD8EyBEBFyrcs"
        solver = GoogleVisionCaptchaSolver(api_key)
        
        result = solver.solve_captcha(found_captcha)
        
        if result:
            print(f"\n✅ CAPTCHA Solved: '{result}'")
            print(f"   Length: {len(result)} characters")
            print("\n👀 Please verify:")
            print(f"   1. Open: {found_captcha}")
            print(f"   2. Check if '{result}' matches the image")
            
            correct = input("\n   Is this correct? (y/n): ").strip().lower()
            
            if correct == 'y':
                print("\n🎉 PERFECT! Google Vision is working great!")
                return True
            else:
                actual = input("   What should it be? ").strip()
                print(f"\n⚠️  Google Vision got: '{result}'")
                print(f"   Actual CAPTCHA was: '{actual}'")
                print("\n   This might be due to:")
                print("   • Case sensitivity")
                print("   • Overlapping characters")
                print("   • Complex fonts")
                print("\n   Don't worry - we have retry logic!")
                return False
        else:
            print("\n❌ Could not solve CAPTCHA")
            print("   Check the image quality")
            
    except Exception as e:
        print(f"\n❌ Error testing CAPTCHA: {e}")
        return False


if __name__ == "__main__":
    print("\n🚀 GOOGLE VISION API TESTER")
    
    # Test 1: API Key
    if not test_api_key():
        print("\n❌ API key test failed!")
        print("Fix the issues above before proceeding.")
        sys.exit(1)
    
    # Test 2: Sample CAPTCHA (if available)
    print("\n")
    test_with_sample_captcha()
    
    print("\n" + "="*70)
    print(" 🎯 READY TO GO!")
    print("="*70)
    print("\nRun the automation with:")
    print("   python test_single.py        # Test with 1 student first")
    print("   python automation.py         # Full automation (180 students)")