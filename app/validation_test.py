import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestLocationResponse(unittest.TestCase):

    def setUp(self):
        chromedriver_bin = "/usr/local/bin/chromedriver"

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(executable_path=chromedriver_bin)

        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get("http://10.0.4.150:5000")
        self.search_input = self.driver.find_element(By.NAME, "query")

    def test_valid_location(self):

        self.search_input.send_keys("Tel Aviv")
        self.search_input.submit()
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Tel Aviv, Israel")
        )
        self.assertIn("Tel Aviv, Israel", self.driver.page_source)

    def test_invalid_location(self):
        self.search_input.send_keys("not")
        self.search_input.submit()
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, "body"), "Failed to fetch data"
            )
        )
        self.assertIn("Failed to fetch data", self.driver.page_source)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
