import json
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class Test_single_us:

    def test_single_us(self, driver, analyze_tc_1_fixture):
        """
        Insert a user story in the input text area and analyze it.
        Check if the result is equal to the oracle.
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
                    features[row.find_elements(By.TAG_NAME, 'td')[0].text] = row.find_elements(By.TAG_NAME, 'td')[1].text.split(' - ')

            with open(oracle, 'r') as file:
                oracle_data = json.load(file)

                assert domain == oracle_data['domain'], "Domain does not match the oracle"
                assert features == oracle_data['features'], "Sensitive features does not match the oracle"

        except TimeoutException:
            assert False, "Modal did not appear."
        except NoSuchElementException:
            assert False, "No matching with the oracle"