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
