

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
