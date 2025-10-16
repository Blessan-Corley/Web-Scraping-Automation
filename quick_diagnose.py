"""
QUICK DIAGNOSTIC - Find exact selectors from YOUR portal
Run this to see what's actually on the page
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def diagnose():
    print("\n" + "="*70)
    print(" 🔍 QUICK DIAGNOSTIC - Finding ALL login fields")
    print("="*70)
    
    options = Options()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    
    try:
        print("\n📡 Loading portal...")
        driver.get("https://portal.kitcbe.com/index.php/Login")
        time.sleep(3)
        
        print("\n" + "="*70)
        print(" 📋 ALL INPUT FIELDS:")
        print("="*70)
        
        # Find ALL inputs
        inputs = driver.find_elements(By.TAG_NAME, "input")
        
        for i, inp in enumerate(inputs, 1):
            input_type = inp.get_attribute('type') or 'text'
            input_name = inp.get_attribute('name') or 'N/A'
            input_id = inp.get_attribute('id') or 'N/A'
            input_placeholder = inp.get_attribute('placeholder') or 'N/A'
            input_class = inp.get_attribute('class') or 'N/A'
            input_readonly = inp.get_attribute('readonly')
            
            print(f"\n INPUT #{i}:")
            print(f"   Type: {input_type}")
            print(f"   ID: {input_id}")
            print(f"   Name: {input_name}")
            print(f"   Placeholder: {input_placeholder}")
            print(f"   Class: {input_class[:50]}...")  # Truncate long classes
            print(f"   Readonly: {input_readonly}")
            
            # Identify field purpose
            if 'text' in input_type or 'mobile' in input_placeholder.lower() or 'email' in input_placeholder.lower():
                print(f"   >>> LIKELY USERNAME FIELD <<<")
                print(f"   Use: By.ID, '{input_id}'")
            
            elif input_type == 'password':
                print(f"   >>> PASSWORD FIELD <<<")
                print(f"   Use: By.ID, '{input_id}'")
            
            elif 'captcha' in input_placeholder.lower() or 'captcha' in input_name.lower() or 'captcha' in input_id.lower():
                print(f"   >>> CAPTCHA FIELD <<<")
                print(f"   Use: By.ID, '{input_id}'")
        
        # Check for CAPTCHA image
        print("\n" + "="*70)
        print(" 🖼️  CAPTCHA IMAGE:")
        print("="*70)
        
        images = driver.find_elements(By.TAG_NAME, "img")
        captcha_found = False
        
        for img in images:
            src = img.get_attribute('src') or ''
            if 'captcha' in src.lower():
                print(f"\n   ✅ CAPTCHA IMAGE FOUND:")
                print(f"   Src: {src}")
                
                # Determine correct selector
                if 'captcha_images' in src:
                    print(f"   Use: By.XPATH, \"//img[contains(@src, 'captcha_images')]\"")
                elif 'captcha.php' in src:
                    print(f"   Use: By.XPATH, \"//img[contains(@src, 'captcha.php')]\"")
                elif 'Captcha' in src:
                    print(f"   Use: By.XPATH, \"//img[contains(@src, 'Captcha')]\"")
                
                captcha_found = True
                break
        
        if not captcha_found:
            print("\n   ⚠️ No obvious CAPTCHA image found")
            print("\n   All images on page:")
            for i, img in enumerate(images, 1):
                src = img.get_attribute('src') or 'N/A'
                print(f"   {i}. {src}")
        
        # Check login button
        print("\n" + "="*70)
        print(" 🔘 LOGIN BUTTON:")
        print("="*70)
        
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for btn in buttons:
            btn_text = btn.text
            btn_class = btn.get_attribute('class')
            
            if 'login' in btn_text.lower():
                print(f"\n   ✅ FOUND: '{btn_text}'")
                print(f"   Class: {btn_class}")
                print(f"   Use: By.XPATH, \"//button[contains(text(), '{btn_text}')]\"")
        
        # Save screenshot
        driver.save_screenshot("diagnostic_screenshot.png")
        print("\n📸 Screenshot saved: diagnostic_screenshot.png")
        
        # CRITICAL: Test if we can interact with fields
        print("\n" + "="*70)
        print(" 🧪 TESTING FIELD INTERACTION:")
        print("="*70)
        
        try:
            # Try to find and fill username
            username_field = driver.find_element(By.ID, "username")
            print(f"\n   ✓ Found username field (ID=username)")
            
            # Check if readonly
            if username_field.get_attribute('readonly'):
                print(f"   ⚠️ Field is READONLY - need to remove attribute")
                driver.execute_script("arguments[0].removeAttribute('readonly')", username_field)
                print(f"   ✓ Readonly removed")
            
            # Try to type
            username_field.clear()
            username_field.send_keys("TEST123")
            entered_value = username_field.get_attribute('value')
            print(f"   ✓ Test input entered: '{entered_value}'")
            
            if entered_value == "TEST123":
                print(f"   ✅ USERNAME FIELD WORKS!")
            else:
                print(f"   ❌ Field didn't accept input properly")
            
        except Exception as e:
            print(f"   ❌ Error interacting with username field: {e}")
        
        try:
            # Try to find and fill password
            password_field = driver.find_element(By.ID, "password1")
            print(f"\n   ✓ Found password field (ID=password1)")
            
            # Try to type
            password_field.clear()
            password_field.send_keys("test")
            print(f"   ✓ Test password entered")
            print(f"   ✅ PASSWORD FIELD WORKS!")
            
        except Exception as e:
            print(f"   ❌ Error with password1: {e}")
            
            # Try alternative IDs
            print(f"\n   Trying alternative password selectors...")
            for alt_id in ['password', 'passwd', 'pass', 'Password']:
                try:
                    password_field = driver.find_element(By.ID, alt_id)
                    print(f"   ✅ Found with ID='{alt_id}'")
                    password_field.send_keys("test")
                    print(f"   ✅ PASSWORD FIELD WORKS with ID={alt_id}!")
                    break
                except:
                    continue
        
        print("\n" + "="*70)
        print(" ✅ DIAGNOSTIC COMPLETE")
        print("="*70)
        
        print("\n📝 NEXT STEPS:")
        print("   1. Copy the selectors shown above")
        print("   2. Update automation.py with correct IDs")
        print("   3. Check diagnostic_screenshot.png")
        
        input("\n⏸️  Press Enter to close browser...")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        driver.quit()

if __name__ == "__main__":
    diagnose()