from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://portal.kitcbe.com/index.php/Login")
time.sleep(2)

# Enter username (removes readonly on focus)
username = driver.find_element(By.ID, "username")
username.click()
username.send_keys("711524BAD001")

# Enter password (need to remove readonly)
password = driver.find_element(By.ID, "password")
driver.execute_script("arguments[0].removeAttribute('readonly');", password)
time.sleep(0.3)
password.send_keys("kit@123")

# Captcha
driver.find_element(By.ID, "captcha").send_keys("TEST123")

# Check login button
login_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
print("Button onclick:", login_btn.get_attribute("onclick"))
print("Button type:", login_btn.get_attribute("type"))

input("Press Enter...")
driver.quit()