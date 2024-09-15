import json

class TestAnalysis:
    def test_analysis_integration(self, client):
        user_story = 'As an economist, I want to summarize economic research reports to ' + \
        'quickly identify key findings and recommendations for policy-making.'

        response = client.post(
            path='/analyzeStory',
            data={
                'story': user_story
            },
            content_type='multipart/form-data'
        )

        assert response.status_code == 200
        assert response.json == {
            "domain": "Economics",
            "tasks": [
                "anomaly detection",
                "clustering",
                "data summarization",
                "representation learning",
                "subset selection"
            ],
            "tasks_features": {
                "anomaly detection": [
                    "age",
                    "gender",
                    "race",
                    "sex"
                ],
                "clustering": [
                    "age",
                    "gender",
                    "geography",
                    "race",
                    "sex"
                ],
                "data summarization": [
                    "age",
                    "gender",
                    "geography",
                    "race",
                    "sex"
                ],
                "representation learning": [
                    "age",
                    "gender",
                    "geography",
                    "race",
                    "sex"
                ],
                "subset selection": [
                    "age",
                    "gender",
                    "geography",
                    "race"
                ]
            },
            "features_counts": {
                "age": 5,
                "gender": 5,
                "geography": 4,
                "race": 5,
                "sex": 4
            },
        }

class TestReportStories:
    def test_report_stories_integration(self, client):
        stories = [
            'As a computer vision researcher, I want to use WordNet to identify synonyms ' + \
            'and related terms in technical texts related to computer vision for better ' + \
            'understanding.',
            'As a healthcare provider, I want to use neural network hardware to ' + \
            'analyze medical data and predict disease outcomes and treatment effectiveness, so ' + \
            'that I can provide better healthcare services to patients.'
        ]

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
            'domain': 'Computer Vision',
            'tasks': [
                'anomaly detection',
                'clustering',
                'representation learning'
            ],
            'features': {
                'anomaly detection': [
                    'age',
                    'gender',
                    'race',
                    'skin tone'
                ],
                'clustering': [
                    'age',
                    'gender',
                    'geography',
                    'race'
                ],
                'representation learning': [
                    'age',
                    'gender',
                    'geography',
                    'race',
                    'skin color',
                    'skin tone'
                ]
            }
        }
        assert response_data[1] == {
            'story': stories[1],
            'domain': 'Health',
            'tasks': [
                'classification',
                'regression'
            ],
            'features': {
                'classification': [
                    'age',
                    'geography',
                    'sex',
                    'ethnicity',
                    'gender'
                ],
                'regression': [
                    'age',
                    'ethnicity',
                    'gender',
                    'geography',
                    'sex'
                ]
            }
        }
