import json
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATTERN = r'^(?!\s*$).{1,1024}$'

class Test_single_us:

    def single_us_tc_1(self, driver):
        """
        Insert a user story that does not match the expected regex pattern.
        Verifies that an alert with the message
        'The User Story did not match the required format.' is displayed.
        """

        expected_alert_message = "The User Story did not match the required format."

        driver.get('http://localhost:5173/')

        user_Story = ""

        driver.find_element(By.CSS_SELECTOR, ".entry_area").find_element(By.TAG_NAME, "input").send_keys(user_Story)
        driver.find_element(By.CSS_SELECTOR, ".analyze").click()

        try:
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            assert alert.text == expected_alert_message, f"Unexpected alert text: {alert.text}"
            alert.accept()
        except TimeoutException:
            assert False, "Alert with the message '" + \
                expected_alert_message + "' did not appear."

    def single_us_tc_2(self, driver, analyze_tc_1_fixture):
        """
        Insert a user story that match the expected pattern in the input text area and analyze it.
        Verifies if the result is equal to the oracle.
        """

        driver.get('http://localhost:5173/')

        oracle = analyze_tc_1_fixture[1]
        user_Story = ("As a radiologist, "
                      "I want to use the ID3 algorithm to develop decision tree models for diagnosing and predicting medical conditions"
                      " based on various medical imaging data, such as X-rays, CT scans, and MRI scans.")

        driver.find_element(By.CSS_SELECTOR, ".entry_area").find_element(By.TAG_NAME, "input").send_keys(user_Story)
        driver.find_element(By.CSS_SELECTOR, ".analyze").click()

        try:
            domain = driver.find_elements(By.CSS_SELECTOR, ".mx-4")[1].text.split(': ')[1]
            table_body = driver.find_elements(By.XPATH, '/html/body/div/div/div[3]/div/div/div[2]/div[1]/table/tbody')
            features = {}

            if table_body:
                for row in table_body:
                    features[row.find_elements(By.TAG_NAME, 'td')[0].text] = row.find_elements(By.TAG_NAME, 'td')[
                        1].text.split(' - ')

            with open(oracle, 'r') as file:
                oracle_data = json.load(file)

                assert domain == oracle_data['domain'], "Domain does not match the oracle"
                assert features == oracle_data['features'], "Sensitive features does not match the oracle"

        except TimeoutException:
            assert False, "Modal did not appear."
        except NoSuchElementException:
            assert False, "No matching with the oracle"
