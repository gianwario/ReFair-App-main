import os
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class TestAnalyze:

    def test_analyze_tc_1(self, driver, analyze_tc_1_fixture):
        """
        Upload a well-formed Excel file and check whether the domain and sensitive characteristics
         of the USs provided are the same as those of the oracle file.
        """

        driver.get('http://localhost:5173/')

        excel_path, oracle = analyze_tc_1_fixture

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(excel_path)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        try:
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-secondary"))).click()
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'modal-content')))

            domain = driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/div/div[2]/p[2]/').text
            sensitive_feature = driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/div/div[2]/div[1]/table/tbody/tr/td[2]').text

            with os.fdopen(oracle, 'r') as file:
                oracle_data = json.load(file)

                assert domain == oracle_data['domain'], "Domain does not match the oracle"
                assert sensitive_feature == oracle_data['sensitive_feature'], "Sensitive feature does not match the oracle"

        except TimeoutException:
            assert False, "Modal did not appear."
        except NoSuchElementException:
            assert False, "No matching with the oracle"
        finally:
            os.close(oracle)




