import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

PATTERN = r'^(?!\s*$).{1,1024}$'

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

    def test_load_tc_8(self, driver, load_tc_8_fixture):
        """
        Uploads an xlsx file named 'stories' containing one sheet. 
        This sheet has a single column labeled 'User Story' and contains 
        10000 well-written user stories.
        Verifies that all user stories in the sheet are correctly loaded.
        """
        stories = pd.read_excel(load_tc_8_fixture)
        expected_stories = stories['User Story'].tolist()

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_8_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        table_rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
        )

        for expected_story, row in zip(expected_stories, table_rows):
            story_in_row = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
            assert expected_story == story_in_row, f"Mismatch found: {expected_story} != {story_in_row}"

    def test_load_tc_9(self, driver, load_tc_9_fixture):
        """
        Uploads an xlsx file named 'stories' containing two sheets. 
        The first sheet has a single column, 'User Story', with one well-written user story. 
        The second sheet has a single column, 'User Story', but contains no user stories.
        Verifies that the user story on the first sheet is correctly loaded.
        """
        stories = pd.read_excel(load_tc_9_fixture)
        expected_stories = stories['User Story'].tolist()

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_9_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        table_rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
        )

        for expected_story, row in zip(expected_stories, table_rows):
            story_in_row = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
            assert expected_story == story_in_row, f"Mismatch found: {expected_story} != {story_in_row}"

    def test_load_tc_10(self, driver, load_tc_10_fixture):
        """
        Uploads an xlsx file named 'stories' containing one sheet. 
        This sheet has a single column labeled 'User Story' that contains 
        only one row of data, a picture.
        Verifies that an alert with the message 'The file could not be loaded because at least one 
        non-textual element was found in the \"User Story\" column.' is displayed.
        """
        expected_alert_message = "The file could not be loaded because at least one " + \
        "non-textual element was found in the \"User Story\" column."

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_10_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        try:
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            assert alert.text == expected_alert_message, f"Unexpected alert text: {alert.text}"
            alert.accept()
        except TimeoutException:
            assert False, "Alert with the message '" + \
                expected_alert_message + "' did not appear."

    def test_load_tc_11(self, driver, load_tc_11_fixture):
        """
        Uploads an xlsx file named 'stories' containing two sheets. 
        The first sheet has a single column, 'User Story', with one well-written user story. 
        The second sheet has a single column, 'User Story', that contains 
        only one row of data, a picture.
        Verifies that the user story on the first sheet is correctly loaded.
        """
        stories = pd.read_excel(load_tc_11_fixture)
        expected_stories = stories['User Story'].tolist()

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_11_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        table_rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
        )

        for expected_story, row in zip(expected_stories, table_rows):
            story_in_row = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
            assert expected_story == story_in_row, f"Mismatch found: {expected_story} != {story_in_row}"

    def test_load_tc_12(self, driver, load_tc_12_fixture):
        """
        Uploads an xlsx file named 'stories' containing two sheets. 
        The first sheet has a single column, 'User Story', with one well-written user story. 
        The second sheet has a single column, 'User Story', with one user story that is too long. 
        Verifies that the user story on the first sheet is correctly loaded.
        """
        stories = pd.read_excel(load_tc_12_fixture)
        expected_stories = stories['User Story'].tolist()

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_12_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        table_rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
        )

        for expected_story, row in zip(expected_stories, table_rows):
            story_in_row = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
            assert expected_story == story_in_row, f"Mismatch found: {expected_story} != {story_in_row}"

    def test_load_tc_13(self, driver, load_tc_13_fixture):
        """
        Uploads an xlsx file named 'stories' containing one sheet. 
        This sheet has a single column labeled 'User Story' and 
        one row of data that does not match the expected regex pattern.
        Verifies that an alert with the message 
        'The file was loaded successfully, but some user stories did not match 
        the required format and were not included.' is displayed, 
        and confirms that no user stories are loaded.
        """
        expected_alert_message = "The file was loaded successfully, but " + \
            "some user stories did not match the required format and were not included."

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_13_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        try:
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            assert alert.text == expected_alert_message, f"Unexpected alert text: {alert.text}"
            alert.accept()
        except TimeoutException:
            assert False, "Alert with the message '" + \
                expected_alert_message + "' did not appear."

        table_rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        assert len(table_rows) == 0, f"The table should have 0 rows - found {len(table_rows)} row(s)"

    def test_load_tc_14(self, driver, load_tc_14_fixture):
        """
        Uploads an xlsx file named 'stories' containing one sheet. 
        This sheet has a single column labeled 'User Story' and 
        one well-written user story.
        Verifies that the user story is correctly loaded.
        """
        stories = pd.read_excel(load_tc_14_fixture)
        expected_stories = stories['User Story'].tolist()

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_14_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        table_rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
        )
        assert len(table_rows) == 1, f"The table should have 1 row - found {len(table_rows)} row(s)"

        for expected_story, row in zip(expected_stories, table_rows):
            story_in_row = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
            assert expected_story == story_in_row, f"Mismatch found: {expected_story} != {story_in_row}"

    def test_load_tc_15(self, driver, load_tc_15_fixture):
        """
        Uploads an xlsx file named 'stories' containing one sheet. 
        This sheet has a single column labeled 'User Story' and 100 user stories.
        One row of data does not match the expected regex pattern.
        Verifies that an alert with the message 
        'The file was loaded successfully, but some user stories did not match 
        the required format and were not included.' is displayed, 
        and confirms that only the user stories matching the expected format are loaded.
        """
        expected_alert_message = "The file was loaded successfully, but " + \
            "some user stories did not match the required format and were not included."
        stories = pd.read_excel(load_tc_15_fixture)
        filtered_stories = stories[stories['User Story'].str.fullmatch(PATTERN)]
        expected_stories = filtered_stories['User Story'].tolist()

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_15_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        try:
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            assert alert.text == expected_alert_message, f"Unexpected alert text: {alert.text}"
            alert.accept()
        except TimeoutException:
            assert False, "Alert with the message '" + \
                expected_alert_message + "' did not appear."

        table_rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
        )

        assert len(table_rows) == 99, f"The table should have 99 rows - found {len(table_rows)} row(s)"

        for expected_story, row in zip(expected_stories, table_rows):
            story_in_row = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
            assert expected_story == story_in_row, f"Mismatch found: {expected_story} != {story_in_row}"

    def test_load_tc_16(self, driver, load_tc_16_fixture):
        """
        Uploads an xlsx file named 'stories' containing one sheet. 
        This sheet has a single column labeled 'User Story' and 100 user stories.
        All rows of data match the expected regex pattern.
        Verifies that all 100 user stories are correctly loaded.
        """
        stories = pd.read_excel(load_tc_16_fixture)
        expected_stories = stories['User Story'].tolist()

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_16_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        table_rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
        )

        assert len(table_rows) == 100, f"The table should have 100 rows - found {len(table_rows)} row(s)"

        for expected_story, row in zip(expected_stories, table_rows):
            story_in_row = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
            assert expected_story == story_in_row, f"Mismatch found: {expected_story} != {story_in_row}"

    def test_load_tc_17(self, driver, load_tc_17_fixture):
        """
        Uploads an xlsx file named 'stories' containing two sheets. 
        The first sheet has a single column labeled 'User Story' and 
        one row of data that does not match the expected regex pattern.
        The second sheet is empty (zero columns).
        Verifies that an alert with the message 
        'The file was loaded successfully, but some user stories did not match 
        the required format and were not included.' is displayed, 
        and confirms that no user stories are loaded.
        """
        expected_alert_message = "The file was loaded successfully, but " + \
            "some user stories did not match the required format and were not included."

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_17_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        try:
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            assert alert.text == expected_alert_message, f"Unexpected alert text: {alert.text}"
            alert.accept()
        except TimeoutException:
            assert False, "Alert with the message '" + \
                expected_alert_message + "' did not appear."

        table_rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        assert len(table_rows) == 0, f"The table should have 0 rows - found {len(table_rows)} row(s)"

    def test_load_tc_18(self, driver, load_tc_18_fixture):
        """
        Uploads an xlsx file named 'stories' containing two sheets. 
        The first sheet has a single column labeled 'User Story' and 
        one well-written user story.
        The second sheet is empty (zero columns).
        Verifies that the user story is correctly loaded.
        """
        stories = pd.read_excel(load_tc_18_fixture)
        expected_stories = stories['User Story'].tolist()

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_18_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        table_rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
        )
        assert len(table_rows) == 1, f"The table should have 1 row - found {len(table_rows)} row(s)"

        for expected_story, row in zip(expected_stories, table_rows):
            story_in_row = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
            assert expected_story == story_in_row, f"Mismatch found: {expected_story} != {story_in_row}"

    def test_load_tc_19(self, driver, load_tc_19_fixture):
        """
        Uploads an xlsx file named 'stories' containing two sheets. 
        The first sheet has a single column labeled 'User Story' and 100 user stories.
        One row of data does not match the expected regex pattern.
        The second sheet is empty (zero columns).
        Verifies that an alert with the message 
        'The file was loaded successfully, but some user stories did not match 
        the required format and were not included.' is displayed, 
        and confirms that only the user stories matching the expected format are loaded.
        """
        expected_alert_message = "The file was loaded successfully, but " + \
            "some user stories did not match the required format and were not included."
        stories = pd.read_excel(load_tc_19_fixture)
        filtered_stories = stories[stories['User Story'].str.fullmatch(PATTERN)]
        expected_stories = filtered_stories['User Story'].tolist()

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_19_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        try:
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            assert alert.text == expected_alert_message, f"Unexpected alert text: {alert.text}"
            alert.accept()
        except TimeoutException:
            assert False, "Alert with the message '" + \
                expected_alert_message + "' did not appear."

        table_rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
        )

        assert len(table_rows) == 99, f"The table should have 99 rows - found {len(table_rows)} row(s)"

        for expected_story, row in zip(expected_stories, table_rows):
            story_in_row = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
            assert expected_story == story_in_row, f"Mismatch found: {expected_story} != {story_in_row}"

    def test_load_tc_20(self, driver, load_tc_20_fixture):
        """
        Uploads an xlsx file named 'stories' containing two sheets.
        The first sheet has a single column labeled 'User Story' and 100 user stories.
        The second sheet is empty (zero columns).
        All rows of data match the expected regex pattern.
        Verifies that all 100 user stories are correctly loaded.
        """
        stories = pd.read_excel(load_tc_20_fixture)
        expected_stories = stories['User Story'].tolist()

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_20_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        table_rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
        )

        assert len(table_rows) == 100, f"The table should have 100 rows - found {len(table_rows)} row(s)"

        for expected_story, row in zip(expected_stories, table_rows):
            story_in_row = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
            assert expected_story == story_in_row, f"Mismatch found: {expected_story} != {story_in_row}"

    def test_load_tc_21(self, driver, load_tc_21_fixture):
        """
        Uploads an xlsx file named 'stories' containing two sheets. 
        The first sheet has a single column labeled 'User Story' and 
        one row of data that does not match the expected regex pattern.
        The second sheet has a single column that is not labeled 'User Story'.
        Verifies that an alert with the message 
        'The file was loaded successfully, but some user stories did not match 
        the required format and were not included.' is displayed, 
        and confirms that no user stories are loaded.
        """
        expected_alert_message = "The file was loaded successfully, but " + \
            "some user stories did not match the required format and were not included."

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_21_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        try:
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            assert alert.text == expected_alert_message, f"Unexpected alert text: {alert.text}"
            alert.accept()
        except TimeoutException:
            assert False, "Alert with the message '" + \
                expected_alert_message + "' did not appear."

        table_rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        assert len(table_rows) == 0, f"The table should have 0 rows - found {len(table_rows)} row(s)"

    def test_load_tc_22(self, driver, load_tc_22_fixture):
        """
        Uploads an xlsx file named 'stories' containing two sheets. 
        The first sheet has a single column labeled 'User Story' and 
        one well-written user story.
        The second sheet has a single column that is not labeled 'User Story'.
        Verifies that the user story is correctly loaded.
        """
        stories = pd.read_excel(load_tc_22_fixture)
        expected_stories = stories['User Story'].tolist()

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_22_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        table_rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
        )
        assert len(table_rows) == 1, f"The table should have 1 row - found {len(table_rows)} row(s)"

        for expected_story, row in zip(expected_stories, table_rows):
            story_in_row = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
            assert expected_story == story_in_row, f"Mismatch found: {expected_story} != {story_in_row}"

    def test_load_tc_23(self, driver, load_tc_23_fixture):
        """
        Uploads an xlsx file named 'stories' containing two sheets. 
        The first sheet has a single column labeled 'User Story' and 100 user stories.
        One row of data does not match the expected regex pattern.
        The second sheet has a single column that is not labeled 'User Story'.
        Verifies that an alert with the message 
        'The file was loaded successfully, but some user stories did not match 
        the required format and were not included.' is displayed, 
        and confirms that only the user stories matching the expected format are loaded.
        """
        expected_alert_message = "The file was loaded successfully, but " + \
            "some user stories did not match the required format and were not included."
        stories = pd.read_excel(load_tc_23_fixture)
        filtered_stories = stories[stories['User Story'].str.fullmatch(PATTERN)]
        expected_stories = filtered_stories['User Story'].tolist()

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_23_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        try:
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            assert alert.text == expected_alert_message, f"Unexpected alert text: {alert.text}"
            alert.accept()
        except TimeoutException:
            assert False, "Alert with the message '" + \
                expected_alert_message + "' did not appear."

        table_rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
        )

        assert len(table_rows) == 99, f"The table should have 99 rows - found {len(table_rows)} row(s)"

        for expected_story, row in zip(expected_stories, table_rows):
            story_in_row = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
            assert expected_story == story_in_row, f"Mismatch found: {expected_story} != {story_in_row}"

    def test_load_tc_24(self, driver, load_tc_24_fixture):
        """
        Uploads an xlsx file named 'stories' containing two sheets.
        The first sheet has a single column labeled 'User Story' and 100 user stories.
        The second sheet has a single column that is not labeled 'User Story'.
        All rows of data match the expected regex pattern.
        Verifies that all 100 user stories are correctly loaded.
        """
        stories = pd.read_excel(load_tc_24_fixture)
        expected_stories = stories['User Story'].tolist()

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_24_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        table_rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
        )

        assert len(table_rows) == 100, f"The table should have 100 rows - found {len(table_rows)} row(s)"

        for expected_story, row in zip(expected_stories, table_rows):
            story_in_row = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
            assert expected_story == story_in_row, f"Mismatch found: {expected_story} != {story_in_row}"

    def test_load_tc_25(self, driver, load_tc_25_fixture):
        """
        Uploads an xlsx file named 'stories' containing two sheets. 
        The first sheet has a single column labeled 'User Story' and 
        one row of data that does not match the expected regex pattern.
        The second sheet also has a single column labeled 'User Story' and
        three rows of data that match the expected regex pattern.
        Verifies that an alert with the message 
        'The file was loaded successfully, but some user stories did not match 
        the required format and were not included.' is displayed, 
        and confirms that no user stories are loaded (only the first sheet's data is considered).
        """
        expected_alert_message = "The file was loaded successfully, but " + \
            "some user stories did not match the required format and were not included."

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_25_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        try:
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            assert alert.text == expected_alert_message, f"Unexpected alert text: {alert.text}"
            alert.accept()
        except TimeoutException:
            assert False, "Alert with the message '" + \
                expected_alert_message + "' did not appear."

        table_rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        assert len(table_rows) == 0, f"The table should have 0 rows - found {len(table_rows)} row(s)"

    def test_load_tc_26(self, driver, load_tc_26_fixture):
        """
        Uploads an xlsx file named 'stories' containing two sheets. 
        The first sheet has a single column labeled 'User Story' and 
        one well-written user story.
        The second sheet also has a single column labeled 'User Story' and
        three rows of data that match the expected regex pattern.
        Verifies that the user story is correctly loaded 
        (only the first sheet's data is considered).
        """
        stories = pd.read_excel(load_tc_26_fixture)
        expected_stories = stories['User Story'].tolist()

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_26_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        table_rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
        )
        assert len(table_rows) == 1, f"The table should have 1 row - found {len(table_rows)} row(s)"

        for expected_story, row in zip(expected_stories, table_rows):
            story_in_row = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
            assert expected_story == story_in_row, f"Mismatch found: {expected_story} != {story_in_row}"

    def test_load_tc_27(self, driver, load_tc_27_fixture):
        """
        Uploads an xlsx file named 'stories' containing two sheets. 
        The first sheet has a single column labeled 'User Story' and 100 user stories.
        One row of data does not match the expected regex pattern.
        The second sheet also has a single column labeled 'User Story' and
        three rows of data that match the expected regex pattern.
        Verifies that an alert with the message 
        'The file was loaded successfully, but some user stories did not match 
        the required format and were not included.' is displayed, 
        and confirms that only the user stories matching the expected format are loaded
        (only the first sheet's data is considered).
        """
        expected_alert_message = "The file was loaded successfully, but " + \
            "some user stories did not match the required format and were not included."
        stories = pd.read_excel(load_tc_27_fixture)
        filtered_stories = stories[stories['User Story'].str.fullmatch(PATTERN)]
        expected_stories = filtered_stories['User Story'].tolist()

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_27_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        try:
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            assert alert.text == expected_alert_message, f"Unexpected alert text: {alert.text}"
            alert.accept()
        except TimeoutException:
            assert False, "Alert with the message '" + \
                expected_alert_message + "' did not appear."

        table_rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
        )

        assert len(table_rows) == 99, f"The table should have 99 rows - found {len(table_rows)} row(s)"

        for expected_story, row in zip(expected_stories, table_rows):
            story_in_row = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
            assert expected_story == story_in_row, f"Mismatch found: {expected_story} != {story_in_row}"

    def test_load_tc_28(self, driver, load_tc_28_fixture):
        """
        Uploads an xlsx file named 'stories' containing two sheets.
        The first sheet has a single column labeled 'User Story' with 
        100 user stories that match the expected regex pattern.
        The second sheet also has a single column labeled 'User Story' with
        three rows of data that match the expected regex pattern.
        Verifies that all 100 user stories from the first sheet are correctly loaded,
        while the data from the second sheet is not considered.
        """
        stories = pd.read_excel(load_tc_28_fixture)
        expected_stories = stories['User Story'].tolist()

        driver.get("http://localhost:5173/")

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_28_fixture)

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        table_rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
        )

        assert len(table_rows) == 100, f"The table should have 100 rows - found {len(table_rows)} row(s)"

        for expected_story, row in zip(expected_stories, table_rows):
            story_in_row = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
            assert expected_story == story_in_row, f"Mismatch found: {expected_story} != {story_in_row}"

    def test_load_tc_button(self, driver):
        """
        Clicks the Load button without selecting a file.
        Verifies that an alert with the message 
        'No file \"stories.xlsx\" loaded' is displayed.
        """
        expected_alert_message = "No file \"stories.xlsx\" loaded"
        
        driver.get("http://localhost:5173/")

        driver.find_element(By.CSS_SELECTOR, ".btn-info").click()

        try:
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            assert alert.text == expected_alert_message, f"Unexpected alert text: {alert.text}"
            alert.accept()
        except TimeoutException:
            assert False, "Alert with the message '" + \
                expected_alert_message + "' did not appear."
