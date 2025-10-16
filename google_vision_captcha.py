"""
Google Vision API CAPTCHA Solver
Uses your API key to solve CAPTCHAs with high accuracy
"""

import requests
import base64
import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)


class GoogleVisionCaptchaSolver:
    """Solve CAPTCHA using Google Cloud Vision API"""
    
    def __init__(self, api_key: str):
        """
        Initialize with API key
        Args:
            api_key: Google Cloud Vision API key
        """
        self.api_key = api_key
        self.api_url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
        logger.info("✓ Google Vision CAPTCHA solver initialized")
    
    def solve_captcha(self, image_path: str) -> Optional[str]:
        """
        Solve CAPTCHA from image file
        
        Args:
            image_path: Path to CAPTCHA image file
            
        Returns:
            CAPTCHA text or None if failed
        """
        try:
            logger.info(f"🔍 Solving CAPTCHA with Google Vision...")
            
            # Read and encode image to base64
            with open(image_path, 'rb') as image_file:
                image_content = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Prepare API request
            request_body = {
                "requests": [
                    {
                        "image": {
                            "content": image_content
                        },
                        "features": [
                            {
                                "type": "TEXT_DETECTION",
                                "maxResults": 10
                            }
                        ]
                    }
                ]
            }
            
            # Call Google Vision API
            response = requests.post(
                self.api_url,
                json=request_body,
                timeout=30
            )
            
            if response.status_code != 200:
                logger.error(f"❌ Google Vision API error: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return None
            
            # Parse response
            result = response.json()
            
            if 'responses' not in result or not result['responses']:
                logger.warning("⚠️ No response from Google Vision")
                return None
            
            response_data = result['responses'][0]
            
            if 'textAnnotations' not in response_data:
                logger.warning("⚠️ No text detected in CAPTCHA")
                return None
            
            # Get detected text (first annotation is the full text)
            detected_text = response_data['textAnnotations'][0]['description']
            
            # Clean up the text
            captcha_text = self._clean_captcha_text(detected_text)
            
            if captcha_text:
                logger.info(f"✅ Google Vision solved: '{captcha_text}' (length: {len(captcha_text)})")
                return captcha_text
            else:
                logger.warning("⚠️ Cleaned CAPTCHA text is empty")
                return None
            
        except requests.exceptions.Timeout:
            logger.error("❌ Google Vision API timeout")
            return None
        except Exception as e:
            logger.error(f"❌ Error solving CAPTCHA: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return None
    
    def _clean_captcha_text(self, text: str) -> Optional[str]:
        """
        Clean and validate CAPTCHA text
        
        Args:
            text: Raw text from OCR
            
        Returns:
            Cleaned CAPTCHA text or None
        """
        if not text:
            return None
        
        # Remove whitespace and newlines
        text = text.strip().replace('\n', '').replace(' ', '').replace('\r', '')
        
        # Remove any non-alphanumeric characters
        text = re.sub(r'[^A-Za-z0-9]', '', text)
        
        # Validate length (typical CAPTCHA is 4-6 characters)
        if 3 <= len(text) <= 7:
            return text
        
        logger.warning(f"⚠️ Invalid CAPTCHA length: {len(text)} (text: '{text}')")
        return None
    
    def test_api_key(self) -> bool:
        """
        Test if API key is valid
        
        Returns:
            True if API key works, False otherwise
        """
        try:
            logger.info("🧪 Testing Google Vision API key...")
            
            # Create a simple test image (1x1 white pixel)
            test_image = base64.b64encode(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x00\x00\x00\x00IEND\xaeB`\x82').decode('utf-8')
            
            request_body = {
                "requests": [{
                    "image": {"content": test_image},
                    "features": [{"type": "TEXT_DETECTION"}]
                }]
            }
            
            response = requests.post(self.api_url, json=request_body, timeout=10)
            
            if response.status_code == 200:
                logger.info("✅ API key is valid!")
                return True
            else:
                logger.error(f"❌ API key test failed: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ API key test error: {e}")
            return False


# Test function
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test with your API key
    api_key = "AIzaSyBiAno0bQ9PtrhUNvJ-lVeD8EyBEBFyrcs"
    solver = GoogleVisionCaptchaSolver(api_key)
    
    # Test API key
    if solver.test_api_key():
        print("\n✅ API key is working!")
        print("\nYou can now run the automation with Google Vision.")
    else:
        print("\n❌ API key test failed!")
        print("Please check:")
        print("  1. API key is correct")
        print("  2. Cloud Vision API is enabled")
        print("  3. Billing is enabled (free tier works)")