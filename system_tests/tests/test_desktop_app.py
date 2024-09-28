import json


def test_desktop_download_all(desktop_download_all_fixture):
    """
    Compares the contents of two JSON files containing all the: one from a desktop application and the other from an Oracle.
    If the contents differ, an assertion error will be raised.
    """
    desktop_app_results = desktop_download_all_fixture[0]
    oracle = desktop_download_all_fixture[1]

    with open(desktop_app_results, 'r') as f1, open(oracle, 'r') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)
    
    assert data1 == data2, f"The content of {desktop_app_results} and {oracle} is not equal."


def test_desktop_single_us(desktop_single_us_fixture):
    """
    Compares the contents of two JSON files containing a single US: one from a desktop application and the other from an Oracle.
    If the contents differ, an assertion error will be raised.
    """
    desktop_app_results = desktop_single_us_fixture[0]
    oracle = desktop_single_us_fixture[1]

    with open(desktop_app_results, 'r') as f1, open(oracle, 'r') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)
    
    assert data1 == data2, f"The content of {desktop_app_results} and {oracle} is not equal."