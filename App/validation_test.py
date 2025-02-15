import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import string
import random

class TestTodoAppBasic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.base_url = "http://localhost:5000"
        cls.username = f"test_user_{''.join(random.choices(string.ascii_lowercase, k=5))}"
        cls.password = "test123"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_01_homepage_accessibility(self):
        driver = self.driver
        driver.get(self.base_url)
        self.assertTrue(driver.title != "", "The homepage should have a title.")

    def test_02_register_page_load(self):
        driver = self.driver
        driver.get(f"{self.base_url}/register")
        # Wait for the username field to load
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        self.assertIsNotNone(username_field, "The registration page should contain a username field.")

    def test_03_registration_form_submission(self):
        """Part 3: Fill out and submit the registration form"""
        driver = self.driver
        driver.get(f"{self.base_url}/register")
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_field = driver.find_element(By.NAME, "password")
        
        username_field.send_keys(self.username)
        password_field.send_keys(self.password)
        
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()

    def test_04_redirect_to_login(self):
        """Part 4: Verify that the user is redirected to the login page after registration"""
        driver = self.driver
        # Wait for the login page to load
        WebDriverWait(driver, 20).until(
            lambda driver: driver.current_url.endswith('/login')
        )
        self.assertTrue(driver.current_url.endswith('/login'), "After registration, the user should be redirected to the /login page.")

if __name__ == "__main__":
    unittest.main()