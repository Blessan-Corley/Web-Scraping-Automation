"""
Test Enhanced CAPTCHA Solver
This will show you the preprocessing results
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageEnhance
import cv2
import numpy as np
import easyocr
import re
import time

def preprocess_and_test():
    print("\n" + "="*70)
    print(" 🧪 ENHANCED CAPTCHA TEST")
    print("="*70)
    
    # Setup browser
    options = Options()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    reader = easyocr.Reader(['en'], gpu=False)
    
    try:
        print("\n📡 Loading portal...")
        driver.get("https://portal.kitcbe.com/index.php/Login")
        time.sleep(3)
        
        # Get CAPTCHA
        print("📸 Capturing CAPTCHA...")
        captcha_img = driver.find_element(By.XPATH, "//img[contains(@src, 'captcha_images')]")
        captcha_img.screenshot('captcha_original.png')
        print("   ✓ Saved: captcha_original.png")
        
        # Method 1: Enhanced contrast
        print("\n🔧 Method 1: Enhanced Contrast")
        img = Image.open('captcha_original.png')
        img = img.convert('RGB')
        
        # Resize 2x
        w, h = img.size
        img = img.resize((w*2, h*2), Image.Resampling.LANCZOS)
        
        # Aggressive contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(3.0)
        
        # Grayscale
        img = img.convert('L')
        
        # Save
        img.save('captcha_method1.png')
        
        # OCR
        result1 = reader.readtext('captcha_method1.png', detail=0)
        text1 = ''.join(result1).strip() if result1 else ''
        text1 = re.sub(r'[^A-Za-z0-9]', '', text1)
        print(f"   Result: {text1}")
        
        # Method 2: OpenCV Adaptive Threshold
        print("\n🔧 Method 2: Adaptive Threshold")
        img = Image.open('captcha_original.png')
        img = img.convert('L')
        
        # Convert to numpy
        img_array = np.array(img)
        
        # Resize
        img_array = cv2.resize(img_array, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        
        # Bilateral filter
        img_array = cv2.bilateralFilter(img_array, 9, 75, 75)
        
        # Adaptive threshold
        img_array = cv2.adaptiveThreshold(
            img_array, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Save
        cv2.imwrite('captcha_method2.png', img_array)
        
        # OCR
        result2 = reader.readtext('captcha_method2.png', detail=0)
        text2 = ''.join(result2).strip() if result2 else ''
        text2 = re.sub(r'[^A-Za-z0-9]', '', text2)
        print(f"   Result: {text2}")
        
        # Method 3: OTSU Threshold
        print("\n🔧 Method 3: OTSU Threshold")
        img_array = cv2.imread('captcha_original.png', cv2.IMREAD_GRAYSCALE)
        
        # Resize
        img_array = cv2.resize(img_array, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        
        # Denoise
        img_array = cv2.fastNlMeansDenoising(img_array, None, 10, 7, 21)
        
        # OTSU threshold
        _, img_array = cv2.threshold(img_array, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Save
        cv2.imwrite('captcha_method3.png', img_array)
        
        # OCR
        result3 = reader.readtext('captcha_method3.png', detail=0)
        text3 = ''.join(result3).strip() if result3 else ''
        text3 = re.sub(r'[^A-Za-z0-9]', '', text3)
        print(f"   Result: {text3}")
        
        # Method 4: With allowlist
        print("\n🔧 Method 4: Original + Allowlist")
        result4 = reader.readtext(
            'captcha_original.png',
            detail=0,
            allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        )
        text4 = ''.join(result4).strip() if result4 else ''
        text4 = re.sub(r'[^A-Za-z0-9]', '', text4)
        print(f"   Result: {text4}")
        
        # Summary
        print("\n" + "="*70)
        print(" 📊 RESULTS SUMMARY")
        print("="*70)
        
        results = [
            ('Method 1 (Contrast)', text1),
            ('Method 2 (Adaptive)', text2),
            ('Method 3 (OTSU)', text3),
            ('Method 4 (Allowlist)', text4)
        ]
        
        for method, text in results:
            status = "✓" if 4 <= len(text) <= 6 else "✗"
            print(f"   {status} {method:20s}: {text:10s} ({len(text)} chars)")
        
        print("\n📁 Check these images:")
        print("   • captcha_original.png  (raw)")
        print("   • captcha_method1.png   (contrast)")
        print("   • captcha_method2.png   (adaptive)")
        print("   • captcha_method3.png   (OTSU)")
        
        print("\n👀 MANUAL CHECK:")
        print(f"   Look at the CAPTCHA in the browser")
        actual = input("   What is the actual CAPTCHA text? ").strip().upper()
        
        print("\n📊 ACCURACY CHECK:")
        for method, text in results:
            match = "✅ CORRECT" if text.upper() == actual else f"❌ WRONG (got {text})"
            print(f"   {method:20s}: {match}")
        
        # Find best method
        correct_methods = [m for m, t in results if t.upper() == actual]
        if correct_methods:
            print(f"\n🎯 BEST METHOD: {correct_methods[0]}")
            print("   We'll use this in the automation!")
        else:
            print(f"\n⚠️ None of the methods got it right")
            print("   The CAPTCHA might be too complex for OCR")
            print("   Consider manual CAPTCHA entry or 2Captcha API")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        input("\n⏸️  Press Enter to close...")
        driver.quit()

if __name__ == "__main__":
    preprocess_and_test()