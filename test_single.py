"""
Test Script - Process single student to verify everything works
FIXED VERSION with correct selectors
"""

import json
from automation import KITPortalAutomation
import logging
import sys

# Setup logging to console only
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_single_student():
    """Test with a single student"""
    
    print("\n" + "="*70)
    print(" 🧪 TEST MODE - Single Student Processing")
    print("="*70)
    
    # Test roll number
    test_roll = "711524BAD001"
    
    print(f"\n📋 Testing with roll number: {test_roll}")
    print("\n This will:")
    print("   1. ✓ Login to portal with FIXED selectors")
    print("   2. ✓ Extract marksheet data")
    print("   3. ✓ Navigate to profile")
    print("   4. ✓ Extract profile data and download photo")
    print("   5. ✓ Save everything to Excel")
    print("\n" + "="*70)
    
    response = input("\n▶️  Continue? (y/n): ")
    if response.lower() != 'y':
        print("Test cancelled!")
        return
    
    try:
        # Initialize automation
        print("\n⚙️  Initializing automation...")
        automation = KITPortalAutomation("config.json")
        automation.setup_driver()
        
        # Process single student
        print("\n🚀 Starting test...")
        print("="*70)
        student_data = automation.process_student(test_roll)
        
        # Display results
        print("\n" + "="*70)
        print(" 📊 RESULTS")
        print("="*70)
        
        if student_data.get('status') == 'Success':
            print("\n✅ SUCCESS! Data extracted:")
            
            print(f"\n📄 MARKSHEET DATA:")
            print(f"   Name: {student_data.get('name', 'N/A')}")
            print(f"   Register Number: {student_data.get('register_number', 'N/A')}")
            print(f"   Branch: {student_data.get('branch', 'N/A')}")
            print(f"   Gender: {student_data.get('gender', 'N/A')}")
            print(f"   DOB: {student_data.get('dob', 'N/A')}")
            print(f"   Regulation: {student_data.get('regulation', 'N/A')}")
            
            print(f"\n👤 PROFILE DATA:")
            print(f"   First Name: {student_data.get('first_name', 'N/A')}")
            print(f"   Last Name: {student_data.get('last_name', 'N/A')}")
            print(f"   Mobile: {student_data.get('mobile', 'N/A')}")
            print(f"   Email: {student_data.get('email', 'N/A')}")
            print(f"   Blood Group: {student_data.get('blood_group', 'N/A')}")
            print(f"   Community: {student_data.get('community', 'N/A')}")
            print(f"   Photo Path: {student_data.get('photo_path', 'N/A')}")
            
            courses = student_data.get('courses', [])
            print(f"\n📚 COURSES: {len(courses)} found")
            if courses:
                print("   Sample courses:")
                for i, course in enumerate(courses[:3], 1):
                    print(f"   {i}. {course.get('course_name', 'N/A')} - Grade: {course.get('grade', 'N/A')}")
                if len(courses) > 3:
                    print(f"   ... and {len(courses) - 3} more courses")
            
            # Count filled fields
            total_fields = len(student_data)
            filled_fields = sum(1 for v in student_data.values() if v and v != '')
            percentage = (filled_fields / total_fields * 100) if total_fields > 0 else 0
            print(f"\n📊 Data completeness: {filled_fields}/{total_fields} fields ({percentage:.1f}%)")
            
            # Save to Excel
            print("\n💾 Saving to Excel...")
            automation.save_to_excel([student_data], f"test_{test_roll}.xlsx")
            
            print("\n" + "="*70)
            print(" ✅ TEST COMPLETED SUCCESSFULLY!")
            print("="*70)
            print("\n📁 Output files created:")
            print(f"   ✓ Excel file: output_data/test_{test_roll}.xlsx")
            if student_data.get('photo_path'):
                print(f"   ✓ Photo: {student_data.get('photo_path')}")
            print(f"   ✓ Log file: automation.log")
            
            print("\n🎯 Next Steps:")
            print("   ✓ Open the Excel file to verify data")
            print("   ✓ Check if photo is embedded correctly")
            print("   ✓ Review automation.log for any warnings")
            print("\n   Ready to process all students? Run:")
            print("   → python automation.py")
            
        else:
            print("\n❌ TEST FAILED!")
            print(f"   Status: {student_data.get('status')}")
            
            print("\n🔍 Troubleshooting Steps:")
            print("   1. Check automation.log for detailed errors:")
            print("      → notepad automation.log")
            
            print("\n   2. Look for screenshot files:")
            print("      → login_failed_711524BAD001.png")
            print("      → profile_navigation_failed.png")
            
            print("\n   3. Verify credentials:")
            print(f"      → Roll number: {test_roll}")
            print("      → Password: kit@123 (check config.json)")
            
            print("\n   4. Test manual login:")
            print("      → Open portal.kitcbe.com in browser")
            print("      → Try logging in manually")
            
            print("\n   5. Check network connection")
            
            # Show partial data if available
            if student_data.get('name'):
                print(f"\n⚠️  Partial data was extracted:")
                print(f"   Name: {student_data.get('name')}")
                print(f"   Register: {student_data.get('register_number')}")
                print("\n   This means LOGIN WORKED but profile navigation failed.")
                print("   The profile selectors might need adjustment.")
            
            print("\n📋 Common Issues:")
            print("   • CAPTCHA misread - Check captcha_temp.png")
            print("   • Wrong password - Verify in config.json")
            print("   • Network timeout - Check internet connection")
            print("   • Portal structure changed - Run diagnose_login.py")
            
    except FileNotFoundError as e:
        print(f"\n❌ FILE NOT FOUND: {e}")
        print("\n📋 Make sure you have:")
        print("   ✓ config.json (copy from config.example.json)")
        print("   ✓ automation.py")
        print("   ✓ requirements.txt")
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        print("\n🔍 System Check:")
        print("   1. Chrome browser installed?")
        print("   2. Internet connection active?")
        print("   3. config.json exists and valid?")
        print("   4. All dependencies installed?")
        print("      → pip install -r requirements.txt")
        
        import traceback
        print("\n📜 Full error trace:")
        print("-" * 70)
        traceback.print_exc()
        print("-" * 70)
        
    finally:
        if 'automation' in locals() and automation.driver:
            automation.driver.quit()
            print("\n🔒 Browser closed")


def test_config():
    """Test if configuration is valid"""
    print("\n" + "="*70)
    print(" ⚙️  TESTING CONFIGURATION")
    print("="*70)
    
    try:
        with open("config.json", 'r') as f:
            config = json.load(f)
        
        print("\n✅ config.json is valid JSON")
        
        # Check required fields
        required_fields = {
            'portal': ['base_url', 'password'],
            'departments': [],
            'output': ['directory']
        }
        
        missing = []
        for section, fields in required_fields.items():
            if section not in config:
                missing.append(section)
            else:
                for field in fields:
                    if field not in config[section]:
                        missing.append(f"{section}.{field}")
        
        if missing:
            print(f"\n⚠️  Missing fields: {', '.join(missing)}")
            return False
        
        print(f"\n🏢 Departments configured:")
        for key, dept in config['departments'].items():
            count = dept['end'] - dept['start'] + 1
            print(f"   {key.upper()}: {dept['name']}")
            print(f"      • {count} students")
            print(f"      • Roll numbers: {dept['prefix']}{dept['start']:03d} to {dept['prefix']}{dept['end']:03d}")
        
        print(f"\n🔐 Portal Settings:")
        print(f"   URL: {config['portal']['base_url']}")
        print(f"   Password: {'*' * len(config['portal']['password'])} ({len(config['portal']['password'])} chars)")
        
        print(f"\n📁 Output Directory: {config['output']['directory']}")
        
        return True
        
    except FileNotFoundError:
        print("\n❌ config.json not found!")
        print("\n📋 Create it by copying config.example.json:")
        print("   copy config.example.json config.json")
        print("   Then edit and add your password")
        return False
        
    except json.JSONDecodeError as e:
        print(f"\n❌ config.json is invalid JSON: {e}")
        print("\n📋 Check for:")
        print("   • Missing commas")
        print("   • Unclosed brackets")
        print("   • Invalid syntax")
        return False


def check_dependencies():
    """Check if all required packages are installed"""
    print("\n" + "="*70)
    print(" 📦 CHECKING DEPENDENCIES")
    print("="*70)
    
    required = {
        'selenium': 'selenium',
        'easyocr': 'easyocr',
        'pandas': 'pandas',
        'openpyxl': 'openpyxl',
        'PIL': 'Pillow',
        'requests': 'requests'
    }
    
    missing = []
    installed = []
    
    for module, package in required.items():
        try:
            __import__(module)
            installed.append(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print(f"\n   Install with: pip install {' '.join(missing)}")
        return False
    
    print("\n✅ All dependencies installed!")
    return True


if __name__ == "__main__":
    print("\n🧪 KIT PORTAL AUTOMATION - TEST MODE")
    print("="*70)
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("\n❌ Install missing dependencies first!")
        exit(1)
    
    # Step 2: Check config
    if not test_config():
        print("\n❌ Fix config.json first!")
        exit(1)
    
    # Step 3: Test single student
    test_single_student()