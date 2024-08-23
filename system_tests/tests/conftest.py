import os
import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    driver = webdriver.Firefox()
    driver.set_window_size(1920, 1080)

    yield driver

    driver.quit()


@pytest.fixture
def xlsx_file_with_bad_filename_and_one_user_story():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'bad_name', 'This file name should not be accepted.xlsx'
    )
