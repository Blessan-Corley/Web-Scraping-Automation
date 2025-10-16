"""
Diagnose Login Redirect Issue
This will help us understand why it goes to /Userlogin instead of /Results
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from google_vision_captcha import GoogleVisionCaptchaSolver

def diagnose_login():
    print("\n" + "="*70)
    print(" DIAGNOSING LOGIN REDIRECT ISSUE")
    print("="*70)
    
    # Setup
    options = Options()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    
    api_key = "AIzaSyBiAno0bQ9PtrhUNvJ-lVeD8EyBEBFyrcs"
    captcha_solver = GoogleVisionCaptchaSolver(api_key)
    
    test_roll = "711524BAD001"
    test_password = "kit@123"
    
    try:
        print(f"\n[STEP 1] Loading login page...")
        driver.get("https://portal.kitcbe.com/index.php/Login")
        time.sleep(3)
        print(f"   Current URL: {driver.current_url}")
        
        # Enter credentials
        print(f"\n[STEP 2] Entering credentials...")
        
        username = driver.find_element(By.ID, "username")
        username.clear()
        username.send_keys(test_roll)
        print(f"   Username entered: {test_roll}")
        
        password = driver.find_element(By.ID, "password1")
        password.clear()
        password.send_keys(test_password)
        print(f"   Password entered")
        
        # Solve CAPTCHA
        print(f"\n[STEP 3] Solving CAPTCHA...")
        captcha_img = driver.find_element(By.XPATH, "//img[contains(@src, 'captcha_images')]")
        captcha_img.screenshot('captcha_diagnostic.png')
        
        captcha_text = captcha_solver.solve_captcha('captcha_diagnostic.png')
        print(f"   CAPTCHA solved: {captcha_text}")
        
        captcha_input = driver.find_element(By.ID, "captcha")
        captcha_input.clear()
        captcha_input.send_keys(captcha_text)
        print(f"   CAPTCHA entered")
        
        # Click login
        print(f"\n[STEP 4] Clicking login button...")
        login_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        
        print(f"   Before click - URL: {driver.current_url}")
        
        # Click with JavaScript
        driver.execute_script("arguments[0].click();", login_btn)
        print(f"   Login button clicked (JS)")
        
        # Monitor URL changes
        print(f"\n[STEP 5] Monitoring page after login...")
        
        for i in range(10):
            time.sleep(2)
            current_url = driver.current_url
            print(f"\n   After {(i+1)*2} seconds:")
            print(f"      URL: {current_url}")
            
            # Check page title
            try:
                title = driver.title
                print(f"      Title: {title}")
            except:
                print(f"      Title: (error getting title)")
            
            # Check for specific elements
            try:
                # Check if results page
                if driver.find_elements(By.XPATH, "//td[contains(text(), 'Register Number')]"):
                    print(f"      >> FOUND: Results table!")
                    print(f"      >> This IS the results page!")
                    break
                
                # Check for error messages
                if driver.find_elements(By.XPATH, "//*[contains(text(), 'Invalid') or contains(text(), 'incorrect')]"):
                    error = driver.find_element(By.XPATH, "//*[contains(text(), 'Invalid') or contains(text(), 'incorrect')]")
                    print(f"      >> ERROR MESSAGE: {error.text}")
                    print(f"      >> CAPTCHA was wrong!")
                    break
                
                # Check what page we're on
                if "Userlogin" in current_url:
                    print(f"      >> Still on some login/user page")
                    
                    # Try to find any text on page
                    body_text = driver.find_element(By.TAG_NAME, "body").text[:200]
                    print(f"      >> Page content: {body_text}...")
                    
                elif "Results" in current_url:
                    print(f"      >> SUCCESS! On results page")
                    break
                
            except Exception as e:
                print(f"      >> Error checking page: {e}")
        
        # Final check
        print(f"\n" + "="*70)
        print(f" FINAL STATUS")
        print(f"="*70)
        print(f"\n   Final URL: {driver.current_url}")
        print(f"   Page Title: {driver.title}")
        
        # Save screenshot
        driver.save_screenshot("diagnostic_final_page.png")
        print(f"\n   Screenshot saved: diagnostic_final_page.png")
        
        # Save page source
        with open("diagnostic_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"   Page source saved: diagnostic_page_source.html")
        
        # Check if we're actually on results page (even if URL is wrong)
        if driver.find_elements(By.XPATH, "//td[contains(text(), 'Register Number')]"):
            print(f"\n   >> RESULTS TABLE FOUND!")
            print(f"   >> Even though URL says '{driver.current_url}'")
            print(f"   >> We ARE on the results page!")
            print(f"\n   >> This means URL check is wrong - need to check page content!")
        else:
            print(f"\n   >> No results table found")
            print(f"   >> Login probably failed")
            print(f"   >> Check diagnostic_final_page.png")
        
        input("\n\nPress Enter to close browser...")
        
    except Exception as e:
        print(f"\n ERROR: {e}")
        import traceback
        traceback.print_exc()
        
        driver.save_screenshot("diagnostic_error.png")
        print(f"\n Screenshot saved: diagnostic_error.png")
    
    finally:
        driver.quit()


if __name__ == "__main__":
    diagnose_login()