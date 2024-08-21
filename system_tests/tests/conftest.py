import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    driver = webdriver.Firefox()
    driver.set_window_size(1920, 1080)

    yield driver

    driver.quit()
