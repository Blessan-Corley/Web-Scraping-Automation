"""
FINAL TEST - Test complete flow with fixed automation
This tests 2 students to verify everything works
"""

import json
import sys
from automation import KITPortalAutomation
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def final_test():
    print("\n" + "="*70)
    print(" 🎯 FINAL TEST - Testing Fixed Automation")
    print("="*70)
    
    print("\nThis will test the complete flow with 2 students:")
    print("   1. 711524BAD001")
    print("   2. 711524BAD002")
    print("\nWhat gets tested:")
    print("   ✓ Login with improved click handling")
    print("   ✓ CAPTCHA solving")
    print("   ✓ Marksheet extraction")
    print("   ✓ Profile navigation")
    print("   ✓ Profile data extraction")
    print("   ✓ Photo download")
    print("   ✓ Excel generation with photos")
    print("   ✓ Logout")
    
    response = input("\n▶️  Continue with test? (y/n): ")
    if response.lower() != 'y':
        print("Test cancelled!")
        return
    
    try:
        # Initialize
        print("\n⚙️  Initializing automation...")
        automation = KITPortalAutomation("config.json")
        automation.setup_driver()
        
        # Test students
        test_rolls = ["711524BAD001", "711524BAD002"]
        all_data = []
        
        for idx, roll in enumerate(test_rolls, 1):
            print(f"\n{'='*70}")
            print(f" Testing {idx}/{len(test_rolls)}: {roll}")
            print(f"{'='*70}")
            
            student_data = automation.process_student(roll)
            all_data.append(student_data)
            
            # Show results
            status = student_data.get('status', 'Unknown')
            if status == 'Success':
                print(f"\n✅ {roll} - SUCCESS!")
                print(f"   Name: {student_data.get('name', 'N/A')}")
                print(f"   Courses: {len(student_data.get('courses', []))} found")
                print(f"   Photo: {'✓' if student_data.get('photo_path') else '✗'}")
            else:
                print(f"\n❌ {roll} - FAILED!")
                print(f"   Status: {status}")
        
        # Save results
        print(f"\n{'='*70}")
        print(" 💾 Saving Results")
        print(f"{'='*70}")
        
        output_file = "final_test_result.xlsx"
        automation.save_to_excel(all_data, output_file)
        
        # Summary
        success_count = sum(1 for s in all_data if s.get('status') == 'Success')
        
        print(f"\n{'='*70}")
        print(" 📊 TEST SUMMARY")
        print(f"{'='*70}")
        print(f"\n   Total Students: {len(test_rolls)}")
        print(f"   Successful: {success_count}")
        print(f"   Failed: {len(test_rolls) - success_count}")
        print(f"   Success Rate: {(success_count/len(test_rolls)*100):.1f}%")
        
        print(f"\n📁 Output Files:")
        print(f"   ✓ Excel: output_data/{output_file}")
        print(f"   ✓ Photos: output_data/photos/")
        print(f"   ✓ Log: automation.log")
        
        if success_count == len(test_rolls):
            print(f"\n{'='*70}")
            print(" 🎉 ALL TESTS PASSED!")
            print(f"{'='*70}")
            print("\n✅ Your automation is working perfectly!")
            print("\n🚀 Ready to process all students? Run:")
            print("   python automation.py")
            print("\n💡 Tips:")
            print("   • Check the Excel file to verify data quality")
            print("   • Review automation.log for any warnings")
            print("   • If you want to process more students, edit last line in automation.py")
            
        elif success_count > 0:
            print(f"\n{'='*70}")
            print(" ⚠️  PARTIAL SUCCESS")
            print(f"{'='*70}")
            print(f"\n{success_count}/{len(test_rolls)} students processed successfully")
            print("\n🔍 Check automation.log to see what failed")
            print("Common issues:")
            print("   • CAPTCHA misread (check captcha_temp.png)")
            print("   • Network timeout")
            print("   • Profile navigation issues")
            
        else:
            print(f"\n{'='*70}")
            print(" ❌ TEST FAILED")
            print(f"{'='*70}")
            print("\n⚠️ No students processed successfully")
            print("\n🔍 Troubleshooting:")
            print("   1. Check automation.log for errors")
            print("   2. Look at screenshot files:")
            print("      • login_failed_*.png")
            print("      • captcha_temp.png")
            print("   3. Verify credentials in config.json")
            print("   4. Test manual login in browser")
        
    except FileNotFoundError as e:
        print(f"\n❌ FILE ERROR: {e}")
        print("\n📋 Required files:")
        print("   ✓ config.json (with correct password)")
        print("   ✓ automation.py")
        print("   ✓ requirements.txt")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        print("\n📜 Full error:")
        traceback.print_exc()
        
    finally:
        if 'automation' in locals() and automation.driver:
            automation.driver.quit()
            print("\n🔒 Browser closed")


if __name__ == "__main__":
    final_test()