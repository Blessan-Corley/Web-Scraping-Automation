"""
Test CAPTCHA solving capability
Run this to verify OCR works before full automation
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import easyocr
import time
import re

def test_captcha_ocr():
    """Test CAPTCHA OCR accuracy"""
    
    print("\n" + "="*70)
    print(" CAPTCHA OCR TESTER")
    print("="*70)
    print("\n This will:")
    print("   1. Open the portal login page")
    print("   2. Take 5 CAPTCHA screenshots")
    print("   3. Try to solve each with OCR")
    print("   4. Show you the results")
    print("\n You'll manually verify if OCR is correct")
    print("="*70)
    
    # Setup driver
    options = Options()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    
    # Setup OCR
    reader = easyocr.Reader(['en'], gpu=False)
    
    try:
        driver.get("https://portal.kitcbe.com/index.php")
        time.sleep(3)
        
        results = []
        
        for i in range(1, 6):
            print(f"\n{'='*70}")
            print(f" TEST {i}/5")
            print(f"{'='*70}")
            
            try:
                # Find CAPTCHA image - using confirmed selector
                captcha_img = driver.find_element(By.XPATH, "//img[contains(@src, 'captcha_images/')]")
                print(f"   ✓ Found CAPTCHA image")
                
                # Get CAPTCHA source for reference
                captcha_src = captcha_img.get_attribute('src')
                print(f"   📷 CAPTCHA URL: {captcha_src}")
                
                # Save CAPTCHA image
                filename = f'captcha_test_{i}.png'
                captcha_img.screenshot(filename)
                print(f"   ✓ Saved screenshot: {filename}")
                
                # Run OCR
                ocr_results = reader.readtext(filename, detail=0)
                
                if ocr_results:
                    captcha_text = ''.join(ocr_results).strip()
                    # Clean up
                    captcha_text = re.sub(r'[^A-Za-z0-9]', '', captcha_text)
                    
                    print(f"\n   OCR Result: '{captcha_text}'")
                    print(f"   Length: {len(captcha_text)} characters")
                    
                    # Manual verification
                    correct = input(f"\n   Is this correct? (y/n): ").strip().lower()
                    
                    if correct == 'y':
                        results.append(True)
                        print("   ✅ OCR Success!")
                    else:
                        actual = input("   What should it be? ").strip()
                        results.append(False)
                        print(f"   ❌ OCR Failed. Expected: '{actual}', Got: '{captcha_text}'")
                else:
                    print("   ✗ OCR returned no results")
                    results.append(False)
                
                # Refresh page for new CAPTCHA
                if i < 5:
                    print("\n   Refreshing page for new CAPTCHA...")
                    driver.refresh()
                    time.sleep(2)
                    
            except Exception as e:
                print(f"   ✗ Error: {e}")
                results.append(False)
        
        # Summary
        print("\n" + "="*70)
        print(" SUMMARY")
        print("="*70)
        
        success_count = sum(results)
        total = len(results)
        accuracy = (success_count / total * 100) if total > 0 else 0
        
        print(f"\n   Tests Run: {total}")
        print(f"   Successful: {success_count}")
        print(f"   Failed: {total - success_count}")
        print(f"   Accuracy: {accuracy:.1f}%")
        
        print("\n" + "="*70)
        print(" RECOMMENDATIONS")
        print("="*70)
        
        if accuracy >= 80:
            print("\n   ✅ OCR accuracy is GOOD!")
            print("   You can proceed with automation confidently.")
        elif accuracy >= 60:
            print("\n   ⚠️  OCR accuracy is MODERATE")
            print("   Automation will work but expect some login failures.")
            print("   Consider:")
            print("   - Adding retry logic (already included in main script)")
            print("   - Manual CAPTCHA fallback")
        else:
            print("\n   ❌ OCR accuracy is LOW")
            print("   Options:")
            print("   1. Use 2Captcha API (paid service)")
            print("   2. Implement manual CAPTCHA entry")
            print("   3. Enhance image preprocessing")
            print("\n   The portal's CAPTCHA might be too complex for free OCR.")
        
        print("\n   Check the saved captcha_test_*.png files to see quality")
        
    finally:
        print("\n Closing browser...")
        driver.quit()


def test_captcha_manual():
    """Test with manual CAPTCHA entry to verify selectors"""
    
    print("\n" + "="*70)
    print(" MANUAL CAPTCHA TEST")
    print("="*70)
    print("\n This will test login with YOUR manual CAPTCHA entry")
    print(" To verify selectors are correct")
    print("="*70)
    
    test_roll = input("\n Enter test roll number (e.g., 711524BAD001): ").strip()
    
    options = Options()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get("https://portal.kitcbe.com/index.php")
        time.sleep(2)
        
        # Find and fill username
        print("\n Looking for username field...")
        username_input = driver.find_element(By.NAME, "username")
        username_input.send_keys(test_roll)
        print(" ✓ Username filled")
        
        # Find and fill password
        print(" Looking for password field...")
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys("kit@123")
        print(" ✓ Password filled")
        
        # Manual CAPTCHA
        print("\n 👀 LOOK AT THE BROWSER WINDOW")
        captcha_text = input(" Enter the CAPTCHA text: ").strip()
        
        # Fill CAPTCHA
        print(" Looking for CAPTCHA input field...")
        captcha_input = driver.find_element(By.XPATH, "//input[@placeholder='Type captcha here']")
        captcha_input.send_keys(captcha_text)
        print(" ✓ CAPTCHA filled")
        
        # Click login
        print(" Clicking login button...")
        login_btn = driver.find_element(By.XPATH, "//button[normalize-space()='Login']")
        login_btn.click()
        
        time.sleep(5)
        
        # Check if logged in
        if "Result" in driver.page_source or "PROVISIONAL RESULTS" in driver.page_source:
            print("\n ✅ LOGIN SUCCESSFUL!")
            print(" All selectors are working correctly!")
        else:
            print("\n ❌ LOGIN FAILED!")
            print(" Check if:")
            print(" 1. Roll number is correct")
            print(" 2. Password is correct")
            print(" 3. CAPTCHA was entered correctly")
            print(" 4. Selectors need updating")
        
        input("\n Press Enter to close browser...")
        
    except Exception as e:
        print(f"\n ✗ Error: {e}")
        print("\n This means selectors are WRONG!")
        print(" Run: python find_selectors.py")
        
    finally:
        driver.quit()


if __name__ == "__main__":
    print("\n🧪 CAPTCHA TESTING TOOL")
    print("\n Choose test mode:")
    print(" 1. Test OCR accuracy (automated)")
    print(" 2. Test login manually (verify selectors)")
    
    choice = input("\n Choice (1 or 2): ").strip()
    
    if choice == '1':
        test_captcha_ocr()
    elif choice == '2':
        test_captcha_manual()
    else:
        print("Invalid choice!")