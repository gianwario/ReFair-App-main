import pandas as pd
from io import StringIO
from REFAIR import intersection, feature_extraction


class TestIntersection:
    
    def test_intersection_with_both_lists_empty(self):
        first_list = []
        second_list = []

        result = intersection(first_list, second_list)

        assert result == []

    def test_intersection_with_first_list_empty(self):
        first_list = []
        second_list = ["Feature1", "Feature2"]

        result = intersection(first_list, second_list)

        assert result == []

    def test_intersection_with_second_list_empty(self):
        first_list = ["Feature1", "Feature2"]
        second_list = []

        result = intersection(first_list, second_list)

        assert result == []

    def test_intersection_with_no_element_in_common(self):
        first_list = ["Feature1", "Feature2"]
        second_list = ["Feature3"]

        result = intersection(first_list, second_list)

        assert result == []

    def test_intersection_with_one_element_in_common(self):
        first_list = ["Feature1", "Feature2"]
        second_list = ["Feature1"]

        result = intersection(first_list, second_list)

        assert result == ["Feature1"]

class TestFeatureExtraction:

    def test_feature_extraction_with_no_tasks(self, mocker):
        domains_mapping_csv_data = 'Domain,Feature\n' + \
        'health,age\n'
        domains_mapping_mock = pd.read_csv(StringIO(domains_mapping_csv_data))
        tasks_mapping_csv_data = 'Task,Feature\n' + \
        'clustering,age\n'
        tasks_mapping_mock = pd.read_csv(StringIO(tasks_mapping_csv_data))

        mocker.patch('REFAIR.domains_mapping', domains_mapping_mock)
        mocker.patch('REFAIR.tasks_mapping', tasks_mapping_mock)

        domain = 'Health'
        mltasks = []

        result = feature_extraction(domain, mltasks)

        assert result == {}

    def test_feature_extraction_with_no_matching_features(self, mocker):
        domains_mapping_csv_data = 'Domain,Feature\n' + \
        'health,age\n'
        domains_mapping_mock = pd.read_csv(StringIO(domains_mapping_csv_data))
        tasks_mapping_csv_data = 'Task,Feature\n' + \
        'clustering,author\n'
        tasks_mapping_mock = pd.read_csv(StringIO(tasks_mapping_csv_data))

        mocker.patch('REFAIR.domains_mapping', domains_mapping_mock)
        mocker.patch('REFAIR.tasks_mapping', tasks_mapping_mock)

        domain = 'Health'
        mltasks = ['Clustering']

        result = feature_extraction(domain, mltasks)

        assert result == {
            'Clustering': []
        }

    def test_feature_extraction_with_single_task(self, mocker):
        domains_mapping_csv_data = 'Domain,Feature\n' + \
        'health,age\n' + \
        'health,ethnicity\n' + \
        'health,gender\n' + \
        'information systems,age\n' + \
        'information systems,brand ownership\n' + \
        'information systems,gay-friendliness\n' + \
        'law,age\n' + \
        'law,ethnicity\n' + \
        'law,gender\n'
        domains_mapping_mock = pd.read_csv(StringIO(domains_mapping_csv_data))
        tasks_mapping_csv_data = 'Task,Feature\n' + \
        'clustering,age\n' + \
        'clustering,author\n' + \
        'clustering,ethnicity\n' + \
        'data summarization,age\n' + \
        'data summarization,caste\n' + \
        'data summarization,gender\n'
        tasks_mapping_mock = pd.read_csv(StringIO(tasks_mapping_csv_data))

        mocker.patch('REFAIR.domains_mapping', domains_mapping_mock)
        mocker.patch('REFAIR.tasks_mapping', tasks_mapping_mock)

        domain = 'Health'
        mltasks = ['Clustering']

        result = feature_extraction(domain, mltasks)

        assert result == {
            'Clustering': [
                'age',
                'ethnicity'
            ]
        }

    def test_feature_extraction_with_multiple_tasks(self, mocker):
        domains_mapping_csv_data = 'Domain,Feature\n' + \
        'health,age\n' + \
        'health,ethnicity\n' + \
        'health,gender\n' + \
        'information systems,age\n' + \
        'information systems,brand ownership\n' + \
        'information systems,gay-friendliness\n' + \
        'law,age\n' + \
        'law,ethnicity\n' + \
        'law,gender\n'
        domains_mapping_mock = pd.read_csv(StringIO(domains_mapping_csv_data))
        tasks_mapping_csv_data = 'Task,Feature\n' + \
        'classification,age\n' + \
        'classification,geography\n' + \
        'classification,race\n' + \
        'clustering,age\n' + \
        'clustering,author\n' + \
        'clustering,ethnicity\n' + \
        'data summarization,age\n' + \
        'data summarization,caste\n' + \
        'data summarization,gender\n'
        tasks_mapping_mock = pd.read_csv(StringIO(tasks_mapping_csv_data))

        mocker.patch('REFAIR.domains_mapping', domains_mapping_mock)
        mocker.patch('REFAIR.tasks_mapping', tasks_mapping_mock)

        domain = 'Health'
        mltasks = ['Classification', 'Clustering']

        result = feature_extraction(domain, mltasks)

        assert result == {
            'Classification' : [
                'age'
            ],
            'Clustering': [
                'age',
                'ethnicity'
            ]
        }
