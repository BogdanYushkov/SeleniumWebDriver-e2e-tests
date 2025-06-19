import pytest
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.utils.api_client import TracksAPIClient


@pytest.fixture(scope="session")
def driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:3000"

@pytest.fixture(scope="session")
def api_client():
    return TracksAPIClient()

@pytest.fixture
def unique_project_name():
    return f"test_project_{uuid.uuid4().hex[:8]}"

@pytest.fixture
def login(driver, base_url):
    driver.get(f"{base_url}/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "user_login")))
    driver.find_element(By.NAME, "user_login").send_keys("admin")
    driver.find_element(By.NAME, "user_password").send_keys("1234567890")
    driver.find_element(By.NAME, "commit").click()
    WebDriverWait(driver, 10).until(lambda d: "/login" not in d.current_url)
