"""
Selector Helper - Find correct selectors when portal structure changes
Run this to identify element selectors interactively
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

class SelectorFinder:
    """Interactive tool to find element selectors"""
    
    def __init__(self):
        self.driver = None
        
    def setup_driver(self):
        """Setup Chrome driver"""
        options = Options()
        options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(options=options)
        
    def find_login_selectors(self):
        """Find selectors for login page"""
        print("\n" + "="*60)
        print("FINDING LOGIN PAGE SELECTORS")
        print("="*60)
        
        self.driver.get("https://portal.kitcbe.com/index.php")
        time.sleep(3)
        
        # Find username/roll number field
        print("\n1. USERNAME/ROLL NUMBER FIELD:")
        try:
            elem = self.driver.find_element(By.CSS_SELECTOR, "input[type='text'], input[name*='user'], input[id*='user']")
            print(f"   ID: {elem.get_attribute('id')}")
            print(f"   Name: {elem.get_attribute('name')}")
            print(f"   Class: {elem.get_attribute('class')}")
            print(f"   Placeholder: {elem.get_attribute('placeholder')}")
            print(f"\n   ✓ Recommended selector:")
            if elem.get_attribute('id'):
                print(f"   By.ID, '{elem.get_attribute('id')}'")
            elif elem.get_attribute('name'):
                print(f"   By.NAME, '{elem.get_attribute('name')}'")
        except Exception as e:
            print(f"   ✗ Could not find: {e}")
            
        # Find password field
        print("\n2. PASSWORD FIELD:")
        try:
            elem = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            print(f"   ID: {elem.get_attribute('id')}")
            print(f"   Name: {elem.get_attribute('name')}")
            print(f"   Class: {elem.get_attribute('class')}")
            print(f"\n   ✓ Recommended selector:")
            if elem.get_attribute('id'):
                print(f"   By.ID, '{elem.get_attribute('id')}'")
        except Exception as e:
            print(f"   ✗ Could not find: {e}")
            
        # Find CAPTCHA input
        print("\n3. CAPTCHA INPUT FIELD:")
        try:
            elem = self.driver.find_element(By.XPATH, "//input[contains(@placeholder, 'captcha') or contains(@name, 'captcha')]")
            print(f"   ID: {elem.get_attribute('id')}")
            print(f"   Name: {elem.get_attribute('name')}")
            print(f"   Placeholder: {elem.get_attribute('placeholder')}")
            print(f"\n   ✓ Recommended selector:")
            print(f"   By.XPATH, \"//input[contains(@placeholder, 'captcha')]\"")
        except Exception as e:
            print(f"   ✗ Could not find: {e}")
            
        # Find CAPTCHA image
        print("\n4. CAPTCHA IMAGE:")
        try:
            elem = self.driver.find_element(By.XPATH, "//img[contains(@src, 'captcha')]")
            print(f"   Src: {elem.get_attribute('src')}")
            print(f"   Alt: {elem.get_attribute('alt')}")
            print(f"\n   ✓ Recommended selector:")
            print(f"   By.XPATH, \"//img[contains(@src, 'captcha')]\"")
        except Exception as e:
            print(f"   ✗ Could not find: {e}")
            
        # Find login button
        print("\n5. LOGIN BUTTON:")
        try:
            elem = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')] | //input[@type='submit']")
            print(f"   Text: {elem.text}")
            print(f"   Type: {elem.get_attribute('type')}")
            print(f"   Class: {elem.get_attribute('class')}")
            print(f"\n   ✓ Recommended selector:")
            print(f"   By.XPATH, \"//button[contains(text(), 'Login')]\"")
        except Exception as e:
            print(f"   ✗ Could not find: {e}")
    
    def find_result_selectors(self):
        """Find selectors for result/marksheet page"""
        print("\n" + "="*60)
        print("FINDING RESULT PAGE SELECTORS")
        print("="*60)
        print("\nNOTE: You need to manually login first!")
        print("Waiting 30 seconds for you to login...")
        time.sleep(30)
        
        # Find name field
        print("\n1. NAME FIELD:")
        try:
            elem = self.driver.find_element(By.XPATH, "//td[contains(text(), 'Name')]/following-sibling::td")
            print(f"   Text: {elem.text}")
            print(f"\n   ✓ Recommended selector:")
            print(f"   By.XPATH, \"//td[text()='Name']/following-sibling::td\"")
        except Exception as e:
            print(f"   ✗ Could not find: {e}")
            
        # Find marks table
        print("\n2. MARKS TABLE:")
        try:
            elem = self.driver.find_element(By.XPATH, "//table[.//th[contains(text(), 'COURSE NAME')]]")
            print(f"   Found table with {len(elem.find_elements(By.TAG_NAME, 'tr'))} rows")
            print(f"\n   ✓ Recommended selector:")
            print(f"   By.XPATH, \"//table[.//th[contains(text(), 'COURSE NAME')]]\"")
        except Exception as e:
            print(f"   ✗ Could not find: {e}")
            
        # Find profile icon
        print("\n3. PROFILE ICON/BUTTON:")
        try:
            elem = self.driver.find_element(By.XPATH, "//img[contains(@class, 'profile')] | //div[contains(@class, 'profile')]")
            print(f"   Class: {elem.get_attribute('class')}")
            print(f"   Src: {elem.get_attribute('src')}")
            print(f"\n   ✓ Recommended selector:")
            print(f"   By.XPATH, \"//img[contains(@class, 'profile')]\"")
        except Exception as e:
            print(f"   ✗ Could not find: {e}")
    
    def find_profile_selectors(self):
        """Find selectors for profile page"""
        print("\n" + "="*60)
        print("FINDING PROFILE PAGE SELECTORS")
        print("="*60)
        print("\nNOTE: Navigate to profile page manually!")
        print("Waiting 15 seconds...")
        time.sleep(15)
        
        # Find profile photo
        print("\n1. PROFILE PHOTO:")
        try:
            elem = self.driver.find_element(By.XPATH, "//img[contains(@src, 'photo') or contains(@src, 'profile')]")
            print(f"   Src: {elem.get_attribute('src')}")
            print(f"\n   ✓ Recommended selector:")
            print(f"   By.XPATH, \"//img[contains(@src, 'photo')]\"")
        except Exception as e:
            print(f"   ✗ Could not find: {e}")
            
        # Find form fields
        print("\n2. SAMPLE FORM FIELDS:")
        fields_to_check = ["First Name", "Last Name", "Date of Birth", "Gender"]
        
        for field_name in fields_to_check:
            try:
                # Try finding input
                elem = self.driver.find_element(By.XPATH, f"//label[contains(text(), '{field_name}')]/following-sibling::input")
                print(f"\n   {field_name}:")
                print(f"   Name: {elem.get_attribute('name')}")
                print(f"   Value: {elem.get_attribute('value')}")
                print(f"   Selector: By.XPATH, \"//label[contains(text(), '{field_name}')]/following-sibling::input\"")
            except:
                try:
                    # Try finding in div/span
                    elem = self.driver.find_element(By.XPATH, f"//label[contains(text(), '{field_name}')]/following-sibling::div")
                    print(f"\n   {field_name}:")
                    print(f"   Text: {elem.text}")
                    print(f"   Selector: By.XPATH, \"//label[contains(text(), '{field_name}')]/following-sibling::div\"")
                except Exception as e:
                    print(f"\n   {field_name}: ✗ Not found")
    
    def interactive_mode(self):
        """Interactive selector finder"""
        print("\n" + "="*60)
        print("INTERACTIVE SELECTOR FINDER")
        print("="*60)
        print("\nEnter XPath or CSS selector to test:")
        print("Examples:")
        print("  xpath://button[text()='Login']")
        print("  css:button.login-btn")
        print("  Type 'quit' to exit")
        
        while True:
            selector = input("\nSelector: ").strip()
            
            if selector.lower() == 'quit':
                break
                
            try:
                if selector.startswith('xpath:'):
                    elem = self.driver.find_element(By.XPATH, selector[6:])
                elif selector.startswith('css:'):
                    elem = self.driver.find_element(By.CSS_SELECTOR, selector[4:])
                else:
                    print("   ✗ Prefix with 'xpath:' or 'css:'")
                    continue
                    
                print(f"\n   ✓ Found element!")
                print(f"   Tag: {elem.tag_name}")
                print(f"   Text: {elem.text[:50]}")
                print(f"   ID: {elem.get_attribute('id')}")
                print(f"   Class: {elem.get_attribute('class')}")
                
            except Exception as e:
                print(f"   ✗ Not found: {e}")
    
    def run(self):
        """Main execution"""
        try:
            self.setup_driver()
            
            print("\n🔍 SELECTOR FINDER TOOL")
            print("This tool helps you find correct selectors for automation")
            
            # Menu
            while True:
                print("\n" + "="*60)
                print("MENU:")
                print("="*60)
                print("1. Find Login Page Selectors")
                print("2. Find Result Page Selectors (requires login)")
                print("3. Find Profile Page Selectors (requires navigation)")
                print("4. Interactive Mode (test custom selectors)")
                print("5. Exit")
                
                choice = input("\nChoice (1-5): ").strip()
                
                if choice == '1':
                    self.find_login_selectors()
                elif choice == '2':
                    self.find_result_selectors()
                elif choice == '3':
                    self.find_profile_selectors()
                elif choice == '4':
                    self.interactive_mode()
                elif choice == '5':
                    break
                else:
                    print("Invalid choice!")
                    
        finally:
            if self.driver:
                print("\nClosing browser in 5 seconds...")
                time.sleep(5)
                self.driver.quit()


if __name__ == "__main__":
    finder = SelectorFinder()
    finder.run()