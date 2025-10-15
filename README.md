# If selectors fail, inspect page and update
```

### 2. Add Delays (if portal is slow)

```python
# In automation.py, increase sleep times:
time.sleep(5)  # Instead of time.sleep(2)
```

### 3. Headless Mode (run without browser window)

```python
# In setup_driver() method, uncomment:
options.add_argument('--headless')
```

### 4. Handle Additional Fields

```python
# In extract_profile_data(), add:
form_fields = {
    'your_new_field': "Field Label on Page",
    # ... existing fields
}
```

---

## 🐛 Troubleshooting

### Issue 1: ChromeDriver Not Found
**Solution:**
```bash
# Check Chrome version
chrome://version

# Download matching ChromeDriver
# From: https://chromedriver.chromium.org/downloads
# Place in project folder or system PATH
```

### Issue 2: CAPTCHA Solve Failing
**Symptoms:** "Login Failed" for all students

**Solutions:**
1. **Check CAPTCHA selector:**
```python
# In solve_captcha(), verify selector:
captcha_img = driver.find_element(By.XPATH, "//img[contains(@src, 'captcha')]")
```

2. **Improve OCR:**
```python
# Install better OCR models:
pip install easyocr --upgrade

# Or switch to manual CAPTCHA solving:
captcha_text = input("Enter CAPTCHA: ")
```

3. **Debug CAPTCHA image:**
```python
# Check saved captcha_temp.png file
# If unclear, adjust image preprocessing
```

### Issue 3: Selectors Not Working
**Symptoms:** NoSuchElementException errors

**Solution:**
```bash
# Open portal manually, inspect elements
# Update XPath/CSS selectors in automation.py

# Use browser console to test:
document.querySelector("#username")  // Should find element
```

### Issue 4: Timeout Errors
**Solution:**
```python
# Increase timeout in config.json:
"selenium": {
    "implicit_wait": 20,  // Increase from 10
    "page_load_timeout": 60  // Increase from 30
}
```

### Issue 5: Profile Navigation Fails
**Solution:**
```python
# Verify profile icon selector:
profile_icon = driver.find_element(By.CSS_SELECTOR, "img.profile-pic")

# Try alternative approach:
driver.get("https://portal.kitcbe.com/profile.php")  # Direct URL
```

### Issue 6: Excel Photo Embedding Fails
**Solution:**
```python
# Check photo paths exist:
import os
os.path.exists(photo_path)  # Should be True

# Verify file permissions
# Try saving without photos first
```

---

## 📝 Logging & Debugging

### View Logs
```bash
# Real-time log viewing (Linux/Mac):
tail -f automation.log

# Windows:
Get-Content automation.log -Wait
```

### Log Levels
```python
# Change in automation.py:
logging.basicConfig(level=logging.DEBUG)  # More detailed
logging.basicConfig(level=logging.WARNING)  # Less verbose
```

### Debug Mode
```python
# Add breakpoints:
import pdb; pdb.set_trace()

# Take screenshots for debugging:
driver.save_screenshot(f"debug_{roll_number}.png")
```

---

## ⚡ Performance Optimization

### 1. Parallel Processing (Advanced)
```python
from concurrent.futures import ThreadPoolExecutor

def process_batch(roll_numbers):
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(process_student, roll_numbers)
```

⚠️ **Warning:** May trigger anti-bot measures!

### 2. Reduce Image Size
```python
# In extract_profile_data():
img.thumbnail((100, 100))  # Smaller size, faster processing
```

### 3. Skip Photos
```python
# Comment out photo download section
# data['photo_path'] = None
```

---

## 🔒 Security & Ethics

### ⚠️ Important Notes:
1. **Use Responsibly:** Only for legitimate academic purposes
2. **Respect Privacy:** Don't share extracted data publicly
3. **Rate Limiting:** Script includes delays to avoid server overload
4. **Authorization:** Ensure you have permission to access this data
5. **Data Protection:** Secure output files with proper access controls

### Best Practices:
```bash
# Encrypt sensitive data
# Delete temporary files after use
# Don't commit credentials to git
# Use .gitignore for output_data/
```

---

## 🎓 Advanced Usage

### Custom Roll Number Patterns

```python
# For non-sequential roll numbers:
def generate_custom_rolls():
    return [
        "711524BAD001",
        "711524BAD005",
        "711524BAD010",
        # ... custom list
    ]

# In main:
roll_numbers = generate_custom_rolls()
```

### Export to Multiple Formats

```python
# Add CSV export:
df.to_csv("output.csv", index=False)

# Add JSON export:
with open("output.json", "w") as f:
    json.dump(all_data, f, indent=2)
```

### Send Email Notification

```python
import smtplib

def send_completion_email():
    # Add email sending logic
    pass

# Call after automation completes
```

---

## 📚 FAQ

**Q: How long does it take?**
A: ~3-5 seconds per student. 180 students = ~15-20 minutes

**Q: Can I run this on a schedule?**
A: Yes! Use cron (Linux) or Task Scheduler (Windows)

**Q: What if portal structure changes?**
A: Update selectors in `automation.py`. Use browser dev tools to find new selectors.

**Q: Can I run multiple departments simultaneously?**
A: Not recommended - may trigger anti-bot measures. Run sequentially.

**Q: How do I handle failed students?**
A: Check `automation.log` for errors. Re-run with only failed roll numbers.

**Q: Excel file is too large?**
A: Split by department or reduce photo quality

---

## 🆘 Getting Help

### Before Asking:
1. Check `automation.log` for error details
2. Verify config.json is correct
3. Test with 2-3 students first
4. Check portal is accessible manually

### Debug Checklist:
```bash
✓ Python 3.8+ installed
✓ Chrome browser installed
✓ Dependencies installed (pip list)
✓ config.json exists and valid JSON
✓ Portal accessible in browser
✓ Correct roll number format
✓ Password correct
```

---

## 📈 Success Indicators

```
✓ WebDriver initialized successfully
✓ Generated 180 roll numbers
✓ Login successful for 711524BAD001
✓ Extracted marksheet data
✓ Navigated to profile page
✓ Downloaded photo
✓ Extracted profile data
✓ Logged out successfully
✓ Successfully processed 711524BAD001
✓ Data saved to output_data/aids_20241015_143022.xlsx
```

---

## 🎉 You're Ready!

Run your first automation:

```bash
python automation.py
```

Watch the magic happen! 🚀

---

## 📞 Support

For issues specific to this automation:
1. Check logs: `automation.log`
2. Review configuration: `config.json`
3. Test selectors manually in browser

**Remember:** Portal structure may change. Selectors may need updates! KIT Portal Automation - Complete Setup Guide

## 📋 Overview
Automated data extraction from KIT portal for student marksheets and profiles. Processes 180+ students in one run with zero manual intervention.

---

## 🚀 Quick Start (5 Minutes)

### 1. Prerequisites
- **Python 3.8+** installed
- **Google Chrome** browser installed
- **ChromeDriver** (auto-installed by selenium-manager)
- Internet connection

### 2. Installation

```bash
# Clone or download the project
cd kit-portal-automation

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. ChromeDriver Setup

**Option A: Automatic (Selenium 4.6+)**
```bash
# No action needed - Selenium Manager will auto-download ChromeDriver
```

**Option B: Manual**
```bash
# Download from: https://chromedriver.chromium.org/
# Place chromedriver.exe in project folder or add to PATH
```

### 4. Project Structure

```
kit-portal-automation/
├── automation.py          # Main script
├── config.json           # Configuration file
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── output_data/         # Created automatically
│   ├── photos/          # Student photos
│   └── *.xlsx           # Excel outputs
└── automation.log       # Execution logs
```

---

## ⚙️ Configuration

### Edit `config.json`

```json
{
  "departments": {
    "aids": {
      "prefix": "711524BAD",
      "start": 1,
      "end": 180
    },
    "cse": {
      "prefix": "712524BCS",
      "start": 1,
      "end": 180
    }
  }
}
```

**To add new department:**
1. Add new entry under `"departments"`
2. Set correct roll number prefix
3. Set start and end numbers

**Example: Adding EEE Department**
```json
"eee": {
  "name": "Electrical and Electronics Engineering",
  "prefix": "716524BEE",
  "start": 1,
  "end": 150
}
```

---

## 🎯 Usage

### Basic Usage

```bash
# Run for AI&DS department
python automation.py
```

### Change Department

**Method 1: Edit automation.py (last line)**
```python
automation.run("cse")  # Change "aids" to "cse" or any dept key
```

**Method 2: Command line argument (if you add argparse)**
```bash
python automation.py --dept cse
```

### Run Multiple Departments

```python
# In automation.py, modify __main__ block:
if __name__ == "__main__":
    automation = KITPortalAutomation("config.json")
    
    # Process multiple departments
    for dept in ["aids", "cse", "ece"]:
        automation.run(dept)
```

---

## 📊 Output Format

### Excel File Structure

| Photo | Roll Number | Status | Name | First Name | Last Name | Gender | DOB | Blood Group | ... |
|-------|------------|--------|------|------------|-----------|--------|-----|-------------|-----|
| 📷    | 711524BAD001 | Success | John Doe | John | Doe | Male | 01-01-2000 | O+ | ... |

**Columns include:**
- Basic Info: Roll, Name, Gender, DOB, Blood Group
- Academic: Branch, Regulation, Course details
- Personal: Father/Mother names, Phone, Email
- Address: Permanent, Communication, City, State, Pincode
- Identity: Aadhar, Nationality, Religion, Caste
- Photo: Embedded image in Excel

### File Naming
```
output_data/aids_20241015_143022.xlsx
            │    │        │
            │    │        └── Timestamp (HHMMSS)
            │    └── Date (YYYYMMDD)
            └── Department key
```

---

## 🔧 Customization

### 1. Change Selectors (if portal structure changes)

In `automation.py`, locate and modify:

```python
# Login selectors
roll_input = driver.find_element(By.ID, "username")
password_input = driver.find_element(By.ID, "password")

#