"""
Diagnostic Script - Find correct selectors for YOUR portal
Run this FIRST to identify the actual element selectors
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def diagnose_login_page():
    """Inspect login page and find all input fields"""
    
    print("\n" + "="*70)
    print(" 🔍 PORTAL LOGIN PAGE DIAGNOSTIC")
    print("="*70)
    
    options = Options()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    
    try:
        print("\n📡 Loading portal login page...")
        driver.get("https://portal.kitcbe.com/index.php/Login")
        time.sleep(3)
        
        print("\n" + "="*70)
        print(" 📋 ALL INPUT FIELDS FOUND:")
        print("="*70)
        
        # Find all input fields
        inputs = driver.find_elements(By.TAG_NAME, "input")
        
        for i, inp in enumerate(inputs, 1):
            input_type = inp.get_attribute('type')
            input_name = inp.get_attribute('name')
            input_id = inp.get_attribute('id')
            input_placeholder = inp.get_attribute('placeholder')
            input_class = inp.get_attribute('class')
            
            print(f"\n INPUT #{i}:")
            print(f"   Type: {input_type}")
            print(f"   Name: {input_name}")
            print(f"   ID: {input_id}")
            print(f"   Placeholder: {input_placeholder}")
            print(f"   Class: {input_class}")
            
            # Suggest best selector
            if input_type == 'text' or (input_placeholder and 'mobile' in input_placeholder.lower()):
                print(f"   ✅ LIKELY USERNAME/ROLL NUMBER FIELD")
                print(f"   Suggested selector:")
                if input_id:
                    print(f"      By.ID, '{input_id}'")
                elif input_name:
                    print(f"      By.NAME, '{input_name}'")
                elif input_placeholder:
                    print(f"      By.XPATH, \"//input[@placeholder='{input_placeholder}']\"")
            
            elif input_type == 'password':
                print(f"   ✅ PASSWORD FIELD")
                print(f"   Suggested selector:")
                if input_id:
                    print(f"      By.ID, '{input_id}'")
                elif input_name:
                    print(f"      By.NAME, '{input_name}'")
                else:
                    print(f"      By.XPATH, \"//input[@type='password']\"")
            
            elif 'captcha' in (input_placeholder or '').lower() or 'captcha' in (input_name or '').lower():
                print(f"   ✅ CAPTCHA FIELD")
                print(f"   Suggested selector:")
                if input_id:
                    print(f"      By.ID, '{input_id}'")
                elif input_name:
                    print(f"      By.NAME, '{input_name}'")
                elif input_placeholder:
                    print(f"      By.XPATH, \"//input[@placeholder='{input_placeholder}']\"")
        
        # Find buttons
        print("\n" + "="*70)
        print(" 🔘 ALL BUTTONS FOUND:")
        print("="*70)
        
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for i, btn in enumerate(buttons, 1):
            btn_text = btn.text
            btn_type = btn.get_attribute('type')
            btn_class = btn.get_attribute('class')
            
            print(f"\n BUTTON #{i}:")
            print(f"   Text: {btn_text}")
            print(f"   Type: {btn_type}")
            print(f"   Class: {btn_class}")
            
            if 'login' in btn_text.lower():
                print(f"   ✅ LOGIN BUTTON")
                print(f"   Suggested selector:")
                print(f"      By.XPATH, \"//button[contains(text(), '{btn_text}')]\"")
        
        # Find CAPTCHA image
        print("\n" + "="*70)
        print(" 🖼️  CAPTCHA IMAGE:")
        print("="*70)
        
        images = driver.find_elements(By.TAG_NAME, "img")
        captcha_found = False
        
        for img in images:
            src = img.get_attribute('src') or ''
            alt = img.get_attribute('alt') or ''
            
            if 'captcha' in src.lower() or 'captcha' in alt.lower():
                print(f"\n ✅ CAPTCHA IMAGE FOUND:")
                print(f"   Src: {src}")
                print(f"   Alt: {alt}")
                print(f"   Suggested selector:")
                print(f"      By.XPATH, \"//img[contains(@src, 'captcha')]\"")
                captcha_found = True
                break
        
        if not captcha_found:
            print("\n ⚠️  No obvious CAPTCHA image found")
            print("   Listing all images:")
            for i, img in enumerate(images, 1):
                src = img.get_attribute('src') or ''
                if 'logo' not in src.lower():
                    print(f"   Image #{i}: {src}")
        
        # Take screenshot
        screenshot_path = "login_page_screenshot.png"
        driver.save_screenshot(screenshot_path)
        print(f"\n📸 Screenshot saved: {screenshot_path}")
        
        # Save page source
        with open("login_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"💾 Page source saved: login_page_source.html")
        
        print("\n" + "="*70)
        print(" ✅ DIAGNOSTIC COMPLETE")
        print("="*70)
        print("\n📝 NEXT STEPS:")
        print("   1. Check the suggested selectors above")
        print("   2. Look at login_page_screenshot.png")
        print("   3. Update automation.py with correct selectors")
        print("   4. Run test_single.py again")
        
        input("\n⏸️  Press Enter to close browser...")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        driver.quit()


if __name__ == "__main__":
    diagnose_login_page()