# 🚀 KIT Portal Automation - Quick Setup Guide

## ✅ What's Fixed in This Version

Based on diagnostic output, ALL selectors have been corrected:

- ✅ **Username field**: Changed to `By.ID, "username"` (Input #13)
- ✅ **Password field**: Changed to `By.ID, "password1"` (Input #14) 
- ✅ **CAPTCHA field**: Changed to `By.ID, "captcha"` (Input #15)
- ✅ **CAPTCHA image**: Uses `//img[contains(@src, 'captcha_images')]`
- ✅ **Login button**: Uses correct class selector
- ✅ **Readonly attribute**: Automatically removed before input
- ✅ **Better error handling**: Screenshots on failure + detailed logs

---

## 🎯 Step-by-Step Setup (5 Minutes)

### Step 1: Install Dependencies

```bash
# Make sure you're in the project directory
cd E:\Blessan\automation

# Activate virtual environment (if not already active)
venv\Scripts\activate

# Install/Update all dependencies
pip install -r requirements.txt
```

### Step 2: Configure Settings

```bash
# Copy the example config
copy config.example.json config.json

# Edit config.json and change:
# - "password": "kit@123"  (or whatever the actual password is)
# - Adjust roll number ranges if needed
```

### Step 3: Test with Single Student

```bash
# Run diagnostic test first (RECOMMENDED)
python test_single.py
```

**Expected Output:**
```
✓ All dependencies installed!
✓ config.json is valid JSON
✓ WebDriver initialized successfully
✓ Roll number entered: 711524BAD001
✓ Password entered
✓ CAPTCHA solved: ABC123
✓ CAPTCHA entered: ABC123
✓ Login button clicked
✓ Login successful for 711524BAD001
✓ Extracted marksheet data
✓ Navigated to profile page
✓ Downloaded photo for 711524BAD001
✓ Extracted profile data
✓ Successfully processed 711524BAD001
✓ Test completed successfully!
```

### Step 4: Run Full Automation

```bash
# Process all AI&DS students (180 students)
python automation.py
```

---

## 📊 Expected Results

After successful run, you'll find:

```
E:\Blessan\automation\
├── output_data/
│   ├── aids_20251015_230145.xlsx    ← Main Excel file with all data
│   └── photos/
│       ├── 711524BAD001.jpg
│       ├── 711524BAD002.jpg
│       └── ... (all student photos)
├── automation.log                    ← Detailed execution log
└── captcha_temp.png                  ← Last CAPTCHA (for debugging)
```

**Excel file contains:**
- Photo (embedded)
- Roll Number, Name, Register Number
- Personal details (DOB, Gender, Blood Group, etc.)
- Contact info (Mobile, Email, Alternative contacts)
- Academic info (Branch, Regulation, All course grades)
- Identity info (Aadhaar, PAN, Community, Caste, Religion, etc.)

---

## 🔍 Troubleshooting

### Issue 1: Login Still Failing

**Check the log file:**
```bash
# Windows - View last 20 lines
Get-Content automation.log -Tail 20

# Or open in notepad
notepad automation.log
```

**Look for screenshots:**
- `login_failed_711524BAD001.png` - See what page you're on
- Check if CAPTCHA is being solved correctly

**Manual verification:**
1. Open Chrome manually
2. Go to `https://portal.kitcbe.com/index.php/Login`
3. Try logging in with: `711524BAD001` / `kit@123`
4. Verify it works manually

### Issue 2: CAPTCHA Failing

**Check CAPTCHA quality:**
```bash
python test_captcha_only.py
```

This will:
- Test 5 CAPTCHAs
- Show you OCR accuracy
- Save CAPTCHA images for inspection

**If OCR accuracy < 80%:**
- CAPTCHAs might be too complex
- Consider manual CAPTCHA entry (I can add this feature)
- Or use 2Captcha API (paid service)

### Issue 3: Profile Navigation Failing

**Screenshots to check:**
- `profile_navigation_failed.png` - Profile button not found
- `profile_dropdown_failed.png` - Dropdown didn't open
- `wrong_profile_page.png` - Wrong page loaded

**Fix:**
The profile click selector might need adjustment. Send me the screenshot and I'll fix it.

### Issue 4: Excel File Too Large

**Reduce photo size:**
Edit `automation.py` line ~590:
```python
img.thumbnail((50, 50))  # Instead of (100, 100)
```

**Or skip photos entirely:**
Comment out the photo embedding section (lines ~575-608)

---

## 🎨 Customization

### Change Department

Edit last line in `automation.py`:
```python
automation.run("cse")  # Change "aids" to "cse", "ece", "mech", "civil"
```

### Process Multiple Departments

Edit the `__main__` block:
```python
if __name__ == "__main__":
    automation = KITPortalAutomation("config.json")
    
    for dept in ["aids", "cse", "ece"]:
        print(f"\n{'='*80}")
        print(f"Processing {dept.upper()} Department")
        print(f"{'='*80}")
        automation.run(dept)
        time.sleep(5)  # Pause between departments
```

### Process Specific Roll Numbers Only

Create `custom_test.py`:
```python
from automation import KITPortalAutomation

automation = KITPortalAutomation("config.json")
automation.setup_driver()

# Process only these students
roll_numbers = [
    "711524BAD001",
    "711524BAD005",
    "711524BAD010",
]

all_data = []
for roll in roll_numbers:
    data = automation.process_student(roll)
    all_data.append(data)

# Save results
automation.save_to_excel(all_data, "custom_batch.xlsx")
automation.driver.quit()
```

### Enable Headless Mode (No Browser Window)

Edit `automation.py` line ~74:
```python
options.add_argument('--headless')  # Uncomment this line
```

---

## 📝 Git Setup

### Initialize Git Repository

```bash
# Initialize git (if not already done)
git init

# Add the .gitignore file (already created)
git add .gitignore

# Add only necessary files
git add automation.py test_single.py requirements.txt README.md config.example.json

# Commit
git commit -m "Initial commit - KIT Portal Automation"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/kit-portal-automation.git

# Push
git push -u origin main
```

### What Gets Committed (Safe)

✅ **Will be committed:**
- `automation.py` - Main script
- `test_single.py` - Test script
- `diagnose_login.py` - Diagnostic tool
- `requirements.txt` - Dependencies
- `README.md` - Documentation
- `config.example.json` - Template config
- `.gitignore` - Git ignore rules

❌ **Will NOT be committed (protected):**
- `config.json` - Contains password
- `automation.log` - Contains student info
- `output_data/` - Student data & photos
- `*.png`, `*.jpg` - Screenshots & CAPTCHAs
- `venv/` - Virtual environment
- `__pycache__/` - Python cache
- Any Excel files

---

## ⚡ Performance Tips

### Speed Up Processing

1. **Reduce delays:**
```python
# In automation.py, reduce sleep times
time.sleep(1)  # Instead of time.sleep(2)
```

2. **Skip profile data:**
If you only need marksheet data, comment out profile extraction:
```python
# if self.navigate_to_profile():
#     profile_data = self.extract_profile_data(roll_number)
#     student_data.update(profile_data)
```

3. **Skip photos:**
Comment out photo download section (lines ~463-489)

### Process in Batches

```python
# Process 50 students at a time
roll_numbers = automation.generate_roll_numbers(dept_config)

for i in range(0, len(roll_numbers), 50):
    batch = roll_numbers[i:i+50]
    # Process batch...
```

---

## 📊 Success Metrics

**Good success rate:** > 95%
**Acceptable:** 85-95%
**Needs investigation:** < 85%

**Common failure reasons:**
1. CAPTCHA misread (~5-10% with simple CAPTCHAs)
2. Network timeout
3. Student data not available on portal
4. Portal structure changed

---

## 🆘 Getting Help

### Before Asking for Help

Run these checks:

```bash
# 1. Check Python version (need 3.8+)
python --version

# 2. Check Chrome is installed
# (Just open Chrome browser manually)

# 3. Check dependencies
pip list | findstr "selenium easyocr pandas openpyxl"

# 4. Run diagnostic
python diagnose_login.py

# 5. Test single student
python test_single.py

# 6. Check logs
type automation.log
```

### What to Share When Reporting Issues

1. **Error output** from terminal (copy-paste)
2. **Last 30 lines of automation.log**
3. **Screenshots** (`login_failed_*.png`, etc.)
4. **Your Python version** (`python --version`)
5. **What step failed** (login, profile, etc.)

---

## 🎉 You're All Set!

Run this to verify everything works:

```bash
# Quick test
python test_single.py
```

If you see **"✓ Test completed successfully!"**, you're ready to process all students!

```bash
# Full automation
python automation.py
```

**Estimated time:**
- 1 student: ~10 seconds
- 180 students: ~30 minutes

---

## 📞 Support Checklist

- [ ] Python 3.8+ installed
- [ ] Chrome browser installed  
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `config.json` created with correct password
- [ ] Virtual environment activated
- [ ] Test single student passed
- [ ] Logs reviewed for errors

If all checked ✓, run full automation!

**Good luck! 🚀**