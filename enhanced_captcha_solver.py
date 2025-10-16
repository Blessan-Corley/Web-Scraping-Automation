"""
Enhanced CAPTCHA Solving with Image Preprocessing
Handles overlapping/stylized text better
"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import easyocr
import re

class EnhancedCaptchaSolver:
    """Improved CAPTCHA solver with image preprocessing"""
    
    def __init__(self):
        self.reader = easyocr.Reader(['en'], gpu=False)
    
    def preprocess_captcha(self, image_path: str) -> str:
        """
        Preprocess CAPTCHA image for better OCR accuracy
        Handles overlapping letters and stylized fonts
        """
        # Load image
        img = Image.open(image_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Method 1: Enhanced contrast + sharpening
        processed1 = self._method_contrast_sharpen(img)
        result1 = self._ocr_image(processed1)
        
        # Method 2: Grayscale + threshold
        processed2 = self._method_grayscale_threshold(img)
        result2 = self._ocr_image(processed2)
        
        # Method 3: Denoise + enhance
        processed3 = self._method_denoise(img)
        result3 = self._ocr_image(processed3)
        
        # Method 4: Binary threshold with morphology
        processed4 = self._method_morphology(img)
        result4 = self._ocr_image(processed4)
        
        # Save all processed versions for debugging
        processed1.save('captcha_method1.png')
        processed2.save('captcha_method2.png')
        processed3.save('captcha_method3.png')
        processed4.save('captcha_method4.png')
        
        # Try all results and pick the best one
        results = [result1, result2, result3, result4]
        best_result = self._choose_best_result(results)
        
        return best_result
    
    def _method_contrast_sharpen(self, img: Image.Image) -> Image.Image:
        """Method 1: Enhance contrast and sharpen"""
        # Increase contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.5)
        
        # Sharpen
        img = img.filter(ImageFilter.SHARPEN)
        img = img.filter(ImageFilter.SHARPEN)  # Apply twice
        
        # Increase brightness slightly
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.2)
        
        return img
    
    def _method_grayscale_threshold(self, img: Image.Image) -> Image.Image:
        """Method 2: Grayscale with adaptive threshold"""
        # Convert to grayscale
        img = img.convert('L')
        
        # Convert to numpy array for OpenCV
        img_array = np.array(img)
        
        # Apply adaptive threshold
        img_array = cv2.adaptiveThreshold(
            img_array, 255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Convert back to PIL
        img = Image.fromarray(img_array)
        
        # Enhance
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)
        
        return img
    
    def _method_denoise(self, img: Image.Image) -> Image.Image:
        """Method 3: Denoise and enhance"""
        # Convert to numpy for OpenCV
        img_array = np.array(img)
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Denoise
        img_array = cv2.fastNlMeansDenoisingColored(img_array, None, 10, 10, 7, 21)
        
        # Convert to grayscale
        img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
        
        # Increase contrast
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        img_array = clahe.apply(img_array)
        
        # Threshold
        _, img_array = cv2.threshold(img_array, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Convert back to PIL
        img = Image.fromarray(img_array)
        
        return img
    
    def _method_morphology(self, img: Image.Image) -> Image.Image:
        """Method 4: Morphological operations"""
        # Convert to grayscale
        img_array = np.array(img.convert('L'))
        
        # Binary threshold
        _, img_array = cv2.threshold(img_array, 127, 255, cv2.THRESH_BINARY)
        
        # Morphological operations to separate overlapping characters
        kernel = np.ones((2,2), np.uint8)
        img_array = cv2.morphologyEx(img_array, cv2.MORPH_CLOSE, kernel)
        img_array = cv2.morphologyEx(img_array, cv2.MORPH_OPEN, kernel)
        
        # Dilate slightly to make text bolder
        kernel = np.ones((1,1), np.uint8)
        img_array = cv2.dilate(img_array, kernel, iterations=1)
        
        # Convert back to PIL
        img = Image.fromarray(img_array)
        
        return img
    
    def _ocr_image(self, img: Image.Image) -> str:
        """Run OCR on processed image"""
        # Save temp file for EasyOCR
        temp_path = 'temp_captcha_ocr.png'
        img.save(temp_path)
        
        try:
            result = self.reader.readtext(temp_path, detail=0)
            if result:
                text = ''.join(result).strip()
                # Clean up - remove spaces and special chars
                text = re.sub(r'[^A-Za-z0-9]', '', text)
                return text
            return ""
        except:
            return ""
    
    def _choose_best_result(self, results: list) -> str:
        """
        Choose the best OCR result from multiple attempts
        Priority: Length between 4-6 chars, alphanumeric only
        """
        # Filter valid results (4-6 characters, alphanumeric)
        valid_results = []
        for r in results:
            if r and 4 <= len(r) <= 6 and r.isalnum():
                valid_results.append(r)
        
        if not valid_results:
            # If no valid results, return longest non-empty result
            valid_results = [r for r in results if r]
            if valid_results:
                return max(valid_results, key=len)
            return ""
        
        # If multiple valid results, use voting/most common
        from collections import Counter
        
        # Count character frequency at each position
        if len(valid_results) == 1:
            return valid_results[0]
        
        # Return the most common length result
        counter = Counter(valid_results)
        most_common = counter.most_common(1)[0][0]
        
        return most_common
    
    def solve_captcha(self, image_path: str, save_debug: bool = True) -> str:
        """
        Main method to solve CAPTCHA
        Returns: CAPTCHA text or None if failed
        """
        try:
            captcha_text = self.preprocess_captcha(image_path)
            
            if captcha_text and 4 <= len(captcha_text) <= 6:
                return captcha_text
            
            return None
            
        except Exception as e:
            print(f"Error solving CAPTCHA: {e}")
            return None


# Test function
if __name__ == "__main__":
    solver = EnhancedCaptchaSolver()
    
    # Test with your captcha
    result = solver.solve_captcha('captcha_temp.png')
    print(f"\nCAPTCHA Result: {result}")
    print(f"\nCheck these processed images:")
    print("  - captcha_method1.png (contrast + sharpen)")
    print("  - captcha_method2.png (grayscale + threshold)")
    print("  - captcha_method3.png (denoise)")
    print("  - captcha_method4.png (morphology)")
    print("\nPick the clearest one and we'll use that method!")
    
    input("\nPress Enter to exit...")