import json
import pandas as pd
from io import BytesIO


class TestLoadStories: 
    def test_load_stories_with_no_file_in_request(self, client):
        response = client.post(
            path='/storiesload'
        )
        assert response.status_code == 200
        assert response.json == {
            'status': 'failure',
            'motivation': 'No file \"stories.xlsx\" loaded'
        }

    def test_load_stories_with_not_allowed_file(self, client):
        data = {
            'stories': (BytesIO(b"Some data."), 'stories.txt')
        }
        response = client.post(
            path='/storiesload',
            content_type='multipart/form-data',
            data=data
        )
        assert response.status_code == 200
        assert response.json == {
            'status': 'failure',
            'motivation': 'No file \"stories.xlsx\" loaded'
        }

    def test_load_stories_without_user_story_column(self, client):
        stories = pd.DataFrame({
            'My stories': [
                'First user story.',
                'Second user story.',
                'Third user story.'
            ]
        })
        buffer = BytesIO()
        stories.to_excel(buffer, index=False)
        buffer.seek(0)
        data = {
            'stories': (buffer, 'file_without_user_story_column.xlsx')
        }
        response = client.post(
            path='/storiesload', 
            content_type='multipart/form-data',
            data=data
        )
        assert response.status_code == 200
        assert response.json == {
            'status': 'failure',
            'motivation': "No column \"User Story\" found"
        }

    def test_load_stories_with_user_story_column(self, client):
        stories = pd.DataFrame({
            'User Story': [
                'First user story.',
                'Second user story.',
                'Third user story.'
            ]
        })
        buffer = BytesIO()
        stories.to_excel(buffer, index=False)
        buffer.seek(0)
        data = {
            'stories': (buffer, 'file_with_user_story_column.xlsx')
        }
        response = client.post(
            path='/storiesload', 
            content_type='multipart/form-data',
            data=data
        )
        assert response.status_code == 200
        assert response.json == {
            'status': 'success',
            'stories': [
                'First user story.',
                'Second user story.',
                'Third user story.'
            ]
        }

class TestAnalysis:
    def test_analysis_with_get_request_not_allowed(self, client):
        response = client.get(
            path='/analyzeStory'
        )
        assert response.status_code == 200
        # Check the raw bytes...
        #assert response.data == b"Not Allowed"
        # ...or check the decoded string. I'll keep this one.
        assert response.data.decode() == 'Not Allowed'

    def test_analysis_with_no_tasks_and_no_features(self, client, mocker):
        mocker.patch('app.get_domain', return_value='ExampleDomain')
        mocker.patch('app.get_ml_task', return_value=[])
        mocker.patch('app.feature_extraction', return_value={})

        response = client.post(
            path='/analyzeStory',
            data={
                'story': 'A user story related to ExampleDomain and no ML tasks.'
            },
            content_type='multipart/form-data'
        )
        assert response.status_code == 200
        assert response.json == {
            'domain': 'ExampleDomain',
            'tasks': [],
            'tasks_features': {},
            'features_counts': {}
        }

    def test_analysis_with_tasks_and_features_appearing_one_time(self, client, mocker):
        return_domain = 'ExampleDomain'
        return_ml_tasks = ['Task_A', 'Task_B']
        return_features = {
            'Task_A': [
                'Feature_1'
            ],
            'Task_B': [
                'Feature_2'
            ]
        }
        mocker.patch('app.get_domain', return_value=return_domain)
        mocker.patch('app.get_ml_task', return_value=return_ml_tasks)
        mocker.patch('app.feature_extraction', return_value=return_features)

        response = client.post(
            path='/analyzeStory',
            data={
                'story': 'A user story that focuses on Task_A and Task_B in the context of ExampleDomain.'
            },
            content_type='multipart/form-data'
        )
        assert response.status_code == 200
        assert response.json == {
            'domain': return_domain,
            'tasks': return_ml_tasks,
            'tasks_features': return_features,
            'features_counts': {
                'Feature_1': 1,
                'Feature_2': 1
            }
        }

    def test_analysis_with_tasks_and_features_appearing_multiple_times(self, client, mocker):
        return_domain = 'ExampleDomain'
        return_ml_tasks = ['Task_A', 'Task_B']
        return_features = {
            'Task_A': [
                'Feature_1',
                'Feature_2'
            ],
            'Task_B': [
                'Feature_2'
            ]
        }
        mocker.patch('app.get_domain', return_value=return_domain)
        mocker.patch('app.get_ml_task', return_value=return_ml_tasks)
        mocker.patch('app.feature_extraction', return_value=return_features)

        response = client.post(
            path='/analyzeStory',
            data={
                'story': 'A user story that focuses on Task_A and Task_B in the context of ExampleDomain.'
            },
            content_type='multipart/form-data'
        )
        assert response.status_code == 200
        assert response.json == {
            'domain': return_domain,
            'tasks': return_ml_tasks,
            'tasks_features': return_features,
            'features_counts': {
                'Feature_1': 1,
                'Feature_2': 2
            }
        }

class TestReportStories:
    def test_report_stories_with_get_request_not_allowed(self, client):
        response = client.get(
            path='/reportStories'
        )
        assert response.status_code == 200
        assert response.data.decode() == 'Not Allowed'

    def test_report_stories_with_empty_data(self, client):
        response = client.post(
            path='/reportStories', 
            data={}
        )
        assert response.status_code == 400

    def test_report_stories_with_single_user_story(self, client, mocker):
        story = 'A user story that focuses on Task_A and Task_B in the context of ExampleDomain.'
        return_domain = 'ExampleDomain'
        return_ml_tasks = ['Task_A', 'Task_B']
        return_features = {
            'Task_A': [
                'Feature_1',
                'Feature_2'
            ],
            'Task_B': [
                'Feature_2'
            ]
        }
        mocker.patch('app.get_domain', return_value=return_domain)
        mocker.patch('app.get_ml_task', return_value=return_ml_tasks)
        mocker.patch('app.feature_extraction', return_value=return_features)

        response = client.post(
            path='/reportStories',
            data={
                'stories': json.dumps([
                    story
                ])
            }
        )

        # Convert response data to a JSON object
        response_data = json.loads(response.get_data(as_text=True).replace("\'", "\""))

        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.headers['Content-Disposition'] == 'attachment;filename=zones.geojson'
        assert len(response_data) == 1
        assert response_data[0] == {
            'story': story,
            'domain': return_domain,
            'tasks': return_ml_tasks,
            'features': return_features
        }

    def test_report_stories_with_two_user_stories(self, client, mocker):
        stories = [
            'A user story that focuses on Task_A and Task_B in the context of ExampleDomain_1.',
            'A user story that focuses on Task_C in the context of ExampleDomain_2.'
        ]
        return_domain = ['ExampleDomain_1', 'ExampleDomain_2']
        return_ml_tasks = [['Task_A', 'Task_B'], ['Task_C']]
        return_features = [
            {
                'Task_A': [
                    'Feature_1',
                    'Feature_2'
                ],
                'Task_B': [
                    'Feature_2'
                ]
            },
            {
                'Task_C': [
                    'Feature_3'
                ]
            }
        ]
        mocker.patch('app.get_domain', side_effect=return_domain)
        mocker.patch('app.get_ml_task', side_effect=return_ml_tasks)
        mocker.patch('app.feature_extraction', side_effect=return_features)

        response = client.post(
            path='/reportStories',
            data={
                'stories': json.dumps(stories)
            }
        )

        # Convert response data to a JSON object
        response_data = json.loads(response.get_data(as_text=True).replace("\'", "\""))

        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.headers['Content-Disposition'] == 'attachment;filename=zones.geojson'
        assert len(response_data) == 2
        assert response_data[0] == {
            'story': stories[0],
            'domain': return_domain[0],
            'tasks': return_ml_tasks[0],
            'features': return_features[0]
        }
        assert response_data[1] == {
            'story': stories[1],
            'domain': return_domain[1],
            'tasks': return_ml_tasks[1],
            'features': return_features[1]
        }

class TestReportStory:
    def test_report_story_with_get_request_not_allowed(self, client):
        response = client.get(
            path='/reportStory'
        )
        assert response.status_code == 200
        assert response.data.decode() == 'Not Allowed'

    def test_report_story_with_empty_data(self, client):
        response = client.post(
            path='/reportStory', 
            data={}
        )
        assert response.status_code == 400

    def test_report_story_with_user_story(self, client, mocker):
        story = 'A user story that focuses on Task_A and Task_B in the context of ExampleDomain.'
        return_domain = 'ExampleDomain'
        return_ml_tasks = ['Task_A', 'Task_B']
        return_features = {
            'Task_A': [
                'Feature_1',
                'Feature_2'
            ],
            'Task_B': [
                'Feature_2'
            ]
        }
        mocker.patch('app.get_domain', return_value=return_domain)
        mocker.patch('app.get_ml_task', return_value=return_ml_tasks)
        mocker.patch('app.feature_extraction', return_value=return_features)

        response = client.post(
            path='/reportStory',
            data={
                'story': json.dumps(story)
            }
        )

        # Convert response data to a JSON object
        response_data = json.loads(response.get_data(as_text=True).replace("\'", "\""))

        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.headers['Content-Disposition'] == 'attachment;filename=zones.geojson'
        assert response_data == {
            'story': story,
            'domain': return_domain,
            'tasks': return_ml_tasks,
            'features': return_features
        }
