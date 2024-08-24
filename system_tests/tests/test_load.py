import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TestLoad:

    def test_load_tc_1(self, driver, load_tc_1_fixture):
        """
        Uploads an Excel file with an incorrect filename and verifies that an alert with the message 
        'The file name is not \"stories\"' is displayed.
        """
        expected_alert_message = "The file name is not \"stories\""

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_1_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        try:
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            assert alert.text == expected_alert_message, f"Unexpected alert text: {alert.text}"
            alert.accept()
        except TimeoutException:
            assert False, "Alert with the message '" + \
                expected_alert_message + "' did not appear."

    def test_load_tc_2(self, driver, load_tc_2_fixture):
        """
        Uploads a .txt file and verifies that an alert with the message
        'This type of file is not supported. Upload an xlsx file.' is displayed.
        """
        expected_alert_message = "This type of file is not supported. Upload an xlsx file."

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_2_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        try:
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            assert alert.text == expected_alert_message, f"Unexpected alert text: {alert.text}"
            alert.accept()
        except TimeoutException:
            assert False, "Alert with the message '" + \
                expected_alert_message + "' did not appear."

    def test_load_tc_3(self, driver, load_tc_3_fixture):
        """
        Uploads an Excel file with a single sheet and no columns, and verifies that an alert 
        with the message 'No column \"User Story\" found' is displayed.
        """
        expected_alert_message = "No column \"User Story\" found"

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_3_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        try:
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            assert alert.text == expected_alert_message, f"Unexpected alert text: {alert.text}"
            alert.accept()
        except TimeoutException:
            assert False, "Alert with the message '" + \
                expected_alert_message + "' did not appear."

    def test_load_tc_4(self, driver, load_tc_4_fixture):
        """
        Uploads an Excel file with a single sheet and two columns (including "User Story"), 
        and verifies that an alert with the message 'The file must contain only a single column.'
        is displayed.
        """
        expected_alert_message = "The file must contain only a single column."

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_4_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        try:
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            assert alert.text == expected_alert_message, f"Unexpected alert text: {alert.text}"
            alert.accept()
        except TimeoutException:
            assert False, "Alert with the message '" + \
                expected_alert_message + "' did not appear."

    def test_load_tc_5(self, driver, load_tc_5_fixture):
        """
        Uploads an xlsx file named 'stories' containing two sheets. 
        The first sheet has a single column, 'User Story', with one well-written user story. 
        The second sheet has two columns, each containing two rows of data (not user stories).
        Verifies that the user story on the first sheet is correctly loaded.
        """
        stories = pd.read_excel(load_tc_5_fixture)
        expected_stories = stories['User Story'].tolist()

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_5_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        table_rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
        )

        for expected_story, row in zip(expected_stories, table_rows):
            story_in_row = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
            assert expected_story == story_in_row, f"Mismatch found: {expected_story} != {story_in_row}"

    def test_load_tc_6(self, driver, load_tc_6_fixture):
        """
        Uploads an xlsx file named 'stories' containing one sheet. 
        This sheet has a single column that is not labeled 'User Story' and 
        contains four rows of data (not user stories).
        Verifies that an alert with the message 'No column \"User Story\" found' is displayed.
        """
        expected_alert_message = "No column \"User Story\" found"

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_6_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        try:
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            assert alert.text == expected_alert_message, f"Unexpected alert text: {alert.text}"
            alert.accept()
        except TimeoutException:
            assert False, "Alert with the message '" + \
                expected_alert_message + "' did not appear."

    def test_load_tc_7(self, driver, load_tc_7_fixture):
        """
        Uploads an xlsx file named 'stories' containing one sheet. 
        This sheet has a single column labeled 'User Story' but contains 
        no rows of data (zero user stories).
        Verifies that an alert with the message 'There are no user stories' is displayed.
        """
        expected_alert_message = "There are no user stories"

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_7_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        try:
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            assert alert.text == expected_alert_message, f"Unexpected alert text: {alert.text}"
            alert.accept()
        except TimeoutException:
            assert False, "Alert with the message '" + \
                expected_alert_message + "' did not appear."
