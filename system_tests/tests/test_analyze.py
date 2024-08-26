import os
import json
from pyexpat import features

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from system_tests.tests.conftest import driver


class TestAnalyze:

    def test_analyze_tc_1(self, driver, analyze_tc_1_fixture):
        """
        Upload a well-formed Excel file and check whether the domain and sensitive characteristics
         of the USs provided are the same as those of the oracle file.
        """

        driver.get('http://localhost:5173/')

        excel, oracle = analyze_tc_1_fixture

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(excel)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        try:
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-secondary"))).click()

            domain = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/div/div/div[2]/p[2]'))).text.split(': ')[1]
            table_body = driver.find_elements(By.XPATH, '/html/body/div/div/div[1]/div/div/div[2]/div[1]/table/tbody')
            task = features = []

            if table_body:
                for row in table_body:
                    for elements in row.find_elements(By.TAG_NAME, 'tr'):
                        task.extend(elements.find_elements(By.TAG_NAME, 'td')[0].text)
                        features.extend(elements.find_elements(By.TAG_NAME, 'td')[1].text)

            sensitive_features = dict(zip(task, features))

            with open(oracle, 'r') as file:
                oracle_data = json.load(file)

                assert domain == oracle_data['domain'], "Domain does not match the oracle"
                assert sensitive_features == oracle_data['features'], "Sensitive feature does not match the oracle"

        except TimeoutException:
            assert False, "Modal did not appear."
        except NoSuchElementException:
            assert False, "No matching with the oracle"





