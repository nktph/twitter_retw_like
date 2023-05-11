import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

login="PamatiSina13435"
password="fsdjkhsdkfjHHT67"
ACCOUNT = "iamcardib"

driver = webdriver.Chrome()
driver.get("https://twitter.com/i/flow/login")
wait = WebDriverWait(driver, 20)
login_field = wait.until(EC.element_to_be_clickable((By.NAME, 'text')))
login_field.click()
login_field.send_keys(login)
next_btn = driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div/span/span')
next_btn.click()
password_field = wait.until(EC.element_to_be_clickable((By.NAME, "password")))
password_field.click()
password_field.send_keys(password)
login_btn = driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div/span/span')
login_btn.click()
time.sleep(10)
driver.get(f"https://twitter.com/{ACCOUNT}")

driver.quit()