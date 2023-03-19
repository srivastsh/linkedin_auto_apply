from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set your LinkedIn credentials
EMAIL = 'email'
PASSWORD = 'password'

# Set the WebDriver path
WEBDRIVER_PATH = '/Users/shagun/Desktop/chromedriver_mac_arm64/chromedriver'

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(executable_path=WEBDRIVER_PATH))

# Open LinkedIn
driver.get('https://www.linkedin.com')

# Wait for the login page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'session_key')))

# Log in
email_input = driver.find_element(By.NAME, 'session_key')
email_input.send_keys(EMAIL)
password_input = driver.find_element(By.NAME, 'session_password')
password_input.send_keys(PASSWORD)
password_input.submit()

# Wait for login to complete
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//nav[contains(@class, 'global-nav')]")))

# Search for jobs
search_input = driver.find_element(By.XPATH, "//input[@placeholder='Search']")
search_input.send_keys('DevOps')  # Add the desired job title
search_input.send_keys(Keys.ENTER)

# Wait for jobs page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search jobs']")))

# Filter jobs by 'Easy Apply'
filter_button = driver.find_element_by_xpath("//button[@aria-label='Filter results by:']")
filter_button.click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='linkedin-features-facet-values-EasyApply-checkbox']")))

easy_apply_checkbox = driver.find_element_by_xpath("//input[@id='linkedin-features-facet-values-EasyApply-checkbox']")
easy_apply_checkbox.click()

# Wait for the Easy Apply filter to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'job-card-list__title')]")))

# Apply for jobs
while True:
    job_elements = driver.find_elements_by_xpath("//div[contains(@class, 'job-card-list__title')]")

    for job_element in job_elements:
        try:
            job_element.click()
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'jobs-apply-button')]")))
            apply_button = driver.find_element_by_xpath("//button[contains(@class, 'jobs-apply-button')]")
            apply_button.click()
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'jobs-easy-apply-footer')]")))
            submit_button = driver.find_element_by_xpath("//button[contains(@class, 'jobs-easy-apply-footer')]")
            submit_button.click()
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'artdeco-toast-item__dismiss')]")))
            close_toast_button = driver.find_element_by_xpath("//button[contains(@class, 'artdeco-toast-item__dismiss')]")
            close_toast_button.click()
        except Exception as e:
            print(e)
            continue

    # Check for next page and navigate
    try:
        next_page = driver.find_element_by_xpath("//button[@aria-label='Next']")
        next_page.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'job-card-list__title')]")))
    except Exception as e:
        print("No more pages or an error occurred:", e)
        break

        # Close the WebDriver
    driver.quit()
