import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8091")

@pytest.fixture
def driver():
    options = Options()
    # Support both linux container path and windows host path
    if os.path.exists("/usr/bin/chromium"):
        options.binary_location = "/usr/bin/chromium"
        service = Service("/usr/bin/chromedriver")
    else:
        service = Service()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")
    options.add_argument("--user-data-dir=/tmp/chrome-test-profile")
    drv = webdriver.Chrome(service=service, options=options)
    yield drv
    drv.quit()

def test_page_title(driver):
    driver.get(BASE_URL)
    assert "FA23-BCT-029" in driver.title
    assert driver.title == "Assignment 3 - FA23-BCT-029"

def test_main_heading(driver):
    driver.get(BASE_URL)
    heading = driver.find_element(By.ID, "main-heading").text
    student_name = driver.find_element(By.ID, "student-name").text
    student_roll = driver.find_element(By.ID, "student-roll").text
    assert heading == "Automated CI/CD Web Application"
    assert student_name == "Muhammad Tallat"
    assert student_roll == "FA23-BCT-029"

def test_button_click(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "btn-message").click()
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "msg-display"), "Continuous Delivery")
    )
    msg = driver.find_element(By.ID, "msg-display").text
    assert "FA23-BCT-029" in msg
    assert msg == "Continuous Delivery Pipeline Active for FA23-BCT-029!"

def test_text_box_input(driver):
    driver.get(BASE_URL)
    test_message = "Automated Selenium Test Verification"
    input_box = driver.find_element(By.ID, "input-text")
    input_box.clear()
    input_box.send_keys(test_message)
    driver.find_element(By.ID, "btn-submit").click()
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "submitted-text"), "Echo: ")
    )
    result = driver.find_element(By.ID, "submitted-text").text
    assert result == f"Echo: {test_message}"
    driver.save_screenshot("screenshot.png")
