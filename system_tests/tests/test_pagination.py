import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

class TestPagination:

    def test_pagination(self, driver, load_tc_28_fixture):
        """
        Check if the first button and the last button of the paginaton are disabled while,
        respectively, users are on the first page or on the last page
        """

        driver.get('http://localhost:5173/')

        file_input = driver.find_element(By.CSS_SELECTOR, ".form-control")
        file_input.send_keys(load_tc_28_fixture)

        driver.find_element(By.CSS_SELECTOR, ".load").click()

        try:
            max_pagination = driver.find_element(By.CSS_SELECTOR, ".pagination").find_element(By.TAG_NAME, "input").get_attribute('max')

            min = driver.find_element(By.CSS_SELECTOR, ".pagination").find_element(By.TAG_NAME, "button").is_enabled()

            input_number = driver.find_element(By.CSS_SELECTOR, ".pagination").find_element(By.TAG_NAME, "input")
            time.sleep(1)
            input_number.send_keys(Keys.BACKSPACE)
            time.sleep(1)
            input_number.send_keys(max_pagination)
            time.sleep(1)
            input_number.send_keys(Keys.ENTER)
            time.sleep(1)
            max = driver.find_element(By.CSS_SELECTOR, ".pagination").find_elements(By.TAG_NAME, "button")[1].is_enabled()

            assert not min and not max, "One or either Button are not disabled"

        except NoSuchElementException:
            assert False, "No element was found in the page."

