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
def load_tc_1_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_1_(2.1.1.2.0.2.0.2.0.3.0)', 'This file name should not be accepted.xlsx'
    )


@pytest.fixture
def load_tc_2_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_2_(1.2.0.0.0.0.0.0.0.0.0)', 'stories.txt'
    )


@pytest.fixture
def load_tc_3_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_3_(1.1.1.1.0.0.0.0.0.0.0)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_4_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_4_(1.1.1.3.0.2.0.2.0.3.0)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_5_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_5_(1.1.2.2.3.2.1.2.0.3.0)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_6_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_6_(1.1.1.2.0.1.0.0.0.0.0)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_7_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_7_(1.1.1.2.0.2.0.1.0.0.0)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_8_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_8_(1.1.1.2.0.2.0.4.0.3.0.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_9_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_9_(1.1.2.2.2.2.2.2.1.3.0.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_10_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_10_(1.1.1.2.0.2.0.2.0.1.0.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_11_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_11_(1.1.2.2.2.2.2.2.2.3.1.)', 'stories.xlsx'
    )


@pytest.fixture
def load_tc_12_fixture():
    return os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'load_tc_12_(1.1.2.2.2.2.2.2.2.3.2.)', 'stories.xlsx'
    )
