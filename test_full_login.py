"""
Complete Login Test - Test actual login with real CAPTCHA solving
This will show us exactly where it fails
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import easyocr
import time
import re

def test_complete_login():
    print("\n" + "="*70)
    print(" 🧪 COMPLETE LOGIN TEST")
    print("="*70)
    
    # Setup
    options = Options()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    reader = easyocr.Reader(['en'], gpu=False)
    
    test_roll = "711524BAD001"
    test_password = "kit@123"
    
    try:
        print(f"\n📋 Testing login for: {test_roll}")
        print(f"   Password: {test_password}")
        
        # Step 1: Load page
        print("\n[STEP 1] Loading login page...")
        driver.get("https://portal.kitcbe.com/index.php/Login")
        time.sleep(3)
        print("   ✓ Page loaded")
        
        # Step 2: Enter username
        print("\n[STEP 2] Entering username...")
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.clear()
        time.sleep(0.5)
        username_field.send_keys(test_roll)
        
        entered_username = username_field.get_attribute('value')
        print(f"   ✓ Entered: {entered_username}")
        
        if entered_username != test_roll:
            print(f"   ⚠️ WARNING: Expected '{test_roll}' but got '{entered_username}'")
        
        # Step 3: Enter password
        print("\n[STEP 3] Entering password...")
        password_field = driver.find_element(By.ID, "password1")
        password_field.clear()
        time.sleep(0.5)
        password_field.send_keys(test_password)
        
        # Don't print actual password, just confirm it's there
        password_value = password_field.get_attribute('value')
        print(f"   ✓ Password entered ({len(password_value)} characters)")
        
        if len(password_value) != len(test_password):
            print(f"   ⚠️ WARNING: Expected {len(test_password)} chars but got {len(password_value)}")
        
        # Step 4: Solve CAPTCHA
        print("\n[STEP 4] Solving CAPTCHA...")
        
        # Find CAPTCHA image
        captcha_img = driver.find_element(By.XPATH, "//img[contains(@src, 'captcha_images')]")
        print(f"   ✓ Found CAPTCHA image")
        
        # Save screenshot
        captcha_img.screenshot('captcha_test.png')
        print(f"   ✓ Saved: captcha_test.png")
        
        # OCR
        print(f"   🔍 Running OCR...")
        result = reader.readtext('captcha_test.png', detail=0)
        
        print(f"   Raw OCR result: {result}")
        
        if result:
            captcha_text = ''.join(result).strip()
            print(f"   After joining: '{captcha_text}'")
            
            # Clean up
            captcha_text = re.sub(r'[^A-Za-z0-9]', '', captcha_text)
            print(f"   After cleanup: '{captcha_text}'")
            print(f"   Length: {len(captcha_text)} characters")
            
            if len(captcha_text) < 4:
                print(f"   ⚠️ WARNING: CAPTCHA too short! Might be misread")
                print(f"\n   👀 PLEASE CHECK: captcha_test.png")
                print(f"   What should the CAPTCHA be?")
                manual_captcha = input("   Enter correct CAPTCHA (or press Enter to use OCR result): ").strip()
                
                if manual_captcha:
                    captcha_text = manual_captcha
                    print(f"   ✓ Using manual CAPTCHA: {captcha_text}")
            
            # Step 5: Enter CAPTCHA
            print("\n[STEP 5] Entering CAPTCHA...")
            captcha_field = driver.find_element(By.ID, "captcha")
            captcha_field.clear()
            time.sleep(0.5)
            captcha_field.send_keys(captcha_text)
            
            entered_captcha = captcha_field.get_attribute('value')
            print(f"   ✓ Entered: '{entered_captcha}'")
            
            if entered_captcha != captcha_text:
                print(f"   ⚠️ WARNING: Expected '{captcha_text}' but field has '{entered_captcha}'")
            
        else:
            print(f"   ❌ OCR failed - no results!")
            print(f"   Check captcha_test.png manually")
            return
        
        # Step 6: Click login
        print("\n[STEP 6] Clicking login button...")
        login_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        
        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView(true);", login_btn)
        time.sleep(0.5)
        
        print(f"   ✓ Login button found")
        print(f"   Clicking...")
        
        login_btn.click()
        print(f"   ✓ Button clicked")
        
        # Step 7: Wait and check result
        print("\n[STEP 7] Waiting for login result...")
        time.sleep(5)
        
        current_url = driver.current_url
        page_source = driver.page_source
        
        print(f"\n   Current URL: {current_url}")
        
        # Check for success indicators
        success_indicators = [
            ("Results" in current_url, "URL contains 'Results'"),
            ("Results" in page_source, "Page contains 'Results'"),
            ("PROVISIONAL RESULTS" in page_source, "Page contains 'PROVISIONAL RESULTS'"),
            ("RESULT" in page_source, "Page contains 'RESULT'"),
        ]
        
        print(f"\n   Checking success indicators:")
        login_successful = False
        for indicator, description in success_indicators:
            status = "✓" if indicator else "✗"
            print(f"   {status} {description}")
            if indicator:
                login_successful = True
        
        # Check for error messages
        print(f"\n   Checking for error messages:")
        try:
            error_elements = driver.find_elements(By.XPATH, 
                "//*[contains(text(), 'Invalid') or contains(text(), 'incorrect') or contains(text(), 'wrong') or contains(text(), 'failed')]")
            
            if error_elements:
                for elem in error_elements:
                    print(f"   ⚠️ Found: '{elem.text}'")
            else:
                print(f"   ✓ No error messages found")
        except:
            print(f"   ✓ No error messages found")
        
        # Final verdict
        print("\n" + "="*70)
        if login_successful:
            print(" ✅ LOGIN SUCCESSFUL!")
            print("="*70)
            print("\n   The automation selectors are working correctly!")
            print("   Main script should work now.")
            
            # Check what's on the page
            print("\n   Page preview:")
            try:
                name = driver.find_element(By.XPATH, "//td[contains(text(), 'Name')]/following-sibling::td").text
                print(f"   Name: {name}")
            except:
                pass
            
        else:
            print(" ❌ LOGIN FAILED!")
            print("="*70)
            print("\n   Possible reasons:")
            print("   1. CAPTCHA was wrong")
            print("   2. Password incorrect")
            print("   3. Roll number invalid")
            print("   4. Network/server issue")
            
            # Save failed screenshot
            driver.save_screenshot("login_test_failed.png")
            print(f"\n   📸 Screenshot saved: login_test_failed.png")
            print(f"   📸 CAPTCHA saved: captcha_test.png")
            print(f"\n   Check these images to diagnose the issue")
        
        print("\n" + "="*70)
        input("\n⏸️  Press Enter to close browser...")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        
        driver.save_screenshot("error_screenshot.png")
        print(f"\n📸 Error screenshot: error_screenshot.png")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    test_complete_login()