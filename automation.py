"""
KIT Portal Student Data Automation - FIXED WITH GOOGLE VISION API
Now uses Google Cloud Vision for 90%+ CAPTCHA accuracy
"""

import time
import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# Google Vision CAPTCHA solver
from google_vision_captcha import GoogleVisionCaptchaSolver

# Fallback OCR
import easyocr
import pandas as pd
from openpyxl import load_workbook
from openpyxl.drawing.image import Image as XLImage
from PIL import Image
import requests
from io import BytesIO

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class KITPortalAutomation:
    """Main automation class with Google Vision CAPTCHA solving"""
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize automation with configuration"""
        self.config = self.load_config(config_path)
        self.driver = None
        
        # Initialize Google Vision CAPTCHA solver
        self.google_vision_solver = None
        if 'captcha' in self.config and 'google_vision_api_key' in self.config['captcha']:
            api_key = self.config['captcha']['google_vision_api_key']
            self.google_vision_solver = GoogleVisionCaptchaSolver(api_key)
            logger.info("🎯 Google Vision CAPTCHA solver initialized")
            
            # Test API key
            if not self.google_vision_solver.test_api_key():
                logger.error("❌ Google Vision API key test failed!")
                logger.error("Check if Cloud Vision API is enabled and billing is set up")
        else:
            logger.warning("⚠️ No Google Vision API key found in config")
        
        # Fallback EasyOCR reader
        self.reader = easyocr.Reader(['en'], gpu=False)
        
        self.base_url = "https://portal.kitcbe.com/index.php/Login"
        self.password = self.config['portal']['password']
        self.output_dir = Path(self.config['output']['directory'])
        self.output_dir.mkdir(exist_ok=True)
        self.photos_dir = self.output_dir / "photos"
        self.photos_dir.mkdir(exist_ok=True)
        
    def load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            raise
    
    def setup_driver(self):
        """Setup Selenium WebDriver with Chrome"""
        options = Options()
        # options.add_argument('--headless')  # Uncomment for headless mode
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        
        # Prevent detection
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.implicitly_wait(10)
        logger.info("✓ WebDriver initialized successfully")
    
    def solve_captcha(self, max_retries: int = 3) -> Optional[str]:
        """
        Solve CAPTCHA using Google Vision (primary) or EasyOCR (fallback)
        """
        for attempt in range(max_retries):
            try:
                time.sleep(1)
                
                # Find CAPTCHA image
                captcha_img = self.driver.find_element(By.XPATH, 
                    "//img[contains(@src, 'captcha_images')]")
                
                if not captcha_img:
                    logger.warning(f"⚠️ CAPTCHA image not found (attempt {attempt + 1})")
                    continue
                
                # Save CAPTCHA screenshot
                captcha_filename = 'captcha_temp.png'
                captcha_img.screenshot(captcha_filename)
                logger.info(f"📸 CAPTCHA screenshot saved")
                
                # Method 1: Try Google Vision (if available)
                if self.google_vision_solver:
                    logger.info("🔍 Trying Google Vision API...")
                    captcha_text = self.google_vision_solver.solve_captcha(captcha_filename)
                    
                    if captcha_text:
                        logger.info(f"✅ Google Vision solved: '{captcha_text}'")
                        return captcha_text
                    else:
                        logger.warning("⚠️ Google Vision failed, falling back to EasyOCR...")
                
                # Method 2: Fallback to EasyOCR
                logger.info("🔍 Trying EasyOCR fallback...")
                result = self.reader.readtext(captcha_filename, detail=0)
                
                if result:
                    captcha_text = ''.join(result).strip()
                    captcha_text = re.sub(r'[^A-Za-z0-9]', '', captcha_text)
                    
                    if 3 <= len(captcha_text) <= 7:
                        logger.info(f"✅ EasyOCR solved: '{captcha_text}'")
                        return captcha_text
                
                logger.warning(f"⚠️ Attempt {attempt + 1} failed, retrying...")
                time.sleep(1)
                
            except Exception as e:
                logger.warning(f"⚠️ CAPTCHA solve attempt {attempt + 1} failed: {e}")
                time.sleep(1)
        
        logger.error("❌ Failed to solve CAPTCHA after all retries")
        return None
    
    def click_login_button(self) -> bool:
        """Try multiple methods to click login button - FASTER"""
        try:
            # No extra delay - click immediately
            
            # Method 1: JavaScript click (fastest and most reliable)
            try:
                logger.info("Clicking login button (JS)...")
                login_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
                self.driver.execute_script("arguments[0].click();", login_btn)
                logger.info("Login button clicked")
                return True
            except Exception as e:
                logger.warning(f"JS click failed: {e}")
            
            # Method 2: Direct click
            try:
                logger.info("Trying direct click...")
                login_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]"))
                )
                login_btn.click()
                logger.info("Login button clicked")
                return True
            except Exception as e:
                logger.warning(f"Direct click failed: {e}")
            
            # Method 3: Submit form
            try:
                logger.info("Trying form submit...")
                form = self.driver.find_element(By.TAG_NAME, "form")
                form.submit()
                logger.info("Form submitted")
                return True
            except Exception as e:
                logger.warning(f"Form submit failed: {e}")
            
            logger.error("All click methods failed!")
            return False
            
        except Exception as e:
            logger.error(f"Error in click_login_button: {e}")
            return False
    
    def login(self, roll_number: str) -> bool:
        """Login to portal"""
        try:
            self.driver.get(self.base_url)
            time.sleep(3)
            
            # Wait for login form
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            
            # Enter username
            logger.info("Entering username...")
            roll_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "username"))
            )
            roll_input.clear()
            time.sleep(0.3)
            roll_input.send_keys(roll_number)
            logger.info(f"Roll number entered: {roll_number}")
            
            # Enter password
            logger.info("Entering password...")
            password_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "password1"))
            )
            password_input.clear()
            time.sleep(0.3)
            password_input.send_keys(self.password)
            logger.info("Password entered")
            
            # Solve CAPTCHA
            captcha_text = self.solve_captcha()
            if not captcha_text:
                logger.error("CAPTCHA solving failed")
                return False
            
            # Enter CAPTCHA
            logger.info("Entering CAPTCHA...")
            captcha_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "captcha"))
            )
            captcha_input.clear()
            time.sleep(0.3)
            captcha_input.send_keys(captcha_text)
            logger.info(f"CAPTCHA entered: {captcha_text}")
            
            # Click login (no extra delay)
            if not self.click_login_button():
                logger.error("Failed to click login button")
                return False
            
            # Wait longer for page load and check multiple times
            logger.info("Waiting for login to complete...")
            
            # Wait and check every 2 seconds for up to 15 seconds
            for attempt in range(8):
                time.sleep(2)
                
                current_url = self.driver.current_url
                logger.info(f"Current URL (attempt {attempt + 1}): {current_url}")
                
                # Check for success indicators
                if "Results" in current_url:
                    logger.info(f"SUCCESS! Login successful for {roll_number}")
                    return True
                
                # Check page source for results page
                page_source = self.driver.page_source
                if any(keyword in page_source for keyword in ["PROVISIONAL RESULTS", "RESULT", "Register Number", "Regulation"]):
                    logger.info(f"SUCCESS! Login successful for {roll_number} (detected in page)")
                    return True
                
                # Check if stuck on error page
                if "Userlogin" in current_url or "Login" in current_url:
                    # Still on login page - might be wrong CAPTCHA
                    if attempt < 3:
                        logger.warning(f"Still on login page (attempt {attempt + 1}) - might be wrong CAPTCHA")
                        continue
                    else:
                        break
            
            # Login failed
            logger.error(f"Login failed for {roll_number}")
            logger.error(f"Final URL: {self.driver.current_url}")
            
            # Save screenshot
            self.driver.save_screenshot(f"login_failed_{roll_number}.png")
            logger.error(f"Screenshot saved: login_failed_{roll_number}.png")
            
            # Check for error messages
            try:
                error_elem = self.driver.find_element(By.XPATH, 
                    "//*[contains(text(), 'Invalid') or contains(text(), 'incorrect') or contains(text(), 'wrong')]")
                logger.error(f"Error message: {error_elem.text}")
            except:
                pass
            
            return False
                
        except Exception as e:
            logger.error(f"Login error for {roll_number}: {e}")
            return False
    
    def extract_marksheet_data(self) -> Dict:
        """Extract data from marksheet/results page"""
        data = {}
        try:
            time.sleep(2)
            
            # Extract basic info
            try:
                data['name'] = self.driver.find_element(By.XPATH, 
                    "//td[contains(text(), 'Name')]/following-sibling::td").text.strip()
            except:
                data['name'] = ''
            
            try:
                data['register_number'] = self.driver.find_element(By.XPATH, 
                    "//td[contains(text(), 'Register Number')]/following-sibling::td").text.strip()
            except:
                data['register_number'] = ''
            
            try:
                data['regulation'] = self.driver.find_element(By.XPATH, 
                    "//td[contains(text(), 'Regulation')]/following-sibling::td").text.strip()
            except:
                data['regulation'] = ''
            
            try:
                data['gender'] = self.driver.find_element(By.XPATH, 
                    "//td[contains(text(), 'Gender')]/following-sibling::td").text.strip()
            except:
                data['gender'] = ''
            
            try:
                data['dob'] = self.driver.find_element(By.XPATH, 
                    "//td[contains(text(), 'Date of Birth')]/following-sibling::td").text.strip()
            except:
                data['dob'] = ''
            
            try:
                data['branch'] = self.driver.find_element(By.XPATH, 
                    "//td[contains(text(), 'Branch')]/following-sibling::td").text.strip()
            except:
                data['branch'] = ''
            
            # Extract courses
            courses = []
            try:
                marks_table = self.driver.find_element(By.XPATH, 
                    "//table[.//th[contains(text(), 'COURSE NAME') or contains(text(), 'Course Name')]]")
                rows = marks_table.find_elements(By.TAG_NAME, "tr")[1:]
                
                for row in rows:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    if len(cols) >= 4:
                        course_data = {
                            'semester': cols[0].text.strip() if len(cols) > 0 else '',
                            'course_code': cols[1].text.strip() if len(cols) > 1 else '',
                            'course_name': cols[2].text.strip() if len(cols) > 2 else '',
                            'grade': cols[3].text.strip() if len(cols) > 3 else '',
                            'gp': cols[4].text.strip() if len(cols) > 4 else '',
                            'result': cols[5].text.strip() if len(cols) > 5 else ''
                        }
                        if course_data['course_name']:
                            courses.append(course_data)
                
                logger.info(f"✓ Extracted {len(courses)} courses")
            except Exception as e:
                logger.warning(f"Could not extract courses: {e}")
            
            data['courses'] = courses
            logger.info(f"✓ Extracted marksheet data")
            
        except Exception as e:
            logger.error(f"Error extracting marksheet data: {e}")
        
        return data
    
    def navigate_to_profile(self) -> bool:
        """Navigate to profile details page"""
        try:
            time.sleep(2)
            
            # Click profile area
            try:
                profile_elem = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, 
                        "//*[contains(@class, 'profile') or contains(text(), 'STUDENTS')]"))
                )
                self.driver.execute_script("arguments[0].click();", profile_elem)
                logger.info("✓ Clicked profile area")
            except:
                logger.error("❌ Could not click profile")
                return False
            
            time.sleep(2)
            
            # Click Profile Details
            try:
                profile_link = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, 
                        "//a[contains(text(), 'Profile Details')]"))
                )
                self.driver.execute_script("arguments[0].click();", profile_link)
                logger.info("✓ Clicked Profile Details")
            except:
                logger.error("❌ Could not click Profile Details")
                return False
            
            time.sleep(3)
            
            # Verify profile page loaded
            if "Usersprofile" in self.driver.current_url or "Edit User" in self.driver.page_source:
                logger.info("✓ Profile page loaded")
                return True
            else:
                logger.error("❌ Profile page not loaded")
                return False
            
        except Exception as e:
            logger.error(f"Error navigating to profile: {e}")
            return False
    
    def extract_profile_data(self, roll_number: str) -> Dict:
        """Extract profile data and download photo"""
        data = {}
        try:
            time.sleep(2)
            
            # Download photo
            try:
                photo_elem = self.driver.find_element(By.XPATH, 
                    "//img[contains(@src, 'upload') or contains(@class, 'profile')]")
                photo_url = photo_elem.get_attribute('src')
                
                if not photo_url.startswith('http'):
                    base = 'https://portal.kitcbe.com'
                    photo_url = base + ('/' if not photo_url.startswith('/') else '') + photo_url
                
                response = requests.get(photo_url, timeout=10)
                if response.status_code == 200:
                    photo_path = self.photos_dir / f"{roll_number}.jpg"
                    with open(photo_path, 'wb') as f:
                        f.write(response.content)
                    data['photo_path'] = str(photo_path)
                    logger.info(f"✓ Photo downloaded")
                else:
                    data['photo_path'] = None
            except:
                data['photo_path'] = None
            
            # Extract form fields
            form_fields = {
                'first_name': "First Name",
                'last_name': "Last Name",
                'blood_group': "Blood Group",
                'mobile': "Mobile Number",
                'email': "Email",
                'alternative_mobile': "Alternative Mobile Number",
                'alternative_email': "Alternative Email",
                'community': "Community",
                'caste': "Caste",
                'religion': "Religion",
                'nationality': "Nationality",
            }
            
            for key, label in form_fields.items():
                try:
                    elem = self.driver.find_element(By.XPATH, 
                        f"//input[preceding-sibling::label[contains(text(), '{label}')]]")
                    value = elem.get_attribute('value')
                    data[key] = value.strip() if value else ''
                except:
                    data[key] = ''
            
            logger.info(f"✓ Profile data extracted")
            
        except Exception as e:
            logger.error(f"Error extracting profile data: {e}")
        
        return data
    
    def logout(self):
        """Logout from portal"""
        try:
            time.sleep(1)
            
            try:
                profile_elem = self.driver.find_element(By.XPATH, 
                    "//*[contains(@class, 'profile')]")
                self.driver.execute_script("arguments[0].click();", profile_elem)
                time.sleep(1)
            except:
                pass
            
            try:
                logout_link = self.driver.find_element(By.XPATH, 
                    "//a[contains(text(), 'Logout')]")
                self.driver.execute_script("arguments[0].click();", logout_link)
                time.sleep(2)
                logger.info("✓ Logged out")
            except:
                self.driver.get("https://portal.kitcbe.com/index.php/Login/logout")
                time.sleep(2)
            
        except Exception as e:
            logger.warning(f"Logout error: {e}")
    
    def process_student(self, roll_number: str) -> Dict:
        """Process single student"""
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing: {roll_number}")
        logger.info(f"{'='*60}")
        
        student_data = {'roll_number': roll_number}
        
        try:
            # Login
            if not self.login(roll_number):
                student_data['status'] = 'Login Failed'
                return student_data
            
            # Extract marksheet
            marksheet_data = self.extract_marksheet_data()
            student_data.update(marksheet_data)
            
            # Navigate to profile
            if self.navigate_to_profile():
                profile_data = self.extract_profile_data(roll_number)
                student_data.update(profile_data)
                student_data['status'] = 'Success'
            else:
                student_data['status'] = 'Profile Navigation Failed'
            
            # Logout
            self.logout()
            
            logger.info(f"✅ Successfully processed {roll_number}")
            
        except Exception as e:
            logger.error(f"❌ Error processing {roll_number}: {e}")
            student_data['status'] = f'Error: {str(e)}'
        
        return student_data
    
    def generate_roll_numbers(self, department_config: Dict) -> List[str]:
        """Generate list of roll numbers"""
        prefix = department_config['prefix']
        start = department_config['start']
        end = department_config['end']
        
        roll_numbers = [f"{prefix}{i:03d}" for i in range(start, end + 1)]
        logger.info(f"Generated {len(roll_numbers)} roll numbers")
        return roll_numbers
    
    def save_to_excel(self, all_data: List[Dict], output_file: str):
        """Save data to Excel with photos"""
        logger.info("Saving to Excel...")
        
        rows = []
        for student in all_data:
            row = {
                'Roll Number': student.get('roll_number', ''),
                'Status': student.get('status', ''),
                'Name': student.get('name', ''),
                'Register Number': student.get('register_number', ''),
                'First Name': student.get('first_name', ''),
                'Last Name': student.get('last_name', ''),
                'Gender': student.get('gender', ''),
                'DOB': student.get('dob', ''),
                'Blood Group': student.get('blood_group', ''),
                'Branch': student.get('branch', ''),
                'Regulation': student.get('regulation', ''),
                'Mobile': student.get('mobile', ''),
                'Email': student.get('email', ''),
                'Alternative Mobile': student.get('alternative_mobile', ''),
                'Alternative Email': student.get('alternative_email', ''),
                'Community': student.get('community', ''),
                'Caste': student.get('caste', ''),
                'Religion': student.get('religion', ''),
                'Nationality': student.get('nationality', ''),
                'Photo Path': student.get('photo_path', ''),
            }
            
            # Add courses
            courses = student.get('courses', [])
            for idx, course in enumerate(courses, 1):
                row[f'Course {idx} Name'] = course.get('course_name', '')
                row[f'Course {idx} Code'] = course.get('course_code', '')
                row[f'Course {idx} Grade'] = course.get('grade', '')
            
            rows.append(row)
        
        df = pd.DataFrame(rows)
        output_path = self.output_dir / output_file
        
        df.to_excel(output_path, index=False, engine='openpyxl')
        logger.info(f"✓ Excel file created")
        
        # Embed photos
        try:
            wb = load_workbook(output_path)
            ws = wb.active
            
            ws.insert_cols(1)
            ws.cell(1, 1, 'Photo')
            ws.column_dimensions['A'].width = 15
            
            for idx, student in enumerate(all_data, start=2):
                photo_path = student.get('photo_path')
                if photo_path and os.path.exists(photo_path):
                    try:
                        img = Image.open(photo_path)
                        img.thumbnail((100, 100))
                        temp_path = f"temp_{idx}.jpg"
                        img.save(temp_path)
                        
                        xl_img = XLImage(temp_path)
                        xl_img.width = 80
                        xl_img.height = 80
                        
                        ws.add_image(xl_img, f'A{idx}')
                        ws.row_dimensions[idx].height = 60
                        
                        os.remove(temp_path)
                    except:
                        pass
            
            wb.save(output_path)
            logger.info(f"✓ Photos embedded")
        except Exception as e:
            logger.warning(f"Could not embed photos: {e}")
        
        logger.info(f"✓ Saved to {output_path}")
        success = sum(1 for s in all_data if s.get('status') == 'Success')
        logger.info(f"✓ Successful: {success}/{len(all_data)}")
    
    def run(self, department_key: str):
        """Main execution"""
        logger.info("="*80)
        logger.info(f"KIT PORTAL AUTOMATION STARTED")
        logger.info(f"Department: {department_key}")
        logger.info(f"Time: {datetime.now()}")
        logger.info("="*80)
        
        try:
            self.setup_driver()
            
            dept_config = self.config['departments'][department_key]
            roll_numbers = self.generate_roll_numbers(dept_config)
            
            all_data = []
            success_count = 0
            failed_count = 0
            
            for idx, roll_number in enumerate(roll_numbers, 1):
                logger.info(f"\nProgress: {idx}/{len(roll_numbers)}")
                
                student_data = self.process_student(roll_number)
                all_data.append(student_data)
                
                if student_data.get('status') == 'Success':
                    success_count += 1
                else:
                    failed_count += 1
                
                time.sleep(2)
            
            # Save to Excel
            output_filename = f"{department_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            self.save_to_excel(all_data, output_filename)
            
            # Summary
            logger.info("\n" + "="*80)
            logger.info("AUTOMATION COMPLETED")
            logger.info(f"Total: {len(roll_numbers)} | Success: {success_count} | Failed: {failed_count}")
            logger.info("="*80)
            
        except Exception as e:
            logger.error(f"Critical error: {e}", exc_info=True)
        
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("Browser closed")


if __name__ == "__main__":
    automation = KITPortalAutomation("config.json")
    automation.run("aids")  # Change to "cse" for other departments