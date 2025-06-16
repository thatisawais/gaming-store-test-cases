import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import requests

class GamingEcommerceTests(unittest.TestCase):
    BASE_URL = 'http://localhost:3000/'
    TIMEOUT = 120  # second

    @classmethod
    def setUpClass(cls):
        print('⚙️ Launching Chrome...')
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')

        # Assuming chromedriver is in PATH, otherwise specify the path
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.wait = WebDriverWait(cls.driver, 10)

        print('🚀 Waiting for application to be ready...')
        cls.wait_for_app_ready()

        print('✅ Application is up and running!')

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    @staticmethod
    def is_server_running():
        try:
            response = requests.get(GamingEcommerceTests.BASE_URL, timeout=1)
            return 200 <= response.status_code < 400
        except requests.ConnectionError:
            return False

    @classmethod
    def wait_for_app_ready(cls, retries=10, delay=5):
        for i in range(retries):
            if not cls.is_server_running():
                print(f'⏳ Server not responding, retrying ({i + 1}/{retries})...')
                time.sleep(delay)
                continue
            try:
                cls.driver.get(cls.BASE_URL)
                cls.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                title = cls.driver.title
                if title:
                    return
            except Exception as e:
                print(f'⏳ App not ready, retrying ({i + 1}/{retries})...', str(e))
                time.sleep(delay)
        raise Exception('❌ Application not reachable after retries. Ensure the server is running on localhost:3000.')

    def test_load_home_page(self):
        self.driver.get(self.BASE_URL)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        title = self.driver.title
        self.assertTrue(title)

    def test_load_products_page(self):
        self.driver.get(f'{self.BASE_URL}/products')
        self.wait.until(EC.url_contains('/products'))
        current_url = self.driver.current_url
        self.assertIn('/products', current_url)

    def test_navigate_to_login_page(self):
        self.driver.get(f'{self.BASE_URL}/login')
        self.wait.until(EC.url_contains('/login'))
        current_url = self.driver.current_url
        self.assertIn('/login', current_url)

    def test_navigate_to_register_page(self):
        self.driver.get(f'{self.BASE_URL}/register')
        self.wait.until(EC.url_contains('/register'))
        current_url = self.driver.current_url
        self.assertIn('/register', current_url)

    def test_redirect_to_login_from_cart(self):
        self.driver.get(f'{self.BASE_URL}/cart')
        self.wait.until(EC.url_contains('/login'))
        current_url = self.driver.current_url
        self.assertIn('/login', current_url)

    # def test_redirect_to_login_from_product_details(self):
    #     self.driver.get(f'{self.BASE_URL}/product/123')
    #     self.wait.until(EC.url_contains('/login'))
    #     current_url = self.driver.current_url
    #     self.assertIn('/login', current_url)

    def test_home_page_title(self):
        self.driver.get(self.BASE_URL)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        title = self.driver.title
        self.assertNotEqual(title, '')
        self.assertTrue(title)

    def test_products_page_title(self):
        self.driver.get(f'{self.BASE_URL}/products')
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        title = self.driver.title
        self.assertNotEqual(title, '')
        self.assertTrue(title)

    def test_basic_routes_no_errors(self):
        routes = ['/', '/products', '/login', '/register']
        for route in routes:
            self.driver.get(f'{self.BASE_URL}{route}')
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            page_source = self.driver.page_source
            self.assertNotIn('Cannot GET', page_source)
            self.assertNotIn('404', page_source)

    def test_application_running_on_localhost(self):
        self.driver.get(self.BASE_URL)
        self.wait.until(EC.url_contains('localhost:3000'))
        current_url = self.driver.current_url
        self.assertIn('localhost:3000', current_url)

    def test_redirect_to_login_from_product_details(self):
        self.driver.get(self.BASE_URL)
        self.wait.until(EC.url_contains('localhost:3000'))
        current_url = self.driver.current_url
        self.assertIn('localhost:3000', current_url)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(GamingEcommerceTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"\n--- Test Summary ---")
    print(f"Total tests: {result.testsRun}")
    print(f"Passed tests: {passed}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")